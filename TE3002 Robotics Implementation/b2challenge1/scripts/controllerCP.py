#!/usr/bin/env python

import rospy
import numpy as np
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist, TwistStamped, Point, Pose
from std_srvs.srv import Empty

class open_loop:
  def _init_(self):
    # create publisher and message as instance variables
    self.publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    self.msg = Twist()
    self.points = [(1,2), (-1,-2), (4,4), (1,1)]
    self.current = 0

    # do some cleanup on shutdown
    rospy.on_shutdown(self.stop)

    # start by moving robot
    rospy.init_node('robot_control')

    self.turn = True
    self.linV = 0
    self.angV = 0
    
    self.pose = Pose()

    rospy.Subscriber("pose", Pose, self.cbPose)
    self.target = Point()

    self.target.x = self.points[self.current][0]
    self.target.y = self.points[self.current][1]

    rospy.wait_for_service('/gazebo/reset_simulation')
    reset_world = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
    reset_world()
    self.main()

  def main(self):
    while not rospy.is_shutdown():
      if self.turn:
        self.thetaT = np.arctan2(self.target.y, self.target.x)
        
        if self.thetaT < 0:
          self.thetaT = self.thetaT*-1 + np.pi

        self.errorAng = self.thetaT - self.pose.orientation.z
        self.angV = 0.8*self.errorAng
        print(self.angV)

        if round(self.errorAng, 2) < 0:
          self.turn = False
          self.angV = 0
          self.move()
          print("done turning")
          rospy.sleep(1)
        else:
          self.move(0, 0, 0, 0, 0, self.angV)
      else:
        self.errorLin = np.sqrt(np.power((self.target.x - self.pose.position.x),2) + np.power((self.target.y - self.pose.position.y),2))
        if self.errorLin - 0.1 < 0.0:
          self.linV = 0
          self.move()
          rospy.sleep(4)
          print("donde")
        else:
          self.linV = 0.8*self.errorLin
          self.move(self.linV, 0, 0, 0, 0, 0)

  def move(self, x=0, y=0, z=0, wx=0, wy=0, wz=0):
    self.msg.linear.x = x
    self.msg.linear.y = y
    self.msg.linear.z = z

    self.msg.angular.x = wx
    self.msg.angular.y = wy
    self.msg.angular.z = wz

    self.publisher.publish(self.msg)

  def cbPose(self, msg):
    self.pose = msg

  def stop(self):
    rospy.loginfo("Closing controller...")
    self.move()


if __name__ == "__main__":
  control = open_loop()
