#!/usr/bin/python3

import rclpy
from rclpy.node import Node
import cv2
import numpy as np
import time


import tf2_ros
import tf2_geometry_msgs
from sensor_msgs.msg import Image, PointCloud2
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PoseStamped
from cv_bridge import CvBridge, CvBridgeError
from visualization_msgs.msg import Marker
from std_msgs.msg import ColorRGBA
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, qos_profile_sensor_data
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from sensor_msgs_py import point_cloud2 as pc2

qos_profile = QoSProfile(
          durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
          reliability=QoSReliabilityPolicy.RELIABLE,
          history=QoSHistoryPolicy.KEEP_LAST,
          depth=1)


class Ring():
    def __init__(self, ellipse1, ellipse2, count_detected=1, position3D=None):
        self.ellipse1 = ellipse1
        self.ellipse2 = ellipse2

        self.center1 = ellipse1[0]
        self.center2 = ellipse2[0]

        self.depth1 = 0
        self.depth2 = 0

        self.position3D = position3D

        self.count_detected = count_detected
        self.timestamp = 0

class RingDetector(Node):
    def __init__(self):
        super().__init__('ring_detector')

        # An object we use for converting images between ROS format and OpenCV format
        self.bridge = CvBridge()

        self.rings = {}
        self.ring_counter = 0
        self.rings_array = []
        self.depth_img = None
        self.robot_position = None  # Shranjena pozicija robota

        # Subscribe to the image and/or depth topi
        self.robot_position_sub = self.create_subscription(
            PoseWithCovarianceStamped, '/amcl_pose', self.robot_position_callback, 10
        )
        self.depth_sub = self.create_subscription(Image, "/oakd/rgb/preview/depth", self.depth_callback, 1)
        self.image_sub = self.create_subscription(Image, "/oakd/rgb/preview/image_raw", self.image_callback, 1)
        self.pointcloud_sub = self.create_subscription(PointCloud2, "/oakd/rgb/preview/depth/points", self.pointcloud_callback, qos_profile_sensor_data)

        self.marker_pub = self.create_publisher(Marker, "/ring", QoSReliabilityPolicy.BEST_EFFORT)

        # Object we use for transforming between coordinate frames
        self.tf_buf = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buf, self)


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



    def robot_position_callback(self, msg):
        # Shrani pozicijo robota iz AMCL topica
        self.robot_position = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])

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

            temp_ring = Ring(e1,e2)
            temp_ring.depth1 = depth1
            temp_ring.depth2 = depth2
            temp_ring.timestamp = time.time()

            self.rings_array.append(temp_ring)
        

        for f in flat_rings:

            e1 = f[0]
            e2 = f[1]

            cv2.putText(cv_image, f"Dist2center: {self.depth_img[int(e1[0][1]), int(e1[0][0])]:.3f}, {self.depth_img[int(e2[0][1]), int(e2[0][0])]:.3f}", (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

            cv2.ellipse(cv_image, e1, (0, 0, 255), 2)
            cv2.ellipse(cv_image, e2, (0, 0, 255), 2)


        if (len(candidates)+len(flat_rings))>0:
                cv2.imshow("Detected rings",cv_image)
                cv2.waitKey(1)

        # self.marker_callback(candidates)


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

        # self.get_logger().info(f"Marker created at {d[0]}, {d[1]}, {d[2]}")

        return marker

    def create_face_coordinates_message(self, face, data):
		# get point cloud attributes
        height = data.height
        width = data.width
        point_step = data.point_step
        row_step = data.row_step	

        ring_coordinates = Marker()
		
        # get 3-channel representation of the point cloud in numpy format
        a = pc2.read_points_numpy(data, field_names= ("x", "y", "z"))
        a = a.reshape((height,width,3))

        # read center coordinates d = [x,y,z] v koordinatah sveta
        x = int(face.center1[0])
        y = int(face.center1[1])
        d = a[y,x,:]
        center_marker = self.create_marker(d, data)

        ring_coordinates.pose = center_marker.pose

        return ring_coordinates
    
    def pointcloud_callback(self, data):
        # iterate over face coordinates
        for ring in self.rings_array:
            ring_coordinates_msg = self.create_face_coordinates_message(ring, data)

            self.marker_callback(ring_coordinates_msg)

    def marker_callback(self, msg):
        if self.robot_position is None:
            self.get_logger().info("Pozicija robota ni bila prejeta, ignoriram zaznane obraze.")
            return
        
        # current_position = np.array([msg.center.pose.position.x, msg.center.pose.position.y, msg.center.pose.position.z])
        current_time = time.time()

        # Poskusimo pridobiti transformacijo iz robotovega koordinatnega sistema v globalni za sredinsko točko in še oba kota
        try:
            transform = self.tf_buf.lookup_transform('map', 'base_link', rclpy.time.Time())
            transformed_pose = tf2_geometry_msgs.do_transform_pose(msg.pose, transform)
            transformed_position = np.array([transformed_pose.position.x, transformed_pose.position.y, transformed_pose.position.z])
            

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().error(f"Napaka pri transformaciji: {e}")
            return

        # Preveri, ali je obraz že bil zaznan
        for ring_id, ring in self.rings.items():
            count = ring.count
            timestamp = ring.current_time
            center = ring.center1

            distance = np.linalg.norm(center - transformed_position)
            
            if distance < self.threshold:
                if current_time - timestamp < self.time_threshold:
                    return
                else:
                    # **Izbrišemo prejšnji marker**
                    self.delete_marker(ring_id)

                    # **Posodobimo obraz s povprečjem**
                    new_position = (count / (count + 1)) * center + (1 / (count + 1)) * transformed_position

                    self.ring[ring_id] = Ring(ring.ellipse1, ring.ellipse2, count + 1, new_position)

                    # **Objavimo nov marker**
                    self.publish_ring_marker(new_position, ring_id)
                    return

        # **Če obraz ni bil zaznan, ga dodamo v slovar**
        self.ring_counter += 1
        self.get_logger().info(f"Zaznan nov obroč z ID-jem {self.ring_counter}.")
        #transformed_bottom_right_position = None; transformed_upper_left_position = None
        self.rings[self.ring_counter] = Ring(self.ring_counter, transformed_position, current_time, self.robot_position)
        self.publish_ring_marker(transformed_position, self.ring_counter)


    def publish_ring_marker(self, position, ring_id):
        """Objavi marker za zaznan obraz."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "faces"
        marker.id = ring_id  # Unikatni ID markerja
        marker.type = Marker.SPHERE  # Oblika markerja
        marker.action = Marker.ADD  # Dodajanje ali posodabljanje markerja
        marker.pose.position.x = position[0]
        marker.pose.position.y = position[1]
        marker.pose.position.z = position[2]
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0  # Polna vidljivost
        marker.lifetime.sec = 0  # Ne izgine avtomatsko

        self.marker_publisher.publish(marker)


    def delete_marker(self, ring_id):
        """Izbriše prejšnji marker, ko posodobimo obraz."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "faces"
        marker.id = ring_id
        marker.action = Marker.DELETE  # Izbriši prejšnji marker

        self.marker_publisher.publish(marker)


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