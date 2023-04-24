#!/usr/bin/env python

import rospy
import numpy as np
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist, TwistStamped, Point, Pose
from std_srvs.srv import Empty


class open_loop:
  def poseEstimation(self, msg):
    self.position_x = msg.position.x
    self.position_y = msg.position.y
    self.orientation_z = msg.orientation.z 

  def __init__(self):
    
    self.position_x = 0.0
    self.position_y = 0.0
    self.orientation_z = 0.0
    self.k = 0.05

    # create publisher
    self.publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    self.msg = Twist()
    
    #Declare initial variables
    self.start_time = 0
    
    #Linear and Angular Speed
    self.linV = 0.75
    self.angV = 0.5
    
    #Waypoints
    self.points = [(1,2), (-1,-2), (4,4), (1,1)]
    self.current = 0

    # do some cleanup on shutdown
    rospy.on_shutdown(self.stop)

    # start by moving robot
    rospy.init_node('robot_control')
    
    #variable that activates turning mode
    self.turn = True
    
    self.distance = 0
    self.position = Point()
    self.target = Point()
    self.initPosition = Point()
    self.angle = 0

    #starting point of the puzzlebot
    self.initPosition.x = -0.95
    self.initPosition.y = 0.75
    self.position.x = self.initPosition.x
    self.position.y = self.initPosition.y
    self.initangle = -1.57

    #set target
    self.target.x = self.points[self.current][0]
    self.target.y = self.points[self.current][1]
    
    #calculate distance and angle from point to point
    self.targetDistance = np.sqrt(np.power(self.target.x - self.initPosition.x,2) + np.power(self.target.y - self.initPosition.y,2))
    self.targetAngle = (np.arctan2(self.target.y - self.initPosition.y, self.target.x - self.initPosition.x) - self.initangle) % 2*np.pi
    
    rospy.Subscriber("pose", Pose, self.poseEstimation)
    #restart simulation
    rospy.wait_for_service('/gazebo/reset_simulation')
    reset_world = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
    reset_world()

    while not rospy.is_shutdown():
      self.seconds = rospy.get_time() - self.start_time
      
      #if turning get angle else, get distance
      if self.turn:
        self.angle = (self.angV * self.seconds) % 6.28
      else:
        self.distance = self.linV * self.seconds
       
      #Calculate position (change this to the data being published by poseEstimation.py)
      self.position.x = (self.linV*np.sin(self.initangle) * self.seconds) + self.initPosition.x
      self.position.y = (self.linV*np.cos(self.initangle) * self.seconds) + self.initPosition.y
      self.position.z = 0
      
      #for this next part, start checking the comments from the bottom up
      
      #if done moving forward
      if self.targetDistance < self.distance:
        self.move()
        print("Done " + str(self.current))
        
        #go to the next waypoint
        self.current += 1
        #loop to 0
        if self.current > len(self.points)-1:
          self.current = 0
        
        #set target x and y, and keep track of the robots current position
        self.target.x = self.points[self.current][0]
        self.target.y = self.points[self.current][1]
        self.initPosition.x = self.position.x
        self.initPosition.y = self.position.y
        

        #get linear distance and angular distance from target 
        self.targetDistance = np.sqrt(np.power(self.target.x - self.position_x,2) + np.power(self.target.y - self.position_y,2))
        self.targetAngle = (np.arctan2(self.target.y - self.position_y, self.target.x - self.position_x) - self.angle) % 6.28
        
        #set to start turning
        self.turn = True
        #reset time
        self.start_time = rospy.get_time()
      elif self.angle > self.targetAngle*0.9 and self.angle < self.targetAngle * 1.1 and self.turn:
        #if in the correct orientation, stop turning the robot and start moving forward
        self.move()
        self.turn = False
        #variable that keeps track of the orientation of the puzzlebot
        self.initangle += self.angle + 0.2
        #wrap to pi
        self.initangle = self.initangle % 6.28
        #reset time
        self.start_time = rospy.get_time()
        self.angle = 0
        print("stop turning")
      else:
        #if the puzzlebot isnt in the correct orientation, turn the puzzlebot
        if self.turn:
          self.move(0,0,0,0,0,self.angV)
         #else move the puzzlebot forward
        else:
          self.move(self.linV,0,0,0,0,0)
  
  #method to move the robot
  def move(self, x=0, y=0, z=0, wx=0, wy=0, wz=0):
    self.msg.linear.x = x
    self.msg.linear.y = y
    self.msg.linear.z = z

    self.msg.angular.x = wx
    self.msg.angular.y = wy
    self.msg.angular.z = wz

    self.error = np.sqrt(np.power(self.target.x - self.initPosition.x,2) + np.power(self.target.y - self.initPosition.y,2))
    # Calculate Proportional part
    self.linV = self.error * self.k

    self.publisher.publish(self.msg)
    print(self.error)
    
  #method to stop the robot when closing the controller
  def stop(self):
    rospy.loginfo("Closing controller...")
    self.move()

if __name__ == "__main__":
  control = open_loop()
