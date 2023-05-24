#!/usr/bin/env python3
import cv2
import rospy
from geometry_msgs.msg import Point 

rospy.init_node("tracker")

pub = rospy.Publisher("Target_pixel", Point, queue_size=1)
msg = Point()
# se declara un tracker csrt
tracker = cv2.TrackerCSRT_create()
video = cv2.VideoCapture(0)

if not video.isOpened():
    print('[ERROR] video no se pudo cargar')
# captura el primer frame
ret, frame = video.read()
if not ret:
    print('[ERROR] no se cargo el frame')
print('[INFO] video y frame cargados')

# seleccionar bounding box del objeto que se busca trackear
bbox = cv2.selectROI("select", frame)
print('[INFO] seleccionar area de interes y presiona ENTER o SPACE')
print('[INFO] cancela con C')
cv2.destroyWindow("select")
color = (0,255,0)

# se inicializa el tracker con el bounding box dado
check = tracker.init(frame, bbox)
(x, y, w, h) = [int(v) for v in bbox]

# se guarda los valores de sus pixeles centrales
(lastPixelu, lastPixelv) = ((x + (x+w))/2, (y + (y+h))/2)
msg.x = lastPixelu
msg.y = lastPixelv

while not rospy.is_shutdown():
    # por cada frame
    ret, frame = video.read()
    if not ret:
        break

    # actualizar el tracker
    check, bbox = tracker.update(frame)

    # si se encontro el objeto
    if check == True:

        # obtener su posicion en la imagen
        (x, y, w, h) = [int(v) for v in bbox]
        (u, v) = ((x + (x+w))/2, (y + (y+h))/2)

        msg.x = u
        msg.y = v

        # se dibuja la posicion actual del objeto
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
        cv2.putText(frame, "csrt", (10, 30), cv2.QT_FONT_NORMAL, 1, (0, 255, 0))
    else:
        # si se perdio el objeto
        print("Lost Tracking")

        # se redeclara el tracker
        tracker = cv2.TrackerCSRT_create()

        # se le pide al usuario redefinir el objeto que se busca trackear
        bbox = cv2.selectROI("select", frame)
        check = tracker.init(frame, bbox)
        cv2.destroyWindow("select")
        
    pub.publish(msg)

    cv2.imshow("Tracking", frame)
    cv2.waitKey(1)
