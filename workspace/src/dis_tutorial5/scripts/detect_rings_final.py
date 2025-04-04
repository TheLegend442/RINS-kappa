#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, QoSReliabilityPolicy

from sensor_msgs.msg import Image, PointCloud2
from sensor_msgs_py import point_cloud2 as pc2

from visualization_msgs.msg import Marker
from custom_messages.msg import RingCoordinates

from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Ring():
    def __init__(self, ellipse1, ellipse2):
        self.ellipse1 = ellipse1
        self.ellipse2 = ellipse2

        self.center1 = Point(0, 0)
        self.center2 = Point(0, 0)

        self.center1.x = int(ellipse1[0][0])
        self.center1.y = int(ellipse1[0][1])

        self.center2.x = int(ellipse2[0][0])
        self.center2.y = int(ellipse2[0][1])

class detect_rings(Node):
    def __init__(self):
        super().__init__('detect_rings')

        self.declare_parameters(
                namespace='',
                parameters=[
                    ('device', ''),
        ])

        marker_topic = '/ring_marker'
        self.detection_color = (255,0,0) # blue
        
        self.device = self.get_parameter('device').get_parameter_value().string_value

        self.bridge = CvBridge() # An object we use for converting images between ROS format and OpenCV format

        self.depth_sub = self.create_subscription(Image, "/oakd/rgb/preview/depth", self.depth_callback, 1)
        self.image_sub = self.create_subscription(Image, "/oakd/rgb/preview/image_raw", self.image_callback, 1)
        self.pointcloud_sub = self.create_subscription(PointCloud2, "/oakd/rgb/preview/depth/points", self.pointcloud_callback, qos_profile_sensor_data)

        self.marker_pub = self.create_publisher(RingCoordinates, marker_topic, QoSReliabilityPolicy.BEST_EFFORT)

        self.depth_img = None
        self.rings = []
        self.flat_rings = []

        ## ____Vizualization____

        # cv2.namedWindow("Binary Image", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("Detected contours", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Detected rings", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("Gray Image", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("Depth window", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Live camera feed", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("Ring depth", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Edges", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Detected ellipses", cv2.WINDOW_NORMAL)


        self.get_logger().info(f"Node has been initialized! Will publish face markers to {marker_topic}.")

    def depth_callback(self,data):
        try:
            depth_image = self.bridge.imgmsg_to_cv2(data, "32FC1")
        except CvBridgeError as e:
            print(e)

        depth_image[depth_image==np.inf] = 0
        self.depth_img = depth_image

        ## ____VIZUALIZATION____

        # image_1 = depth_image / 65536.0 * 255 # Do the necessairy conversion so we can visuzalize it in OpenCV
        # image_1 = image_1/np.max(image_1)*255

        # image_viz = np.array(image_1, dtype= np.uint8)

        # cv2.imshow("Depth window", image_viz)
        # cv2.waitKey(1)

    def image_callback(self,data):

        if self.depth_img is None: # Check if depth image is present
            self.get_logger().info("No depth image yet, skipping this image")
            return
        
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        
        ## ____VIZUALIZATION (dashed line at y=90)____

        cv_dashed = cv_image.copy()
        start_point = (0, 90)
        end_point = (cv_image.shape[1], 90)

        dash_length, gap_length = 10, 5
        line_length = int(np.linalg.norm(np.array(start_point) - np.array(end_point)))

        for i in range(0, line_length, dash_length + gap_length):
            x1 = int(start_point[0] + i * (end_point[0] - start_point[0]) / line_length)
            y1 = int(start_point[1] + i * (end_point[1] - start_point[1]) / line_length)
            
            x2 = int(start_point[0] + (i + dash_length) * (end_point[0] - start_point[0]) / line_length)
            y2 = int(start_point[1] + (i + dash_length) * (end_point[1] - start_point[1]) / line_length)
     
            cv2.line(cv_dashed, (x1, y1), (x2, y2), (0, 0, 0), 1)

        cv2.imshow("Live camera feed", cv_dashed)
        cv2.waitKey(1)


        ## ____ELLIPSE DETECTION____

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        self.rings = []
        self.flat_rings = []

        def ellipse_detection(image, canny_threshold1=50, canny_threshold2=150, min_major_axis=10, max_major_axis=50):
            cut_image = image[0:90,0:320]
            image_blured = cv2.GaussianBlur(cut_image, (3, 3), 0)
            
            ellipses = []
            
            edges = cv2.Canny(image_blured, canny_threshold1, canny_threshold2) # Apply Canny edge detection
            
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            
            for contour in contours:
                if len(contour) >= 5:  # Fit ellipse requires at least 5 points
                    ellipse = cv2.fitEllipse(contour)
                    (center, axes, angle) = ellipse
                    major_axis = max(axes)
                    minor_axis = min(axes)
                    if major_axis == 0 or minor_axis == 0:
                        continue
                    if major_axis/minor_axis > 2:
                        continue
                    if min_major_axis <= major_axis <= max_major_axis:
                        ellipses.append(ellipse)
            
            return ellipses, edges

        elps, edges = ellipse_detection(gray)

        # Find ellipses that form a ring
        for n in range(len(elps)):
            for m in range(n + 1, len(elps)):
                # e[0] is the center of the ellipse (x,y), e[1] are the lengths of major and minor axis (major, minor), e[2] is the rotation in degrees
                
                e1 = elps[n]
                e2 = elps[m]
                dist = np.sqrt(((e1[0][0] - e2[0][0]) ** 2 + (e1[0][1] - e2[0][1]) ** 2))
                angle_diff = np.abs(e1[2] - e2[2])

                # The centers of the two elipses should be within 5 pixels of each other (is there a better treshold?)
                if dist >= 5:
                    continue

                # The center of the elipses should be above the line
                if e1[0][1] > 90 or e2[0][1] > 90: 
                    continue

                # The rotation of the elipses should be whitin 4 degrees of eachother
                # if angle_diff>4:
                #     continue

                e1_minor_axis = e1[1][0]
                e1_major_axis = e1[1][1]

                e2_minor_axis = e2[1][0]
                e2_major_axis = e2[1][1]

                if e1_major_axis>=e2_major_axis and e1_minor_axis>=e2_minor_axis: # the larger ellipse should have both axis larger
                    le = e1 # e1 is larger ellipse
                    se = e2 # e2 is smaller ellipse
                elif e2_major_axis>=e1_major_axis and e2_minor_axis>=e1_minor_axis:
                    le = e2 # e2 is larger ellipse
                    se = e1 # e1 is smaller ellipse
                else:
                    continue # if one ellipse does not contain the other, it is not a ring

                h, w = 320, 240

                x1, y1 = e1[0]
                x2, y2 = e2[0]

                # Check if the coordinates are within the image bounds
                if not (0 <= x1 < w and 0 <= y1 < h and 0 <= x2 < w and 0 <= y2 < h):
                    continue

                depth1 = self.depth_img[int(y1), int(x1)]
                depth2 = self.depth_img[int(y2), int(x2)]

                if np.isnan(depth1) or np.isnan(depth2):
                    continue  # Ignore invalid depth values

                # Check if the depth is within a certain range - detection of flat objects
                if (depth1 > 0.01 and depth1 < 3) or (depth2 > 0.01 and depth2 < 3):
                    self.flat_rings.append(Ring(e1,e2))
                    continue
                    
                self.rings.append(Ring(e1,e2))


        ## ____VIZUALIZATION (grayscale)____

        # cv2.imshow("Gray Image", gray)
        # cv2.waitKey(1)


        ## ____VIZUALIZATION (edges)____

        cv2.imshow("Edges", edges)
        cv2.waitKey(1)


        ## ____VIZUALIZATION (detected ellipses)____

        cv_elps = cv_image.copy()
        for e in elps:
            cv2.ellipse(cv_elps, e, (255, 0, 0), 2)
        cv2.imshow("Detected ellipses", cv_elps)
        cv2.waitKey(1)


        ## ____VIZUALIZATION (detected rings)____
        for c in self.rings:

            depth1 = self.depth_img[c.center1.y,c.center1.x]
            depth2 = self.depth_img[c.center2.y,c.center2.x]

            cv2.putText(cv_image, f"Dist2center: {depth1:.3f}, {depth2:.3f}", (0, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

            # drawing the ellipses on the image
            cv2.ellipse(cv_image, c.ellipse1, (0, 255, 0), 2)
            cv2.ellipse(cv_image, c.ellipse2, (0, 255, 0), 2)


        ## ____VIZUALITATION (detected flat rings)____

        for f in self.flat_rings:

            depth1 = self.depth_img[f.center1.y,f.center1.x]
            depth2 = self.depth_img[f.center2.y,f.center2.x]

            cv2.putText(cv_image, f"Dist2center: {depth1:.3f}, {depth2:.3f}", (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

            cv2.ellipse(cv_image, f.ellipse1, (0, 0, 255), 2)
            cv2.ellipse(cv_image, f.ellipse2, (0, 0, 255), 2)

            if (len(self.rings)+len(self.flat_rings))>0:
                cv2.imshow("Detected rings",cv_image)
                cv2.waitKey(1)


    def create_marker(self, d, data):
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
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        # Set the pose of the marker
        marker.pose.position.x = float(d[0])
        marker.pose.position.y = float(d[1])
        marker.pose.position.z = float(d[2])

        return marker


    def create_ring_coordinates_message(self, ring, data):
        # get point cloud attributes
        height = data.height
        width = data.width	

        ring_coordinates = RingCoordinates()

        # get 3-channel representation of the point cloud in numpy format
        a = pc2.read_points_numpy(data, field_names= ("x", "y", "z"))
        a = a.reshape((height,width,3))

        # read center coordinates d = [x,y,z] v koordinatah sveta
        x = ring.center1.x
        y = ring.center1.y
        d = a[y,x,:]
        center = self.create_marker(d, data)

        ring_coordinates.center = center

        return ring_coordinates


    def pointcloud_callback(self, data):		

        # iterate over ring coordinates
        for ring in self.rings:

            ring_coordinates_msg = self.create_ring_coordinates_message(ring, data)
            self.marker_pub.publish(ring_coordinates_msg)


def main():
	print('Ring detection node starting.')

	rclpy.init(args=None)
	node = detect_rings()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()