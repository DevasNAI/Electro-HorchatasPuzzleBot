#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32

if __name__ == '__main__':
  
      rospy.init_node('input')
      pwm = rospy.get_param("pwm", 201)
  
      pwm_pub = rospy.Publisher("/cmd_pwm", Float32, queue_size=1)
      rate = rospy.Rate(10)



      # spin() simply keeps python from exiting until this node is stopped
      while not rospy.is_shutdown():

        #Write your code here

        pwm_pub.publish(pwm)

        rate.sleep()
  
  

#// Write your code here 
