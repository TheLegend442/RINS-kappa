#!/usr/bin/env python3

import rclpy
import time

from dis_tutorial1.srv import AddArray

mynode = None

def add_array_callback(request, response):
    global mynode
    response.sum = sum(request.numbers)
    mynode.get_logger().info(f'Incoming request na:\n {request.numbers[0]}\nReturning response: {response.sum}')
    return response

def main(args=None):
    global mynode

    rclpy.init(args=args)

    mynode = rclpy.create_node("py_simple_server_node") 
    server = mynode.create_service(AddArray, 'add_array', add_array_callback)

    mynode.get_logger().info("Server is ready!")
    rclpy.spin(mynode)

    mynode.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()