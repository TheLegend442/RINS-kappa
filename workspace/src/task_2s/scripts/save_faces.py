#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from custom_messages.msg import FaceCoordinates
from custom_messages.srv import PosesInFrontOfFaces
from geometry_msgs.msg import PoseWithCovarianceStamped, Pose
import numpy as np
import time
import tf2_ros
import tf2_geometry_msgs  # Za uporabo transformacij med sporočili
from turtle_tf2_py.turtle_tf2_broadcaster import quaternion_from_euler

class Face():

    def __init__(self, id, center_point, bottom_right_point=None, upper_left_point=None, current_time=None, robot_position=None, count=1, gender_count=0):
        self.id = id
        self.center_point = center_point
        self.bottom_right_point = bottom_right_point
        self.upper_left_point = upper_left_point
        self.current_time = current_time
        self.robot_position = robot_position
        self.count = count
        self.gender_count = gender_count#positve for men, negative for women

class PeopleMarkerSubscriber(Node):
    def __init__(self):
        super().__init__('people_marker_subscriber')
        
        # Inicializacija TF2 listenerja
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Publisher za markerje
        self.marker_publisher = self.create_publisher(Marker, '/detected_faces', 10)

        # Subscription za Marker (Obrazi)
        self.subscription = self.create_subscription(
            FaceCoordinates, '/people_marker', self.marker_callback, 10
        )
        
        # Subscription za pozicijo robota (AMCL)
        self.robot_position_subscription = self.create_subscription(
            PoseWithCovarianceStamped, '/amcl_pose', self.robot_position_callback, 10
        )
        
        # Service that returns poses in front of detected faces
        self.service = self.create_service(PosesInFrontOfFaces, 'get_face_pose', self.get_face_pose_callback)

        self.robot_position = None  # Shranjena pozicija robota
        self.faces = {}  # Slovar {face_id: (position, timestamp, robot_position, count)}
        self.threshold = 0.7  # Razdalja za zaznavanje istega obraza
        self.time_threshold = 0.02  # Sekunde preden obraz ponovno upoštevamo
        self.detections_needed = 30
        self.face_counter = 0  # Števec za unikatne ID-je obrazov

        self.marker_queue = []  # Čakalna vrsta za markerje

    def get_face_pose_callback(self, request, response):
        response.poses = []

        for face in self.faces.values():
            if face.count < self.detections_needed:
                self.get_logger().info(f"Obraz {face.id} ima premalo zaznav, da bi izračunali pozicijo.")
                continue
            
            center = face.center_point
            # if height is higher than 1m, ignore
            if center[2] > 1.0:
                continue

            bottom_right = face.bottom_right_point
            upper_left = face.upper_left_point
            bottom_left = np.array([upper_left[0], upper_left[1], bottom_right[2]])
            robot_position_when_detected = face.robot_position

            #print(f"Center: {center}, Bottom left: {bottom_left}, Upper left: {upper_left}, Bottom right: {bottom_right}, Robot: {robot_position_when_detected}")

            # Izračun točke pol metra pred sliko
            # normala je pravokotna na bottom_right -> bottom_right in ima z koordinato enako 0
            smer_slike = bottom_right - bottom_left
            normala = np.array([smer_slike[1], -smer_slike[0], 0.0])
            normala = normala / np.linalg.norm(normala)

            # hočemo, da je normala obrnjena proti robotu
            if np.dot(robot_position_when_detected - center, normala) < 0:
                normala = -normala

            tocka_pred_sliko = center + 0.7 * normala
            tocka_pred_sliko[2] = 0.0 # na tleh

            # orientacija mora biti v isto smer kot negativna normala
            orientation = np.arctan2(-normala[1], -normala[0])

            pose = Pose()
            pose.position.x = tocka_pred_sliko[0]
            pose.position.y = tocka_pred_sliko[1]
            pose.position.z = tocka_pred_sliko[2]

            #transform orientation to quaternion
            quaternion = quaternion_from_euler(0.0, 0.0, orientation)
            pose.orientation.x = quaternion[0]
            pose.orientation.y = quaternion[1]
            pose.orientation.z = quaternion[2]
            pose.orientation.w = quaternion[3]

            # self.get_logger().info(f"Face {face.id} detected at {center}, robot at {robot_position_when_detected}, pose in front of face: {pose}")
            # print(pose)
            response.poses.append(pose)
            spol = "M" if face.gender_count > 0 else "Ž"
            response.genders.append(spol)
            
        return response

    def robot_position_callback(self, msg):
        # Shrani pozicijo robota iz AMCL topica
        self.robot_position = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])

    def marker_callback(self, msg):
        if self.robot_position is None:
            self.get_logger().info("Pozicija robota ni bila prejeta, ignoriram zaznane obraze.")
            return

        self.marker_queue.append(msg)
        self.process_markers()

    def process_marker(self, msg):
        """ returns True, if marker was processed, False if not """
        current_position = np.array([msg.center.pose.position.x, msg.center.pose.position.y, msg.center.pose.position.z])
        current_time = time.time()
        stamp = msg.center.header.stamp
        try:
            transform = self.tf_buffer.lookup_transform('map', 'base_link', stamp ,timeout=rclpy.duration.Duration(seconds=0.1))
            
            transformed_pose = tf2_geometry_msgs.do_transform_pose(msg.center.pose, transform)
            transformed_position = np.array([transformed_pose.position.x, transformed_pose.position.y, transformed_pose.position.z])
            
            # transform for bottom_right
            transformed_bottom_right_pose = tf2_geometry_msgs.do_transform_pose(msg.bottom_right.pose, transform)
            transformed_bottom_right_position = np.array([transformed_bottom_right_pose.position.x, transformed_bottom_right_pose.position.y, transformed_bottom_right_pose.position.z])

            # transform for upper_left
            transformed_upper_left_pose = tf2_geometry_msgs.do_transform_pose(msg.upper_left.pose, transform)
            transformed_upper_left_position = np.array([transformed_upper_left_pose.position.x, transformed_upper_left_pose.position.y, transformed_upper_left_pose.position.z])

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            msg = str(e)
            self.get_logger().error(f"Napaka pri transformaciji: {msg}")

            if "extrapolation into the past" in msg.lower():
                # Transform requested in the past
                return True

            return False
        
        men = 1 if msg.center.color.b > 0.9 else -1
        self.get_logger().info(f"Zaznan obraz z barvo: {msg.center.color.r}, {msg.center.color.g}, {msg.center.color.b}")
        for face_id, face in self.faces.items():
            count = face.count
            gender_count = face.gender_count
            timestamp = face.current_time
            center_point = face.center_point
            bottom_right_point = face.bottom_right_point
            upper_left_point = face.upper_left_point

            distance = np.linalg.norm(center_point - transformed_position)
            
            if distance < self.threshold:
                if current_time - timestamp < self.time_threshold:
                    return True
                else:
                    # **Izbrišemo prejšnji marker**
                    self.delete_marker(face_id)

                    # **Posodobimo obraz s povprečjem**
                    new_position = (count / (count + 1)) * center_point + (1 / (count + 1)) * transformed_position
                    new_bottom_right_position = (count / (count + 1)) * bottom_right_point + (1 / (count + 1)) * transformed_bottom_right_position
                    new_upper_left_position = (count / (count + 1)) * upper_left_point + (1 / (count + 1)) * transformed_upper_left_position

                    if not( center_point[2] > -0.1 and center_point[2] < 0):
                        self.get_logger().info(f"Obraz {face_id} je bil zaznan na višini {center_point[2]}, ki ni prava.")
                        return True
                    self.faces[face_id] = Face(face_id, new_position, new_bottom_right_position, new_upper_left_position, current_time, self.robot_position, count + 1, gender_count + men )
                    
                    if count + 1 >= self.detections_needed:
                        # **Objavimo nov marker**
                        self.publish_face_marker(new_position, face_id, gender_count + men)
                    return True

        # **Če obraz ni bil zaznan, ga dodamo v slovar**
        self.face_counter += 1
        self.get_logger().info(f"Zaznan nov obraz z ID-jem {self.face_counter}.")
        #transformed_bottom_right_position = None; transformed_upper_left_position = None
        self.faces[self.face_counter] = Face(self.face_counter, transformed_position, transformed_bottom_right_position, transformed_upper_left_position, current_time, self.robot_position)
        # self.publish_face_marker(transformed_position, self.face_counter)
        return True

        
    def process_markers(self):
        self.get_logger().info(f"Obdelujem {len(self.marker_queue)} markerjev.")
        new_queue = []
        for msg in self.marker_queue:
            was_proccessed = self.process_marker(msg)
            if not was_proccessed:
                new_queue.append(msg)
        
        # copy new queue into marker queue
        self.marker_queue = new_queue.copy()

    def publish_face_marker(self, position, face_id, gender):
        """Objavi marker za zaznan obraz."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "faces"
        marker.id = face_id  # Unikatni ID markerja
        marker.type = Marker.CUBE # Oblika markerja
        marker.action = Marker.ADD  # Dodajanje ali posodabljanje markerja
        marker.pose.position.x = position[0]
        marker.pose.position.y = position[1]
        marker.pose.position.z = position[2]
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 1.0
        marker.color.a = 1.0  # Polna vidljivost
        marker.lifetime.sec = 0  # Ne izgine avtomatsko

        self.marker_publisher.publish(marker)

    def delete_marker(self, face_id):
        """Izbriše prejšnji marker, ko posodobimo obraz."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "faces"
        marker.id = face_id
        marker.action = Marker.DELETE  # Izbriši prejšnji marker

        self.marker_publisher.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    node = PeopleMarkerSubscriber()
    node.get_logger().info("People Marker Subscriber is running...")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
