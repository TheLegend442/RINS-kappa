#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from custom_messages.msg import RingCoordinates
# from custom_messages.srv import PosesInFrontOfRings
from geometry_msgs.msg import PoseWithCovarianceStamped, Pose
import numpy as np
import time
import tf2_ros
import tf2_geometry_msgs  # Za uporabo transformacij med sporočili

class Ring():
    def __init__(self, id, center, current_time=None, robot_position=None, count=1):
        self.id = id
        self.center = center
        self.current_time = current_time
        self.robot_position = robot_position
        self.count = count

class RingMarkerSubscriber(Node):
    def __init__(self):
        super().__init__('ring_marker_subscriber')

        # Inicializacija TF2 listenerja
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Publisher za markerje
        marker_topic = '/detected_rings'
        self.marker_pub = self.create_publisher(Marker, marker_topic, 10)
        self.marker_sub = self.create_subscription(RingCoordinates, '/ring_marker', self.marker_callback, 10)

        # Subscription za pozicijo robota (AMCL)
        self.robot_position_subscription = self.create_subscription(
            PoseWithCovarianceStamped, '/amcl_pose', self.robot_position_callback, 10
        )

        # Service that returns poses in front of detected rings
        # self.service = self.create_service(PosesInFrontOfRings, 'get_ring_pose', self.get_ring_pose_callback)

        self.robot_position = None  # Shranjena pozicija robota
        self.rings = {}  # Slovar {ring_id: (position, timestamp, robot_position, count)}
        self.threshold = 0.7  # Razdalja za zaznavanje istega obroča
        self.time_threshold = 5  # Sekunde preden obroč ponovno upoštevamo
        self.ring_counter = 0  # Števec za unikatne ID-je obročev

    # def get_ring_pose_callback(self, request, response):
    #     response.poses = []

    #     for ring in self.rings.values():
    #         center = ring.center
    #         robot_position_when_detected = ring.robot_position

    def robot_position_callback(self, msg):
        # Shrani pozicijo robota iz AMCL topica
        self.robot_position = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])

    def marker_callback(self, msg):
        if self.robot_position is None:
            self.get_logger().info("Pozicija robota ni bila prejeta, ignoriram zaznane obroče.")
            return
        
        current_position = np.array([msg.center.pose.position.x, msg.center.pose.position.y, msg.center.pose.position.z])
        current_time = time.time()

        # Poskusimo pridobiti transformacijo iz robotovega koordinatnega sistema v globalni za sredinsko točko in še oba kota
        # try:
        #     transform = self.tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
        #     transformed_pose = tf2_geometry_msgs.do_transform_pose(msg.center.pose, transform)
        #     transformed_position = np.array([transformed_pose.position.x, transformed_pose.position.y, transformed_pose.position.z])

        # except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
        #     self.get_logger().error(f"Napaka pri transformaciji: {e}")
        #     return

        # Preveri, ali je obroč že bil zaznan
        transformed_position = np.array([msg.center.pose.position.x, msg.center.pose.position.y, msg.center.pose.position.z])
        for ring_id, ring in self.rings.items():
            count = ring.count
            timestamp = ring.current_time
            center_point = ring.center

            distance = np.linalg.norm(center_point - transformed_position)
            
            if distance < self.threshold:
                if current_time - timestamp < self.time_threshold:
                    return
                else:
                    # **Izbrišemo prejšnji marker**
                    self.delete_marker(ring_id)

                    # **Posodobimo obraz s povprečjem**
                    new_position = (count / (count + 1)) * center_point + (1 / (count + 1)) * transformed_position
                    self.rings[ring_id] = Ring(ring_id, new_position, current_time, self.robot_position, count + 1)

                    # **Objavimo nov marker**
                    self.publish_ring_marker(new_position, ring_id)
                    return

        # **Če obroč ni bil zaznan, ga dodamo v slovar**
        self.ring_counter += 1
        self.get_logger().info(f"Zaznan nov obroč z ID-jem {self.ring_counter}.")
    
        for ring in self.rings.values():
            print(ring.center)

        self.rings[self.ring_counter] = Ring(self.ring_counter, transformed_position, current_time, self.robot_position)
        self.publish_ring_marker(transformed_position, self.ring_counter)

    def publish_ring_marker(self, position, ring_id):
        """Objavi marker za zaznan obroč."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "rings"
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

        self.marker_pub.publish(marker)

    def delete_marker(self, ring_id):
        """Izbriše prejšnji marker, ko posodobimo obroč."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "rings"
        marker.id = ring_id
        marker.action = Marker.DELETE  # Izbriši prejšnji marker

        self.marker_pub.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    node = RingMarkerSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()