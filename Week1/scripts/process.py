#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
import numpy as np

#   Variable definition
pi = np.pi
signal = 0 
time = 0
#   This varaible will help us change the direction of an absolute Cosine signal
negative = False

#   Time Callback
def callbackTime(msg):
    """
        CallbackTime
        Receives a message and assigns the message to a local and global variable
    """
    #   Assigns the topic value into a global variable
    global time
    time = msg.data
    #   Prints time
    rospy.loginfo("Time: " + str(time))


#   Signal Callback
def callbackSignal(msg):
    """
        Receives a sine signal and tries to use the same signal to add a cosine signal,
            it then goes through trigonometric opperations and publishes the topic.
    """
    global negative

    #   Processed signal Publisher topic
    newSignal = rospy.Publisher("proc_signal", Float32, queue_size=10)

    #   Receives a sine signal from the topic
    signalSin = msg.data

    #   It obtains a Cosine signal through the trigonometric identity: 1 = cos2(t) + sen2(t)
    signalCos = np.sqrt((1 - pow(signalSin, 2)))

    #   We obtain an inverse Tangent with the cosine and sine signals
    p = round(np.arctan2(signalCos, signalSin),2)
    
    #   Conditions to change the resulted cosine value to negative or positive with the help of the arctangent.
    if abs(p) >= 3.08:
        #   negative variable state changes to True
        negative = True
    #   If arctan value is reaching 0,
    elif abs(p) <= 0.06:
        #   It changes negative variable state to False
        negative = False

    #   If the control variable is positive, then the cosine signal will have a negative value.
    if negative:
        #   Cosine negative multiplication
        signalCos = -signalCos

    #   Signal gets shifted with sin(a + b) = sin(a)*cos(b) + sin(b)*cos(a) formula
    #       and 'y's amplitude is changed and shifted upwar.
    x = signalSin * np.cos(pi/2)
    y = signalCos * np.sin(pi/2)
    #=  Final signal
    signal = (x+y)*0.5 + 1

    #   Signal is printed and published in a topic
    rospy.loginfo("signal = " + str(signal))
    newSignal.publish(signal)

if __name__ == "__main__":
    #   Process node initialization
    rospy.init_node("process")
    
    #   ROS Topic Subscription
    rospy.Subscriber("/signal", Float32, callbackSignal)
    rospy.Subscriber("/time", Float32, callbackTime)

    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        rate.sleep()
