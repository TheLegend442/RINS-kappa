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
import random
import numpy as np
from task_2s.srv import GetGenderService
from ultralytics import YOLO
from collections import deque

from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
# from PIL import Image
# from rclpy.parameter import Parameter
# from rcl_interfaces.msg import SetParametersResult

class Point():
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Face():

	def __init__(self, center_point, bottom_right_point, upper_left_point,detection_time,spol,image):
		self.center_point = center_point
		self.bottom_right_point = bottom_right_point
		self.upper_left_point = upper_left_point
		self.detection_time = detection_time
		self.spol = spol
		self.image = image


class detect_faces(Node):

	def __init__(self):
		super().__init__('detect_faces')

		self.declare_parameters(
			namespace='',
			parameters=[
				('device', ''),
		])

		marker_topic = "/people_marker"

		self.detection_color = (0,0,255)
		self.device = self.get_parameter('device').get_parameter_value().string_value

		self.bridge = CvBridge()
		self.scan = None

		self.rgb_image_sub = self.create_subscription(Image, "/oakd/rgb/preview/image_raw", self.rgb_callback, qos_profile_sensor_data)
		self.pointcloud_sub = self.create_subscription(PointCloud2, "/oakd/rgb/preview/depth/points", self.pointcloud_callback, qos_profile_sensor_data)

		self.marker_pub = self.create_publisher(FaceCoordinates, marker_topic, QoSReliabilityPolicy.BEST_EFFORT) # Publish face markers (center, bottom right, upper left)

		

		self.gender_service = self.create_service(GetGenderService,"/get_gender_service", self.get_gender_callback)	

		self.model = YOLO("yolov8n.pt")
		self.faces = []
		self.last_face = None

		self.get_logger().info(f"Node has been initialized! Will publish face markers to {marker_topic}.")

		self.processor = None
		self.model_gender = None

	def get_gender_callback(self, request, response):
		if self.model_gender is None:
			model_name = "prithivMLmods/Realistic-Gender-Classification"
			self.processor = AutoImageProcessor.from_pretrained(model_name, use_fast=True)
			self.model_gender = AutoModelForImageClassification.from_pretrained(model_name)
		response = GetGenderService.Response()
		if len(self.faces) == 0:
			self.get_logger().info("No faces detected.")
			return response

		# Get the first bird's image
		face = self.last_face
		current_time = self.get_clock().now()
		print(f"Current time: {current_time}")
		print(f"Face detection time: {face.detection_time}")
		time_diff = (current_time - face.detection_time).nanoseconds / 1e9  # Convert to seconds
		self.get_logger().info(f"Bird detection difference: {time_diff} seconds")

		if time_diff > 2.0:
			self.get_logger().info("Face detection time is too old.")
			response.isok = False
			return response
		spol = self.predict_gender(face.image)
		if(spol == "male portrait" or spol == "Man"):
			response.gender = "M"
		else:
			response.gender = "F"
		self.get_logger().info(f"Face species: {spol}")
		return response
	
	def predict_gender(self, image):
		inputs = self.processor(images=image, return_tensors="pt")
		with torch.no_grad():
			outputs = self.model_gender(**inputs)
			logits = outputs.logits
			predicted_class = logits.argmax(-1).item()
		label = self.model_gender.config.id2label[predicted_class]
		return label
	
	def rgb_callback(self, data):
		self.faces = []
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
			#self.get_logger().info(f"Received RGB image with size: {cv_image.shape[0]}x{cv_image.shape[1]}")
			# self.get_logger().info(f"Running inference on image...")
			detection_time  = self.get_clock().now()
			# run inference
			res = self.model.predict(cv_image, imgsz=(256, 320), show=False, verbose=False, classes=[0], device=self.device)
			# iterate over results
			for x in res:
				bbox = x.boxes.xyxy
				if bbox.nelement() == 0: # skip if empty
					continue

				#self.get_logger().info(f"Person has been detected!")

				bbox = bbox[0]
				small_image = cv_image[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
				spol = "Female"
				if spol == 'Man':
					self.detection_color = (255, 0, 0)
				else:
					self.detection_color = (255, 0, 255)
				# draw rectangle
				cv_image = cv2.rectangle(cv_image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), self.detection_color, 3)

				cx = int((bbox[0]+bbox[2])/2)
				cy = int((bbox[1]+bbox[3])/2)

				bottom_right_x = int((2/3*bbox[0]+1/3*bbox[2]))
				bottom_right_y = int((2/3*bbox[1]+1/3*bbox[3]))
				upper_left_x = int((1/3*bbox[0]+2/3*bbox[2]))
				upper_left_y = int((1/3*bbox[1]+2/3*bbox[3]))

				bottom_right_point = Point(bottom_right_x, bottom_right_y)
				upper_left_point = Point(upper_left_x, upper_left_y)
				center_point = Point(cx, cy)

				# draw the center of bounding box
				cv_image = cv2.circle(cv_image, (cx,cy), 5, self.detection_color, -1)
				cv_image = cv2.circle(cv_image, (bottom_right_x, bottom_right_y), 5, self.detection_color, -1)
				cv_image = cv2.circle(cv_image, (upper_left_x, upper_left_y), 5, self.detection_color, -1)

				self.faces.append(Face(center_point, bottom_right_point, upper_left_point,detection_time, spol, small_image))
				self.last_face = self.faces[-1]
			cv2.imshow("image", cv_image)
			key = cv2.waitKey(1)
			if key==27:
				print("exiting")
				exit()
			
		except CvBridgeError as e:
			print(e)

	def create_marker(self, d,color, data):
		marker = Marker()

		marker.header.frame_id = "/base_link"
		marker.header.stamp = data.header.stamp

		marker.type = 2
		marker.id = 0

		# Set the scale of the marker
		scale = 0.1
		marker.scale.x = scale
		marker.scale.y = scale
		marker.scale.z = scale

		# Set the color
		marker.color.r = color[0] / 255.0
		marker.color.g = color[1] / 255.0
		marker.color.b = color[2] / 255.0
		marker.color.a = 1.0

		# Set the pose of the marker
		marker.pose.position.x = float(d[0])
		marker.pose.position.y = float(d[1])
		marker.pose.position.z = float(d[2])

		# self.get_logger().info(f"Marker created at {d[0]}, {d[1]}, {d[2]}")

		return marker

	def create_face_coordinates_message(self, face, data):
		# get point cloud attributes
		height = data.height
		width = data.width
		point_step = data.point_step
		row_step = data.row_step    

		face_coordinates = FaceCoordinates()

		# get 3-channel representation of the point cloud in numpy format
		a = pc2.read_points_numpy(data, field_names=("x", "y", "z"))
		a = a.reshape((height, width, 3))

		# gender
		spol = face.spol
		if spol == 'Man':
			color = (0, 0, 255)
		else:
			color = (255, 0, 0)

		# read center coordinates
		x = face.center_point.x
		y = face.center_point.y
		center_point = a[y, x, :]
		center_marker = self.create_marker(center_point, color, data)

		# read bottom right coordinates
		x = face.bottom_right_point.x
		y = face.bottom_right_point.y
		bottom_right_point = a[y, x, :]
		bottom_right_marker = self.create_marker(bottom_right_point, color, data)

		# read upper left coordinates
		x = face.upper_left_point.x
		y = face.upper_left_point.y
		upper_left_point = a[y, x, :]
		upper_left_marker = self.create_marker(upper_left_point, color, data)

		# Pogoj: objavi samo, če so vsi markerji pod 0.5 m višine (Z koordinata)
		if (
			center_point[2] < 0.5 and
			bottom_right_point[2] < 0.5 and
			upper_left_point[2] < 0.5
		):
			face_coordinates.center = center_marker
			face_coordinates.bottom_right = bottom_right_marker
			face_coordinates.upper_left = upper_left_marker
			return face_coordinates
		else:
			return None

	def pointcloud_callback(self, data):
		# get point cloud attributes
		height = data.height
		width = data.width
		point_step = data.point_step
		row_step = data.row_step
		self.get_logger().info(f"Publishing face markers for {len(self.faces)} detected faces.")
		# get 3-channel representation of the point cloud in numpy format
		# iterate over face coordinates
		for face in self.faces:
			face_coordinates_msg = self.create_face_coordinates_message(face, data)
			if face_coordinates_msg is not None:
				self.marker_pub.publish(face_coordinates_msg)

def main():
	print('Face detection node starting.')
	rclpy.init(args=None)
	node = detect_faces()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
