#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from task_2s.srv import SpeechService
from task_2s.msg import Bird

from cv_bridge import CvBridge
import cv2

class SpeechClient(Node):
    def __init__(self):
        super().__init__('speech_client')
        self.cli = self.create_client(SpeechService, 'speech_service')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for speech_service...')

        self.send_request()

    def send_request(self):
        request = SpeechService.Request()

        self.bridge = CvBridge()
        image = cv2.imread('src/task_2s/images/bridge_path_color.png')  # Replace with your actual image path
        image_msg = self.bridge.cv2_to_imgmsg(image, encoding="bgr8")

        bird1 = Bird()
        bird1.species = 'laysan albatross'
        bird1.image = image_msg  # Adjust type accordingly
        bird1.location = 'Park'
        bird1.ring_color = 'Red'
        bird1.detection_time = '2024-05-01 12:00:00'

        bird2 = Bird()
        bird2.species = 'american crow'
        bird2.image = image_msg
        bird2.location = 'Mountain'
        bird2.ring_color = 'Blue'
        bird2.detection_time = '2024-05-01 14:30:00'

        request.birds = [bird1, bird2]
        request.gender = "F" # Or "M" for male

        future = self.cli.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info(f'Service call successful - favourite bird: {future.result().favourite_bird.title()}')
        else:
            self.get_logger().error('Service call failed.')

def main(args=None):
    rclpy.init(args=args)
    node = SpeechClient()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()