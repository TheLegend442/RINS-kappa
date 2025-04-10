#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from custom_messages.msg import RingCoordinates
from builtin_interfaces.msg import Time
from custom_messages.srv import PosesInFrontOfRings
from geometry_msgs.msg import PoseWithCovarianceStamped, Pose
from nav_msgs.msg import OccupancyGrid

import numpy as np
import time
import cv2
import yaml
import tf2_ros
import tf2_geometry_msgs  # Za uporabo transformacij med sporočili


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Ring():
    def __init__(self, id, center, current_time=None, robot_position=None, count=1, color=None):
        self.id = id
        self.center = center
        self.current_time = current_time
        self.robot_position = robot_position
        self.count = count
        self.color = color

class RingMarkerSubscriber(Node):
    def __init__(self):
        super().__init__('ring_marker_subscriber')

        # Inicializacija TF2 listenerja
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Publisher za markerje
        marker_topic = '/detected_rings'
        self.marker_pub = self.create_publisher(Marker, marker_topic, 10)
        self.marker_sub = self.create_subscription(RingCoordinates, '/ring_marker', self.marker_callback, 10)

        # Subscription za pozicijo robota (AMCL)
        self.robot_position_subscription = self.create_subscription(
            PoseWithCovarianceStamped, '/amcl_pose', self.robot_position_callback, 10
        )

        # self.map_subscriber = self.create_subscription(OccupancyGrid, '/map', self.map_callback, 10)

        # Service that returns poses in front of detected rings
        self.service = self.create_service(PosesInFrontOfRings, 'get_ring_pose', self.get_ring_pose_callback)

        self.robot_position = None  # Shranjena pozicija robota
        self.rings = {}  # Slovar {ring_id: (position, timestamp, robot_position, count)}
        self.threshold = 0.7  # Razdalja za zaznavanje istega obroča
        self.time_threshold = 5  # Sekunde preden obroč ponovno upoštevamo
        self.ring_counter = 0  # Števec za unikatne ID-je obročev

        def load_map(self, pgm_path, yaml_path):
            """Naloži PGM sliko in YAML metapodatke zemljevida"""
            with open(yaml_path, 'r') as yaml_file:
                map_metadata = yaml.safe_load(yaml_file)

            map_image = cv2.imread(pgm_path, cv2.IMREAD_GRAYSCALE)
            if map_image is None:
                self.get_logger().error("Napaka pri nalaganju map.pgm!")
                exit(1)

            # Obrni sliko, če je potrebno (PGM zemljevidi so pogosto obrnjeni)
            #map_image = cv2.flip(map_image, 0)

            return map_image, map_metadata
        
        #Load the map
        self.map_image, self.map_metadata = load_map('src/dis_tutorial3/maps/map.pgm', 'src/dis_tutorial3/maps/map.yaml')

        self.map_data = None
        self.map_height, self.map_width = self.map_image.shape
        self.map_resolution = self.map_metadata['resolution']
        origin = self.map_metadata['origin']
        self.map_origin = Point(x=origin[0], y=origin[1], z=0.0)

    def robot_position_callback(self, msg):
        # Shrani pozicijo robota iz AMCL topica
        self.robot_position = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])

    def marker_callback(self, msg):
        if self.robot_position is None:
            self.get_logger().info("Pozicija robota ni bila prejeta, ignoriram zaznane obroče.")
            return
        
        current_position = np.array([msg.center.pose.position.x, msg.center.pose.position.y, msg.center.pose.position.z])
        color = msg.color
        current_time = time.time()
        stamp = msg.center.header.stamp
        # Poskusimo pridobiti transformacijo iz robotovega koordinatnega sistema v globalni za sredinsko točko in še oba kota
        try:
            transform = self.tf_buffer.lookup_transform('map', 'base_link', stamp)
            transformed_pose = tf2_geometry_msgs.do_transform_pose(msg.center.pose, transform)
            transformed_position = np.array([transformed_pose.position.x, transformed_pose.position.y, transformed_pose.position.z])

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().error(f"Napaka pri transformaciji: {e}")
            return

        # Preveri, ali je obroč že bil zaznan
        for ring_id, ring in self.rings.items():
            count = ring.count
            timestamp = ring.current_time
            center_point = ring.center

            distance = np.linalg.norm(center_point - transformed_position)
            
            if distance < self.threshold:
                if current_time - timestamp < self.time_threshold:
                    return
                else:
                    # **Izbrišemo prejšnji marker**
                    self.delete_marker(ring_id)

                    # **Posodobimo obraz s povprečjem**
                    new_position = (count / (count + 1)) * center_point + (1 / (count + 1)) * transformed_position
                    self.rings[ring_id] = Ring(ring_id, new_position, current_time, self.robot_position, count + 1, color=color)

                    # **Objavimo nov marker**
                    self.publish_ring_marker(new_position, ring_id)
                    return

        # **Če obroč ni bil zaznan, ga dodamo v slovar**
        self.ring_counter += 1
        self.get_logger().info(f"Zaznan nov obroč z ID-jem {self.ring_counter}.")
    
        for ring in self.rings.values():
            print(ring.center)

        self.rings[self.ring_counter] = Ring(self.ring_counter, transformed_position, current_time, self.robot_position, color=color)
        self.publish_ring_marker(transformed_position, self.ring_counter)

    def ring2rgb(self, ring):
        color = ring.color

        mapping = {
            "RED": (1.0, 0.0, 0.0),
            "GREEN": (0.0, 1.0, 0.0),
            "BLUE": (0.0, 0.0, 1.0),
            "YELLOW": (1.0, 1.0, 0.0),
            "BLACK" : (0.0, 0.0, 0.0),
        }

        return {"r": mapping[color][0], "g": mapping[color][1], "b": mapping[color][2]}

    def publish_ring_marker(self, position, ring_id):
        """Objavi marker za zaznan obroč."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "rings"
        marker.id = ring_id  # Unikatni ID markerja
        marker.type = Marker.SPHERE  # Oblika markerja
        marker.action = Marker.ADD  # Dodajanje ali posodabljanje markerja
        marker.pose.position.x = position[0]
        marker.pose.position.y = position[1]
        marker.pose.position.z = position[2]
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2

        ring = self.rings[ring_id]
        rgb = self.ring2rgb(ring)

        marker.color.r = rgb["r"]
        marker.color.g = rgb["g"]
        marker.color.b = rgb["b"]
        marker.color.a = 1.0  # Polna vidljivost
        marker.lifetime.sec = 0  # Ne izgine avtomatsko

        self.marker_pub.publish(marker)

    def delete_marker(self, ring_id):
        """Izbriše prejšnji marker, ko posodobimo obroč."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "rings"
        marker.id = ring_id
        marker.action = Marker.DELETE  # Izbriši prejšnji marker

        self.marker_pub.publish(marker)

    def map_callback(self,msg):
        # Get the map's metadata
        self.map_data = np.array(msg.data).reshape((msg.info.height, msg.info.width))
        self.map_width = msg.info.width
        self.map_height = msg.info.height
        self.map_resolution = msg.info.resolution
        self.map_origin = msg.info.origin.position

        self.get_logger().info("Map data received successfully")

    def get_ring_pose_callback(self, request, response):

        if self.map_data is None:
            self.get_logger().error("Map data not available")
            return response
        
        response.poses = []

        for ring in self.rings.values():
            center_x = ring.center[0]
            center_y = ring.center[1]

            cell_x = int((center_x - self.map_origin.x) / self.map_resolution)
            cell_y = int((center_y - self.map_origin.y) / self.map_resolution)

            nearest_wall_x, nearest_wall_y = self.find_nearest_wall(cell_x, cell_y)

            if nearest_wall_x is not None and nearest_wall_y is not None:
                # Add an offset from the wall (for example, 2 cells away)
                offset = 2
                marker_x = nearest_wall_x + offset
                marker_y = nearest_wall_y + offset

                # Convert marker position back to meters
                marker_x_meters = marker_x * self.map_resolution + self.map_origin.x
                marker_y_meters = marker_y * self.map_resolution + self.map_origin.y

                # Populate the response with the marker position
                pose = Pose()
                pose.position.x = marker_x_meters
                pose.position.y = marker_y_meters
                pose.position.z = 0

                response.poses.append(pose)
            else:
                self.get_logger().error("No wall found near the ring")
                continue
        
        return response


    def find_nearest_wall(self, start_x, start_y):
        """Helper function to find the nearest wall in the occupancy grid"""
        visited = np.zeros_like(self.map_data)
        queue = [(start_x, start_y)]
        visited[start_y, start_x] = 1

        while queue:
            x, y = queue.pop(0)

            # Check if the current cell is an occupied space (wall)
            if self.map_data[y, x] == 100:
                return x, y  # Return the coordinates of the nearest wall

            # Explore the neighboring cells
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.map_width and 0 <= ny < self.map_height and not visited[ny, nx]:
                    visited[ny, nx] = 1
                    queue.append((nx, ny))

        return None, None  # No wall found

def main(args=None):
    rclpy.init(args=args)
    node = RingMarkerSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()