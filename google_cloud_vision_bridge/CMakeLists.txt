cmake_minimum_required(VERSION 2.8.3)
project(google_cloud_vision_bridge)

find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
)

catkin_python_setup()

catkin_package(
)
