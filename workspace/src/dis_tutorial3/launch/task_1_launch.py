from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dis_tutorial3',
            executable='save_faces.py',
            name='save_faces_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='dis_tutorial3',
            executable='detect_people.py',
            name='detect_people_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='dis_tutorial3',
            executable='robot_commander.py',
            name='robot_commander_node',
            output='screen',
            emulate_tty=True,
        ),
    ])