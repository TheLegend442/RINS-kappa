import rclpy
import time
import random

from custom_messages.srv import Shape
from rclpy.node import Node

class DrawClient(Node):

    def __init__(self, nodename='draw_client'):
        super().__init__(nodename)

        self.client = self.create_client(Shape, 'shape')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Shape.Request()
    
    def send_request(self, shape, duration):
        self.req.shape = shape
        self.req.duration = duration
        self.get_logger().info(f"Sending a request to draw a {shape} for {duration} seconds")
        
        future = self.client.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()

        self.get_logger().info(f"drew a {response.shape}")

def main(args=None):
    rclpy.init(args=args)
    dc = DrawClient()
    for i in range(10):
        dc.send_request("random", 5)
        time.sleep(2)
    rclpy.spin(dc)
    rclpy.shutdown()

if __name__ == "__main__":
    main()