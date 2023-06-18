#!/usr/bin/env python3
#
#Code developed by: Team EHorchatas
#Date: 18/06/2023


#Libraries Definition
from std_msgs.msg import String, Bool, Float32
from geometry_msgs.msg import Twist
from controller import LineFollower
from intersection import Intersection
from yolo import YOLO
from sensor_msgs.msg import Image
from std_srvs.srv import Empty
import numpy as np
import rospy
import time
import cv2

#Class Definition, "RETO"
class Reto:
    def __init__(self):
        #Init controller
        self.LineFollower = LineFollower()
        self.detectionIntersection = Intersection()
        #TODO 
        # Add YOLO class instance
        self.detection = YOLO()
        #Publishers and Subscribers
        self.run = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        self.rawImg = None

        self.velocity = "Fast"
        self.inIntersection = False
        self.turn = "Forward"

    
    #Method to open the camera, permits the setting up parameters
    def gstreamer_pipeline(self, sensor_id=0,capture_width=1280,capture_height=720,display_width=1280,display_height=720,framerate=30,flip_method=0):
        return (
            "nvarguscamerasrc sensor-id=%d ! "
            "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                sensor_id,
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )

    def main(self):

        #Define variable to capture video
        camera = cv2.VideoCapture(self.gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
        
        while not rospy.is_shutdown():
            ret, img = camera.read()

            self.rawImg = img
            
            if not ret:
                break

            vel = Twist()
            if self.rawImg is None:
                rospy.loginfo("NO CAM")
                continue

            self.inIntersection = self.detectionIntersection.callback(self.rawImg)

            #Get YOLO inference
            results = self.detection.detect(self.rawImg)

            #FYOLOV5 detection for each variable

            for detection in results:
                if detection == "verde":
                    self.velocity = "Fast"

                elif detection == "amarillo":
                    self.velocity = "Slow"

                elif detection == "rojo":
                    self.velocity == "stop"

                elif detection == "Slow":
                    self.velocity = "Slow"

                elif detection == "Right":
                    self.turn = "Right"

                elif detection == "Left":
                    self.turn = "Left"

                elif detection == "Forward":
                    self.turn = "Forward"
                else:
                    self.velocity="Fast"

            #Add logic of semaphore to when intersection is detected
            if self.inIntersection:
                rospy.loginfo("In intersection")
                if self.velocity == "Fast" or self.velocity == "Slow":
                    if self.turn == "Left":
                        rospy.loginfo("Turn Left")
                        self.run.publish(self.LineFollower.turn90(-1))
                        #time.sleep(2.75)

                    elif self.turn == "Right":
                        rospy.loginfo("Turn Right")
                        self.run.publish(self.LineFollower.turn90(1))
                    #time.sleep(2.75)

                    else:
                        rospy.loginfo("Crossing the street")
                        self.run.publish(self.LineFollower.cross())
                        #time.sleep(2)
                    vel = self.LineFollower.stop()
                    self.inIntersection = False

                else:
                    vel = self.LineFollower.stop()
            else:
                vel = self.LineFollower.callback(self.rawImg)
                if self.velocity == "Slow":
                    rospy.loginfo("Slow mode")
                    vel.linear.x *= 0.7
            #Last thing
            self.run.publish(vel)
        camera.release()


if __name__ == "__main__":
    # Initialize the node and create a ROS subscriber for receiving images from camera topic
    rospy.init_node('controller', anonymous=True)

    robot = Reto()
    robot.main()
# Destroy all the windows
    cv2.destroyAllWindows()