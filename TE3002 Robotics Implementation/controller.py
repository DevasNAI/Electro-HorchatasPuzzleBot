#!/usr/bin/env python3
#
#Code developed by: Team EHorchatas
#Date: 18/06/2023


#Libraries Definition
import cv2
import numpy as np
import time
import rospy
from std_msgs.msg import Float32, String
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class LineFollower:

    def __init__(self):

        #class variables initialization
        self.p=0.0015
        self.d=0.00005
        self.prev_error=0
        self.width, self.height = 480, 360
        self.cx=0
        self.maxSpeed=0.2
        self.minSpeed=0.05
        self.errorMax_Speed=80
        self.line_Speed=0
        self.flag=0
        self.last_time=0
        self.msg = Twist()
        self.imgThres = None
        self.avgError = []

    
    #Function to ctrop the received image
    def crop_size(self,height, width):
        #Get the measures to crop the image
        return (8*height//10, 10*height//10, 2*width//10, 8*width//10)


    #Function to apply filters and get the line to be followed by the Puzzlebot
    def crop_thres(self,crop):
        
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00'] != 0:
                self.cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.line(crop,(self.cx,0),(self.cx,720),(255,0,0),1)
                cv2.line(crop,(0,cy),(1280,cy),(255,0,0),1)
                frame = cv2.drawContours(crop, c, -1, (255,255,0), 1)

        return self.cx


    #Function to make a 90 degrees turn
    def turn90(self, orientation):
        line=0.15
        speed=0.1*orientation
        self.move(line,0,0,0,0,speed)
        print("turn90")
        return self.msg 
        
    #Function to stop 
    def stop(self):
        self.move(0,0,0,0,0,0)
        print("stop")
        return self.msg 
        
    #Function to folow an straight line
    def cross(self):
        self.move(0.1,0,0,0,0,0)
        print("cross")
        return self.msg 
        
    #FUnction to implement the PD controller, defines the linear and angular velocity
    def lineFollower(self, desired_pos,point):
        error=desired_pos-point
        avg=0
        current_time=rospy.get_time()
        dt=current_time-self.last_time
        
        pd=self.p*error + self.d*(error-self.prev_error)/dt

        self.prev_error=error
        self.last_time=current_time

        speed=round(float(pd),2)        

        if len(self.avgError) >= 10:
            self.avgError.pop()
        self.avgError.append(error)
        
        for error in self.avgError:
            avg += error
        
        avg = avg / len(self.avgError)

        vel=abs(self.maxSpeed-(abs(float(avg))/1000))
        line=round(vel,3)
        
        self.move(line,0,0,0,0,speed)


    #Function to set corresponding speed values 
    def move(self, x=0, y=0, z=0, wx=0, wy=0, wz=0):
        self.msg.linear.x = x
        self.msg.linear.y = y
        self.msg.linear.z = z

        self.msg.angular.x = wx
        self.msg.angular.y = wy
        self.msg.angular.z = wz

    
    #Function to receive image and give corresponding configurations 
    def callback(self, image):
        self.cv_image=cv2.flip(image,0)
        self.cv_image=cv2.flip(self.cv_image,1)
        
        self.cv_image=cv2.resize(self.cv_image,(self.width,self.height))
        
        crop_h_start, crop_h_stop, crop_w_start, crop_w_stop = self.crop_size(self.height, self.width)
        crop = self.cv_image[crop_h_start:crop_h_stop, crop_w_start:crop_w_stop]
        crop_h, crop_w,_=crop.shape
        self.desired_pos=crop_w/2
        
        self.point=self.crop_thres(crop)
        self.lineFollower(self.desired_pos, self.point)
        return self.msg

        