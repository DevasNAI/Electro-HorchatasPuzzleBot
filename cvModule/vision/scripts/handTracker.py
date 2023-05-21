#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Point
import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

cap = cv2.VideoCapture(0)
print(cap.isOpened())
bridge = CvBridge()

class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils # it gives small dots onhands total 20 landmark points


    def handsFinder(self,image,draw=True):
        imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def positionFinder(self, image, handNo=0, result=Point()):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id,cx,cy])
            label = MessageToDict(self.results.multi_handedness[handNo])['classification'][0]['label']
        
            if label == "Right":
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

                result.x = cx/640 * 6.5
                result.y = cy/480 * 3
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
                cv2.circle(image,(cx,cy), 15 , (255,0,255), cv2.FILLED)

                #regla de 3 simple para position
                result.z = cy/480 * 3
                return result
            else:
                return Point()

def main():
    pub = rospy.Publisher('/handTracker', Image, queue_size = 1)
    position = rospy.Publisher('/position', Point, queue_size = 1)
    rospy.init_node('image', anonymous = False)
    rate = rospy.Rate(10)
    detector = handTracker()
    position_msg = Point()

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if not ret:
            break
        frame = detector.handsFinder(frame)
        if detector.results.multi_hand_landmarks:
            position_msg = detector.positionFinder(frame, 0, position_msg)

            if len(detector.results.multi_handedness) == 2:
                position_msg = detector.positionFinder(frame, 1, position_msg)

            position.publish(position_msg)
        msg = bridge.cv2_to_imgmsg(frame, 'bgr8')
        pub.publish(msg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
