#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, QoSReliabilityPolicy
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy
from rclpy.qos import QoSReliabilityPolicy, QoSProfile

import rclpy.time
from sensor_msgs.msg import Image, PointCloud2
from sensor_msgs_py import point_cloud2 as pc2
from std_msgs.msg import String

from visualization_msgs.msg import Marker
from custom_messages.msg import FaceCoordinates

from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

from ultralytics import YOLO

import torch
import torchvision.models as models  # or your custom model
import torch.nn as nn
from PIL import Image as PILImage
from torchvision import transforms
import joblib
from sklearn.preprocessing import LabelEncoder
from task_2s.srv import MarkerArrayService, GetImage

import time

# from rclpy.parameter import Parameter
# from rcl_interfaces.msg import SetParametersResult

qos_profile = QoSProfile(
		  durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
		  reliability=QoSReliabilityPolicy.RELIABLE,
		  history=QoSHistoryPolicy.KEEP_LAST,
		  depth=1)

class Bird():
	def __init__(self, center, detection_time, species, image,image_procent=None):
		self.center = center
		self.detection_time = detection_time
		self.species = species
		self.image = image
		self.image_procent = image_procent


class Detect_birds(Node):

	def __init__(self):
		super().__init__('detect_birds')

		self.arm_pub = self.create_publisher(String, '/arm_command', qos_profile)
		self.arm_pub.publish(String(data='manual:[0.,0.,0.6,1.0]'))
		time.sleep(3) # Wait for the robot arm to reach the starting position


		self.declare_parameters(
			namespace='',
			parameters=[
				('device', 'cuda' if torch.cuda.is_available() else 'cpu'),
		])

		self.detection_color = (0,0,255)
		self.device = self.get_parameter('device').get_parameter_value().string_value

		self.bird_classification_model = torch.load('./src/task_2s/models/bird_species_model.pth')
		self.bird_classification_model = self.bird_classification_model.to(self.device)
		self.bird_classification_model.eval()

		self.label_encoder = joblib.load('./src/task_2s/models/label_encoder.pkl')

		self.bird_image_transform = transforms.Compose([
			transforms.Resize((224, 224)),
			transforms.ToTensor(),
		])

		marker_topic = "/bird_marker"


		self.last_bird_image = None
		self.is_bird_image = False
		self.bridge = CvBridge()
		self.scan = None

		self.rgb_image_sub = self.create_subscription(Image, "top_camera/rgb/preview/image_raw", self.rgb_callback, qos_profile_sensor_data)
		self.pointcloud_sub = self.create_subscription(PointCloud2, "/top_camera/rgb/preview/depth/points", self.pointcloud_callback, qos_profile_sensor_data)

		self.marker_pub = self.create_publisher(Marker, marker_topic, QoSReliabilityPolicy.BEST_EFFORT) # Publish face markers (center, bottom right, upper left)
		self.text_pub = self.create_publisher(Marker, "/text", QoSReliabilityPolicy.BEST_EFFORT) # Publish text markers (Bird)

		self.bird_image_service = self.create_service(GetImage, "/bird_image", self.get_bird_image_callback)

		self.model = YOLO("yolov8n.pt")

		self.birds = []

		self.get_logger().info(f"Node has been initialized! Will publish face markers to {marker_topic}.")

	def get_bird_image_callback(self, request, response):
		response = GetImage.Response()
		if len(self.birds) == 0:
			self.get_logger().info("No birds detected.")
			return response

		# Get the first bird's image
		bird = self.birds[-1]
		response.image = self.bridge.cv2_to_imgmsg(bird.image, encoding="bgr8")
		response.species_name = bird.species
		current_time = self.get_clock().now()
		print(f"Current time: {current_time}")
		print(f"Bird detection time: {bird.detection_time}")
		time_diff = (current_time - bird.detection_time).nanoseconds / 1e9  # Convert to seconds
		self.get_logger().info(f"Bird detection difference: {time_diff} seconds")

		if time_diff > 2.0:
			self.get_logger().info("Bird detection time is too old.")
			response.isok = False
			return response
		print(f"Bird procent : {bird.image_procent}")
		if bird.image_procent < 0.03:
			self.get_logger().info("Bird image is too small.")
			response.isok = False
			return response
		if bird.image.shape[0]/bird.image.shape[1] > 2:
			self.get_logger().info("Bird image is too tall.")
			response.isok = False
			return response
		
		response.isok = True
		self.get_logger().info(f"Bird species: {bird.species}")
		return response

	def rgb_callback(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			self.get_logger().error(f"CvBridge Error: {e}")
			return

		# Run YOLO detection on the image
		results = self.model(cv_image, verbose=False, device=self.device)
		detection_time  = self.get_clock().now()
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

					# classify bird species
					border = 10
					x_min = max(0, int(xyxy[0]) - border)
					x_max = min(cv_image.shape[1], int(xyxy[2]) + border)
					y_min = max(0, int(xyxy[1]) - border)
					y_max = min(cv_image.shape[0], int(xyxy[3]) + border)
					bird_proportion = (x_max - x_min) * (y_max - y_min) / (cv_image.shape[0] * cv_image.shape[1])
					bird_image_cropped = cv_image[y_min:y_max, x_min:x_max]
					image_copy = bird_image_cropped.copy()
					bird_image = cv2.cvtColor(bird_image_cropped, cv2.COLOR_BGR2RGB)
					bird_image = PILImage.fromarray(bird_image)
					bird_image = self.bird_image_transform(bird_image)
					bird_image = bird_image.unsqueeze(0).to(self.device)
					with torch.no_grad():
						outputs = self.bird_classification_model(bird_image)
						_, predicted = torch.max(outputs, 1)
						predicted_label = self.label_encoder.inverse_transform(predicted.cpu().numpy())[0]
						self.get_logger().info(f"Predicted bird species: {predicted_label}")


					cv2.imshow(f"cropped bird", bird_image_cropped)
					# Save bird center pixel coordinates (we'll map to 3D in pointcloud_callback)
					self.birds.append(Bird(center=(x_center, y_center), detection_time=detection_time, species=predicted_label, image=image_copy, image_procent=bird_proportion))

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
		scale = 0.3
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

		text_marker = Marker()
		text_marker.header.frame_id = "/base_link"
		text_marker.header.stamp = data.header.stamp
		text_marker.type = Marker.TEXT_VIEW_FACING
		text_marker.id = 1  # Important: unique ID per marker in same namespace

		text_marker.scale.z = 0.2  # Only scale.z matters for text
		text_marker.color.r = 1.0
		text_marker.color.g = 1.0
		text_marker.color.b = 1.0
		text_marker.color.a = 1.0

		text_marker.pose.position.x = float(d[0])
		text_marker.pose.position.y = float(d[1])
		text_marker.pose.position.z = float(d[2]) + 0.4  # Offset upward to float above sphere

		text_marker.text = "Bird"

		return [marker, text_marker]

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

			sphere_marker, text_marker = self.create_marker(d, data)
			self.marker_pub.publish(sphere_marker)
			self.text_pub.publish(text_marker)


def main():
	print('Bird recognition node starting.')

	rclpy.init(args=None)
	node = Detect_birds()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()