#!/usr/bin/env python3

import cv2
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '/home/chelis/Downloads/xArm-Python-SDK/example/wrapper/common/9000-set_linear_track.py'))
from xarm.wrapper import XArmAPI
arm = XArmAPI('192.168.1.203')
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)
time.sleep(1)

x_min = 409
x_max = 165


y_min = -195
y_max = 137

z_min = 350
z_max = 174

deltaX = x_max - x_min
deltaY = y_max - y_min
deltaZ = z_max - z_min
Z = 174

video = cv2.VideoCapture(4)
videoCam = cv2.VideoCapture(2)


# se declara un tracker csrt
trackerX = cv2.legacy.TrackerCSRT_create()
trackerY = cv2.legacy.TrackerCSRT_create()

ret1, frame1 = video.read()
ret2, frame2 = videoCam.read()

height1, width1, _ = frame1.shape
height2, width2, _ = frame2.shape 

# seleccionar bounding box del objeto que se busca trackear
bboxX = cv2.selectROI("select objX", frame1)
print('[INFO] seleccionar area de interes y presiona ENTER o SPACE')
print('[INFO] cancela con C')
cv2.destroyWindow("select objX")

bboxY = cv2.selectROI("select objY", frame2)
print('[INFO] seleccionar area de interes y presiona ENTER o SPACE')
print('[INFO] cancela con C')
cv2.destroyWindow("select objY")

# se inicializa el tracker con el bounding box dado
check = trackerX.init(frame1, bboxX)
checkObj = trackerY.init(frame2, bboxY)

while video.isOpened() and videoCam.isOpened():
    ret1, frame1 = video.read()
    ret2, frame2 = videoCam.read()

    if not ret1 or not ret2:
            break
    # actualizar el tracker
    check, bboxX = trackerX.update(frame1)
    checkObj, bboxY = trackerY.update(frame2)

    # si se encontro el objeto
    if check and checkObj:

        # obtener su posicion en la imagen
        (x, y, w, h) = [int(v) for v in bboxX]
        (uX, vX) = ((x + (x+w))/2, (y + (y+h))/2)
        color = (0,255,0)

        # se dibuja la posicion actual del objeto
        cv2.rectangle(frame1, (x, y), (x+w, y+h), color, 3)

        # obtener su posicion en la imagen
        (x, y, w, h) = [int(v) for v in bboxY]
        (uY, vY) = ((x + (x+w))/2, (y + (y+h))/2)
        
        XX = (uX/width1*deltaX) + x_min
        YY = (uY/width2*deltaY) + y_min
        ZZ = (vY/height1*deltaZ) + z_min - 20
        point = ((uX/width1*deltaX) + x_min, (uY/width2*deltaY) + y_min, Z)

        print(point)
        arm.set_position(x=XX, y=YY, z=ZZ, roll=-180, pitch=0, yaw=0, speed=20, is_radian=False, wait=True)

        color = (255,0,0)
        # se dibuja la posicion actual del objeto
        cv2.rectangle(frame2, (x, y), (x+w, y+h), color, 3)

        cv2.putText(frame1, "csrt", (10, 30), cv2.QT_FONT_NORMAL, 1, (0, 255, 0))
        cv2.putText(frame2, "csrt", (10, 30), cv2.QT_FONT_NORMAL, 1, (0, 255, 0))


    else:
        # si se perdio el objeto
        print("Lost Tracking")

        # se redeclara el tracker
        trackerX = cv2.legacy.TrackerCSRT_create()
        trackerY = cv2.legacy.TrackerCSRT_create()

        # se le pide al usuario redefinir el objeto que se busca trackear
        bboxX = cv2.selectROI("select objX", frame1)
        check = trackerX.init(frame1, bboxX)
        cv2.destroyWindow("select objX")

        bboxY = cv2.selectROI("select objY", frame2)
        check = trackerY.init(frame2, bboxY)
        cv2.destroyWindow("select objY")
    
    # se guarda la posicion actual
    cv2.imshow("TrackingX", frame1)
    cv2.imshow("TrackingY", frame2)
    cv2.waitKey(1)
