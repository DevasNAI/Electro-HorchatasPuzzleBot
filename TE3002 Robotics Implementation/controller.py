#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist, TwistStamped, Point, Pose
from std_srvs.srv import Empty

class open_loop:
  def __init__(self):
    # create publisher and message as instance variables
    print("INIT S")
    self.publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    self.msg = Twist()
    self.points = [(1,2), (0,0), (-1,-2), (3,3), (1,1)]
    self.current = 0
    self.thetaT = 0 
    print("Currently on init")
    # do some cleanup on shutdown
    rospy.on_shutdown(self.stop)

    # start by moving robot
    rospy.init_node('robot_control')

    self.turn = True
    self.linV = 0
    self.angV = 0
    self.integral = 0

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
        if (self.target.x - self.pose.position.x < 0 and self.target.y - self.pose.position.y < 0 and np.arctan2(self.target.y, self.target.x) != 0):
          self.thetaT2 = (np.arctan2(self.target.y - self.pose.position.y , self.target.x - self.pose.position.x) + 6.28)
          self.thetaT = self.thetaT2
          print(self.thetaT)

        if self.thetaT < 0:
          self.thetaT = 2*np.pi + self.thetaT
        elif self.thetaT <= 0:
          self.thetaT2 = (np.arctan2(self.target.y - self.pose.position.y , self.target.x - self.pose.position.x) + 6.28)
          self.thetaT = self.thetaT2

        
        self.errorAng = self.thetaT - self.pose.orientation.z
        self.angV = 0.65*self.errorAng

        if round(abs(self.errorAng), 3)-0.01 < 0:
          self.turn = False
          self.angV = 0
          self.move()
          print("done turning")
          rospy.sleep(0.1)
        else:
          self.move(0, 0, 0, 0, 0, self.angV)

      else:
        self.errorLin = np.sqrt(np.power((self.target.x - self.pose.position.x),2) + np.power((self.target.y - self.pose.position.y),2))
        print(self.errorLin)
        if self.errorLin - 0.10 < 0: # CHANGE
          self.linV = 0
          self.move()
          rospy.sleep(1)
          print("Done point " + str(self.current))

          self.current += 1
          if self.current > len(self.points)-1:
            self.current = 0
          
          self.target.x = self.points[self.current][0]
          self.target.y = self.points[self.current][1]
          #print(self.target.x)
          #print(self.target.y)
          self.turn = True
          
        else:
          self.linV = 0.42*self.errorLin 
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
