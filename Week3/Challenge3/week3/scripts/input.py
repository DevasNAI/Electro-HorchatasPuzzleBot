#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float32

# Setup Variables, parameters and messages to be used (if required)

#Setpoint to send
goal = Float32() 
#goal.status = "Setpoint has been sent"

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
  sp = rospy.Publisher("/cdm_pwm", Float32, queue_size=1)

  print("The Set Point Generator is Running")

  #Initialize the time before the loop so we can rest it on the future
  initTime = rospy.get_time()
  #Run the node
  while not rospy.is_shutdown():
    #Write your code here
    #To calculate the seconds we take the real time and rest it the time we save before
    seconds = rospy.get_time() - initTime

#-------------------------------------------- SIGNALS ----------------------------------
    #If type is sine publish a sine wave
    if signalType == "sine":
      goal = np.sin(rospy.get_time())*setpointAmplitude + signalOffset # Calculate the sine with the parameters predefined and save on the setpoint variable
    #If type is step publish a constant value
    elif signalType == "step":
      goal = 200
    #If type is square publish a square wave
    elif signalType == "square":
      if seconds < 5.0: #If seconds is less than 5s the setpoint is 200
        goal = 200
      elif seconds > 5.0 and seconds < 10:  #If seconds is more than 5s and less than 10s the setpoint is 0
        goal = 0
      elif seconds > 10.0: #If the time is more than 10s we restart the time, and with this restart the wave
        initTime = rospy.get_time()
    else: #The setpoint is going to be the Amplitude
      goal = setpointAmplitude
#--------------------------------------------------------------------------------------

  #Publish setpoint
  sp.publish(goal)
  rate.sleep()