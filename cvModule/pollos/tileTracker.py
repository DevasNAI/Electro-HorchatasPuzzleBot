#!/usr/bin/python3
import cv2
import numpy as np
import csv

# funcion para calcular distancia entre los puntos
dist = lambda pt1, pt2: ((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)**0.5

video = cv2.VideoCapture("/home/jorge/Documents/Vision/pollo.mp4")
ladoCuadrado = []

while video.isOpened():
    # por cada frame
    ret, img = video.read()
    if ret:
        # se filtra la imagen
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        th, threshed = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # se obtienen los contornos de la imagen
        cnts = cv2.findContours(threshed,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

        # variables para limitar la cantidad de recuadros que detecta en el piso
        H,W = img.shape[:2]
        AREA = H*W
        xcnts = []
        R = 0.8

        # por cada contorno
        for cnt in cnts:
            # obtener su area y checar que no sea muy grande
            area = cv2.contourArea(cnt)
            if(area<AREA/100):
                continue

            # calcular el perimetro del contorno
            arclen = cv2.arcLength(cnt, closed=True)
            approx = cv2.approxPolyDP(cnt, arclen*0.02, closed=True)
            
            # si la distancia entre los 4 puntos es similar, marcar como cuadro del piso
            pts = np.array(approx).reshape(-1,2)
            if len(pts) == 4:
                lens = np.array(list(dist(pts[i], pts[(i+1)%4]) for i in range(4)))
                flag = True
                for x in lens:
                    if not (R< x/lens[0] < 1.0/R):
                        flag = False
                        continue
                if flag:
                    xcnts.append(cnt)

        # guardar resultados
        res = img.copy()

        # si detecto recuadros en el piso, obtener el valor de un lado, si no detecta, guarda el del frame anterior
        if len(xcnts) > 0: 
            avg = 0
            for cnt in xcnts:
                perimeter = cv2.arcLength(cnt,True)
                avg += perimeter
                cv2.drawContours(res, [cnt], -1, (0,255,0), -1, cv2.LINE_AA)
            avg = avg/(len(xcnts)*4)
        print(avg)

        # guardar en la lista final
        ladoCuadrado.append([avg])
        cv2.imshow("contours", res)
        cv2.waitKey(1)
    else:
        break

# escribir en el csv de los valores de los lados
with open("lado.csv", 'w') as f:
    write = csv.writer(f)
    write.writerows(ladoCuadrado)

