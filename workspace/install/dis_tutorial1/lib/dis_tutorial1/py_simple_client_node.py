#!/usr/bin/env python3

import rclpy
import time
import random

from dis_tutorial1.srv import AddArray

mynode = None

def main(args=None):
    global mynode

    rclpy.init(args=args)

    mynode = rclpy.create_node("py_simple_client_node") 
    client = mynode.create_client(AddArray, 'add_array')

    request = AddArray.Request()
    
    while rclpy.ok():
        request.numbers = [random.randint(0, 100) for i in range(10)]
        request.description = "Random numbers"
        
        mynode.get_logger().info("Sending a request!")
        future = client.call_async(request)
        
        rclpy.spin_until_future_complete(mynode, future)
        response = future.result()
        mynode.get_logger().info(f'Result of add_array: for {request.numbers} is {response.sum}')
        
        time.sleep(1)

    mynode.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()