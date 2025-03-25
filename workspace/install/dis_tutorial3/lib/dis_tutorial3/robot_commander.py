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
from lifecycle_msgs.srv import GetState
from nav2_msgs.action import Spin, NavigateToPose
from turtle_tf2_py.turtle_tf2_broadcaster import quaternion_from_euler

from irobot_create_msgs.action import Dock, Undock
from irobot_create_msgs.msg import DockStatus

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

from custom_messages.msg import FaceCoordinates
from custom_messages.srv import PosesInFrontOfFaces
from visualization_msgs.msg import Marker


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

        # client that receives poses in front of detected faces
        self.pose_client = self.create_client(PosesInFrontOfFaces, 'get_face_pose')
        
        # publisher for publishing markers of spots in front of faces
        self.spots_in_front_of_faces_pub = self.create_publisher(Marker, '/spots_in_front_of_faces', 10)

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
            self.map_image, self.map_metadata = self.load_map('src/dis_tutorial3/maps/map.pgm', 'src/dis_tutorial3/maps/map.yaml')
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
    
def main(args=None):
    
    rclpy.init(args=args)
    rc = RobotCommander()

    # Wait until Nav2 and Localizer are available
    rc.waitUntilNav2Active()

    # Check if the robot is docked, only continue when a message is recieved
    while rc.is_docked is None:
        rclpy.spin_once(rc, timeout_sec=0.5)

    # If it is docked, undock it first
    if rc.is_docked:
        rc.undock()
    #Load the map
    rc.map_image, rc.map_metadata = rc.load_map('src/dis_tutorial3/maps/map.pgm', 'src/dis_tutorial3/maps/map.yaml')
    cv2.imshow("Map", rc.map_image)
    cv2.setMouseCallback("Map", rc.mouse_callback)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    for i, (px, py, orientation) in enumerate(rc.clicked_points):
        world_x, world_y = rc.pixel_to_world(px, py)
        rc.get_logger().info(f"Točka {i+1}: ({world_x}, {world_y})")

        goal_msg = PoseStamped()
        goal_msg.header.frame_id = "map"
        goal_msg.header.stamp = rc.get_clock().now().to_msg()
        goal_msg.pose.position.x = world_x
        goal_msg.pose.position.y = world_y
        goal_msg.pose.orientation = rc.YawToQuaternion(orientation)  
        rc.goToPose(goal_msg)
        while not rc.isTaskComplete():
            rc.info("Waiting for the task to complete...")
            time.sleep(3.0)

    
    # go to all detected faces
    request = PosesInFrontOfFaces.Request()
    future = rc.pose_client.call_async(request)
    rclpy.spin_until_future_complete(rc, future)
    response = future.result()

    for i, pose in enumerate(response.poses):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rc.get_clock().now().to_msg()
        marker.ns = "spots_in_front_of_faces"
        marker.id = i
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position = pose.position
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 1.0
        marker.lifetime = Duration(sec=0)
        rc.spots_in_front_of_faces_pub.publish(marker)

        print(pose)

    
    
    for pose in response.poses:
        goal_msg = PoseStamped()
        goal_msg.header.frame_id = "map"
        goal_msg.header.stamp = rc.get_clock().now().to_msg()
        goal_msg.pose = pose
    
        rc.goToPose(goal_msg)
        while not rc.isTaskComplete():
            rc.info("Waiting for the task to complete...")
            time.sleep(3.0)
    

    rc.destroyNode()

    # And a simple example
if __name__=="__main__":
    main()