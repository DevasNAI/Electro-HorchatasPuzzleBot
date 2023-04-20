#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist, TwistStamped, Point, Pose
from std_srvs.srv import Empty

wl = 0.0
wr = 0.0
angle = -1.57
positionx = -0.95
positiony = 0.75
position = Pose()

lastTime = 0.0
dt = 0.0

def cbWL(msg):
    global wl
    wl = msg.data

def cbWR(msg):
    global wr
    wr = msg.data

if __name__ == "__main__":

    #Publishers
    posePub = rospy.Publisher("pose", Pose, queue_size=1)

    #Subscribers
    rospy.Subscriber("wl", Float32, cbWL)
    rospy.Subscriber("wr", Float32, cbWR)
    
    #Inicializacion del nodo
    rospy.init_node("pose_generator")
    
    while not rospy.is_shutdown():
        currentTime = rospy.get_time()

        if currentTime <= 1:
            angle = -1.57
            positionx = -0.95
            positiony = 0.75

        dt = currentTime - lastTime

        angle += 0.05*((wr - wl) / 0.19) * dt

        angle = angle % 6.28

        positionx += 0.05*((wr + wl) / 2) * dt * np.cos(angle)
        positiony += 0.05*((wr + wl) / 2) * dt * np.sin(angle)
        
        position.position.x = positionx
        position.position.y = positiony
        position.orientation.z = angle

        posePub.publish(position)
        print(position)
        lastTime = currentTime
