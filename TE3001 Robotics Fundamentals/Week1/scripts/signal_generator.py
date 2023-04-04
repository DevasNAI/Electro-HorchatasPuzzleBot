#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
import numpy as np

if __name__ == "__main__":

    #   ROS Topic Publishers
    #       Signal topic will be a Sine signal in respect to current time
    #       Time topic will have the current time value
    signal = rospy.Publisher("signal", Float32, queue_size=10)
    time = rospy.Publisher("time", Float32, queue_size=10)
    
    #   Signal Generator Node initialization
    rospy.init_node("signal_generator")

    rate = rospy.Rate(10)
    #   Infinite loop
    while not rospy.is_shutdown():
        #   Current time is obtained
        currentTime = rospy.get_time()

        #   Sine value in "current Time" is obtained
        currentY = np.sin(currentTime)

        #   Current time and Sine signal are published through their respective topics
        signal.publish(currentY)
        time.publish(Float32(currentTime))
        #   Time and Sine values are printed on terminal
        rospy.loginfo("Y (" + str(currentTime) + ") = "  + str(currentY))

        rate.sleep()