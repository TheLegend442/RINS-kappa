#!/usr/bin/python3

import rclpy
from rclpy.node import Node
import cv2
import numpy as np


import tf2_ros
import tf2_geometry_msgs
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PointStamped, Vector3, Pose
from cv_bridge import CvBridge, CvBridgeError
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
import message_filters

qos_profile = QoSProfile(
          durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
          reliability=QoSReliabilityPolicy.RELIABLE,
          history=QoSHistoryPolicy.KEEP_LAST,
          depth=1)


class Ring():
    def __init__(self, ellipse1, ellipse2):
        self.ellipse1 = ellipse1
        self.ellipse2 = ellipse2

        self.center1 = ellipse1[0]
        self.center2 = ellipse2[0]

        self.depth1 = 0
        self.depth2 = 0

class RingDetector(Node):
    def __init__(self):
        super().__init__('ring_detector')

        # Basic ROS stuff
        timer_frequency = 2
        timer_period = 1/timer_frequency

        # An object we use for converting images between ROS format and OpenCV format
        self.bridge = CvBridge()

        # Marker array object used for visualizations
        self.marker_array = MarkerArray()
        self.marker_id = 0

        self.depth_img = None

        # Subscribe to the image and/or depth topi
        self.depth_sub = self.create_subscription(Image, "/oakd/rgb/preview/depth", self.depth_callback, 1)
        self.image_sub = self.create_subscription(Image, "/oakd/rgb/preview/image_raw", self.image_callback, 1)

        # self.robot_position_subscription = self.create_subscription(
        #     PoseWithCovarianceStamped, '/amcl_pose', self.robot_position_callback, 10
        # )

        # Publiser for the visualization markers
        self.marker_pub = self.create_publisher(MarkerArray, "/ring", QoSReliabilityPolicy.BEST_EFFORT)

        # Object we use for transforming between coordinate frames
        self.tf_buf = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buf, self)

        # cv2.namedWindow("Binary Image", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("Detected contours", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Detected rings", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("Gray Image", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("Depth window", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Live camera feed", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("Ring depth", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Edges", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Detected ellipses", cv2.WINDOW_NORMAL)

    def image_callback(self, data):
        # self.get_logger().info(f"I got a new image! Will try to find rings...")
        
        if self.depth_img is None:
            self.get_logger().info("No depth image yet, skipping this image")
            return
        
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        blue = cv_image[:,:,0]
        green = cv_image[:,:,1]
        red = cv_image[:,:,2]

        cv_image_copy = cv_image.copy()


        ## ____Draw dashed a line on the image at y=90____
        start_point = (0, 90)
        end_point = (cv_image.shape[1], 90)

        dash_length, gap_length = 10, 5
    
        line_length = int(np.linalg.norm(np.array(start_point) - np.array(end_point)))

        for i in range(0, line_length, dash_length + gap_length):
            x1 = int(start_point[0] + i * (end_point[0] - start_point[0]) / line_length)
            y1 = int(start_point[1] + i * (end_point[1] - start_point[1]) / line_length)
            
            x2 = int(start_point[0] + (i + dash_length) * (end_point[0] - start_point[0]) / line_length)
            y2 = int(start_point[1] + (i + dash_length) * (end_point[1] - start_point[1]) / line_length)
     
            cv2.line(cv_image_copy, (x1, y1), (x2, y2), (0, 0, 0), 1)
        
        
        ## ____Check for the image dimensions____
        ## Image dimensions: 240x320
        # cv2.putText(cv_image_copy, f"HxW: {cv_image.shape[0]}x{cv_image.shape[1]}", (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        cv2.imshow("Live camera feed", cv_image_copy)
        cv2.waitKey(1)

        # Tranform image to grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Gray Image", gray)
        # cv2.waitKey(1)
        
        ##
        ## ____Original ellipse detectiion code____
        ##

        # # Apply Gaussian Blur
        # gray = cv2.GaussianBlur(gray,(3,3),0)

        # # Do histogram equalization
        # # gray = cv2.equalizeHist(gray)

        # # Binarize the image, there are different ways to do it
        # #ret, thresh = cv2.threshold(img, 50, 255, 0)
        # #ret, thresh = cv2.threshold(img, 70, 255, cv2.THRESH_BINARY)
        # # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 30)
        # _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # kernel = np.ones((5,5), np.uint8)
        # thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # cv2.imshow("Binary Image", thresh)
        # cv2.waitKey(1)

        # # Extract contours
        # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # # Example of how to draw the contours, only for visualization purposes
        # cv2.drawContours(gray, contours, -1, (255, 0, 0), 3)
        # cv2.imshow("Detected contours", gray)
        # cv2.waitKey(1)

        # # Fit elipses to all extracted contours
        # elps = []
        # elps_flat = []
        # for cnt in contours:
        #     #     print cnt
        #     #     print cnt.shape
        #     if cnt.shape[0] >= 20:

        #         # mask = np.zeros(gray.shape, dtype=np.uint8)
        #         # mask = cv2.drawContours(mask, [cnt], -1, (255, 0, 0), -1)

        #         # depth_image = self.depth_img
        #         # depth_image[depth_image == np.inf] = 0
        #         # depth_image[depth_image == 0] = 0
        #         # # depth_image = cv2.GaussianBlur(depth_image, (3, 3), 0)
        #         # depth_values = depth_image[mask == 255]

        #         # cv2.imshow("Ring depth", depth_values)
        #         # cv2.waitKey(1)

        #         # if len(depth_values) > 0:
        #         #     depth_variation = np.std(depth_values)
        #         #     depth_range = np.max(depth_values) - np.min(depth_values)
                
        #         ellipse = cv2.fitEllipse(cnt)
        #         elps.append(ellipse)
        #         # if depth_variation < 0.1 and depth_range < 0.1:
        #         #     elps_flat.append(ellipse)
        #         # else:
        #         #     elps.append(ellipse)
        
        ##
        ## ____End of original ellipse detection code____
        ##

        ## ____New ellipse detection code____

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

        cv2.imshow("Edges", edges)
        cv2.waitKey(1)

        img_ellipses = cv_image.copy()
        for e in elps:
            cv2.ellipse(img_ellipses, e, (255, 0, 0), 2)
        cv2.imshow("Detected ellipses", img_ellipses)
        cv2.waitKey(1)

        # Find two elipses with same centers
        candidates = []
        flat_rings = []
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
                
                # # The widths of the ring along the major and minor axis should be roughly the same
                # border_major = (le[1][1]-se[1][1])/2
                # border_minor = (le[1][0]-se[1][0])/2
                # border_diff = np.abs(border_major - border_minor)

                # if border_diff>4:
                #     continue


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
                    flat_rings.append((e1,e2))
                    continue
                    
                candidates.append((e1,e2))

    
        print("Processing is done! found", len(candidates), "candidates for rings")

        # Plot the rings on the image
        for c in candidates:

            # the centers of the ellipses
            e1 = c[0]
            e2 = c[1]

            center1 = e1[0]
            center2 = e2[0]
            depth1 = self.depth_img[int(center1[1]), int(center1[0])]
            depth2 = self.depth_img[int(center2[1]), int(center2[0])]


            cv2.putText(cv_image, f"Dist2center: {depth1:.3f}, {depth2:.3f}", (0, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

            # drawing the ellipses on the image
            cv2.ellipse(cv_image, e1, (0, 255, 0), 2)
            cv2.ellipse(cv_image, e2, (0, 255, 0), 2)

            # Get a bounding box, around the first ellipse ('average' of both elipsis)
            size = (e1[1][0]+e1[1][1])/2
            center = (e1[0][1], e1[0][0])

            x1 = int(center[0] - size / 2)
            x2 = int(center[0] + size / 2)
            x_min = x1 if x1>0 else 0
            x_max = x2 if x2<cv_image.shape[0] else cv_image.shape[0]

            y1 = int(center[1] - size / 2)
            y2 = int(center[1] + size / 2)
            y_min = y1 if y1 > 0 else 0
            y_max = y2 if y2 < cv_image.shape[1] else cv_image.shape[1]

        for f in flat_rings:

            e1 = f[0]
            e2 = f[1]

            cv2.putText(cv_image, f"Dist2center: {self.depth_img[int(e1[0][1]), int(e1[0][0])]:.3f}, {self.depth_img[int(e2[0][1]), int(e2[0][0])]:.3f}", (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

            cv2.ellipse(cv_image, e1, (0, 0, 255), 2)
            cv2.ellipse(cv_image, e2, (0, 0, 255), 2)


        if (len(candidates)+len(flat_rings))>0:
                cv2.imshow("Detected rings",cv_image)
                cv2.waitKey(1)

        # Publish the markers for the detected rings
        self.publish_ellipse_markers(candidates)


    def depth_callback(self,data):

        try:
            depth_image = self.bridge.imgmsg_to_cv2(data, "32FC1")
        except CvBridgeError as e:
            print(e)

        self.depth_img = depth_image

        depth_image[depth_image==np.inf] = 0


        
        # Do the necessairy conversion so we can visuzalize it in OpenCV
        image_1 = depth_image / 65536.0 * 255
        image_1 = image_1/np.max(image_1)*255

        image_viz = np.array(image_1, dtype= np.uint8)

        # cv2.imshow("Depth window", image_viz)
        cv2.waitKey(1)

    def transform_point(self, x, y, z, from_frame='base_link', to_frame="map"):

        try:
            # Create a PoseStamped message with the detected point
            pose = PoseStamped()
            pose.header.frame_id = from_frame
            pose.header.stamp = self.get_clock().now().to_msg()

            # Set the point's position
            pose.pose.position.x = float(x)
            pose.pose.position.y = float(y)
            pose.pose.position.z = float(z)

            # Transform the point to the target frame
            transform = self.tf_buffer.lookup_transform(to_frame, from_frame, rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=1.0))
            transformed_pose = tf2_geometry_msgs.do_transform_pose(pose, transform)

            return (
                transformed_pose.pose.position.x,
                transformed_pose.pose.position.y,
                transformed_pose.pose.position.z
            )

        except tf2_ros.LookupException:
            self.get_logger().warn(f"TF lookup failed: {from_frame} -> {to_frame}")
            return None
        except tf2_ros.ConnectivityException:
            self.get_logger().warn(f"TF connectivity issue: {from_frame} -> {to_frame}")
            return None
        except tf2_ros.ExtrapolationException:
            self.get_logger().warn(f"TF extrapolation issue: {from_frame} -> {to_frame}")
            return None

    def publish_ellipse_markers(self, candidates):
        for c in candidates:
            e1, _ = c
            marker = Marker()
            marker.header.frame_id = "base_link"  # Or whichever frame you are using
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "ring_detector"
            marker.id = self.marker_id
            self.marker_id += 1
            marker.type = Marker.SPHERE  # Or any type that suits your use case
            marker.action = Marker.ADD
            marker.pose.position.x = e1[0][0]  # X position from ellipse 1 center
            marker.pose.position.y = e1[0][1]  # Y position from ellipse 1 center
            marker.pose.position.z = 0  # Or depth from depth image
            
            marker.scale.x = 0.1  # Size of the marker, adjust as necessary
            marker.scale.y = 0.1
            marker.scale.z = 0.1
            
            marker.color = ColorRGBA(1.0, 0.0, 0.0, 1.0)  # Red color, fully opaque
            
            self.marker_array.markers.append(marker)
        
        # Publish all markers in the MarkerArray
        self.marker_pub.publish(self.marker_array)


def main():

    rclpy.init(args=None)
    rd_node = RingDetector()

    rclpy.spin(rd_node)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()