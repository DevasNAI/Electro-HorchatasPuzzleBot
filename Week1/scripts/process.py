#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
import numpy as np

#Definicion de variables
pi = np.pi
signal = 0 
time = 0
negative = False

#Callback del tiempo
def callbackTime(msg):
    #Imprimir el tiempo
    global time
    time = msg.data
    rospy.loginfo("Time: " + str(time))


#   Callback de la señal
def callbackSignal(msg):
    global negative

    #Publisher de la señal procesada 
    newSignal = rospy.Publisher("proc_signal", Float32, queue_size=10)

    #Se recibe la señal senoidal generada
    signalSin = msg.data

    #Se obtiene el coseno con la identidad trigonometrica 1 = cos²(t) + sen²(t)
    signalCos = np.sqrt((1 - pow(signalSin, 2)))

    #Se obtiene atan2 del coseno y del seno
    p = round(np.arctan2(signalCos, signalSin),2)
    
    #Si atan2 se aproxima a pi
    if abs(p) >= 3.08:
        #Cambiar el estado de la variable negative a True
        negative = True
    #Si atan2 se aproxima a 0
    elif abs(p) <= 0.06:
        #Cambiar el estado de la variable negative a True
        negative = False

    #Si negative == True
    if negative:
        #Multiplicar el coseno por -1
        signalCos = -signalCos

    #Se recorre la señal con la formula sen(a + b) = sen(a)*cos(b) + sen(b)*cos(a)
    # y se cambia la amplitud y se mueve para arriba
    x = signalSin * np.cos(pi/2)
    y = signalCos * np.sin(pi/2)
    signal = (x+y)*0.5 + 1

    #Se imprime y se publica la señal
    rospy.loginfo("signal = " + str(signal))
    newSignal.publish(signal)

if __name__ == "__main__":
    #Inicializacion del nodo
    rospy.init_node("process")
    
    #Subscribers
    rospy.Subscriber("/signal", Float32, callbackSignal)
    rospy.Subscriber("/time", Float32, callbackTime)

    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        rate.sleep()
