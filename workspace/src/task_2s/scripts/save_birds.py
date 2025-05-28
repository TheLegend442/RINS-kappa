#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray
from custom_messages.msg import FaceCoordinates
from custom_messages.srv import PosesInFrontOfFaces
from geometry_msgs.msg import PoseWithCovarianceStamped, Pose
import numpy as np
import time
import tf2_ros
import tf2_geometry_msgs  # Za uporabo transformacij med sporočili
from task_2s.srv import MarkerArrayService, GetImage

class Bird():

    def __init__(self, id, center_point, robot_position, count=1):
        self.id = id
        self.center_point = center_point
        self.count = count
        self.current_time = time.time()
        self.robot_position = robot_position

class BirdMarkerSubscriber(Node):
    def __init__(self):
        super().__init__('bird_marker_subscriber')
        
        # Inicializacija TF2 listenerja
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Publisher za markerje
        self.marker_publisher = self.create_publisher(Marker, '/detected_birds', 10)

        # Subscription za Marker (Obrazi)
        self.subscription = self.create_subscription(
            Marker, '/bird_marker', self.marker_callback, 10
        )
        
        # Subscription za pozicijo robota (AMCL)
        self.robot_position_subscription = self.create_subscription(
            PoseWithCovarianceStamped, '/amcl_pose', self.robot_position_callback, 10
        )

        self.service = self.create_service(MarkerArrayService, 'get_birds', self.get_birds_callback)
        
        self.robot_position = None  # Shranjena pozicija robota
        self.birds = {}  # Slovar {face_id: (position, timestamp, robot_position, count)}
        self.threshold = 0.7  # Razdalja za zaznavanje istega obraza
        self.time_threshold = 0.1  # Sekunde preden obraz ponovno upoštevamo
        self.detections_needed = 2
        self.bird_counter = 0  # Števec za unikatne ID-je obrazov

        self.marker_queue = []  # Čakalna vrsta za markerje

    def get_birds_callback(self, request, response):
        # Obdelaj vse markerje v čakalni vrsti
        self.process_markers()

        # Pripravi odgovor
        response.marker_array = MarkerArray()
        for bird in self.birds.values():
            if bird.count < self.detections_needed:
                continue
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "birds"
            marker.id = bird.id
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            marker.pose.position.x = bird.center_point[0]
            marker.pose.position.y = bird.center_point[1]
            marker.pose.position.z = bird.center_point[2]
            marker.scale.x = 0.2
            marker.scale.y = 0.2
            marker.scale.z = 0.2
            marker.color.r = 0.0
            marker.color.g = 0.0
            marker.color.b = 1.0
            marker.color.a = 1.0
            response.marker_array.markers.append(marker)

            robot_position_marker = Marker()
            robot_position_marker.header.frame_id = "map"
            robot_position_marker.header.stamp = self.get_clock().now().to_msg()
            robot_position_marker.ns = "robot_position"
            robot_position_marker.id = bird.id + 1000
            robot_position_marker.type = Marker.SPHERE
            robot_position_marker.action = Marker.ADD
            robot_position_marker.pose.position.x = bird.robot_position[0]
            robot_position_marker.pose.position.y = bird.robot_position[1]
            robot_position_marker.pose.position.z = bird.robot_position[2]
            response.robot_positions.markers.append(robot_position_marker)

        return response

    def robot_position_callback(self, msg):
        # Shrani pozicijo robota iz AMCL topica
        self.robot_position = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])
        self.process_markers()

    def marker_callback(self, msg):
        if self.robot_position is None:
            self.get_logger().info("Pozicija robota ni bila prejeta, ignoriram zaznane obraze.")
            return

        self.marker_queue.append(msg)
        self.process_markers()

    def process_marker(self, msg):
        """ returns True, if marker was processed, False if not """
        current_position = np.array([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])
        current_time = time.time()
        stamp = msg.header.stamp
        try:
            transform = self.tf_buffer.lookup_transform('map', 'base_link', stamp,timeout=rclpy.duration.Duration(seconds=0.1))
            transformed_pose = tf2_geometry_msgs.do_transform_pose(msg.pose, transform)
            transformed_position = np.array([transformed_pose.position.x, transformed_pose.position.y, transformed_pose.position.z])

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            msg = str(e)
            self.get_logger().error(f"Napaka pri transformaciji: {msg}")

            if "extrapolation into the past" in msg.lower():
                # Transform requested in the past
                return True

            return False

        # Preveri, ali je obraz že bil zaznan
        for bird_id, bird in self.birds.items():
            count = bird.count
            timestamp = bird.current_time
            center_point = bird.center_point

            distance = np.linalg.norm(center_point - transformed_position)
            
            if distance < self.threshold:
                if current_time - timestamp < self.time_threshold:
                    return True
                else:
                    # **Izbrišemo prejšnji marker**
                    self.delete_marker(bird_id)

                    # **Posodobimo obraz s povprečjem**
                    new_position = (count / (count + 1)) * center_point + (1 / (count + 1)) * transformed_position
                    self.birds[bird_id] = Bird(bird_id, new_position, robot_position=self.robot_position, count=count + 1)
                    
                    if count + 1 >= self.detections_needed:
                        # **Objavimo nov marker**
                        self.publish_bird_marker(new_position, bird_id)
                    return True

        # check if transformed_position contains nan
        if np.isnan(transformed_position).any():
            return False

        # **Če obraz ni bil zaznan, ga dodamo v slovar**
        self.bird_counter += 1
        self.get_logger().info(f"Zaznan nov ptič z ID-jem {self.bird_counter}.")
        print(transformed_position)
        #transformed_bottom_right_position = None; transformed_upper_left_position = None
        self.birds[self.bird_counter] = Bird(self.bird_counter, transformed_position, self.robot_position, count=1)
        # self.publish_face_marker(transformed_position, self.bird_counter)
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

    def publish_bird_marker(self, position, face_id):
        """Objavi marker za zaznan obraz."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "birds"
        marker.id = face_id  # Unikatni ID markerja
        marker.type = Marker.CUBE # Oblika markerja
        marker.action = Marker.ADD  # Dodajanje ali posodabljanje markerja
        marker.pose.position.x = position[0]
        marker.pose.position.y = position[1]
        marker.pose.position.z = position[2]
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2
        marker.color.r = 0.0
        marker.color.g = 0.0
        marker.color.b = 1.0
        marker.color.a = 1.0  # Polna vidljivost
        marker.lifetime.sec = 0  # Ne izgine avtomatsko

        self.marker_publisher.publish(marker)

    def delete_marker(self, bird_id):
        """Izbriše prejšnji marker, ko posodobimo obraz."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "birds"
        marker.id = bird_id
        marker.action = Marker.DELETE  # Izbriši prejšnji marker

        self.marker_publisher.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    node = BirdMarkerSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("KeyboardInterrupt received, shutting down.")
    finally:
        if rclpy.ok():  # ✅ only shut down if still running
            rclpy.shutdown()

if __name__ == '__main__':
    main()
