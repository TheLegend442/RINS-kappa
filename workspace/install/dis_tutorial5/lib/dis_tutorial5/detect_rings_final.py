#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, QoSReliabilityPolicy

from sensor_msgs.msg import Image, PointCloud2
from sensor_msgs_py import point_cloud2 as pc2
from geometry_msgs.msg import PoseWithCovarianceStamped

from visualization_msgs.msg import Marker
from custom_messages.msg import RingCoordinates
import tf2_geometry_msgs 

from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
from enum import Enum

import tf2_ros

class RingColor(Enum):
    BLACK = 1
    RED = 2
    YELLOW = 3
    GREEN = 4
    BLUE = 5
    UNKNOWN = 0

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Ring():
    def __init__(self, ellipse1, ellipse2, center3D=None, mask=None, color=RingColor.UNKNOWN):
        self.ellipse1 = ellipse1
        self.ellipse2 = ellipse2

        self.center1 = Point(0, 0)
        self.center2 = Point(0, 0)

        self.center1.x = int(ellipse1[0][0])
        self.center1.y = int(ellipse1[0][1])

        self.center2.x = int(ellipse2[0][0])
        self.center2.y = int(ellipse2[0][1])

        self.center3D = center3D  # np.array([x, y, z]=

        self.mask = mask
        self.color = color
        self.avg_hue = 0
        self.avg_saturation = 0

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

        # self.tf_buffer = tf2_ros.Buffer()
        # self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        # self.robot_position_subscription = self.create_subscription(
        #     PoseWithCovarianceStamped, '/amcl_pose', self.robot_position_callback, 10
        # )

        self.depth_sub = self.create_subscription(Image, "/oakd/rgb/preview/depth", self.depth_callback, 1)
        self.image_sub = self.create_subscription(Image, "/oakd/rgb/preview/image_raw", self.image_callback, 1)
        # self.pointcloud_sub = self.create_subscription(PointCloud2, "/oakd/rgb/preview/depth/points", self.pointcloud_callback, qos_profile_sensor_data)

        self.marker_pub = self.create_publisher(RingCoordinates, marker_topic, QoSReliabilityPolicy.BEST_EFFORT)

        self.robot_position = None  # Shranjena pozicija robota
        self.transform = None

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
        cv2.namedWindow("Ring mask", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Ring mask", 600, 600)


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

        # try:
        #     self.transform = self.tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
        # except:
        #     self.get_logger().warn("Transform not available yet")
        #     return
        
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

                h, w = cv_image.shape[:2]

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
                if (depth1 > 0.01 and depth1 < 10) or (depth2 > 0.01 and depth2 < 10):
                    self.flat_rings.append(Ring(le,se)) # First large, then small ellipse
                    continue

                ## _____COLOR DETECTION (only for the 3D rings)_____

                ring = Ring(le,se)
                yy, xx = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')

                def ellipse_mask(xx, yy, center, axes, angle_deg):
                    a = axes[0] / 2
                    b = axes[1] / 2
                    x_prime = xx - center[0]
                    y_prime = yy - center[1]
                    angle_rad = np.radians(angle_deg)
                    cos = np.cos(angle_rad)
                    sin = np.sin(angle_rad)
                    ellipse_eq = ((cos * x_prime + sin * y_prime) ** 2) / (a ** 2) + \
                                ((sin * x_prime - cos * y_prime) ** 2) / (b ** 2)
                    return ellipse_eq < 1
                
                outer_mask = ellipse_mask(xx, yy, (ring.center1.x, ring.center1.y), ring.ellipse1[1], ring.ellipse1[2])
                inner_mask = ellipse_mask(xx, yy, (ring.center2.x, ring.center2.y), ring.ellipse2[1], ring.ellipse2[2])
                ring_mask = outer_mask & (~inner_mask)

                valid_depth = (self.depth_img > 0) # eliminate background pixels
                final_mask = ring_mask & valid_depth

                ring_colors = cv_image[final_mask].copy()

                ## Conversion to HSV
                if ring_colors.size > 0:
                    hsv_colors = cv2.cvtColor(ring_colors.reshape(-1, 1, 3).astype(np.uint8), cv2.COLOR_BGR2HSV).reshape(-1, 3)

                    hue = hsv_colors[:, 0]
                    saturation = hsv_colors[:, 1]

                    ring.avg_hue = np.mean(hue)
                    ring.avg_saturation = np.mean(saturation)
                else:
                    self.get_logger().warn("No ring colors found inside mask — skipping color conversion.")
                    return
            
                
                ring.mask = final_mask
                self.rings.append(ring) # First large, then small ellipse


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
        det_rings = cv_image.copy()

        for c in self.rings:    

            depth1 = self.depth_img[c.center1.y,c.center1.x]
            depth2 = self.depth_img[c.center2.y,c.center2.x]

            cv2.putText(det_rings, f"Dist2center: {depth1:.3f}, {depth2:.3f}", (0, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

            # drawing the ellipses on the image
            cv2.ellipse(det_rings, c.ellipse1, (0, 255, 0), 2)
            cv2.ellipse(det_rings, c.ellipse2, (0, 255, 0), 2)


        ## ____VIZUALITATION (detected flat rings)____

        for f in self.flat_rings:

            depth1 = self.depth_img[f.center1.y,f.center1.x]
            depth2 = self.depth_img[f.center2.y,f.center2.x]

            cv2.putText(det_rings, f"Dist2center: {depth1:.3f}, {depth2:.3f}", (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

            cv2.ellipse(det_rings, f.ellipse1, (0, 0, 255), 2)
            cv2.ellipse(det_rings, f.ellipse2, (0, 0, 255), 2)

            if (len(self.rings)+len(self.flat_rings))>0:
                cv2.imshow("Detected rings",det_rings)
                cv2.waitKey(1)

        ## ____VIZUALITATION (inside of the ring)____
        
        if len(self.rings) > 0:
            ring = self.rings[-1]
            masked_image = cv_image.copy()
            masked_image[~ring.mask] = 255
            
            # Get the bounding boxes of the ellipses
            (x1, y1), (a1, b1), _ = ring.ellipse1
            (x2, y2), (a2, b2), _ = ring.ellipse2

            # Get the center of the ring (average of centers)
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Define padding around the ring (adjust as needed)
            padding = int(max(a1, b1, a2, b2)) * 2  # e.g., 2x the ellipse size

            # Define crop boundaries
            x_min = max(center_x - padding, 0)
            x_max = min(center_x + padding, masked_image.shape[1])
            y_min = max(center_y - padding, 0)
            y_max = min(center_y + padding, masked_image.shape[0])

            # Crop the image
            cropped = masked_image[y_min:y_max, x_min:x_max]
            
            scale = 4.0
            resized_crop = cv2.resize(cropped, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

            cv2.putText(resized_crop, f"Mean hue: {ring.avg_hue:.3f} | Mean saturation: {ring.avg_saturation:.3f}", (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            
            cv2.imshow("Ring mask", resized_crop)
            cv2.waitKey(1)
        

    def create_marker(self, d, data):
        marker = Marker()

        marker.header.frame_id = "/map"
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
        map_2d_to_3d = pc2.read_points_numpy(data, field_names= ("x", "y", "z"))
        map_2d_to_3d = map_2d_to_3d.reshape((height,width,3))

        # read center coordinates d[y_slika][x_slika] = [x,y,z] v koordinatah sveta

        # we look for all pixels in the image between the two ellipses
        # we take the average of the depth values which are not nan
        coordinate_sum = np.array([.0,.0,.0])
        points_between_counter = 0
        for y in range(height):
            for x in range(width):
                # if [x, y] is inside ring.ellipse1 and outside ring.ellipse2


                a1b1 = ring.ellipse1[1]
                a1 = a1b1[0] / 2
                b1 = a1b1[1] / 2
                x1_prime = x - ring.center1.x
                y1_prime = y - ring.center1.y
                fi1 = ring.ellipse1[2]
                cos1 = np.cos(np.radians(fi1))
                sin1 = np.sin(np.radians(fi1))

                # Check if the point is inside the ellipse1
                if ((cos1 * x1_prime + sin1 * y1_prime) ** 2) / (a1 ** 2) + ((sin1 * x1_prime - cos1 * y1_prime) ** 2) / (b1 ** 2) < 1:
                    # Check if the point is outside the ellipse2
                    a2b2 = ring.ellipse2[1]
                    a2 = a2b2[0] / 2
                    b2 = a2b2[1] / 2
                    x2_prime = x - ring.center2.x
                    y2_prime = y - ring.center2.y
                    fi2 = ring.ellipse2[2]
                    cos2 = np.cos(np.radians(fi2))
                    sin2 = np.sin(np.radians(fi2))

                    if ((cos2 * x2_prime + sin2 * y2_prime) ** 2) / (a2 ** 2) + ((sin2 * x2_prime - cos2 * y2_prime) ** 2) / (b2 ** 2) > 1:
                        d = map_2d_to_3d[y,x,:]
                        # check if 3D coordinates are valid (not inf or nan)
                        if not np.isnan(d[0]) and not np.isinf(d[0]):
                            points_between_counter += 1
                            coordinate_sum += d
        
        # average the coordinates
        if points_between_counter > 0:
            coordinate_sum /= points_between_counter
        else:
            # raise error
            self.get_logger().error("No points between the ellipses")

        # x = ring.center1.x
        # y = ring.center1.y
        # d = a[y,x,:]
        # center = self.create_marker(d, data)
        # ring_coordinates.center = center

        # transform into map frame
        
        # try:
        #     transformed_pose = tf2_geometry_msgs.do_transform_pose(coordinate_sum, self.transform)
        #     transformed_position = np.array([transformed_pose.position.x, transformed_pose.position.y, transformed_pose.position.z])
        # except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
        #     self.get_logger().error(f"Napaka pri transformaciji: {e}")
        #     return
        
        # ring_coordinates.center = self.create_marker(transformed_position, data)
    

        return ring_coordinates


    # def pointcloud_callback(self, data):	
        
	

    #     # iterate over ring coordinates
    #     # for ring in self.rings:

    #         # ring_coordinates_msg = self.create_ring_coordinates_message(ring, data)
    #         # self.marker_pub.publish(ring_coordinates_msg)

    #     return None
    
    # def robot_position_callback(self, msg):
    #     # Shrani pozicijo robota iz AMCL topica
    #     self.robot_position = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])


def main():
	print('Ring detection node starting.')

	rclpy.init(args=None)
	node = detect_rings()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()