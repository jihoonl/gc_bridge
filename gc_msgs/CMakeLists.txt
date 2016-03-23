cmake_minimum_required(VERSION 2.8.3)
project(gc_msgs)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  sensor_msgs
  diagnostic_msgs
  message_generation
  message_runtime
)

add_service_files(
  FILES
  RequestAnnotations.srv
)

generate_messages(
  DEPENDENCIES
  sensor_msgs
  diagnostic_msgs
)

catkin_package()
