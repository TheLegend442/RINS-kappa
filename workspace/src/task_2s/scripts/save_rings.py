#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray
from custom_messages.msg import RingCoordinates
from builtin_interfaces.msg import Time
from custom_messages.srv import PosesInFrontOfRings
from geometry_msgs.msg import PoseWithCovarianceStamped, Pose
import numpy as np
import time
import cv2
import yaml
import tf2_ros
import tf2_geometry_msgs
from nav_msgs.msg import OccupancyGrid
from collections import deque
import matplotlib.pyplot as plt
from turtle_tf2_py.turtle_tf2_broadcaster import quaternion_from_euler
import math
from task_2s.srv import MarkerArrayService

class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class Ring():
    def __init__(self, id, center, current_time=None, robot_position=None, count=1, color=None):
        self.id = id
        self.center = center
        self.current_time = current_time
        self.robot_position = robot_position
        self.count = count
        self.color_counts = {color: 1} if color else {}
        self.color = color
        self.color_strength = 0
        self.num_detections = 1

    def update_color(self, new_color, new_strength):
        if new_color in self.color_counts:
            self.color_counts[new_color] += 1
        else:
            self.color_counts[new_color] = 1

        if new_strength > self.color_strength:
            self.color_strength = new_strength
            self.color = new_color
        # else:
        #     self.color = max(self.color_counts, key=self.color_counts.get)
        #     self

class RingMarkerSubscriber(Node):
    def __init__(self):
        super().__init__('ring_marker_subscriber')

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.marker_pub = self.create_publisher(Marker, '/detected_rings', 10)
        self.marker_sub = self.create_subscription(RingCoordinates, '/ring_marker', self.marker_callback, 10)

        self.robot_position_subscription = self.create_subscription(
            PoseWithCovarianceStamped, '/amcl_pose', self.robot_position_callback, 10
        )

        self.service = self.create_service(PosesInFrontOfRings, 'get_ring_pose', self.get_ring_pose_callback)
        self.get_rings_service = self.create_service(MarkerArrayService, 'get_rings', self.get_rings_callback)

        self.robot_position = None
        self.rings = {}
        self.threshold = 0.7
        self.time_threshold = 0.1
        self.ring_counter = 0
        self.min_wall_distance_m = 0.7
        self.ring_count_threshold = 3
        self.load_and_process_map('src/task_2s/maps/bird_map.pgm', 'src/task_2s/maps/bird_map.yaml')
        self.map_data = (self.map_image.flatten() / 255 * 100).astype(int).tolist()

        self.marker_queue = []
        self.get_logger().info("RingMarkerSubscriber initialized.")

    
    def load_and_process_map(self, pgm_path, yaml_path):
        """Loads map, metadata, and computes the distance transform."""
        self.get_logger().info(f"Loading map from {yaml_path} and {pgm_path}")
        try:
            with open(yaml_path, 'r') as yaml_file:
                self.map_metadata = yaml.safe_load(yaml_file)

            self.map_image = cv2.imread(pgm_path, cv2.IMREAD_GRAYSCALE)
            if self.map_image is None:
                raise IOError(f"Failed to load map image: {pgm_path}")

            self.map_height, self.map_width = self.map_image.shape
            self.get_logger().info(f"Map size: {self.map_width} x {self.map_height}")
            self.get_logger().info(f"Map resolution: {self.map_metadata['resolution']} m/pixel")
            self.map_resolution = self.map_metadata['resolution']
            origin = self.map_metadata['origin']
            self.map_origin = Point(x=origin[0], y=origin[1])

            occupied_thresh = self.map_metadata.get('occupied_thresh', 0.65) * 255
            free_thresh = self.map_metadata.get('free_thresh', 0.196) * 255

            self.map_matrix_np = np.zeros_like(self.map_image, dtype=np.int8)
            self.map_matrix_np[self.map_image < free_thresh] = 100
            self.map_matrix_np[self.map_image > occupied_thresh] = 0
            mask_unknown = (self.map_image >= free_thresh) & (self.map_image <= occupied_thresh)
            self.map_matrix_np[mask_unknown] = 100

            if self.map_metadata.get('negate', 0):
                self.get_logger().info("Negating map interpretation.")
                occupied_mask = (self.map_matrix_np == 100)
                free_mask = (self.map_matrix_np == 0)
                self.map_matrix_np[occupied_mask] = 0
                self.map_matrix_np[free_mask] = 100

            self.get_logger().info("Calculating distance transform...")
            binary_map_for_dist = np.zeros_like(self.map_matrix_np, dtype=np.uint8)
            binary_map_for_dist[self.map_matrix_np == 0] = 255
            self.distance_map = cv2.distanceTransform(binary_map_for_dist, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
            self.get_logger().info("Distance transform calculated.")

            self.min_wall_distance_cells = int(self.min_wall_distance_m / self.map_resolution)
            self.get_logger().info(f"Minimum wall distance set to {self.min_wall_distance_m} m ({self.min_wall_distance_cells} cells)")

            # # Uporabimo Matplotlib za prikaz z legendo
            # fig, ax = plt.subplots(figsize=(8, 6))
            # im = ax.imshow(self.distance_map, cmap='jet')
            # cbar = plt.colorbar(im, ax=ax)
            # cbar.set_label('Razdalja do zida (v pikslijih)')

            # ax.set_title('Razdalja do zidov (distance map)')
            # ax.axis('off')  # skrij osi (če želiš jih lahko pustiš)
            # plt.show()

        except FileNotFoundError as e:
            self.get_logger().error(f"Map file not found: {e}. Shutting down.")
            rclpy.shutdown()
        except Exception as e:
            self.get_logger().error(f"Error loading or processing map: {e}")
            rclpy.shutdown()

    def robot_position_callback(self, msg):
        self.robot_position = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])

    def marker_callback(self, msg):
        if self.robot_position is None:
            self.get_logger().info("Pozicija robota ni bila prejeta, ignoriram zaznane obroče.")
            return
        
        self.marker_queue.append(msg)
        self.proccess_markers()

    def proccess_markers(self):
        new_queue = []
        self.get_logger().info(f"Processing {len(self.marker_queue)} markers")
        for msg in self.marker_queue:
            was_proccessed = self.proccess_marker(msg)
            if not was_proccessed:
                new_queue.append(msg)
        self.marker_queue = new_queue.copy()
    
    def proccess_marker(self, msg):
        """ returns True if marker was proccessed, False if not"""
        current_position = np.array([msg.center.pose.position.x, msg.center.pose.position.y, msg.center.pose.position.z])
        color = msg.color
        strength = msg.strength
        current_time = time.time()
        stamp = msg.center.header.stamp

        try:
            transform = self.tf_buffer.lookup_transform('map', 'base_link', stamp,timeout=rclpy.duration.Duration(seconds=0.3))
            transformed_pose = tf2_geometry_msgs.do_transform_pose(msg.center.pose, transform)
            transformed_position = np.array([transformed_pose.position.x, 
                                             transformed_pose.position.y, 
                                             transformed_pose.position.z])
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            msg = str(e)
            self.get_logger().error(f"Napaka pri transformaciji: {msg}")

            if "extrapolation into the past" in msg.lower():
                # Transform requested in the past
                return True

            return False

        for ring_id, ring in self.rings.items():
            count = ring.count
            timestamp = ring.current_time
            center_point = ring.center

            distance = np.linalg.norm(center_point - transformed_position)

            if distance < self.threshold:
                if current_time - timestamp < self.time_threshold:
                    return True
                else:
                    self.delete_marker(ring_id)

                    new_position = (count / (count + 1)) * center_point + (1 / (count + 1)) * transformed_position
                    ring.center = new_position
                    ring.current_time = current_time
                    ring.robot_position = self.robot_position
                    ring.count += 1
                    ring.update_color(color, strength)
                    ring.num_detections += 1

                    self.rings[ring_id] = ring
                    if ring.num_detections >= 5: self.publish_ring_marker(new_position, ring_id)
                    return True

        self.ring_counter += 1
        self.get_logger().info(f"Zaznan nov obroč z ID-jem {self.ring_counter}.")
        new_ring = Ring(self.ring_counter, transformed_position, current_time, self.robot_position, color=color)
        new_ring.color_strength = strength
        self.rings[self.ring_counter] = new_ring

    def ring2rgb(self, ring):
        color = ring.color
        mapping = {
            "RED": (1.0, 0.0, 0.0),
            "GREEN": (0.0, 1.0, 0.0),
            "BLUE": (0.0, 0.0, 1.0),
            "YELLOW": (1.0, 1.0, 0.0),
            "BLACK": (0.0, 0.0, 0.0),
        }
        if color in mapping:
            return {"r": mapping[color][0], "g": mapping[color][1], "b": mapping[color][2]}
        else:
            return {"r": 1.0, "g": 1.0, "b": 1.0}

    def publish_ring_marker(self, position, ring_id):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "rings"
        marker.id = ring_id
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x = position[0]
        marker.pose.position.y = position[1]
        marker.pose.position.z = float(position[2])  # Poskrbimo, da je tip float
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2

        ring = self.rings[ring_id]
        rgb = self.ring2rgb(ring)

        marker.color.r = rgb["r"]
        marker.color.g = rgb["g"]
        marker.color.b = rgb["b"]
        marker.color.a = 1.0
        marker.lifetime.sec = 0

        print(position)
        self.marker_pub.publish(marker)

    def delete_marker(self, ring_id):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "rings"
        marker.id = ring_id
        marker.action = Marker.DELETE

        self.marker_pub.publish(marker)

    def get_rings_callback(self, request, response):
        response.marker_array = MarkerArray()  # ✅ This matches your .srv definition

        for ring in self.rings.values():
            if ring.count < self.ring_count_threshold:
                self.get_logger().warn(f"Skipping ring {ring.id} with count {ring.count}")
                continue

            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "rings"
            marker.id = ring.id
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.pose.position.x = float(ring.center[0])
            marker.pose.position.y = float(ring.center[1])
            marker.pose.position.z = float(ring.center[2])
            marker.scale.x = 0.2
            marker.scale.y = 0.2
            marker.scale.z = 0.2
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = 1.0

            robot_position_marker = Marker()
            robot_position_marker.header.frame_id = "map"
            robot_position_marker.header.stamp = self.get_clock().now().to_msg()
            robot_position_marker.ns = "robot_position"
            robot_position_marker.id = ring.id + 1000
            robot_position_marker.type = Marker.SPHERE
            robot_position_marker.action = Marker.ADD
            robot_position_marker.pose.position.x = float(ring.robot_position[0])
            robot_position_marker.pose.position.y = float(ring.robot_position[1])
            robot_position_marker.pose.position.z = float(ring.robot_position[2])


            response.marker_array.markers.append(marker)  # ✅ Access `.markers` list
            response.robot_positions.markers.append(robot_position_marker)  # ✅ Access `.markers` list
            response.colors.append(ring.color)  # Add color to the response

        return response




    def get_ring_pose_callback(self, request, response):
        self.get_logger().info("Processing request for ring poses")
        self.get_logger().info(f"Received {len(self.rings)} rings")
        response.poses = []
        response.colors = []

        for ring in self.rings.values():
            if ring.count < self.ring_count_threshold:
                self.get_logger().warn(f"Skipping ring {ring.id} with count {ring.count}")
                continue

            center_x = ring.center[0]
            center_y = ring.center[1]

            cell_x = int((center_x - self.map_origin.x) / self.map_resolution)
            cell_y = int((center_y - self.map_origin.y) / self.map_resolution)
            cell_y = self.map_height - cell_y

            valid_position = self.find_valid_position_optimized(cell_x, cell_y)

            if valid_position is not None:  
                valid_position = (valid_position[0],self.map_height - valid_position[1])  # Flip y-coordinate
                marker_x_meters = valid_position[0] * self.map_resolution + self.map_origin.x
                marker_y_meters = valid_position[1] * self.map_resolution + (self.map_origin.y)

                pose = Pose()
                pose.position.x = float(marker_x_meters)
                pose.position.y = float(marker_y_meters)
                pose.position.z = 0.0

                
                dx = center_x - marker_x_meters
                dy = center_y - marker_y_meters
                yaw = np.arctan2(dy, dx)
                
                pose.orientation.z = yaw


                response.poses.append(pose)
                response.colors.append(ring.color)
            else:
                # pose = Pose()
                # pose.position.x = float(center_x)
                # pose.position.y = float(center_y)
                # pose.position.z = 0.0
                # response.poses.append(pose)
                # response.colors.append(ring.color)
                self.get_logger().warn(f"Invalid position found for ring {ring.id}, using original position.")

        # # Uporabimo Matplotlib za prikaz z legendo
        # fig, ax = plt.subplots(figsize=(8, 6))
        # im = ax.imshow(self.distance_map, cmap='jet')
        # cbar = plt.colorbar(im, ax=ax)
        # cbar.set_label('Razdalja do zida (v pikslijih)')

        # for pose in response.poses:
        #     x = (pose.position.x - self.map_origin.x) / self.map_resolution
        #     y = (pose.position.y - self.map_origin.y) / self.map_resolution
        #     y = self.map_height - y
        #     ax.plot(x, y, 'ro', markersize=5) 

        # ax.set_title('Razdalja do zidov (distance map)')
        # ax.axis('off')  # skrij osi (če želiš jih lahko pustiš)
        # plt.show()

        return response
    
    def find_valid_position_optimized(self, start_x, start_y):
        """
        Performs BFS starting from (start_x, start_y) to find the nearest cell
        that is free space and at least `self.min_wall_distance_cells` away
        from the nearest obstacle, using the precomputed distance map.
        """
        if not (0 <= start_x < self.map_width and 0 <= start_y < self.map_height):
            self.get_logger().warn(f"Start position ({start_x}, {start_y}) is outside map bounds ({self.map_width}x{self.map_height}).")
            return None

        q = deque([(start_x, start_y)])
        visited = set([(start_x, start_y)])

        while q:
            x, y = q.popleft()

            # Check map bounds just in case (should be handled by neighbor check)
            if not (0 <= x < self.map_width and 0 <= y < self.map_height):
                continue

            if self.distance_map[y, x] >= self.min_wall_distance_cells:
                self.get_logger().info(f"Found valid cell ({x}, {y}) with distance {self.distance_map[y, x]:.2f} >= {self.min_wall_distance_cells}")
                return x, y 

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy

                if (0 <= nx < self.map_width and 0 <= ny < self.map_height and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    q.append((nx, ny))

        self.get_logger().warn(f"BFS completed without finding a valid cell starting from ({start_x}, {start_y}) with min distance {self.min_wall_distance_cells}.")
        return None

def main(args=None):
    rclpy.init(args=args)
    node = RingMarkerSubscriber()

    # fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4), sharex=True, sharey=True)
    # ax = axes.ravel()

    # ax[0].imshow(node.map_image, cmap=plt.cm.gray)
    # ax[0].axis('off')
    # ax[0].set_title('original', fontsize=20)

    # ax[1].imshow(node.distance_map, cmap=plt.cm.gray)
    # ax[1].axis('off')
    # ax[1].set_title('skeleton', fontsize=20)
    # fig.tight_layout()
    # plt.show()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
    print("!!!")

if __name__ == '__main__':
    main()
