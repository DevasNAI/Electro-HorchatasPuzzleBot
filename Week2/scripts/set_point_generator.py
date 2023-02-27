#!/usr/bin/env python
import rospy
import numpy as np
from challenge2.msg import set_point

# Setup Variables, parameters and messages to be used (if required)

#Setpoint to send
goal = set_point()
goal.status = "Setpoint has been sent"
#Parameters
setpointAmplitude = rospy.get_param("/setpointAmplitude", 5.0)
signalType = rospy.get_param("/signalType", "sine")
signalOffset = rospy.get_param("/signalOffset", setpointAmplitude+1.0)

#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
  print("Stopping")


if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("Set_Point_Generator")
    rate = rospy.Rate(100)
    rospy.on_shutdown(stop)

    #Setup Publishers and subscribers here
    sp = rospy.Publisher("/set_point", set_point, queue_size=1)

    print("The Set Point Generator is Running")

    initTime = rospy.get_time()

    #Run the node
    while not rospy.is_shutdown():
        #Write your code here
        goal.time = rospy.get_time()

        #If type is sine publish a sine wave, else publish a step
        if signalType == "sine":
          goal.setpoint = np.sin(goal.time)*setpointAmplitude + signalOffset
        else:
          goal.setpoint = setpointAmplitude

        #Publish setpoint
        sp.publish(goal)
        rate.sleep()