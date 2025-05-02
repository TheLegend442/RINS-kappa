#!/usr/bin/python3

import rclpy
import rclpy.duration
from rclpy.node import Node

from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from action_msgs.msg import GoalStatus

from std_msgs.msg import String
from trajectory_msgs.msg import JointTrajectoryPoint
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy
from rclpy.qos import QoSProfile, QoSReliabilityPolicy


qos_profile = QoSProfile(
          durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
          reliability=QoSReliabilityPolicy.RELIABLE,
          history=QoSHistoryPolicy.KEEP_LAST,
          depth=1)

class BridgeFollower(Node):
    def __init__(self):
        super().__init__('bridge_follower')

        self.arm_pub = self.create_publisher(String, '/arm_command', qos_profile)
        self.arm_pub.publish(String(data='manual:[0.,-0.8,1.7,1.5]'))

        self.get_logger().info(f"Initialized the Bridge Follower node! Waiting for commands...")


def main():

    rclpy.init(args=None)
    rd_node = BridgeFollower()

    rclpy.spin(rd_node)

if __name__ == '__main__':
    main()