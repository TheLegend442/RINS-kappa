cmake_minimum_required(VERSION 3.5)
project(task_2s)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)

find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(std_srvs REQUIRED)

find_package(rosidl_default_generators REQUIRED)

install(DIRECTORY
  launch
  config
  worlds
  maps
  DESTINATION share/${PROJECT_NAME}/
)

install(PROGRAMS
  scripts/detect_people.py
  scripts/robot_commander.py
  scripts/save_faces.py
  scripts/talker_node.py
  scripts/detect_rings_final.py
  scripts/save_rings.py
  scripts/bridge_follower.py
  scripts/detect_birds.py
  scripts/bird_catalogue_server.py
  scripts/bird_client_example.py
  scripts/save_birds.py
  scripts/speech_server.py
  scripts/speech_client_example.py
  scripts/detect_people3.py
  DESTINATION lib/${PROJECT_NAME})

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Bird.msg"
  "srv/BirdCollection.srv"
  "srv/MarkerArrayService.srv"
  "srv/GetImage.srv"
  "srv/SpeechService.srv"
  "srv/GoBridgeFollower.srv"
  "srv/GetGenderService.srv"
  DEPENDENCIES sensor_msgs visualization_msgs
)

ament_export_dependencies(rosidl_default_runtime)

ament_package()
