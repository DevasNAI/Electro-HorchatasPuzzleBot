import cv2
import numpy as np
from time import sleep
import sys
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist, TwistStamped, Point, Pose
from std_srvs.srv import Empty
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class LineFollower:
  
    def __init__(self):
        self.bridge = CvBridge()
        self.hsvVals = [0, 0, 0, 146, 255, 88]
        self.sensors = 3
        self.threshold = 0.2
        self.width, self.height = 480, 360

        self.sensitivity = 3  # if the number is high, decrease sensitivity
        self.weights = [.1, .05, .5, -.05, -.1]
        self.curve = 0
        self.fSpeed = .1

        self.p=0.01
        self.d=0.5
        self.prev_error=0
        self.desired_pos=self.width // 2


        rospy.init_node("line_follower")
        self.publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("video_source/raw", Image, self.callback)
        self.msg = Twist()
        self.img = None
        self.imgThres = None



    def main(self):
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if self.img is not None:
                cv2.imshow("Output", self.img)
            if self.imgThres is not None:
                cv2.imshow("Path", self.imgThres)

            # Add the following line to process OpenCV events
            cv2.waitKey(1)

        cv2.destroyAllWindows()
   
    def thresholding(self, img):
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower = np.array([self.hsvVals[0], self.hsvVals[1], self.hsvVals[2]])
            upper = np.array([self.hsvVals[3], self.hsvVals[4], self.hsvVals[5]])
            mask = cv2.inRange(hsv, lower, upper)
            return mask


    def getContours(self, imgThres):
        cx = 0
        contours, hierarchy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            biggest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(biggest)
            cx = x + w // 2
            cy = y + h // 2

            cv2.drawContours(self.img, contours, -1, (255, 0, 255), 7)
            cv2.circle(self.img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        return cx



    def getSensorOutput(self, imgThres, sensors):
        imgs = np.hsplit(imgThres, sensors)
        senOut = []
        totalPixels = (self.img.shape[1] // sensors) * self.img.shape[0]
        for x, im in enumerate(imgs):
            pixelCount = cv2.countNonZero(im)
            if pixelCount > self.threshold * totalPixels:
                senOut.append(1)
            else:
                senOut.append(0)
            cv2.imshow(str(x), im)
        print(senOut)
        return senOut
   

    def sendCommands(self, senOut):
  

        error=self.desired_pos-self.cx
        pid=self.p*error+self.d*(error-self.prev_error)
        self.prev_error=error
        speed=float(np.clip(pid,-0.3,0.3))
        print("speed: ",speed)
        print("error: ", error)


        # rotation
        if senOut == [1, 0, 0]:
            self.move(0,0,0,0,0,-speed)

        elif senOut == [1, 1, 0]:
            self.move(0,0,0,0,0,-speed)

        elif senOut == [0, 1, 0]:
            self.move(0.2,0,0,0,0,0)
        elif senOut == [0, 1, 1]:
            self.move(0,0,0,0,0,-speed)
        elif senOut == [0, 0, 1]:
            self.move(0,0,0,0,0,-speed)

        elif senOut == [0, 0, 0]:
            self.move(-.05,0,0,0,0,0)
        elif senOut == [1, 1, 1]:
            self.move(0,0,0,0,0,0)
        elif senOut == [1, 0, 1]:
            self.move(-1,0,0,0,0,0)
        sleep(0.1)

    def move(self, x=0, y=0, z=0, wx=0, wy=0, wz=0):
        self.msg.linear.x = x
        self.msg.linear.y = y
        self.msg.linear.z = z

        self.msg.angular.x = wx
        self.msg.angular.y = wy
        self.msg.angular.z = wz

        self.publisher.publish(self.msg)




    def callback(self, msg):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.cv_image=cv2.flip(self.cv_image,0)

            self.cv_image=cv2.flip(self.cv_image,1)
            self.img = cv2.resize(self.cv_image, (self.width, self.height))
            self.imgThres = self.thresholding(self.img)

            self.cx = self.getContours(self.imgThres)
            self.senOut = self.getSensorOutput(self.imgThres, self.sensors)
            self.sendCommands(self.senOut)
        except CvBridgeError as e:
            rospy.logerr(e)


if __name__ == '__main__':
    line_follower = LineFollower()
    line_follower.main()
    rospy.spin()

