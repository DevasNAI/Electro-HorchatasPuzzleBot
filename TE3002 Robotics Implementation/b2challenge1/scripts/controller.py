#!/usr/bin/env python

import rospy
import numpy as np
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist, TwistStamped, Point
from std_srvs.srv import Empty

class open_loop:
  def __init__(self):
    # create publisher and message as instance variables
    self.publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    self.msg = Twist()
    self.start_time = 0

    self.linV = 0.75
    self.angV = 0.5

    self.points = [(1,2), (-1,-2), (4,4), (1,1)]
    self.current = 0

    # do some cleanup on shutdown
    rospy.on_shutdown(self.stop)

    # start by moving robot
    rospy.init_node('robot_control')

    self.turn = True
    self.distance = 0
    
    self.position = Point()
    self.target = Point()
    self.initPosition = Point()

    self.angle = 0

    self.initPosition.x = -0.95
    self.initPosition.y = 0.75

    self.position.x = self.initPosition.x
    self.position.y = self.initPosition.y

    self.initangle = -1.57

    self.target.x = self.points[self.current][0]
    self.target.y = self.points[self.current][1]

    self.targetDistance = np.sqrt(np.power(self.target.x - self.initPosition.x,2) + np.power(self.target.y - self.initPosition.y,2))
    self.targetAngle = (np.arctan2(self.target.y - self.initPosition.y, self.target.x - self.initPosition.x) - self.initangle) % 2*np.pi

    rospy.wait_for_service('/gazebo/reset_simulation')
    reset_world = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
    reset_world()

    while not rospy.is_shutdown():
      self.seconds = rospy.get_time() - self.start_time

      if self.turn:
        self.angle = (self.angV * self.seconds) % 6.28
      else:
        self.distance = self.linV * self.seconds
          
      self.position.x = (self.linV*np.sin(self.initangle) * self.seconds) + self.initPosition.x
      self.position.y = (self.linV*np.cos(self.initangle) * self.seconds) + self.initPosition.y
      self.position.z = 0

      if self.targetDistance < self.distance:
        self.move()
        print("Done " + str(self.current))
        print(self.initangle)
        self.current += 1
        if self.current > len(self.points)-1:
          self.current = 0
        
        self.target.x = self.points[self.current][0]
        self.target.y = self.points[self.current][1]
        self.initPosition.x = self.position.x
        self.initPosition.y = self.position.y

        print(self.initPosition)
        self.targetDistance = np.sqrt(np.power(self.target.x - self.position.x,2) + np.power(self.target.y - self.position.y,2))
        self.targetAngle = (np.arctan2(self.target.y - self.position.y, self.target.x - self.position.x) - self.angle) % 6.28
        
        #print(self.position)
        self.turn = True
        self.start_time = rospy.get_time()
      elif self.angle > self.targetAngle*0.9 and self.angle < self.targetAngle * 1.1 and self.turn:
        #turning off
        self.move()
        self.turn = False
        self.initangle += self.angle + 0.2
        self.initangle = self.initangle % 6.28
        self.start_time = rospy.get_time()
        self.angle = 0
        print("stop turning")
      else:
        if self.turn:
          self.move(0,0,0,0,0,self.angV)
        else:
          self.move(self.linV,0,0,0,0,0)

  def move(self, x=0, y=0, z=0, wx=0, wy=0, wz=0):
    self.msg.linear.x = x
    self.msg.linear.y = y
    self.msg.linear.z = z

    self.msg.angular.x = wx
    self.msg.angular.y = wy
    self.msg.angular.z = wz

    self.publisher.publish(self.msg)

  def stop(self):
    rospy.loginfo("Closing controller...")
    self.move()


if __name__ == "__main__":
  control = open_loop()