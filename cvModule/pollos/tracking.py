import cv2
import csv

data = []
positions = []

# Abrir el csv con los valores de lado en pixeles por cada frame y almacenar en una lista
with open("lado.csv") as file:
    csv_reader = csv.reader(file, delimiter=' ')
    lineCount = 0

    for row in csv_reader:
        data.append(float(row[0]))
        lineCount += 1

# se declara un tracker csrt
tracker = cv2.legacy.TrackerCSRT_create()
video = cv2.VideoCapture('/home/jorge/Documents/Vision/pollo.mp4')
index = 0

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

# se declara que inicia en 0,0 
posx = 0
posy = 0
positions.append([posx,posy])

# indice para indicar en que frame vamos
index += 1


while True:
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

        # obtener desplazamiento en pixeles
        (dpx, dpy) = (u - lastPixelu , v - lastPixelv)

        # conversion a metros
        dx = dpx * 30 / (data[index] * 1000)
        dy = dpy * 30 / (data[index] * 1000)

        # se le suma a la posicion anterior para obtener posicion actual
        posx += dx
        posy += dy

        # se dibuja la posicion actual del objeto
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
        cv2.putText(frame, "csrt", (10, 30), cv2.QT_FONT_NORMAL, 1, (0, 255, 0))
    else:
        # si se perdio el objeto
        print("Lost Tracking")

        # se redeclara el tracker
        tracker = cv2.legacy.TrackerCSRT_create()

        # se le pide al usuario redefinir el objeto que se busca trackear
        bbox = cv2.selectROI("select", frame)
        check = tracker.init(frame, bbox)
        cv2.destroyWindow("select")
    
    # se guarda la posicion actual
    positions.append([posx,posy])
    index += 1

    cv2.imshow("Tracking", frame)
    cv2.waitKey(1)

print(positions)

# se guardan las posiciones en cada frame en un csv 
with open("positions.csv", 'w') as f:
    header = ['X','Y']
    write = csv.writer(f)
    write.writerow(header)
    write.writerows(positions)