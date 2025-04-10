#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pyttsx3

class SpeechNode(Node):
    def __init__(self):
        super().__init__('speech_node')
        self.subscription = self.create_subscription(
            String,
            'speech_text',
            self.listener_callback,
            10)
        self.engine = pyttsx3.init()
        self.get_logger().info("Speech node ready. Waiting for text...")

    def listener_callback(self, msg):
        self.get_logger().info(f'Will say: "{msg.data}"')
        self.engine.say(msg.data)
        self.engine.runAndWait()

def main(args=None):
    rclpy.init(args=args)
    node = SpeechNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
