#! /usr/bin/env python3
# Mofidied from Samsung Research America
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from enum import Enum
import time

from action_msgs.msg import GoalStatus
from builtin_interfaces.msg import Duration
from geometry_msgs.msg import Quaternion, PoseStamped, PoseWithCovarianceStamped, Pose
from visualization_msgs.msg import Marker, MarkerArray
from lifecycle_msgs.srv import GetState
from nav2_msgs.action import Spin, NavigateToPose
from turtle_tf2_py.turtle_tf2_broadcaster import quaternion_from_euler

from irobot_create_msgs.action import Dock, Undock
from irobot_create_msgs.msg import DockStatus
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
from sklearn.cluster import KMeans
from geometry_msgs.msg import Quaternion, PoseStamped, PoseWithCovarianceStamped, Pose
from task_2s.srv import MarkerArrayService, GetImage, BirdCollection
from task_2s.msg import Bird


import rclpy
from rclpy.action import ActionClient
from rclpy.duration import Duration as rclpyDuration
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from rclpy.qos import qos_profile_sensor_data
import cv2
import yaml
import math
import subprocess
import os
import numpy as np
from random import randrange
from collections import deque

from custom_messages.msg import FaceCoordinates
from custom_messages.srv import PosesInFrontOfFaces, PosesInFrontOfRings
from custom_messages.msg import RingCoordinates
from std_msgs.msg import String
from visualization_msgs.msg import Marker
from task_2s.srv import MarkerArrayService, GetImage, BirdCollection, SpeechService
from task_2s.msg import Bird


class TaskResult(Enum):
    UNKNOWN = 0
    SUCCEEDED = 1
    CANCELED = 2
    FAILED = 3

amcl_pose_qos = QoSProfile(
          durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
          reliability=QoSReliabilityPolicy.RELIABLE,
          history=QoSHistoryPolicy.KEEP_LAST,
          depth=1)

class RobotCommander(Node):

    def __init__(self, node_name='robot_commander', namespace=''):
        super().__init__(node_name=node_name, namespace=namespace)
        
        #Parameters
        self.min_wall_distance_m = 0.5
        
        #Parameters
        
        self.pose_frame_id = 'map'
        
        # Flags and helper variables
        self.goal_handle = None
        self.result_future = None
        self.feedback = None
        self.status = None
        self.initial_pose_received = False
        self.is_docked = None
        self.clicked_points = []
        self.is_dragging = False
        self.start_point = None
        self.map_image, self.map_metadata = None, None
        # ROS2 subscribers
        self.create_subscription(DockStatus,
                                 'dock_status',
                                 self._dockCallback,
                                 qos_profile_sensor_data)
        
        self.localization_pose_sub = self.create_subscription(PoseWithCovarianceStamped,
                                                              'amcl_pose',
                                                              self._amclPoseCallback,
                                                              amcl_pose_qos)
        
        # ROS2 publishers
        self.initial_pose_pub = self.create_publisher(PoseWithCovarianceStamped,
                                                      'initialpose',
                                                      10)
        #ROS2 speach
        self.speech_pub = self.create_publisher(String, '/speech_text', 10)

        # client that receives poses in front of detected faces
        self.pose_client = self.create_client(PosesInFrontOfFaces, 'get_face_pose')

        self.birds_spots_pub = self.create_publisher(MarkerArray, '/spots_in_front_of_birds', 10)
        
        self.get_bird_image_client = self.create_client(GetImage, '/bird_image')

        self.bird_catalogue_client = self.create_client(BirdCollection, 'bird_catalogue')
        # client that receives poses in front of detected rings
        self.ring_client = self.create_client(PosesInFrontOfRings, 'get_ring_pose')

        self.rings_client = self.create_client(MarkerArrayService, 'get_rings')

        self.birds_client = self.create_client(MarkerArrayService, 'get_birds')
        
        # publisher for publishing markers of spots in front of faces
        self.spots_in_front_of_faces_pub = self.create_publisher(Marker, '/spots_in_front_of_faces', 10)

        # publisher for publishing markers of spots near rings
        self.ring_spots_pub = self.create_publisher(Marker, '/spots_in_front_of_rings', 10)
        
        self.sweep_spots_pub = self.create_publisher(Marker, '/sweep_spots', 10)

        self.birds_spots_pub = self.create_publisher(MarkerArray, '/spots_in_front_of_birds', 10)
        
        self.get_bird_image_client = self.create_client(GetImage, '/bird_image')

        self.bird_catalogue_client = self.create_client(BirdCollection, 'bird_catalogue')

        self.speech_client = self.create_client(SpeechService, 'speech_service')
        # ROS2 Action clients
        self.nav_to_pose_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.spin_client = ActionClient(self, Spin, 'spin')
        self.undock_action_client = ActionClient(self, Undock, 'undock')
        self.dock_action_client = ActionClient(self, Dock, 'dock')

        self.get_logger().info(f"Robot commander has been initialized!")
        
    def destroyNode(self):
        self.nav_to_pose_client.destroy()
        super().destroy_node()     

    def goToPose(self, pose, behavior_tree=''):
        """Send a `NavToPose` action request."""
        self.debug("Waiting for 'NavigateToPose' action server")
        while not self.nav_to_pose_client.wait_for_server(timeout_sec=1.0):
            self.info("'NavigateToPose' action server not available, waiting...")

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose
        goal_msg.behavior_tree = behavior_tree

        self.info('Navigating to goal: ' + str(pose.pose.position.x) + ' ' +
                  str(pose.pose.position.y) + '...')
        send_goal_future = self.nav_to_pose_client.send_goal_async(goal_msg,
                                                                   self._feedbackCallback)
        rclpy.spin_until_future_complete(self, send_goal_future)
        self.goal_handle = send_goal_future.result()

        if not self.goal_handle.accepted:
            self.error('Goal to ' + str(pose.pose.position.x) + ' ' +
                       str(pose.pose.position.y) + ' was rejected!')
            return False

        self.result_future = self.goal_handle.get_result_async()
        return True

    def spin(self, spin_dist=1.57, time_allowance=10):
        self.debug("Waiting for 'Spin' action server")
        while not self.spin_client.wait_for_server(timeout_sec=1.0):
            self.info("'Spin' action server not available, waiting...")
        goal_msg = Spin.Goal()
        goal_msg.target_yaw = spin_dist
        goal_msg.time_allowance = Duration(sec=time_allowance)

        self.info(f'Spinning to angle {goal_msg.target_yaw}....')
        send_goal_future = self.spin_client.send_goal_async(goal_msg, self._feedbackCallback)
        rclpy.spin_until_future_complete(self, send_goal_future)
        self.goal_handle = send_goal_future.result()

        if not self.goal_handle.accepted:
            self.error('Spin request was rejected!')
            return False

        self.result_future = self.goal_handle.get_result_async()
        return True
    
    def undock(self):
        """Perform Undock action."""
        self.info('Undocking...')
        self.undock_send_goal()

        while not self.isUndockComplete():
            time.sleep(0.1)

    def undock_send_goal(self):
        goal_msg = Undock.Goal()
        self.undock_action_client.wait_for_server()
        goal_future = self.undock_action_client.send_goal_async(goal_msg)

        rclpy.spin_until_future_complete(self, goal_future)

        self.undock_goal_handle = goal_future.result()

        if not self.undock_goal_handle.accepted:
            self.error('Undock goal rejected')
            return

        self.undock_result_future = self.undock_goal_handle.get_result_async()

    def isUndockComplete(self):
        """
        Get status of Undock action.

        :return: ``True`` if undocked, ``False`` otherwise.
        """
        if self.undock_result_future is None or not self.undock_result_future:
            return True

        rclpy.spin_until_future_complete(self, self.undock_result_future, timeout_sec=0.1)

        if self.undock_result_future.result():
            self.undock_status = self.undock_result_future.result().status
            if self.undock_status != GoalStatus.STATUS_SUCCEEDED:
                self.info(f'Goal with failed with status code: {self.status}')
                return True
        else:
            return False

        self.info('Undock succeeded')
        return True

    def cancelTask(self):
        """Cancel pending task request of any type."""
        self.info('Canceling current task.')
        if self.result_future:
            future = self.goal_handle.cancel_goal_async()
            rclpy.spin_until_future_complete(self, future)
        return

    def isTaskComplete(self):
        """Check if the task request of any type is complete yet."""
        if not self.result_future:
            # task was cancelled or completed
            return True
        rclpy.spin_until_future_complete(self, self.result_future, timeout_sec=0.10)
        if self.result_future.result():
            self.status = self.result_future.result().status
            if self.status != GoalStatus.STATUS_SUCCEEDED:
                self.debug(f'Task with failed with status code: {self.status}')
                return True
        else:
            # Timed out, still processing, not complete yet
            return False

        self.debug('Task succeeded!')
        return True

    def getFeedback(self):
        """Get the pending action feedback message."""
        return self.feedback

    def getResult(self):
        """Get the pending action result message."""
        if self.status == GoalStatus.STATUS_SUCCEEDED:
            return TaskResult.SUCCEEDED
        elif self.status == GoalStatus.STATUS_ABORTED:
            return TaskResult.FAILED
        elif self.status == GoalStatus.STATUS_CANCELED:
            return TaskResult.CANCELED
        else:
            return TaskResult.UNKNOWN

    def waitUntilNav2Active(self, navigator='bt_navigator', localizer='amcl'):
        """Block until the full navigation system is up and running."""
        self._waitForNodeToActivate(localizer)
        if not self.initial_pose_received:
            time.sleep(1)
        self._waitForNodeToActivate(navigator)
        self.info('Nav2 is ready for use!')
        return

    def _waitForNodeToActivate(self, node_name):
        # Waits for the node within the tester namespace to become active
        self.debug(f'Waiting for {node_name} to become active..')
        node_service = f'{node_name}/get_state'
        state_client = self.create_client(GetState, node_service)
        while not state_client.wait_for_service(timeout_sec=1.0):
            self.info(f'{node_service} service not available, waiting...')

        req = GetState.Request()
        state = 'unknown'
        while state != 'active':
            self.debug(f'Getting {node_name} state...')
            future = state_client.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            if future.result() is not None:
                state = future.result().current_state.label
                self.debug(f'Result of get_state: {state}')
            time.sleep(2)
        return
    
    def YawToQuaternion(self, angle_z = 0.):
        quat_tf = quaternion_from_euler(0, 0, angle_z)

        # Convert a list to geometry_msgs.msg.Quaternion
        quat_msg = Quaternion(x=quat_tf[0], y=quat_tf[1], z=quat_tf[2], w=quat_tf[3])
        return quat_msg

    def _amclPoseCallback(self, msg):
        self.debug('Received amcl pose')
        self.initial_pose_received = True
        self.current_pose = msg.pose
        return

    def _feedbackCallback(self, msg):
        self.debug('Received action feedback message')
        self.feedback = msg.feedback
        return
    
    def _dockCallback(self, msg: DockStatus):
        self.is_docked = msg.is_docked

    def setInitialPose(self, pose):
        msg = PoseWithCovarianceStamped()
        msg.pose.pose = pose
        msg.header.frame_id = self.pose_frame_id
        msg.header.stamp = 0
        self.info('Publishing Initial Pose')
        self.initial_pose_pub.publish(msg)
        return

    def info(self, msg):
        self.get_logger().info(msg)
        return

    def warn(self, msg):
        self.get_logger().warn(msg)
        return

    def error(self, msg):
        self.get_logger().error(msg)
        return

    def debug(self, msg):
        self.get_logger().debug(msg)
        return
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

            self.map_matrix_np = np.zeros_like(self.map_image, dtype=np.uint8)
            self.map_matrix_np[self.map_image >= 3] = 255
            self.map_matrix_np[self.map_image < 3] = 0

            num_free = np.sum(self.map_matrix_np == 255)
            num_occupied = np.sum(self.map_matrix_np == 0)
            self.get_logger().info("Calculating distance transform...")
            binary_map_for_dist = np.zeros_like(self.map_matrix_np, dtype=np.uint8)
            binary_map_for_dist[self.map_matrix_np == 255] = 255
            self.distance_map = cv2.distanceTransform(binary_map_for_dist, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
            self.get_logger().info("Distance transform calculated.")

            self.min_wall_distance_cells = int(self.min_wall_distance_m / self.map_resolution)
            self.get_logger().info(f"Minimum wall distance set to {self.min_wall_distance_m} m ({self.min_wall_distance_cells} cells)")
            self.map_image[self.map_image == 3] = 255
            self.map_image[self.map_image == 2] = 100
            self.map_image[self.map_image == 0] = 0
            # # Uporabimo Matplotlib za prikaz z legendo
            # fig, ax = plt.subplots(figsize=(8, 6))
            # im = ax.imshow(self.map_matrix_np, cmap='jet')
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
    def draw_arrow(self, start, end):
        """Draw an arrow from start to end point."""
        cv2.arrowedLine(self.map_image, start, end, (0, 255, 0), 2)

    def mouse_callback(self, event, x, y, flags, param):
        """Shrani klikane točke in prikaži jih na sliki"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.is_dragging = True
            self.start_point = (x, y)  # Save the starting point for dragging
            self.get_logger().info(f"Started dragging from: {x}, {y}")
        elif event == cv2.EVENT_MOUSEMOVE and self.is_dragging:
            # Clear the image and redraw previous points
            self.map_image, self.map_metadata = self.load_map('src/task_2s/maps/bird_map.pgm', 'src/task_2s/maps/bird_map.yaml')
            self.draw_previous_markers()  # Re-draw any previously stored points
            # Draw the current arrow
            self.draw_arrow(self.start_point, (x, y))
            cv2.imshow("Map", self.map_image)
        elif event == cv2.EVENT_LBUTTONUP and self.is_dragging:
            self.is_dragging = False
            # Calculate orientation in degrees
            orientation = self.calculate_orientation(self.start_point, (x, y))
            self.clicked_points.append((self.start_point[0], self.start_point[1], orientation))
            #self.draw_arrow(self.start_point, (x, y))  # Draw final arrow
            cv2.imshow("Map", self.map_image)
            self.get_logger().info(f"Clicked point: {x}, {y} with orientation: {orientation}°")

    def calculate_orientation(self, start, end):
        """Calculate the angle of the arrow from start to end point."""
        delta_x = end[0] - start[0]
        delta_y = start[1] - end[1]  # Invert y-axis for image coordinates
        angle = math.atan2(delta_y, delta_x)  # Calculate angle in radians
        return angle

    def draw_previous_markers(self):
        """Redraw all previously stored points and arrows."""
        for point in self.clicked_points:
            x, y, orientation = point
            # Draw point
            #cv2.circle(self.map_image, (x, y), 5, (0, 255, 0), -1)
            if orientation is not None:
                # Calculate the arrow end position based on orientation
                arrow_length = 30
                x_end = int(x + arrow_length * math.cos(orientation))
                y_end = int(y - arrow_length * math.sin(orientation))  # Inverted Y-axis for image coordinates
                self.draw_arrow((x, y), (x_end, y_end))


    def pixel_to_world(self, pixel_x, pixel_y):
        """Pretvori slikovne koordinate v metrične glede na YAML podatke"""
        origin = self.map_metadata['origin']
        resolution = self.map_metadata['resolution']
        height, _ = self.map_image.shape

        world_x = origin[0] + pixel_x * resolution
        world_y = origin[1] + (height - pixel_y) * resolution  # Obrnemo os Y

        return world_x, world_y
    def world_to_pixel(self, world_x, world_y):
        """Pretvori svetovne koordinate v slikovne glede na YAML podatke"""
        origin = self.map_metadata['origin']
        resolution = self.map_metadata['resolution']

        pixel_x = int((world_x - origin[0]) / resolution)
        pixel_y = int((world_y - origin[1]) / resolution)
        height, _ = self.map_image.shape
        pixel_y = height - pixel_y  # Obrnemo os Y
        return pixel_x, pixel_y
    def say_something(self, text):
        """Send a message to the speech node"""
        msg = String()
        msg.data = text
        self.speech_pub.publish(msg)
        self.get_logger().info(f"Sending speech command: {text}")
        return
    def automatic_Sweeping(self):

        def select_evenly_distributed(points, percentage=0.1):
            num_clusters = max(1, int(len(points) * percentage))
            kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(points)
            centers = kmeans.cluster_centers_
            return centers 
        def check_if_close_to_wall(point, map_image):
            x = int(round(point[0]))
            y = int(round(point[1]))
            if self.distance_map[x][y] < self.min_wall_distance_cells:
                return False
            else:
                # Draw a circle around the point
                cv2.circle(map_image, (point[1], point[0]), 1, (255), -1)
                return True
        def find_best_points(points, map_image):
            def normalize_angle_rad(angle):
                return (angle + 2 * math.pi) % (2 * math.pi)

            def je_notri(i, j, x, y, angle_rad):
                dx = x - i
                dy = y - j
                if math.hypot(dx, dy) > 50:
                    return False

                theta = math.atan2(dy, dx)
                delta = normalize_angle_rad(min(theta - angle_rad,2* math.pi + angle_rad - theta))

                return abs(delta) <= math.radians(50)

            best_point = None
            best_points = []

            for point in tqdm(points):
                map_points = [
                    (i, j)
                    for i in range(map_image.shape[0])
                    for j in range(map_image.shape[1])
                    if map_image[i][j] == 255
                ]
                pokrije = 0
                for angle_rad in [a * math.pi / 180 for a in range(0, 370, 10)]:
                    t_pokrije = 0
                    for x, y in map_points:
                        if je_notri(point[0], point[1], x, y, angle_rad):
                            t_pokrije += 1
                    if t_pokrije >= pokrije:
                        pokrije = t_pokrije
                        best_point = (point[0], point[1], angle_rad)
                best_points.append(best_point)
                for x, y in map_points:
                    if je_notri(point[0], point[1], x, y, best_point[2]):
                        map_image[x][y] = 0




            return best_points
        # 1. Naredi binarno sliko za skeletonize (npr. vse vrednosti >= 3 naj bodo 1)
        binary_map = (self.map_image >= 255).astype(np.uint8)
        walls_map = cv2.cvtColor(self.map_image,cv2.COLOR_GRAY2BGR)
        walls_map[self.map_image == 0] = (255,0,0) 
        bin_map_walls = np.zeros_like(self.map_image, dtype=np.uint8)
        bin_map_walls[self.map_image == 0] = 255

        # 2. Skeletonize pričakuje bool tip
        skeleton = skeletonize(binary_map.astype(bool))

        prepareed_map = self.map_image.copy()
        points_cor = [(i, j) for i in range(skeleton.shape[0]) for j in range(skeleton.shape[1]) if skeleton[i][j]]
        points_cor = np.array(points_cor)
        random_points = select_evenly_distributed(points_cor, 0.02)
        random_points = list(random_points)
        random_points = [(int(point[0]), int(point[1])) for point in random_points]
        self.info(f"Found {len(random_points)} random points")
        #print(random_points)
        good_points = []
        for point in random_points:
            if check_if_close_to_wall(point, prepareed_map):
                good_points.append((point[1], point[0], 0.0))
        self.info(f"Found {len(good_points)} good points")
        

        best_points = []
        best_points = find_best_points(good_points, bin_map_walls)
        
        print(best_points)

        best_points_map = np.zeros_like(self.map_image, dtype=np.uint8)
        for point in best_points:
            cv2.circle(best_points_map, (point[0], point[1]), 1, (255), -1)
        
        map_points = np.zeros_like(self.map_image, dtype=np.uint8)
        for point in good_points:
            cv2.circle(map_points, (point[0], point[1]), 1, (255), -1)
        
        fig, axes = plt.subplots(nrows=1, ncols=7, figsize=(8, 4), sharex=True, sharey=True)


        ax = axes.ravel()

        ax[0].imshow(prepareed_map, cmap=plt.cm.gray)
        ax[0].axis('off')
        ax[0].set_title('original', fontsize=20)

        ax[1].imshow(skeleton, cmap=plt.cm.gray)
        ax[1].axis('off')
        ax[1].set_title('skeleton', fontsize=20)

        ax[2].imshow(self.distance_map, cmap=plt.cm.gray)
        ax[2].axis('off')
        ax[2].set_title('distance_map', fontsize=20)

        ax[3].imshow(map_points, cmap=plt.cm.gray)
        ax[3].axis('off')
        ax[3].set_title('points', fontsize=20)

        ax[4].imshow(best_points_map, cmap=plt.cm.gray)
        ax[4].axis('off')
        ax[4].set_title('best_points', fontsize=20)

        ax[5].imshow(walls_map)
        ax[5].axis('off')
        ax[5].set_title('walls', fontsize=20)

        ax[6].imshow(bin_map_walls)
        ax[6].axis('off')
        ax[6].set_title('bin_map_walls', fontsize=20)

        fig.tight_layout()
        plt.show()

        self.info(f"Trying to find best points")

        return best_points
    
    def najboljsi_obhod(self,clicked_points):
        def distance_between_points(self, start_x, start_y, end_x, end_y):
            """
            Performs BFS starting from (start_x, start_y) to find the nearest cell
            that is free space and at least `self.min_wall_distance_cells` away
            from the nearest obstacle, using the precomputed distance map.
            """
            if not (0 <= start_x < self.map_width and 0 <= start_y < self.map_height):
                self.get_logger().warn(f"Start position ({start_x}, {start_y}) is outside map bounds ({self.map_width}x{self.map_height}).")
                return None

            q = deque([(start_x, start_y, 0)])
            visited = set([(start_x, start_y)])

            while q:
                x, y, d = q.popleft()
                # Check map bounds just in case (should be handled by neighbor check)
                if not (0 <= x < self.map_width and 0 <= y < self.map_height):
                    continue
                if self.map_matrix_np[y][x] == 0:
                    continue

                if x == end_x and y == end_y:
                    return d

                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy

                    if (0 <= nx < self.map_width and 0 <= ny < self.map_height and (nx, ny) not in visited):
                        visited.add((nx, ny))
                        q.append((nx, ny, d + 1))

            self.get_logger().warn(f"BFS completed without finding a valid cell starting from ({start_x}, {start_y}) with min distance {self.min_wall_distance_cells}.")
            return None
        
        def trenutna_dolzina_poti(robot_position, permutation, distance_matrix):
            # Dobimo trenutno pot robota
            current_position = 0
            distance = 0
            for target in permutation:
                distance += distance_matrix[current_position][target]
                current_position = target
            return distance
        
        distance_matrix = np.zeros((len(clicked_points), len(clicked_points)))
        for i in tqdm(range(len(clicked_points))):
            for j in range(len(clicked_points)):
                if i <= j:
                    distance_matrix[i][j] = distance_between_points(self, clicked_points[i][0], clicked_points[i][1], clicked_points[j][0], clicked_points[j][1])
                    distance_matrix[j][i] = distance_matrix[i][j]
        permutation = []
        for i in range(len(clicked_points)):
            permutation.append(i)
        best_score = trenutna_dolzina_poti(0, permutation, distance_matrix)
        for i in range(10000):
            k,m = randrange(1, len(clicked_points)), randrange(1, len(clicked_points))
            permutation[k], permutation[m] = permutation[m], permutation[k]
            new_score = trenutna_dolzina_poti(0, permutation, distance_matrix)
            if new_score < best_score:
                best_score = new_score
            else:
                permutation[k], permutation[m] = permutation[m], permutation[k]
        best_permutation = []
        for i in range(len(clicked_points)):
            best_permutation.append(clicked_points[permutation[i]])
        return best_permutation
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

def best_round(robot_position, all_targets):
    def trenutna_dolžina_poti(robot_position, all_targets):
        # Dobimo trenutno pot robota
        current_position = robot_position
        distance = 0
        for target in all_targets:
            distance += math.sqrt((current_position[0] - target["pose"].position.x) ** 2 +
                                 (current_position[1] - target["pose"].position.y) ** 2)
            
            current_position = (target["pose"].position.x, target["pose"].position.y)
        return distance
    current_score = trenutna_dolžina_poti(robot_position, all_targets)
    for i in range(10000):
        k,m = randrange(0, len(all_targets)), randrange(0, len(all_targets))
        all_targets[k], all_targets[m] = all_targets[m], all_targets[k]
        new_score = trenutna_dolžina_poti(robot_position, all_targets)
        if new_score < current_score:
            current_score = new_score
        else:
            all_targets[k], all_targets[m] = all_targets[m], all_targets[k]
    return all_targets
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
def get_poses_in_front_of_birds(rc):
    request_rings = MarkerArrayService.Request()
    future_rings = rc.rings_client.call_async(request_rings)
    rclpy.spin_until_future_complete(rc, future_rings)
    response_rings = future_rings.result()

    request_birds = MarkerArrayService.Request()
    future_birds = rc.birds_client.call_async(request_birds)
    rclpy.spin_until_future_complete(rc, future_birds)
    response_birds = future_birds.result()

    ring_bird_pairs = []
    for ring_marker, ring_color in zip(response_rings.marker_array.markers, response_rings.colors):
        for bird_marker, robot_position_marker in zip(response_birds.marker_array.markers, response_birds.robot_positions.markers):
            distance = math.sqrt((ring_marker.pose.position.x - bird_marker.pose.position.x) ** 2 +
                                 (ring_marker.pose.position.y - bird_marker.pose.position.y) ** 2)
            if distance < 0.5:
                ring_bird_pairs.append((ring_marker, bird_marker, robot_position_marker, ring_color))

    print(len(ring_bird_pairs), "pairs of rings and birds found")
    marker_array = MarkerArray()
    i = 0
    ring_colors = []

    for ring_marker, bird_marker, robot_position_marker, ring_color in ring_bird_pairs:
        ring_colors.append(ring_color)

        dx = bird_marker.pose.position.x - ring_marker.pose.position.x
        dy = bird_marker.pose.position.y - ring_marker.pose.position.y

        bird_px, bird_py = rc.world_to_pixel(bird_marker.pose.position.x, bird_marker.pose.position.y)

        # Določimo pravokotno smer samo po x ali y
        if abs(dx) > abs(dy):
            # smer bolj horizontalna => pravokotno po y osi
            candidates = [(0, 1), (0, -1)]
        else:
            # smer bolj vertikalna => pravokotno po x osi
            candidates = [(1, 0), (-1, 0)]

        found = False
        for step in range(1, 30):  # do 30 pixlov v vsako stran
            for offset_x, offset_y in candidates:
                nx = int(bird_px + step * offset_x)
                ny = int(bird_py + step * offset_y)

                if not (0 <= nx < rc.map_width and 0 <= ny < rc.map_height):
                    continue

                if rc.distance_map[ny, nx] >= rc.min_wall_distance_cells:
                    found = True
                    break
            if found:
                break

        if not found:
            rc.get_logger().warn("Could not find valid position in front of bird.")
            continue

        # Svetovne koordinate
        world_x, world_y = rc.pixel_to_world(nx, ny)

        # Orientacija proti ptiču
        angle_to_bird = math.atan2(bird_marker.pose.position.y - world_y,
                                   bird_marker.pose.position.x - world_x)
        q = quaternion_from_euler(0, 0, angle_to_bird)

        pose = Pose()
        pose.position.x = world_x
        pose.position.y = world_y
        pose.position.z = bird_marker.pose.position.z
        pose.orientation.x = q[0]
        pose.orientation.y = q[1]
        pose.orientation.z = q[2]
        pose.orientation.w = q[3]

        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rc.get_clock().now().to_msg()
        marker.ns = "spots_in_front_of_birds"
        marker.id = i
        marker.type = Marker.ARROW
        marker.action = Marker.ADD
        marker.pose = pose
        marker.scale.x = 0.4
        marker.scale.y = 0.1
        marker.scale.z = 0.1
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 1.0
        marker.lifetime = Duration(sec=0)
        marker_array.markers.append(marker)
        i += 1

    rc.birds_spots_pub.publish(marker_array)
    return marker_array, ring_colors


def get_location(marker):
    x = marker.pose.position.x
    y = marker.pose.position.y
    # zgoraj
    # x: -4.4358811378479
    # y: 3.3039188385009766
    # spodaj
    # x: 1.9387037754058838
    # y: 3.322540283203125
    # loči, na kateri strani premice je marker

    zgoraj = np.array([-4.4358811378479, 3.3039188385009766])
    spodaj = np.array([1.9387037754058838, 3.322540283203125])
    # ločilna premica
    # y = kx + b
    k = (zgoraj[1] - spodaj[1]) / (zgoraj[0] - spodaj[0])
    if zgoraj[0] < spodaj[0]:
        k = -k
    b = zgoraj[1] - k * zgoraj[0]
    if y > k*x + b:
        return "CENTER"
    else:
        return "EAST"



def pojdi_na_nejcovo_tocko(rc):
    nejc_point = [90,168]
    world_x, world_y = rc.pixel_to_world(nejc_point[0], nejc_point[1])
    rc.info(f"Točka {0}: ({world_x}, {world_y})")
    goal_msg = PoseStamped()
    goal_msg.header.frame_id = "map"
    goal_msg.header.stamp = rc.get_clock().now().to_msg()
    goal_msg.pose.position.x = world_x
    goal_msg.pose.position.y = world_y
    goal_msg.pose.orientation = rc.YawToQuaternion(-math.pi/2)
    rc.info(f"Going to pose: {goal_msg.pose.position.x}, {goal_msg.pose.position.y}")
    rc.goToPose(goal_msg)
    while not rc.isTaskComplete():
        #rc.info("Waiting for the task to complete...")
        time.sleep(0.1)
        
def main(args=None):
    rclpy.init(args=args)
    rc = RobotCommander()

    rc.waitUntilNav2Active()

    rc.load_and_process_map('src/task_2s/maps/bird_map.pgm', 'src/task_2s/maps/bird_map.yaml')
    rc.get_logger().info("Map loaded and processed.")

    current_pose = rc.world_to_pixel(rc.current_pose.pose.position.x, rc.current_pose.pose.position.y)
    current_pose = (int(current_pose[0]), int(current_pose[1]), rc.current_pose.pose.orientation.z)

    rc.get_logger().info(f"Moving arm to starting position")
    process = subprocess.Popen(["ros2", "topic", "pub", "--once", "/arm_command", "std_msgs/msg/String","{data: 'manual:[0.,0.,0.6,1.0]'}"])
    time.sleep(5) # Wait for the robot arm to reach the starting position
    process.terminate()


    if not os.path.exists('src/task_2s/data/obhod.npy'):
        rc.clicked_points = rc.automatic_Sweeping()
        rc.clicked_points = [current_pose] + rc.clicked_points
        rc.clicked_points = rc.najboljsi_obhod(rc.clicked_points)
        np.save('src/task_2s/data/obhod.npy', rc.clicked_points)
    else:
        print("Obhod že obstaja")
        rc.clicked_points = np.load('src/task_2s/data/obhod.npy')

    # show_points = np.zeros_like(rc.map_image)
    # for (px, py, orientation) in rc.clicked_points:
    #     world_x, world_y = rc.pixel_to_world(px, py)
    #     cv2.circle(show_points, (int(px), int(py)), 3, (255), -1)
    # cv2.imshow("Map", show_points)
 

    # POSTAVI MARKERJE ZA OBHOD
    for i, (px, py, orientation) in enumerate(rc.clicked_points):
        world_x, world_y = rc.pixel_to_world(px, py)
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = rc.get_clock().now().to_msg()
        pose.pose.position.x = world_x
        pose.pose.position.y = world_y
        pose.pose.orientation = rc.YawToQuaternion(orientation)

        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rc.get_clock().now().to_msg()
        marker.ns = "spots_in_front_of_rings"
        marker.id = i
        marker.type = Marker.ARROW
        marker.action = Marker.ADD
        marker.pose = pose.pose
        marker.scale.x = 0.4
        marker.scale.y = 0.1
        marker.scale.z = 0.1
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 1.0
        marker.lifetime = Duration(sec=0)
        rc.sweep_spots_pub.publish(marker)
        time.sleep(0.1)
    

    for i, (px, py, orientation) in enumerate(rc.clicked_points):
        world_x, world_y = rc.pixel_to_world(px, py)
        rc.get_logger().info(f"Točka {i+1}: ({world_x}, {world_y})")

        goal_msg = PoseStamped()
        goal_msg.header.frame_id = "map"
        goal_msg.header.stamp = rc.get_clock().now().to_msg()
        goal_msg.pose.position.x = world_x
        goal_msg.pose.position.y = world_y
        goal_msg.pose.orientation = rc.YawToQuaternion(orientation)  
        rc.info(f"Going to pose: {goal_msg.pose.position.x}, {goal_msg.pose.position.y}")
        rc.goToPose(goal_msg)
        while not rc.isTaskComplete():
            #rc.info("Waiting for the task to complete...")
            time.sleep(0.1)

    for i  in range(10):
        rc.info("KOČAL Z OBHODOM")

    # obhod po detektiranih parih ptič-obroč
    marker_array, ring_colors = get_poses_in_front_of_birds(rc)
    birds = []
    
    for marker, ring_color in zip(marker_array.markers, ring_colors):
        print(ring_color, type(ring_color))
        pose = marker.pose
        goal_msg = PoseStamped()
        goal_msg.header.frame_id = "map"
        goal_msg.header.stamp = rc.get_clock().now().to_msg()
        goal_msg.pose = pose
        rc.info(f"Going to pose: {goal_msg.pose.position.x}, {goal_msg.pose.position.y}")
        rc.goToPose(goal_msg)
        while not rc.isTaskComplete():
            #rc.info("Waiting for the task to complete...")
            time.sleep(0.1)
        
        # get a picture and classify bird
        request = GetImage.Request()
        future = rc.get_bird_image_client.call_async(request)
        rclpy.spin_until_future_complete(rc, future)
        response = future.result()
        if response is None:
            rc.error("Error while getting image")
        else:
            bird = Bird()
            bird.species = response.species_name
            bird.image = response.image
            bird.location = get_location(marker)
            bird.ring_color = ring_color
            bird.detection_time = "TODO"
            birds.append(bird)
            rc.info(f"Bird species: {bird.species}")
            rc.info(f"Ring color: {bird.ring_color}")
            rc.say_something(f"Detected {bird.species} with {bird.ring_color} ring")
        time.sleep(1)

    # generate bird catalogue
    request = BirdCollection.Request()
    request.birds = birds
    future = rc.bird_catalogue_client.call_async(request)
    #rclpy.spin_until_future_complete(rc, future) NEKI KATALOG NE DELA
    #response = future.result()                   NEKI KATALOG NE DELA


        

    # # Dobimo obroče
    # request_rings = PosesInFrontOfRings.Request()
    # future_rings = rc.ring_client.call_async(request_rings)
    # rclpy.spin_until_future_complete(rc, future_rings)
    # response_rings = future_rings.result()
    # rc.info(f"{len(response_rings.poses)} detected rings")

    # # Simulirano: dodajamo 'color' atribut (tu bi moral biti del dejanskega odziva)
    # rings_with_meta = [{"pose": pose, "type": "ring", "color": color} for pose, color in zip(response_rings.poses, response_rings.colors)]

    # for i, item in enumerate(rings_with_meta):
    #     pose = item["pose"]
    #     marker = Marker()
    #     marker.header.frame_id = "map"
    #     marker.header.stamp = rc.get_clock().now().to_msg()
    #     marker.ns = "spots_in_front_of_rings"
    #     marker.id = i
    #     marker.type = Marker.ARROW
    #     marker.action = Marker.ADD
    #     marker.pose = pose
    #     marker.pose.orientation = rc.YawToQuaternion(pose.orientation.z)
    #     marker.scale.x = 0.4
    #     marker.scale.y = 0.1
    #     marker.scale.z = 0.1
    #     marker.color.r = 0.0
    #     marker.color.g = 1.0
    #     marker.color.b = 0.0
    #     marker.color.a = 1.0
    #     marker.lifetime = Duration(sec=0)
    #     rc.ring_spots_pub.publish(marker)

    #Dobimo obraze
    rc.info("Getting faces")
    request_faces = PosesInFrontOfFaces.Request()
    future_faces = rc.pose_client.call_async(request_faces)
    rclpy.spin_until_future_complete(rc, future_faces)
    response_faces = future_faces.result()
    rc.info(f"{len(response_faces.poses)} detected faces")

    faces_with_meta = [{"pose": pose, "type": "face", "gender": gender} for pose,gender in zip(response_faces.poses, response_faces.genders)]

    for i, item in enumerate(faces_with_meta):
        pose = item["pose"]
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rc.get_clock().now().to_msg()
        marker.ns = "spots_in_front_of_faces"
        marker.id = i
        marker.type = Marker.ARROW
        marker.action = Marker.ADD
        marker.pose = pose
        marker.pose.orientation = rc.YawToQuaternion(pose.orientation.z)
        gender = item["gender"]
        if gender == "M":
            marker.color.r = 0.0
            marker.color.g = 0.0
            marker.color.b = 1.0
        else:
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
        marker.color.a = 1.0

        marker.scale.x = 0.4
        marker.scale.y = 0.1
        marker.scale.z = 0.1
        marker.lifetime = Duration(sec=0)
        rc.spots_in_front_of_faces_pub.publish(marker)

    # Združimo v eno zaporedje
    all_targets =  faces_with_meta #+ rings_with_meta
    all_targets = best_round((rc.current_pose.pose.position.x, rc.current_pose.pose.position.y), all_targets)
    rc.info(f"Going to {len(all_targets)} targets")

    for i, item in enumerate(all_targets):
        pose = item["pose"]
        goal_msg = PoseStamped()
        goal_msg.header.frame_id = "map"
        goal_msg.header.stamp = rc.get_clock().now().to_msg()
        goal_msg.pose = pose
        if math.isnan(goal_msg.pose.position.x) or math.isnan(goal_msg.pose.position.y):
            rc.info("NaN detected, skipping this target")
            continue
        rc.info(f"Going to pose {i+1}: {goal_msg.pose.position.x}, {goal_msg.pose.position.y}")
        rc.goToPose(goal_msg)

        while not rc.isTaskComplete():
            time.sleep(0.1)

        if item["type"] == "face":
            # strings = ["Hello how are you?", "Nice to meet you!", "Hi there friend!"]
            # random_string = strings[randrange(len(strings))]
            spol = item["gender"]
            request = SpeechService.Request()
            request.gender = spol
            request.birds = birds
            future = rc.speech_client.call_async(request)
            rclpy.spin_until_future_complete(rc, future)
            response = future.result()
            # rc.say_something("Hello how are you?")
        elif item["type"] == "ring":
            barva = item["color"]
            rc.say_something(f"This is {barva.lower()} ring.")

        time.sleep(2.0)
    
    pojdi_na_nejcovo_tocko(rc)
    process = subprocess.Popen(["ros2", "run", "task_2s", "bridge_follower.py"])
    time.sleep(30)
    process.terminate()
    rc.destroyNode()

    # And a simple example
if __name__=="__main__":
    main()
