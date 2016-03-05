cmake_minimum_required(VERSION 2.8.3)
project(gc_vision_bridge)

find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
)

catkin_add_env_hooks(25.gc-vision-bridge SHELLS sh DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/env-hooks)


catkin_python_setup()

catkin_package()
