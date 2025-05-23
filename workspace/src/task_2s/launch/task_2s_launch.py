from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    task_2s_dir = get_package_share_directory('task_2s')

    return LaunchDescription([
        # 1. Vključi obstoječi launch file za RViz + Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(task_2s_dir, 'launch', 'rviz_gazebo.launch.py')
            )
        ),

        # 2. Node: arm_mover_actions.py (iz drugega paketa)
        Node(
            package='dis_tutorial7',
            executable='arm_mover_actions.py',
            name='arm_mover_node',
            output='screen'
        ),

        # 3. task_2s nodi
        Node(
            package='task_2s',
            executable='detect_people.py',
            name='detect_people_node',
            output='screen'
        ),
        Node(
            package='task_2s',
            executable='save_faces.py',
            name='save_faces_node',
            output='screen'
        ),
        Node(
            package='task_2s',
            executable='detect_rings_final.py',
            name='detect_rings_node',
            output='screen'
        ),
        Node(
            package='task_2s',
            executable='save_rings.py',
            name='save_rings_node',
            output='screen'
        ),
        Node(
            package='task_2s',
            executable='detect_birds.py',
            name='detect_birds_node',
            output='screen'
        ),
        Node(
            package='task_2s',
            executable='save_birds.py',
            name='save_birds_node',
            output='screen'
        ),
        Node(
            package='task_2s',
            executable='talker_node.py',
            name='talker_node',
            output='screen'
        ),
        Node(
            package='task_2s',
            executable='bird_catalogue_server.py',
            name='bird_catalogue_server_node',
            output='screen'
        ),
        Node(
            package='task_2s',
            executable='bridge_follower.py',
            name='bridge_follower_node',
            output='screen'
        )
    ])
