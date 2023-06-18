#!/usr/bin/env python3.8

#
#Code developed by: Team EHorchatas
#Date: 18/06/2023


#Libraries Definition
import sys
import cv2
import imutils
import numpy as np
from yoloDet import YoloTRT



# Use the path for library and engine file to model
class YOLO:
	def __init__(self):
		# Charge the model
		self.model = YoloTRT(library="libmyplugins.so", engine="traffic_pp.engine", conf=0.5, yolo_ver="v5")
		self.classes = []
		#self.color_tone = [(0, 255, 0), (0, 0, 255), (0, 255, 255)]

	def detect(self,frame):
		# Charge the frame and use the model
		detections, t = self.model.Inference(frame)
		for obj in detections:
			clase = obj['class']
			bbox = obj['box']
			conf = obj['conf']
			data = ""

			if clase == "Semaforo":
				# Call the semaphore class
				cropped_image = frame[bbox.y+bbox.h, bbox.x+bbox.w]
				data = self.semaforo(cropped_image)

			elif clase == "Right" or clase == "left":
				#Call the turn signal direction class
				cropped_image = frame[bbox.y+bbox.h, bbox.x+bbox.w]
				data = self.signals(cropped_image)

			elif clase == "contruction":
				# Call the construction sign class to slow down
				data = "Slow"

			elif clase == "red" or clase == "Stop":
				# Call the stop sign class or red color detection
				data = "stop"
			else:
				data = clase
			self.classes.append(data)
		return self.classes

	#Function to confirm the turn direction signal
	def signals(self, image):
		lower_blue=np.array([69,55,105])
		upper_blue=np.array([90,255,255])
		image_blue=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
		blue_mask=cv2.inRange(image_blue, lower_blue,upper_blue)
		h,w=blue_mask.shape
		half=w//2
		left=blue_mask[:,:half]
		right=blue_mask[:,half:]
		number_of_blue_left_pix = np.sum(left == 255)   
		number_of_blue_right_pix = np.sum(right == 255)
		if number_of_blue_left_pix>number_of_blue_right_pix:
			flag="Left"
		elif number_of_blue_left_pix<number_of_blue_right_pix:
			flag="Right"
		else:
			flag="none"
		return flag
	#_________________________________________SEMAPHORE COLOR DETECTION PROCESS_BEGIN
	def preprocess_image(self, img):
		kernel = np.ones((5, 5), "uint8")
		imageFrame = img.copy()
		image_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		return imageFrame, image_hsv, kernel
	
	def detect_contours(self, image_hsv, lower_range, upper_range, kernel):
		mask = cv2.inRange(image_hsv, lower_range, upper_range)
		mask = cv2.dilate(mask, kernel)
		contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		return contours
	
	def find_largest_contour(self, contours):
		largest_contour = None
		max_area = 0
		for contour in contours:
			area = cv2.contourArea(contour)
			if area > max_area:
				max_area = area
				largest_contour = contour
		return largest_contour, max_area
	
	def draw_contour(self, img, contour, color, text, x, y, w, h):
		cv2.drawContours(img, [contour], -1, color, 1)
		cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
		cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color)

	def semaforo(self, img):
		imageFrame, image_hsv, kernel = self.preprocess_image(img)
		# Detect red contours
		lower_red1 = np.array([0, 100, 20])
		upper_red1 = np.array([10, 255, 255])
		lower_red2 = np.array([160, 100, 20])
		upper_red2 = np.array([179, 255, 255])
		red_contours = self.detect_contours(image_hsv, lower_red1, upper_red1, kernel)
		red_contour, red_area = self.find_largest_contour(red_contours)
		red_contours2 = self.detect_contours(image_hsv, lower_red2, upper_red2, kernel)
		red_contour2, red_area2 = self.find_largest_contour(red_contours2)

        # Combine red contours
		if red_contour2 is not None and red_area2 > red_area:
			red_contour = red_contour2
			red_area = red_area2

        # Detect green contours
		lower_green = np.array([35, 24, 24], dtype="uint8")
		upper_green = np.array([75, 255, 255], dtype="uint8")
		green_contours = self.detect_contours(image_hsv, lower_green, upper_green, kernel)
		green_contour, green_area = self.find_largest_contour(green_contours)

        # Detect yellow contours
		lower_yellow = np.array([23, 50, 0], dtype="uint8")
		upper_yellow = np.array([65, 255, 255], dtype="uint8")
		yellow_contours = self.detect_contours(image_hsv, lower_yellow, upper_yellow, kernel)
		yellow_contour, yellow_area = self.find_largest_contour(yellow_contours)

        # Create a blank image
		blank_image = np.zeros_like(img)
		if red_contour is not None and red_area > 150:
			#color = self.color_tone[1]
			flag = "rojo"
			x, y, w, h = cv2.boundingRect(red_contour)
			#self.draw_contour(blank_image, red_contour, color, "red", x, y, w, h)
		elif green_contour is not None and green_area > 150:
			#color = self.color_tone[0]
			flag = "verde"
			x, y, w, h = cv2.boundingRect(green_contour)
			#self.draw_contour(blank_image, green_contour, color, "green", x, y, w, h)
		elif yellow_contour is not None and yellow_area > 150:
			#color = self.color_tone[2]
			flag = "amarillo"
			x, y, w, h = cv2.boundingRect(yellow_contour)
			#self.draw_contour(blank_image, yellow_contour, color, "yellow", x, y, w, h)
		else:
			flag="none_smph"
		return flag
		#_________________________________________SEMAPHORE COLOR DETECTION PROCESS_END