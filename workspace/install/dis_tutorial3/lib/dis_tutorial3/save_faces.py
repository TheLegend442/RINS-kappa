#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseWithCovarianceStamped
import numpy as np
import time
import tf2_ros
import tf2_geometry_msgs  # Za uporabo transformacij med sporočili

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
            Marker, '/people_marker', self.marker_callback, 10
        )
        
        # Subscription za pozicijo robota (AMCL)
        self.robot_position_subscription = self.create_subscription(
            PoseWithCovarianceStamped, '/amcl_pose', self.robot_position_callback, 10
        )
        
        self.robot_position = None  # Shranjena pozicija robota
        self.faces = {}  # Slovar {face_id: (position, timestamp, robot_position, count)}
        self.threshold = 0.7  # Razdalja za zaznavanje istega obraza
        self.time_threshold = 5  # Sekunde preden obraz ponovno upoštevamo
        self.face_counter = 0  # Števec za unikatne ID-je obrazov

    def robot_position_callback(self, msg):
        # Shrani pozicijo robota iz AMCL topica
        self.robot_position = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])

    def marker_callback(self, msg):
        if self.robot_position is None:
            self.get_logger().info("Pozicija robota ni bila prejeta, ignoriram zaznane obraze.")
            return
        
        current_position = np.array([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])
        current_time = time.time()

        # Poskusimo pridobiti transformacijo iz robotovega koordinatnega sistema v globalni
        try:
            transform = self.tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
            transformed_pose = tf2_geometry_msgs.do_transform_pose(msg.pose, transform)
            transformed_position = np.array([transformed_pose.position.x, transformed_pose.position.y, transformed_pose.position.z])

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().error(f"Napaka pri transformaciji: {e}")
            return

        # Preveri, ali je obraz že bil zaznan
        for face_id, (face, timestamp, robot_position, count) in self.faces.items():
            distance = np.linalg.norm(face - transformed_position)
            
            if distance < self.threshold:
                if current_time - timestamp < self.time_threshold:
                    return
                else:
                    # **Izbrišemo prejšnji marker**
                    self.delete_marker(face_id)

                    # **Posodobimo obraz s povprečjem**
                    new_position = (count / (count + 1)) * face + (1 / (count + 1)) * transformed_position
                    self.faces[face_id] = (new_position, current_time, self.robot_position, count + 1)

                    # **Objavimo nov marker**
                    self.publish_face_marker(new_position, face_id)
                    return

        # **Če obraz ni bil zaznan, ga dodamo v slovar**
        self.face_counter += 1
        self.get_logger().info(f"Zaznan nov obraz z ID-jem {self.face_counter}.")
        self.faces[self.face_counter] = (transformed_position, current_time, self.robot_position, 1)
        self.publish_face_marker(transformed_position, self.face_counter)

    def publish_face_marker(self, position, face_id):
        """Objavi marker za zaznan obraz."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "faces"
        marker.id = face_id  # Unikatni ID markerja
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
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
