# Challenge 3

#### For this challenge we had to communicate the set point to an Arduino Mega with the purpose of controll a DC motor.

## To replicate this:
#### 1. Install Arduino IDE: [Arduino IDE](https://www.arduino.cc/en/software)
#### 2. Install Rosserial library:
'''
sudo apt-get install ros-{ROS-DISTRO}-rosserial
'''
#### 3. Open the ports:
'''
sudo chmod 666 /dev/ttyACM*
sudo chmod 666 /dev/ttyUSB*
'''
#### If you want to make this permanent follow the next instructions: [Ports](https://askubuntu.com/questions/58119/changing-permissions-on-serial-port)

#### 4. Now you have to dowload 2 things, the Arduino code and the ROS files.

#### 5. Change the serial port of your arduino on the .launch achieve

#### 6. Upload the code to the Arduino

#### 7. Launch the ros code with the next command:
'''
rosrun week3 input.py
'''