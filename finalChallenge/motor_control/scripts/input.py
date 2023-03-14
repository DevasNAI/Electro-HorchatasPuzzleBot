#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float32
from motor_control.msg import set_point

# Setup Variables, parameters and messages to be used (if required)

#Setpoint to send
goal = set_point()
#Parameters
setpointAmplitude = rospy.get_param("/setpointAmplitude", 30.0)
signalType = rospy.get_param("/signalType", "sine")

#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
  print("Stopping")


if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("input")
    rate = rospy.Rate(50)
    rospy.on_shutdown(stop)

    #Setup Publishers and subscribers here
    sp = rospy.Publisher("/set_point", set_point, queue_size=1)

    print("The Input Generator is Running")
    start_time = rospy.get_time()
    negative = 1

    goal.status = "Running"

    #Run the node
    while not rospy.is_shutdown():
        time = rospy.get_time() - start_time

        #If type is sine publish a sine wave, else publish a step
        if signalType == "sine":
          goal.setpoint = np.sin(rospy.get_time())*setpointAmplitude
        elif signalType == "square":
          goal.setpoint = setpointAmplitude*negative
          if time > 5:
            negative *= -1 
            start_time = rospy.get_time()
        else:
          goal.setpoint = setpointAmplitude

        goal.time = rospy.get_time()
        #Publish setpoint
        sp.publish(goal)
        rate.sleep()