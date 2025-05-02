from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='task_2s',
            executable='detect_people.py',
            name='detect_people_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='task_2s',
            executable='save_faces.py',
            name='save_faces_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='task_2s',
            executable='talker_node.py',
            name='talker_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='task_2s',
            executable='detect_rings_final.py',
            name='detect_rings_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='task_2s',
            executable='save_rings.py',
            name='save_rings_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='task_2s',
            executable='robot_commander.py',
            name='robot_commander_node',
            output='screen',
            emulate_tty=True,
        ),
    ])