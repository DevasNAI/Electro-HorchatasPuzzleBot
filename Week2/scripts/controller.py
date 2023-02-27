#!/usr/bin/env python
import rospy
import numpy as np
from challenge2.msg import motor_output
from challenge2.msg import motor_input
from challenge2.msg import set_point

class Controller():
  def __init__(self):
    self.setpoint = 0.0
    self.u_val = 0.0
    self.output = 0.0

    self.lastError = 0.0
    self.error_prev = 0.0
    self.t_prev = rospy.get_time()

    self.motor = motor_input()

    #Parameters
    self.u_max = rospy.get_param("/u_max", 1.0)
    self.u_min = rospy.get_param("/u_min", -1.0)
    self.kp = rospy.get_param("/kp", 0.02)
    self.ki = rospy.get_param("/ki", 0.025)
    self.kd = rospy.get_param("/kd", 0)

    #Setup Publishers and subscribers here
    rospy.Subscriber("/set_point", set_point, self.callbackSetpoint)
    rospy.Subscriber("/motor_output", motor_output, self.callbackMotorOutput)

    self.inputSignal = rospy.Publisher("/motor_input", motor_input, queue_size=1)

    pass

  def control(self):
      #Get delta t
      t = rospy.get_time()
      dt = t - self.t_prev

      #Calculate the error and approximate its integral with a sum and the derivative with the slope of the last and current error.
      error = (self.setpoint - self.output) 
      self.error_prev += error*dt
      self.error_future = (error - self.lastError)/dt

      #Calculate the signal to be sent to the system
      self.u_val += (error * self.kp) + (self.error_prev * self.ki) + (self.error_future*self.kd)

      #Bound the signal to within the upper and lower limits
      if self.u_val > self.u_max:
        self.u_val = self.u_max
      elif self.u_val < self.u_min:
        self.u_val = self.u_min

      #Store the current error and time
      self.lastError = error
      self.t_prev = t

      #Return the processed signal
      return self.u_val

  #Callback for when a setpoint is recieved
  def callbackSetpoint(self, msg):
      #Set the setpoint
      self.setpoint = float(msg.setpoint)

  #Callback for when the feedback of the system is recieved
  def callbackMotorOutput(self, msg):
      #Send the feedback to the controller and publish the adjusted signal
      self.output = float(msg.output)
      self.motor.input = self.control()
      self.inputSignal.publish(self.motor)
      
#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
  print("Stopping")


if __name__=='__main__':

    #Initialise and Setup node
    rospy.init_node("controller")
    rate = rospy.Rate(100)
    rospy.on_shutdown(stop)

    print("The Controller is Running")

    #Create the controller
    pid = Controller()
    
    #Run the node
    while not rospy.is_shutdown():
      pid.motor.time = rospy.get_time()
      rate.sleep()
