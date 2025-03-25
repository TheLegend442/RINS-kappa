from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='dis_tutorial2',
            executable='draw_shape',
            name='draw_shape',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='dis_tutorial2',
            executable='draw_client',
            name='draw_client',
            output='screen',
            emulate_tty=True,
        ),
    ])