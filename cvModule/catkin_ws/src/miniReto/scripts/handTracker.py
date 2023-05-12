#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Point
import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict


#   Gets Camera stream
cap = cv2.VideoCapture(0)
#   Confirms that the camera was opened
print(cap.isOpened())
#   Creates instance of CvBridge
bridge = CvBridge()

class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        """
            handTracker Class
                Brings hand detection tool from mediapipe Hands
            @   mode            |   Treat input images as batch of static or video stream 
            @   maxHands        |   Maximum number of hands in the model
            @   detectionCon    |   Complexity of the hand landmark model: 0 or 1. Landmark accuracy as well as inference latency generally go up with the
            model complexity.
            @   modelComplexity |   Minimum confidence value ([0.0, 1.0]) for hand detection to be considered successful.
            @   trackCon        |   Minimum confidence value ([0.0, 1.0]) for the hand landmarks to be considered tracked succesfully
        
        """
        #   https://solutions.mediapipe.dev/hands#static_image_mode
        self.mode = mode
        self.maxHands = maxHands
        #   https://solutions.mediapipe.dev/hands#model_complexity
        self.detectionCon = detectionCon
        #   https://solutions.mediapipe.dev/hands#min_detection_confidence
        self.modelComplex = modelComplexity
        #   https://solutions.mediapipe.dev/hands#min_tracking_confidence
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils # it gives small dots onhands total 21 landmark points


    def handsFinder(self,image,draw=True):
        """
            Searches for hands in a provided image

            @   image   |   Image to find hands in
            @   draw    |   Hand drawing state for hand detection
            @   returns image with the found hands
        """
        #   Changes the opencv image from BGR to RGB
        imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        #   Processes the image input with the Hands object, returns the hand landmarks and handedness of each detected hand as ndarray
        self.results = self.hands.process(imageRGB)

        #   Results have hand landmarks on each hand
        if self.results.multi_hand_landmarks:
            #   Iterating in hand landmarks
            for handLms in self.results.multi_hand_landmarks:
                #   If draw is true, the hand connections are drawn in the image
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def positionFinder(self, image, handNo=0, result=Point()):
        """
            Finds the hand's position in the image

            @   image   |   Image to find the hand's position
            @   handNo  |   Number of hands to be analyzed 
            @   result  |   Position of the hand in the image
        
        """
        #   Blank auxiliar list
        lmlist = []
        #   If there are hand landmarks in each hand...
        if self.results.multi_hand_landmarks:
            #   Assign hand landmarks to a local variable
            Hand = self.results.multi_hand_landmarks[handNo]
            #   Creates an iterator of each hand landmark and iterates in it
            for id, lm in enumerate(Hand.landmark):
                #   Gets the shape of the image in each dimention
                h,w,c = image.shape
                #   Gets the hand position in the x and y axis
                cx,cy = int(lm.x*w), int(lm.y*h)
                #   Adds the value of the position in the auxiliar list
                lmlist.append([id,cx,cy])
            #   Converts the field that contains the handdness (left or right) into a dictionary with classification and label
            label = MessageToDict(self.results.multi_handedness[handNo])['classification'][0]['label']
            #   If the dictionary label is Rght...
            if label == "Right":
                #   Sets starting point for x and y coordinates
                (cx,cy) = (0,0)

                cx += lmlist[0][1]
                cy += lmlist[0][2]
                cx += lmlist[5][1]
                cy += lmlist[5][2]
                cx += lmlist[9][1]
                cy += lmlist[9][2]
                cx += lmlist[13][1]
                cy += lmlist[13][2]
                cx += lmlist[17][1]
                cy += lmlist[17][2]
                cx = int(cx/5)
                cy = int(cy/5)
                cv2.circle(image,(cx,cy), 15 , (255,0,255), cv2.FILLED)

                #regla de 3 simple para position

                result.x = cx/640 * 5
                result.y = cy/480 * 5
                return result

            elif label == "Left":
                (cx,cy) = (0,0)

                cx += lmlist[0][1]
                cy += lmlist[0][2]
                cx += lmlist[5][1]
                cy += lmlist[5][2]
                cx += lmlist[9][1]
                cy += lmlist[9][2]
                cx += lmlist[13][1]
                cy += lmlist[13][2]
                cx += lmlist[17][1]
                cy += lmlist[17][2]
                cx = int(cx/5)
                cy = int(cy/5)
                #   Draws a magenta filled circle within the center of the hand
                cv2.circle(image,(cx,cy), 15 , (255,0,255), cv2.FILLED)

                #regla de 3 simple para position
                result.z = cy/480 * 5
                return result
            else:
                return Point()

def main():
    #   Defines publishers
    pub = rospy.Publisher('/handTracker', Image, queue_size = 1)
    position = rospy.Publisher('/position', Point, queue_size = 1)
    #   Initializes node and frequency rate
    rospy.init_node('image', anonymous = False)
    rate = rospy.Rate(10)
    #   Creates hand Tracker instance
    detector = handTracker()
    #   Creates a point message
    position_msg = Point()
    #   ROS Running
    while not rospy.is_shutdown():
        #   Gets image reading frame by frame
        ret, frame = cap.read()
        #   If frame isn't read correctly, ret is false
        if not ret:
            break
        #   Checks if frame has hands
        frame = detector.handsFinder(frame)
        #   Hand has detector landmarks detected in each hand
        if detector.results.multi_hand_landmarks:
            #   The position message is updated with the hand position
            position_msg = detector.positionFinder(frame, 0, position_msg)
            #   If the length of the detection is 2, it does the same for the other hand
            if len(detector.results.multi_handedness) == 2:
                position_msg = detector.positionFinder(frame, 1, position_msg)
            #   Publishes position message
            position.publish(position_msg)
        #   Changes cv2 image to ROS Image message
        msg = bridge.cv2_to_imgmsg(frame, 'bgr8')
        #   Publishes image message
        pub.publish(msg)
        #cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
