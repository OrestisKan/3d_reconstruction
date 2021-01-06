cmake_minimum_required(VERSION 3.0.2)
project(reconstruction_3d)

find_package(
    catkin REQUIRED
    # Specify dependencies
    COMPONENTS
    std_msgs
    sensor_msgs
    rospy
    message_generation
)

add_service_files(
  FILES
  Reconstruct.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
  sensor_msgs
)

catkin_package(
    # Specify package dependencies
    CATKIN_DEPENDS
    std_msgs
    rospy
    message_runtime
)

include_directories(${catkin_INCLUDE_DIRS})
