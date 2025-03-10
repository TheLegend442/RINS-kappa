import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'dis_tutorial1'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vicos',
    maintainer_email='matej.dobrevski@fri.uni-lj.si',
    description='DIS tutorial 2 packages - demonstrating basic ROS2 capabilities.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'py_simple_publisher = dis_tutorial1.py_simple_publisher:main',
            'py_simple_subscriber = dis_tutorial1.py_simple_subscriber:main',
            'py_simple_service_node = dis_tutorial1.py_simple_service_node:main',
            'py_simple_server_node = dis_tutorial1.py_simple_server_node:main',
            'py_simple_client_node = dis_tutorial1.py_simple_client_node:main',
            'py_complete_node = dis_tutorial1.py_complete_node:main',
            'py_draw_square = dis_tutorial1.py_draw_square:main',
        ],
    },

)
