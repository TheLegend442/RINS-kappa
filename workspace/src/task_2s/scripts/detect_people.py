#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, QoSReliabilityPolicy

from sensor_msgs.msg import Image, PointCloud2
from sensor_msgs_py import point_cloud2 as pc2

from visualization_msgs.msg import Marker
from custom_messages.msg import FaceCoordinates
from deepface import DeepFace

from cv_bridge import CvBridge, CvBridgeError
import cv2
import random
import numpy as np

from ultralytics import YOLO

# from rclpy.parameter import Parameter
# from rcl_interfaces.msg import SetParametersResult

class Point():
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Face():

	def __init__(self, center_point, bottom_right_point, upper_left_point,spol):
		self.center_point = center_point
		self.bottom_right_point = bottom_right_point
		self.upper_left_point = upper_left_point
		self.spol = spol


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

		self.model = YOLO("yolov8n.pt")

		self.faces = []

		self.get_logger().info(f"Node has been initialized! Will publish face markers to {marker_topic}.")

	def rgb_callback(self, data):

		self.faces = []

		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

			# self.get_logger().info(f"Running inference on image...")

			# run inference
			res = self.model.predict(cv_image, imgsz=(256, 320), show=False, verbose=False, classes=[0], device=self.device)
			# iterate over results
			for x in res:
				bbox = x.boxes.xyxy
				if bbox.nelement() == 0: # skip if empty
					continue

				# self.get_logger().info(f"Person has been detected!")

				bbox = bbox[0]
				small_image = cv_image[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
				result = DeepFace.analyze(small_image, actions=['gender'], enforce_detection=True)
				#result = [{'gender': 'Man' if random.random() < 0.5 else	"Woman"}] # Sim
				spol = result[0]['gender']
				if spol == 'Man':
					self.detection_color = (255, 0, 0)
				else:
					self.detection_color = (0, 0, 255)
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

				self.faces.append(Face(center_point, bottom_right_point, upper_left_point,spol))

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
		a = pc2.read_points_numpy(data, field_names= ("x", "y", "z"))
		a = a.reshape((height,width,3))

		# gender
		spol = face.spol
		if spol == 'Man':
			color = (0, 0, 255)
		else:
			color = (255, 0, 0)
		

		# read center coordinates d = [x,y,z] v koordinatah sveta
		x = face.center_point.x
		y = face.center_point.y
		d = a[y,x,:]
		center_marker = self.create_marker(d, color, data)

		# read bottom right coordinates d = [x,y,z] v koordinatah sveta
		x = face.bottom_right_point.x
		y = face.bottom_right_point.y
		d = a[y,x,:]
		bottom_right_marker = self.create_marker(d, color,  data)
		
		# read upper left coordinates d = [x,y,z] v koordinatah sveta
		x = face.upper_left_point.x
		y = face.upper_left_point.y
		d = a[y,x,:]
		upper_left_marker = self.create_marker(d, color, data)

		face_coordinates.center = center_marker
		face_coordinates.bottom_right = bottom_right_marker
		face_coordinates.upper_left = upper_left_marker

		return face_coordinates

	def pointcloud_callback(self, data):

		# get point cloud attributes
		height = data.height
		width = data.width
		point_step = data.point_step
		row_step = data.row_step		

		# iterate over face coordinates
		for face in self.faces:

			face_coordinates_msg = self.create_face_coordinates_message(face, data)

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
