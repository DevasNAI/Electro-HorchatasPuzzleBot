# Install script for directory: /home/andy/Documents/Repositorios/catkin_ws/src/xarm_ros/xarm_gripper

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/andy/Documents/Repositorios/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xarm_gripper/action" TYPE FILE FILES "/home/andy/Documents/Repositorios/catkin_ws/src/xarm_ros/xarm_gripper/action/Move.action")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xarm_gripper/msg" TYPE FILE FILES
    "/home/andy/Documents/Repositorios/catkin_ws/devel/share/xarm_gripper/msg/MoveAction.msg"
    "/home/andy/Documents/Repositorios/catkin_ws/devel/share/xarm_gripper/msg/MoveActionGoal.msg"
    "/home/andy/Documents/Repositorios/catkin_ws/devel/share/xarm_gripper/msg/MoveActionResult.msg"
    "/home/andy/Documents/Repositorios/catkin_ws/devel/share/xarm_gripper/msg/MoveActionFeedback.msg"
    "/home/andy/Documents/Repositorios/catkin_ws/devel/share/xarm_gripper/msg/MoveGoal.msg"
    "/home/andy/Documents/Repositorios/catkin_ws/devel/share/xarm_gripper/msg/MoveResult.msg"
    "/home/andy/Documents/Repositorios/catkin_ws/devel/share/xarm_gripper/msg/MoveFeedback.msg"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xarm_gripper/cmake" TYPE FILE FILES "/home/andy/Documents/Repositorios/catkin_ws/build/xarm_ros/xarm_gripper/catkin_generated/installspace/xarm_gripper-msg-paths.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/andy/Documents/Repositorios/catkin_ws/devel/include/xarm_gripper")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/andy/Documents/Repositorios/catkin_ws/devel/share/roseus/ros/xarm_gripper")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/andy/Documents/Repositorios/catkin_ws/devel/share/common-lisp/ros/xarm_gripper")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/andy/Documents/Repositorios/catkin_ws/devel/share/gennodejs/ros/xarm_gripper")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/andy/Documents/Repositorios/catkin_ws/devel/lib/python3/dist-packages/xarm_gripper")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/andy/Documents/Repositorios/catkin_ws/devel/lib/python3/dist-packages/xarm_gripper")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/andy/Documents/Repositorios/catkin_ws/build/xarm_ros/xarm_gripper/catkin_generated/installspace/xarm_gripper.pc")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xarm_gripper/cmake" TYPE FILE FILES "/home/andy/Documents/Repositorios/catkin_ws/build/xarm_ros/xarm_gripper/catkin_generated/installspace/xarm_gripper-msg-extras.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xarm_gripper/cmake" TYPE FILE FILES
    "/home/andy/Documents/Repositorios/catkin_ws/build/xarm_ros/xarm_gripper/catkin_generated/installspace/xarm_gripperConfig.cmake"
    "/home/andy/Documents/Repositorios/catkin_ws/build/xarm_ros/xarm_gripper/catkin_generated/installspace/xarm_gripperConfig-version.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xarm_gripper" TYPE FILE FILES "/home/andy/Documents/Repositorios/catkin_ws/src/xarm_ros/xarm_gripper/package.xml")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xarm_gripper/config" TYPE DIRECTORY FILES "/home/andy/Documents/Repositorios/catkin_ws/src/xarm_ros/xarm_gripper/config/")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xarm_gripper/launch" TYPE DIRECTORY FILES "/home/andy/Documents/Repositorios/catkin_ws/src/xarm_ros/xarm_gripper/launch/")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xarm_gripper/meshes" TYPE DIRECTORY FILES "/home/andy/Documents/Repositorios/catkin_ws/src/xarm_ros/xarm_gripper/meshes/")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/xarm_gripper/urdf" TYPE DIRECTORY FILES "/home/andy/Documents/Repositorios/catkin_ws/src/xarm_ros/xarm_gripper/urdf/")
endif()

