#!/usr/bin/python3

import rclpy
import rclpy.duration
from rclpy.node import Node

from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from action_msgs.msg import GoalStatus

from std_msgs.msg import String
from trajectory_msgs.msg import JointTrajectoryPoint
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy
from rclpy.qos import QoSReliabilityPolicy, QoSProfile

from sensor_msgs.msg import Image, PointCloud2
from visualization_msgs.msg import Marker
from custom_messages.msg import RingCoordinates
from geometry_msgs.msg import Twist
from task_2s.srv import GoBridgeFollower

from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import time
import subprocess


qos_profile = QoSProfile(
          durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
          reliability=QoSReliabilityPolicy.RELIABLE,
          history=QoSHistoryPolicy.KEEP_LAST,
          depth=1)

class BridgeFollower(Node):
    def __init__(self):
        super().__init__('bridge_follower')
        self.active_service = self.create_service(GoBridgeFollower, '/active_service', self.make_active_callback)
        self.active = False

        self.arm_pub = self.create_publisher(String, '/arm_command', qos_profile)
        self.bridge = CvBridge()

        self.depth_sub = self.create_subscription(Image, "/oakd/rgb/preview/depth", self.depth_callback, 1)
        self.image_sub = self.create_subscription(Image, "/top_camera/rgb/preview/image_raw", self.image_callback, 1)
        self.oakd_image_sub = self.create_subscription(Image, "/oakd/rgb/preview/image_raw", self.oakd_image_callback, 1)
        self.amcl_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.send_cmd_vel)

        self.cmd = Twist()
        self.depth_img = None
        self.oakd_img = None

        self.parked = False


        self.get_logger().info(f"Initialized the Bridge Follower node! Waiting for commands...")
        

        cv2.namedWindow("Live camera feed", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("Binary Image", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Directions", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("Depth window", cv2.WINDOW_NORMAL)

    def make_active_callback(self, request, response):
        process = subprocess.Popen(["ros2", "topic", "pub", "--once", "/arm_command", "std_msgs/msg/String","{data: 'manual:[0.,0.,0.4,2.19]'}"])
        time.sleep(3) # Wait for the robot arm to reach the starting position
        process.terminate()
        self.active = True
        response.success = True
        self.get_logger().info("Bridge follower is active!")
        return response

    def send_cmd_vel(self):
        self.amcl_pub.publish(self.cmd)

    def send_driving_instructions(self, angle, deafult_speed=1.5):
        speed = deafult_speed
        if np.abs(angle) < 0.5:
            speed = deafult_speed
            angle = 0.0
        elif np.abs(angle) < 5:
            speed = 0.7
            angle = angle / 10
        elif np.abs(angle) < 10:
            speed = 0.5
            angle = angle / 20
        else:
            speed = 0.3
            angle = angle / 50
        
        angle = np.round(angle, 2)
        angle = np.clip(angle, -0.5, 0.5)

        self.update_cmd_vel(angle, speed)

    def send_parking_instructions(self):
        self.update_cmd_vel(1.0, 0.0)

    def update_cmd_vel(self, angle, speed):
        self.cmd.linear.x = speed
        self.cmd.angular.z = angle

    def oakd_image_callback(self,data):

        if self.parked or not self.active: # Check if depth image is present
            return
        
        try:
            oakd_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        self.oakd_img = oakd_image

        cv2.imshow("Live camera feed", oakd_image)

    def depth_callback(self,data):

        if self.parked or not self.active: # Check if depth image is present
            return
        
        try:
            depth_image = self.bridge.imgmsg_to_cv2(data, "32FC1")
        except CvBridgeError as e:
            print(e)

        depth_image[depth_image==np.inf] = 0
        self.depth_img = depth_image

        image_1 = depth_image / 65536.0 * 255 # Do the necessairy conversion so we can visuzalize it in OpenCV
        image_1 = image_1/np.max(image_1)*255

        image_viz = np.array(image_1, dtype= np.uint8)

        # cv2.putText(image_viz, f"{self.depth_img[150,150]} ", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # cv2.imshow("Depth window", image_viz)
        # cv2.waitKey(1)

    def image_callback(self,data):

        if self.parked or not self.active: # Check if depth image is present
            return

        if self.depth_img is None: # Check if depth image is present
            self.get_logger().info("No depth image yet, skipping this image")
            return
        
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        cv_raw = cv_image.copy()

        def process_image(image):
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, np.ones((20, 20), np.uint8))
            eroded = cv2.erode(closed, np.ones((20, 20), np.uint8), iterations=1)
            dilated = cv2.dilate(eroded, np.ones((10, 10), np.uint8), iterations=1)

            return dilated

        dilated = process_image(cv_image)
        edges = cv2.Canny(dilated, 50, 150)


        # Convert to color so we can draw in red later
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        directions = cv_image.copy()
        height, width, _ = edges_colored.shape

        # Define 3 horizontal lines at fixed Y-positions
        scan_lines = [int(height * 0.5), int(height * 0.65), int(height * 0.8)]

        midpoints = []
        for y in scan_lines:
            # Get x-coordinates where edge exists on that scanline
            x_coords = np.where(edges_colored[y, :] > 0)[0]

            # Keep only x-coordinates that are well separated
            x_coords = x_coords[np.diff(x_coords, prepend=-1) > 10]
            
            cv2.line(directions, (0, y), (width - 1, y), (0, 255, 0), 1)

            if len(x_coords) > 2:
                # Get the x-coordinates of the intersections
                self.get_logger().info(f"To many intersections detected{len(x_coords)} - skipping this frame")
                return
            elif len(x_coords) == 2: # Two intersections detected
                cv2.circle(directions, (x_coords[0], y), radius=5, color=(0, 0, 255), thickness=-1)
                cv2.circle(directions, (x_coords[1], y), radius=5, color=(0, 0, 255), thickness=-1)
                midpoint = int((x_coords[0] + x_coords[1]) / 2)
                cv2.circle(directions, (midpoint, y), radius=5, color=(0, 255, 0), thickness=-1)
            elif len(x_coords) == 1: # One intersection detected
                cv2.circle(directions, (x_coords[0], y), radius=5, color=(0, 0, 255), thickness=-1)
                if x_coords[0] < width / 2:
                    midpoint = int((width - x_coords[0]) / 2 + x_coords[0] + width / 8)
                    cv2.circle(directions, (midpoint, y), radius=5, color=(0, 255, 0), thickness=-1)
                else:
                    midpoint = int(x_coords[0] / 2) - int(width / 8)
                    cv2.circle(directions, (midpoint, y), radius=5, color=(0, 255, 0), thickness=-1)
            elif len(x_coords) == 0: # No intersections detected
                self.get_logger().info("No intersections detected - skipping this frame")
                return
            
            midpoints.append((midpoint, y))
            
        # Calculate the final midpoint
        if len(midpoints) != 3:
            self.get_logger().info("Not enough midpoints detected - skipping this frame")
            return
        if np.abs((midpoints[1][0] + midpoints[2][0]) / 2 - midpoints[0][0]) < width / 3:
            final_midpoint = [0.3 * midpoints[0][0] + 0.3 * midpoints[1][0] + 0.4 * midpoints[2][0], midpoints[0][1]]
        else:
            final_midpoint = [0.5 * midpoints[1][0] + 0.5 * midpoints[2][0], midpoints[0][1]]
        
        # Calculate the angle
        ref_point = (width // 2, height - 1)
        target_point = tuple(map(int, final_midpoint))
        angle = np.arctan2(ref_point[0] - target_point[0], np.abs(target_point[1] - ref_point[1]))
        angle = np.degrees(angle)

        ## ____POLE DETECTION____

        depth_h, depth_w = self.depth_img.shape
        y1, y2 = depth_h // 2 - 5, depth_h // 2 + 5
        x1, x2 = depth_w // 2 - 30, depth_w // 2 + 30
        window_of_interest = self.depth_img[y1:y2, x1:x2]
        mask = np.where(window_of_interest > 0)

        ## ____CMD VEL INSTRUCTIONS____

        if len(mask[0]) > 0:
            avg_depth = np.mean(window_of_interest[mask])
            if avg_depth < 0.76: # Reached the pole
                self.parked = True
                self.get_logger().info("Parked!")
                self.send_parking_instructions()
                self.arm_pub.publish(String(data='manual:[0.,-0.8,2.3,1.]'))
                self.parked = True
                time.sleep(3) # Wait before destroying the windows
                cv2.destroyAllWindows()
                return
            else:
                self.send_driving_instructions(angle)
        else: 
            self.send_driving_instructions(angle)

        ## ____VIZUALIZATION (depth image)____

        image_1 = self.depth_img / 65536.0 * 255 # Do the necessairy conversion so we can visuzalize it in OpenCV
        image_1 = image_1/np.max(image_1)*255

        image_viz = np.array(image_1, dtype= np.uint8)
        image_viz_color = cv2.cvtColor(image_viz, cv2.COLOR_GRAY2BGR)

        if len(mask[0]) > 0:
            avg_depth = np.mean(window_of_interest[mask])
            color = (0, 255, 0) if avg_depth < 1.2 else (255, 0, 255)
            cv2.putText(image_viz_color, f"Avg depth: {avg_depth:.2f} m", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            if avg_depth < 1.2:
                region = image_viz_color[y1:y2, x1:x2]
                region[mask] = [0, 255, 0]
                image_viz_color[y1:y2, x1:x2] = region

        
        cv2.rectangle(image_viz_color, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue rectangle
        # cv2.imshow("Depth window", image_viz_color)
        # cv2.waitKey(1)

        ## ____VIZUALIZATION (directions)____

        cv2.putText(
            directions,
            f"Angle: {angle:.2f} deg",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )
        cv2.arrowedLine(directions, ref_point, target_point, color=(0, 0, 255), thickness=2, tipLength=0.1)
        cv2.imshow("Directions", directions)
        cv2.waitKey(1)
        

        ## ____VIZUALIZATION (raw image)____

        def draw_dashed_rect(img, pt1, pt2, color, thickness=1, dash_length=5):
                x1, y1 = pt1
                x2, y2 = pt2

                # Draw dashed top and bottom
                for x in range(x1, x2, dash_length * 2):
                    cv2.line(img, (x, y1), (min(x + dash_length, x2), y1), color, thickness)
                    cv2.line(img, (x, y2), (min(x + dash_length, x2), y2), color, thickness)

                # Draw dashed left and right
                for y in range(y1, y2, dash_length * 2):
                    cv2.line(img, (x1, y), (x1, min(y + dash_length, y2)), color, thickness)
                    cv2.line(img, (x2, y), (x2, min(y + dash_length, y2)), color, thickness)
        if self.oakd_img is not None:
            cv_oakd = self.oakd_img.copy()
            if len(mask[0]) > 0:
                avg_depth = np.mean(window_of_interest[mask])
                color = (0, 255, 0) if avg_depth < 1.2 else (0, 0, 255)
                cv2.putText(cv_oakd, f"Avg depth: {avg_depth:.2f} m", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

                draw_dashed_rect(cv_oakd, (x1, y1), (x2, y2), (255, 255, 255), thickness=1, dash_length=4)

                if avg_depth < 1.2:
                    region = cv_oakd[y1:y2, x1:x2]
                    region[mask] = [0, 255, 0]
                    cv_oakd[y1:y2, x1:x2] = region

            cv2.imshow("Live camera feed", cv_oakd)
            cv2.waitKey(1)

        ## ____VIZUALIZATION (raw image)____
        
        # cv2.imshow("Binary image", dilated)
        cv2.waitKey(1)

def main():

    rclpy.init(args=None)
    rd_node = BridgeFollower()

    rclpy.spin(rd_node)

if __name__ == '__main__':
    main()