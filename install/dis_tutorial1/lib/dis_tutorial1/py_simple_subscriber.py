#!/usr/bin/env python3

import rclpy

from std_msgs.msg import String
from dis_tutorial1.msg import CustomMessage

mynode = None

def topic_callback(msg):
    global mynode
    mynode.get_logger().info(f'I heard {msg.id}, {msg.content}, {msg.is_active}')

def main(args=None):
    global mynode
    rclpy.init(args=args)
    mynode = rclpy.create_node("py_simple_subscriber_node")
    
    subscription = mynode.create_subscription(CustomMessage, "/chat", topic_callback, 10)

    while rclpy.ok():
        rclpy.spin_once(mynode)

    mynode.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()