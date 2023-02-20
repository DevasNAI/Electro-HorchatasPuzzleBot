#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
import numpy as np

if __name__ == "__main__":

    #Publishers
    signal = rospy.Publisher("signal", Float32, queue_size=10)
    time = rospy.Publisher("time", Float32, queue_size=10)
    
    #Inicializacion del nodo
    rospy.init_node("signal_generator")

    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        #Se obtiene el tiempo actual
        currentTime = rospy.get_time()

        #Se calcula el valor del seno
        currentY = np.sin(currentTime)

        #Se publica la señal y el tiempo actual
        signal.publish(currentY)
        time.publish(Float32(currentTime))
        rospy.loginfo("Y (" + str(currentTime) + ") = "  + str(currentY))

        rate.sleep()