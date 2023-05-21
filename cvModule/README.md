# Computer Vision Module
  The computer vision module presents us with different kinds of applications and usage of computer vision within the industry and the principles of the camera models that allow us to process images as we need.

## Quasi-static robot Visuocontrol
  Having learned the fundamentals of computer vision, starting from pinholes cameras, to stereo camera models, this section presents an application of some of the different models to detect aspects of an image in order to do a certain action.
  
  The objective of this challenge, is use the concepts of epipolar geometry and single view metrology to select a box from a simulating environment and teleoperate a robot (with the minimum degrees of freedom to reach the object, which moves asuming a perfect velocity and position control) to take each box and collocate them in a position objective as the image below suggests.
  ![image](https://github.com/DevasNAI/Electro-HorchatasPuzzleBot/assets/55808186/8d7ec7fb-73dd-4cad-a3d5-35938ca764b7)

  In our case, we decided to have a pinhole camera approach in order to teleoperate the robot, detecting two hands from our webcamera, including our fingers, using 21 points, and once we detected our hands, we estimated their position depending on the place in which the generated points are located in the image matrix, for which the right hand brings us the x and y axis, while the left hand provides us the z axis.
  
  
  (Insertar video de mano sola)
  [![Watch the video](https://drive.google.com/file/d/1AH9lAAqefOJhfmlqpU-pGO1G-nx83wwM/view?usp=share_link)](https://drive.google.com/file/d/1AH9lAAqefOJhfmlqpU-pGO1G-nx83wwM/view?usp=share_link)
  
  Once we were able to obtain the position of our hands, we then proceeded to find a way to implement and manipulate a robot with our sample data. First, we decided to use the xarm7 manipulator robot, which is open source and has a variety of plugins that allow us to use multiple functions and commands, which could be useful for this application.
  
# Welcome to my super coool branch! (wooooooo)

1. Clone the vision package inside cvModule.

Dependencies:

- ROS Noetic Full Desktop
- Mediapipe
- Gazebo


2. How to run (each command in a different shell)

```
  roslaunch vision arm_control_gazebo.launch
  rosrun vision goaltoArm.py
  rosrun vision handTracker.py
```

2. How to activate gripper

```
  #Turn gripper on
  rosservice call /vacuum_gripper/on "{}"
  #Turn gripper off
  rosservice call /vacuum_gripper/off "{}"
```

# Demo
https://drive.google.com/file/d/1YVtcEvpTbjajCyVIS5WszinHCdRcJD20/view?usp=share_link
