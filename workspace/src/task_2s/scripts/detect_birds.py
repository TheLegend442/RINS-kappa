#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, QoSReliabilityPolicy

from sensor_msgs.msg import Image, PointCloud2
from sensor_msgs_py import point_cloud2 as pc2

from visualization_msgs.msg import Marker
from custom_messages.msg import FaceCoordinates

from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

from ultralytics import YOLO

# from rclpy.parameter import Parameter
# from rcl_interfaces.msg import SetParametersResult

class Bird():
	def __init__(self, center, detection_time):
		self.center = center
		self.detection_time = detection_time


class detect_faces(Node):

	def __init__(self):
		super().__init__('detect_faces')

		self.declare_parameters(
			namespace='',
			parameters=[
				('device', ''),
		])

		marker_topic = "/bird_marker"

		self.detection_color = (0,0,255)
		self.device = self.get_parameter('device').get_parameter_value().string_value

		self.bridge = CvBridge()
		self.scan = None

		self.rgb_image_sub = self.create_subscription(Image, "/oakd/rgb/preview/image_raw", self.rgb_callback, qos_profile_sensor_data)
		self.pointcloud_sub = self.create_subscription(PointCloud2, "/oakd/rgb/preview/depth/points", self.pointcloud_callback, qos_profile_sensor_data)

		self.marker_pub = self.create_publisher(Marker, marker_topic, QoSReliabilityPolicy.BEST_EFFORT) # Publish face markers (center, bottom right, upper left)

		self.model = YOLO("yolov8n.pt")

		self.birds = []

		self.get_logger().info(f"Node has been initialized! Will publish face markers to {marker_topic}.")

	def rgb_callback(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			self.get_logger().error(f"CvBridge Error: {e}")
			return

		# Run YOLO detection on the image
		results = self.model(cv_image, verbose=False, device=self.device)
		detection_time = data.header.stamp

		self.birds = []  # clear previous detections


		for r in results:
			for box in r.boxes:
				cls_id = int(box.cls)
				cls_name = self.model.names[cls_id]

				if cls_name == 'bird':
					# Get bounding box center in image coordinates
					xyxy = box.xyxy[0].cpu().numpy()  # [x1, y1, x2, y2]
					x_center = int((xyxy[0] + xyxy[2]) / 2)
					y_center = int((xyxy[1] + xyxy[3]) / 2)

					# Save bird center pixel coordinates (we'll map to 3D in pointcloud_callback)
					self.birds.append(Bird(center=(x_center, y_center), detection_time=detection_time))

					# Optionally, draw detection on image
					cv2.rectangle(cv_image, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), self.detection_color, 2)
					# show center
					cv2.circle(cv_image, (x_center, y_center), 2, self.detection_color, -1)

					cv2.putText(cv_image, cls_name, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.detection_color, 2)

		# Optionally show image for debugging
		cv2.imshow("Bird Detection", cv_image)
		cv2.waitKey(1)


	def create_marker(self, d, data):
		marker = Marker()

		marker.header.frame_id = "/base_link"
		marker.header.stamp = data.header.stamp

		marker.type = 2
		marker.id = 0

		# Set the scale of the marker
		scale = 0.5
		marker.scale.x = scale
		marker.scale.y = scale
		marker.scale.z = scale

		# Set the color
		marker.color.r = 1.0
		marker.color.g = 0.0
		marker.color.b = 0.0
		marker.color.a = 1.0

		# Set the pose of the marker
		marker.pose.position.x = float(d[0])
		marker.pose.position.y = float(d[1])
		marker.pose.position.z = float(d[2])

		# self.get_logger().info(f"Marker created at {d[0]}, {d[1]}, {d[2]}")

		return marker


		return face_coordinates

	def pointcloud_callback(self, data):

		# get point cloud attributes
		height = data.height
		width = data.width
		point_step = data.point_step
		row_step = data.row_step		

		# iterate over birds
		for bird in self.birds:
			# get bird coordinates in 2D
			[x, y] = bird.center
			# transform into base_link coordinates
			a = pc2.read_points_numpy(data, field_names= ("x", "y", "z"))
			a = a.reshape((height,width,3))
			d = a[y, x, :]

			marker = self.create_marker(d, data)
			self.marker_pub.publish(marker)


def main():
	print('Face detection node starting.')

	rclpy.init(args=None)
	node = detect_faces()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()