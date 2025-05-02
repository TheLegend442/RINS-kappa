#!/usr/bin/env python3

import rclpy
import random
import math
from time import time

from rclpy.node import Node
from custom_messages.srv import Shape
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

PI = 3.14

class DrawShape(Node):
    
    def __init__(self, nodename='draw_shape', frequency=10):
        super().__init__(nodename)

        self.server = self.create_service(Shape, 'shape', self.draw)
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.get_logger().info("Server is ready!")

    def publish_vel(self, lin, ang):
        cmd_msg = Twist()
        cmd_msg.linear.x = lin
        cmd_msg.angular.z = ang
        self.publisher.publish(cmd_msg)
        # self.counter += 1

    def draw(self, request, response):
        
        shape = request.shape
        self.get_logger().info(f"Received a request to draw a {shape} for {request.duration} seconds")
        if shape == "random":
            shape = random.choice(["circle", "square", "triangle"])
            self.get_logger().info(f"Random shape selected: {shape}")

        

        if shape == "circle":
            start_time = time()
            while time() - start_time < request.duration:
                self.publish_vel(2.0, 2 * PI / request.duration)
            self.publish_vel(0.0, 0.0)

        elif shape == "square":
            start_time = time()
            for i in range(4):
                while time() - start_time < (2*i+1) * request.duration / 8:
                    self.publish_vel(4.0, 0.0)
                while time() - start_time < (2*i+2) * request.duration / 8:
                    self.publish_vel(0.0, 2.0 * PI / (4 * request.duration / 8))
            self.publish_vel(0.0, 0.0)

        elif shape == "triangle":
            start_time = time()
            for i in range(3):
                while time() - start_time < (2*i+1) * request.duration / 6:
                    self.publish_vel(4.0, 0.0)
                while time() - start_time < (2*i+2) * request.duration / 6:
                    self.publish_vel(0.0, 2.0 * PI / (3 * request.duration / 6))
            self.publish_vel(0.0, 0.0)
        response.shape = shape
        return response

    
def main(args=None):
    rclpy.init(args=args)

    ds = DrawShape("draw_shape")
    rclpy.spin(ds)

    rclpy.shutdown()

if __name__ == "__main__":
    main()