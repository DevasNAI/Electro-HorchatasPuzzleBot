# !usr/bin/python
import cv2
import numpy as np
from time import sleep
import sys
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class Intersection:
    
    def __init__(self):
        """
            Initialiazes Intersection class
            Connects image with CV Bridge and subscribes to video_source/raw topic, as well as 
                publishing the intersection topic using classic vision.
            @intersection   |   Boolean that determines if there is an intersection on the road.
        
        """
        self.bridge = CvBridge()
        self.hsvVals = [0, 0, 0, 146, 255, 88]
        self.sensors = 3
        self.boxes = 0
        self.width, self.height = 480, 360

        self.sensitivity = 3  # if the number is high, decrease sensitivity
        self.weights = [.1, .05, .5, -.05, -.1]

        rospy.init_node("intersection")
        self.publisher = rospy.Publisher("/intersection", Bool, queue_size=1)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("video_source/raw", Image, self.callback)
        self.msg = Twist()
        self.img = None
        self.imgThres = None
        self.imgCon = None
        self.isIntersection = False

    def main(self):
        """
            Displays image on computer.
            @Original image
            @Masked image
            @Contoured image
        """
        while True:
            #   Kills displaying
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            #   Displays image
            if self.img is not None:
                cv2.imshow("Output", self.img)
            if self.imgThres is not None:
                cv2.imshow("Dark Path", self.imgThres)
                cv2.imshow("Contour", self.imgCon)

            # Add the following line to process OpenCV events
            cv2.waitKey(1)

        cv2.destroyAllWindows()
    
    def boxCount(self, boxes):
        """
            Determines the presence of the intersection depending on the number of boxes
                found by the contour finder.
            @   Boxes   |   Number of boxes found on the image

            Returns @interc |   Boolean that states if there is an intersection
        
        """
        #   If there are boxes, then there is intersection
        interc = None
        if(boxes >= 5):
            interc = True
        else:
            interc = False
        #   Return veredict
        return interc
        


    def resizeImage(self, img):
        """
            Changes the size of the image into a workable size for the intersection detection,
                deleting unnecessary information.
            @   img |   Opencv video capture
        
        """
        #   Sets new dimention
        dim = (self.width, self.height)

        #   Scaled image
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        print("New:", self.img.shape)
        #   Resized image to limit our vision
        img = img[230:360, 30:450]
        #   Returns new image
        return img


    def tresholding(self, img):
        """
            Applies a tresh binary into the image and returns a threshold to highlight 
                the contours.
            @   img |   Image to be processed

            Returns @thresh with applied mask 
        
        """
        #   Converts image into grayscale and HSV
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #   Limits image into a threshold
        lower = np.array([self.hsvVals[0], self.hsvVals[1], self.hsvVals[2]])
        upper = np.array([self.hsvVals[3], self.hsvVals[4], self.hsvVals[5]])
        #   Applies treshold to image and generates a mask
        mask = cv2.inRange(hsv, lower, upper)
        cv2.imshow("Dark Mask", mask)
        #   120 to 100
        #   Gets threshold 
        ret,thresh = cv2.threshold(gray,120,255,cv2.THRESH_BINARY)
        return thresh
    
    def getContours(self, img, imgThres):
        """
            Determines the contours of the image and draws squares or rectangles depending on the
                form of the contours.
            @   img         |   Image to be processed
            @   imgThres    |   Image with applied mask

            Returns @image_copy with drawn squares and rectangle and @len(afig) with the number of generated boxes.
        
        """
        #   Copy of original image to paste the contours
        image_copy = img.copy()

        #   Detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
        contours, hierarchy = cv2.findContours(image=imgThres, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        print("Number of contours detected:", len(contours))
        #   If there are contours, draws a square or rectangle and adds to list
        if len(contours) != 0:
            #   Gets the maximum of contours and bounding rectangles from this maximum
            biggest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(biggest)
            #   List that counts how many figures are in image
            afig = []
            #   Iterates in contours for figure prediction
            for cnt in contours:
                x1,y1 = cnt[0][0]
                #   Calculates polygons
                approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(cnt)
                    ratio = float(w)/h
                    #   Adding contour if is of size 4
                    afig.append(cnt)
                    if ratio >= 0.9 and ratio <= 1.1:
                        image_copy = cv2.drawContours(image_copy, [cnt], -1, (0,255,255), 3)
                        cv2.putText(image_copy, 'Square', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                    else:
                        cv2.putText(image_copy, 'Rectangle', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        image_copy = cv2.drawContours(image_copy, [cnt], -1, (0,255,0), 3)
            print(len(afig))
            #   Draws contours into image
            cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        #   Return image and figure size
        return image_copy, len(afig)


    def callback(self, msg):
        """
            ROS Callback for image
        
        """
        try:
            #   Gets image from topic and flips it
            self.cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.cv_image=cv2.flip(self.cv_image,0)
            self.cv_image=cv2.flip(self.cv_image,1)
            #   Resize processing space
            self.img = cv2.resize(self.cv_image, (self.width, self.height), interpolation = cv2.INTER_AREA)
            #self.img = self.img[230:360, 30:450]
            #   Gets threshold and contours
            self.imgThres = self.tresholding(self.img)
            self.imgCon, self.boxes = self.getContours(self.imgThres)
            #   Determines if there is an intersection on the road
            self.isIntersection = self.boxCount(self)
            #   Publishes topic of intersection
            self.publisher(self.isIntersection)
        except CvBridgeError as e:
            rospy.logerr(e)



if __name__ == '__main__':
    interceramic = Intersection()
    interceramic.main()
    rospy.spin()
