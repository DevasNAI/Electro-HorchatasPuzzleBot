#!/usr/bin/env python

import rospy
import numpy as np
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist, TwistStamped, Point, Pose
from std_srvs.srv import Empty

class open_loop:
  def __init__(self):
    # create publisher and message as instance variables
    self.publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    self.errorP = rospy.Publisher("/error", Float32, queue_size=1)
    self.msg = Twist()
    self.robotPose = 0

    # Declaration of initial variables
    self.start_time = 0
    # LInear and Angular Speeds
    self.linV = 0.75
    self.angV = 0.5

    # Waypoints to move to
    self.points = [(1,1)] #(1,2), (-1,-2), (2,1), (
    self.current = 0

    # do some cleanup on shutdown
    rospy.on_shutdown(self.stop)

    # start by moving robot
    rospy.init_node('robot_control')

    # Variable that activates turning mode
    self.turn = True

    self.distance = 0
    # Position vector
    self.position = Point()
    self.target = Point()
    self.initPosition = Point()

    self.POSITIONX = 0
    self.TARGETY = 0
    self.ORIENTATIONZ = 0


    self.angle = 0
    # Initial puzzlebot position
    self.initPosition.x = -0.95
    self.initPosition.y = 0.75
    # Set point position
    self.position.x = self.initPosition.x
    self.position.y = self.initPosition.y
    self.initangle = -1.57

    # Sets target point
    self.target.x = self.points[self.current][0]
    self.target.y = self.points[self.current][1]

    # Calculates distance required to reach point
    self.targetDistance = np.sqrt(np.power(self.target.x - self.initPosition.x,2) + np.power(self.target.y - self.initPosition.y,2))
    # Calculates the angle the robot needs to be in order to go to the point
    self.targetAngle = (np.arctan2(self.target.y - self.initPosition.y, self.target.x - self.initPosition.x) - self.initangle) % 2*np.pi

    # Controller constants
    self.linK = 0.3
    self.anK = 0.46
    rospy.Subscriber("/pose", Pose, self.poseCallback)
    
    # Resets the simiulation status
    rospy.wait_for_service('/gazebo/reset_simulation')
    reset_world = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
    reset_world()
    
    # Loop  
    while not rospy.is_shutdown():
      # Gets time
      self.seconds = rospy.get_time() - self.start_time
      # Turns robot until it finds the right angle to travers to the point
      # If the robot is turning, it gets the current angle, else, it gets the distance
      if self.turn:
        self.angle = (self.angV * self.seconds) % 6.28
      else:
        self.distance = self.linV * self.seconds

      # Calculate position (ESTO DEBO CAMBIAR POR OS DATOS DE POSE ESTIMATION)
      # Updates the position of x and y
      self.position.x = self.POSITIONX + self.initPosition.x #(self.linV*np.sin(self.initangle) * self.seconds) + self.initPosition.x
      self.position.y = self.TARGETY + self.initPosition.y#(self.linV*np.cos(self.initangle) * self.seconds) + self.initPosition.y
      self.position.z = self.ORIENTATIONZ

      # SI la distancia del robot es menor a la distancia objetivo
      if self.targetDistance < self.distance:
        # Moves the robot
        self.move()
        print("Done " + str(self.current))
        print(self.initangle)
        self.current += 1
        # Actual point status
        if self.current > len(self.points)-1:
          self.current = 0
        
        # Set target x and y, and keeps track of the robot current position 
        self.target.x = self.points[self.current][0]
        self.target.y = self.points[self.current][1]
        self.initPosition.x = self.position.x
        self.initPosition.y = self.position.y

        # Gets linear distance and angular distance from target
        print(self.initPosition)
        self.targetDistance = np.sqrt(np.power(self.target.x - self.position.x,2) + np.power(self.target.y - self.position.y,2))
        self.targetAngle = (np.arctan2(self.target.y - self.position.y, self.target.x - self.position.x) - self.angle) % (2*np.pi)
        # Set to start rotating the robot
        self.turn = True
        self.start_time = rospy.get_time()

      # If robot in correct orientation, stop robot's turning the robot and start moving forward
      elif self.angle > self.targetAngle*0.9 and self.angle < self.targetAngle * 1.1 and self.turn:
        #turning off
        # 
        self.move()
        self.turn = False
        # Variable that keeps track of the orientation of the puzzlebot
        self.initangle += self.angle + 0.2
        # Wrap to pi
        self.initangle = self.initangle % 6.28
        # Resets time
        self.start_time = rospy.get_time()
        self.angle = 0
        print("stop turning")
      else:
        # If the puzzlebot isn't in correct orientation, turn the puzzlebot
        if self.turn:
          self.move(0,0,0,0,0,self.angV)
        # Moves the puzzlebot forward
        else:
          self.move(self.linV,0,0,0,0,0)

  def move(self, x=0, y=0, z=0, wx=0, wy=0, wz=0):
    """
      x     | Float, x axis linear velocity
      y     | Float, y axis linear velocity
      z     | Float, z axis linear velocity
      wx    | Float, x axis angular velocity
      wy    | Float, y axis angular velocity
      wz    | Float, z axis angular velocity
      MOves the robot
    """

    self.msg.linear.x = x
    self.msg.linear.y = y
    self.msg.linear.z = z

    self.msg.angular.x = wx
    self.msg.angular.y = wy
    self.msg.angular.z = wz


    self.angError = (np.arctan2(self.target.y - self.initPosition.y, self.target.x - self.initPosition.x) - self.angle) % (2*np.pi)
    self.angV = self.anK * self.angError

    self.linError = np.sqrt(np.power(self.target.x - self.initPosition.x,2) + np.power(self.target.y - self.initPosition.y,2))
    # Calculate Proportional part
    self.linV = self.linError * self.linK

    self.publisher.publish(self.msg)
    self.errorP.publish(self.targetDistance)

  # Callback for Pose Estimation code 
  def poseCallback(self, msg):
      self.POSITIONX = msg.position.x
      self.TARGETY = msg.position.y
      self.ORIENTATIONZ = msg.orientation.z


  # Stops the robot
  def stop(self):
    rospy.loginfo("Closing controller...")
    self.move()


if __name__ == "__main__":
  control = open_loop()
