#!/usr/bin/env python
import rospy
import numpy as np
from challenge2.msg import motor_output
from challenge2.msg import motor_input
from challenge2.msg import set_point

class Controller():
  def __init__(self):
    """
      Controller

      This class will act as a simulated PID Controller for a Direct Current Motor
      All the PID calculation is done with no external dependencies.

      This controller has two topic Subscriptions and one topic Publication.
      /set_point      Is provided by the used through the setpoint generator Node.
      /motor_output   This is the output that is done by the System Node, which is used as feedback data.
      /motor_input    This will be the System input, the u(t) value of the controller.
    
    """
    #  Variable initialization
    #   The value in which the motor should go into.
    self.setpoint = 0.0
    #   Controller obtained value
    self.u_val = 0.0
    #   Controller's feedback value
    self.output = 0.0
    #   Kp  calculation of Error
    self.lastError = 0.0
    #   Ki  calculation of Error
    self.error_prev = 0.0
    #   Time retrieval
    self.t_prev = rospy.get_time()
    #   Controller's final value
    self.motor = motor_input()

    # Controller Parameters
    #   Motor's operation range
    self.u_max = rospy.get_param("/u_max", 1.0)
    self.u_min = rospy.get_param("/u_min", -1.0)
    #   PID Controller values
    self.kp = rospy.get_param("/kp", 0.02)
    self.ki = rospy.get_param("/ki", 0.025)
    self.kd = rospy.get_param("/kd", 0)

    # Publisher and subscription setup
    rospy.Subscriber("/set_point", set_point, self.callbackSetpoint)
    rospy.Subscriber("/motor_output", motor_output, self.callbackMotorOutput)

    self.inputSignal = rospy.Publisher("/motor_input", motor_input, queue_size=1)

    pass

  def control(self):
    """
        Control

        This function acts as the controller for the Controller Class, it calculates
          the u value which is sent to the system Node in order to perform the motor's behavior.
        Returns @ self.u_val  The processed control signal

    """
    # It obtaines a time differential
    t = rospy.get_time()
    dt = t - self.t_prev

    # Calculates the error and approximate its integral with a sum and the derivative with the slope of the last and current error.
    error = (self.setpoint - self.output) 
    self.error_prev += error*dt
    self.error_future = (error - self.lastError)/dt

    #`Calculates the controller signal to be sent to the system
    self.u_val = (error * self.kp) + (self.error_prev * self.ki) + (self.error_future*self.kd)

    # Range Bound to the signal between the upper and lower limits
    if self.u_val > self.u_max:
      self.u_val = self.u_max
    elif self.u_val < self.u_min:
      self.u_val = self.u_min

    # Stores the current error and time for future iteration
    self.lastError = error
    self.t_prev = t

    # Returns the processed signal
    return self.u_val

  # Setpoint Callback for setpoint reception
  def callbackSetpoint(self, msg):
      # Assigns the setpoint value from parameter file
      self.setpoint = float(msg.setpoint)

  # System feedback Callback 
  def callbackMotorOutput(self, msg):
      # Sends the feedback to the controller and publishes the adjusted signal
      self.output = float(msg.output)
      self.motor.input = self.control()
      self.inputSignal.publish(self.motor)
      
# Stop Condition
def stop():
 #  Stops the program
  print("Stopping")
  self.inputSignal.publish(0)


if __name__=='__main__':

    # Node initialization
    rospy.init_node("controller")
    rate = rospy.Rate(100)
    rospy.on_shutdown(stop)

    print("The Controller is Running")

    # Creates the controller
    pid = Controller()
    
    #Run the node
    while not rospy.is_shutdown():
      pid.motor.time = rospy.get_time()
      rate.sleep()
