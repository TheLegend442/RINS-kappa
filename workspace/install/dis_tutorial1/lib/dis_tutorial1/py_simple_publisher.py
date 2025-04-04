#!/usr/bin/env python3

#print('I am alive!')
import rclpy
import time

from std_msgs.msg import String
from dis_tutorial1.msg import CustomMessage

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("py_simple_publisher_node")
    
    publisher = node.create_publisher(CustomMessage, "/chat", 10)
    
    message = CustomMessage()
    message.content = "Hello"
    message.id = 1
    message.is_active = True
    id = 1
    while rclpy.ok():
        #message.content = "Hello"
        message.id = id
        publisher.publish(message)

        node.get_logger().info("Publisher: I performed new iteration!")
        time.sleep(1)
        id += 1
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()