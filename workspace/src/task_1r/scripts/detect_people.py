#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, QoSReliabilityPolicy
from rclpy.clock import ClockType
from rclpy.clock import Clock

from sensor_msgs.msg import Image, CameraInfo
from visualization_msgs.msg import Marker
from custom_messages.msg import FaceCoordinates

from geometry_msgs.msg import Pose

from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

from ultralytics import YOLO

import tf2_ros
import tf2_geometry_msgs

import time

from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import ExternalShutdownException
from rclpy.executors import MultiThreadedExecutor


class CameraIntrinsics:
    def __init__(self):
        self.fx = 0.0
        self.fy = 0.0
        self.cx = 0.0
        self.cy = 0.0
        self.ready = False


class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Face():
    def __init__(self, center_point, bottom_right_point, upper_left_point):
        self.center_point = center_point
        self.bottom_right_point = bottom_right_point
        self.upper_left_point = upper_left_point



        self.maksov_time = None # Hvala Maks!!!


class DetectFaces(Node):

    def __init__(self):
        super().__init__('detect_faces')

        self.declare_parameters(namespace='', parameters=[('device', '')])

        self.intrinsics = CameraIntrinsics()
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.detection_color = (0, 0, 255)
        self.device = self.get_parameter('device').get_parameter_value().string_value

        self.bridge = CvBridge()
        self.faces = []
        self.depth_img = None

        self.depth_sub = self.create_subscription(Image, "/oak/stereo/image_raw", self.depth_callback, 1)
        self.rgb_image_sub = self.create_subscription(Image, "/oak/rgb/image_raw", self.rgb_callback, qos_profile_sensor_data)
        self.cam_info_sub = self.create_subscription(CameraInfo, '/oak/rgb/camera_info', self.cam_info_callback, qos_profile_sensor_data)

        self.marker_pub = self.create_publisher(FaceCoordinates, "/people_marker", QoSReliabilityPolicy.BEST_EFFORT)
        self.marker_pub_debug = self.create_publisher(Marker, "/people_marker_debug", QoSReliabilityPolicy.BEST_EFFORT)

        self.model = YOLO("yolov8n.pt")

        self.get_logger().info("Node has been initialized! Will publish face markers to /people_marker.")

    def cam_info_callback(self, msg: CameraInfo):
        self.intrinsics.fx = msg.k[0]
        self.intrinsics.fy = msg.k[4]
        self.intrinsics.cx = msg.k[2]
        self.intrinsics.cy = msg.k[5]
        self.intrinsics.ready = True
        # self.get_logger().info("Camera intrinsics received.")
        # self.cam_info_sub.destroy()

    def depth_callback(self, data):
        try:
            depth_image = self.bridge.imgmsg_to_cv2(data, "16UC1")
            depth_image[depth_image == np.inf] = 0
            self.depth_img = depth_image
        except CvBridgeError as e:
            print(e)

    def rgb_callback(self, data):

        maksov_time = data.header.stamp

        if not self.intrinsics.ready or self.depth_img is None:
            return

        self.faces = []

        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            res = self.model.predict(cv_image, imgsz=(256, 320), show=False, verbose=False, classes=[0], device=self.device)

            for x in res:
                bbox = x.boxes.xyxy
                if bbox.nelement() == 0:
                    continue

                bbox = bbox[-1]
                cv_image = cv2.rectangle(cv_image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), self.detection_color, 3)

                cx = int((bbox[0] + bbox[2]) / 2)
                cy = int((bbox[1] + bbox[3]) / 2)

                center = self.intrinsic_tf(cx, cy, maksov_time)
                if center is None:
                    continue

                bottom_right_x = int((2/3 * bbox[0] + 1/3 * bbox[2]))
                bottom_right_y = int((2/3 * bbox[1] + 1/3 * bbox[3]))
                bottom_right = self.intrinsic_tf(bottom_right_x, bottom_right_y, maksov_time)

                upper_left_x = int((1/3 * bbox[0] + 2/3 * bbox[2]))
                upper_left_y = int((1/3 * bbox[1] + 2/3 * bbox[3]))
                upper_left = self.intrinsic_tf(upper_left_x, upper_left_y, maksov_time)

                if bottom_right is None or upper_left is None:
                    continue

                face = Face(Point(*center), Point(*bottom_right), Point(*upper_left))
                face.maksov_time = maksov_time

                
                if 0.13 < face.center_point.z < 0.3:
                    self.faces.append(face)

                    face_coordinates_msg = self.create_face_coordinates_message(face)
                    #time.sleep(0.3)
                    self.marker_pub.publish(face_coordinates_msg)

                    cv_image = cv2.circle(cv_image, (cx, cy), 5, self.detection_color, -1)
                cv2.putText(cv_image, f"height: {face.center_point.z}",(0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                # cv2.line(cv_dashed, (0, y1), (x2, y2), (0, 0, 0), 1)

            cv2.imshow("image", cv_image)
            key = cv2.waitKey(1)
            if key == 27:
                print("Exiting")
                exit()

        except CvBridgeError as e:
            print(e)

    def intrinsic_tf(self, cx, cy, stamp):
        Z = float(self.depth_img[cy, cx]) / 1000.0 # iz mm v m
        if Z == 0:
            return None

        X = (cx - self.intrinsics.cx) * Z / self.intrinsics.fx
        Y = (cy - self.intrinsics.cy) * Z / self.intrinsics.fy

        pose = Pose()
        pose.position.x = X
        pose.position.y = Y
        pose.position.z = Z
        # print([X,Y,Z])
        try:
            #stamp = self.get_clock().now().to_msg()
            transform = self.tf_buffer.lookup_transform('map', 'oakd_rgb_camera_optical_frame', rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=0.3))
            transformed_pose = tf2_geometry_msgs.do_transform_pose(pose, transform)
            return (
                transformed_pose.position.x,
                transformed_pose.position.y,
                transformed_pose.position.z
            )
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().error(f"Transformation error: {e}")
            return None

    def create_marker(self, point, ros_time):
        marker = Marker()
        marker.header.frame_id = "/map"
        # ros_time = Clock(clock_type=ClockType.ROS_TIME).now()
        marker.header.stamp = ros_time

        marker.type = Marker.SPHERE
        marker.id = 0
        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.scale.z = 0.1

        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        marker.pose.position.x = point.x
        marker.pose.position.y = point.y
        marker.pose.position.z = point.z
        return marker

    def create_face_coordinates_message(self, face):
        face_coordinates = FaceCoordinates()
        face_coordinates.center = self.create_marker(face.center_point, face.maksov_time)
        face_coordinates.bottom_right = self.create_marker(face.bottom_right_point, face.maksov_time)
        face_coordinates.upper_left = self.create_marker(face.upper_left_point, face.maksov_time)

        current_center_marker = face_coordinates.center
        current_center_marker.color.b = 1.0
        current_center_marker.header.frame_id = "map"
        self.marker_pub_debug.publish(current_center_marker)

        return face_coordinates


def main():
    print('Face detection node starting.')
    rclpy.init()
    node = DetectFaces()
    rclpy.spin(node)
    # executor = MultiThreadedExecutor(num_threads=4)
    # executor.add_node(node)
    # executor.spin()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
