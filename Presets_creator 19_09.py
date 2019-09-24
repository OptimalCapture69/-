import cv2
from pyzbar import pyzbar
import numpy as np
import math
from tkinter import *
from tkinter import filedialog as fd
import requests

#Создание окон
wind1 = "c" 
wind2 = "s"
cv2.namedWindow(wind1)
cv2.namedWindow(wind2)

if __name__ == '__main__':
	def nothing(*arg):
		pass

def quita(self):
    self.root.destroy()

cap = cv2.VideoCapture(0)

sm = 0.19811320754716982  # qr/pix

#Создание ползунков
cv2.createTrackbar('h1', wind1, 0, 255, nothing)
cv2.createTrackbar('s1', wind1, 0, 255, nothing)
cv2.createTrackbar('v1', wind1, 0, 255, nothing)
cv2.createTrackbar('h2', wind1, 0, 255, nothing)
cv2.createTrackbar('s2', wind1, 0, 255, nothing)
cv2.createTrackbar('v2', wind1, 0, 255, nothing)

cv2.createTrackbar('noise', wind2, 0, 250, nothing)

cv2.createTrackbar('min_height', wind2, 0, 480, nothing)
cv2.createTrackbar('min_width', wind2, 0, 640, nothing)

cv2.createTrackbar('max_height', wind2, 0, 480, nothing)
cv2.createTrackbar('max_width', wind2, 0, 640, nothing)
cv2.createTrackbar('Zone', wind2, 0, 8, nothing)

cv2.createTrackbar('vac', wind2, 0, 1, nothing)
crange = [0, 0, 0, 0, 0, 0]

while True:
	frame, img = cap.read()
	# преобразуем RGB картинку в HSV модель
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	cv2.circle(img, (0, 0), 3, (255, 0, 255), -1)

	#Считывание положения ползунков
	h1 = cv2.getTrackbarPos('h1', wind1)
	s1 = cv2.getTrackbarPos('s1', wind1)
	v1 = cv2.getTrackbarPos('v1', wind1)
	h2 = cv2.getTrackbarPos('h2', wind1)
	s2 = cv2.getTrackbarPos('s2', wind1)
	v2 = cv2.getTrackbarPos('v2', wind1)
	v2 = cv2.getTrackbarPos('v2', wind1)

	noise = cv2.getTrackbarPos('noise', wind2)

	min_height = cv2.getTrackbarPos('min_height', wind2)
	min_width = cv2.getTrackbarPos('min_width', wind2)

	max_height = cv2.getTrackbarPos('max_height', wind2)
	max_width = cv2.getTrackbarPos('max_width', wind2)
	zone = cv2.getTrackbarPos('Zone', wind2)
	vac = cv2.getTrackbarPos('vac', wind2)


	if cv2.waitKey(5) & 0xFF == ord('q'):						#выход
		quit()
	if cv2.waitKey(5) & 0xFF == ord('s'):						#сохранение пресета
		root = Tk()
		file_name = fd.asksaveasfilename(filetypes=(("Python file", "*.py"),
													("All files", "*.*")))+".py"
		root.destroy()
		try:
			f = open(file_name, 'w', encoding='utf8')
			s = """
sm=%s         #qr/pix

h1 = %s
s1 = %s
v1 = %s

h2 = %s
s2 = %s
v2 = %s

noise = %s

min_height = %s
min_width = %s

max_height = %s
max_width = %s

zone=%s
vac=%s
""" % (sm, h1, s1, v1, h2, s2, v2, noise, min_height, min_width, max_height, max_width, zone, vac)
			f.write(s)
			f.close()

		except:
			pass
	if cv2.waitKey(5) & 0xFF == ord("o"):			#загрузка пресета
		root = Tk()
		file_name = fd.askopenfilename(filetypes=(("Python file", "*.py"),
													("All files", "*.*")))
		root.destroy()
		try:
			f = open(file_name, 'r')
			f = f.read()
			exec(f)
			cv2.setTrackbarPos('h1', wind1, h1)
			cv2.setTrackbarPos('s1', wind1, s1)
			cv2.setTrackbarPos('v1', wind1, v1)
			cv2.setTrackbarPos('h2', wind1, h2)
			cv2.setTrackbarPos('s2', wind1, s2)
			cv2.setTrackbarPos('v2', wind1, v2)

			cv2.setTrackbarPos('noise', wind2, noise)
			cv2.setTrackbarPos('min_width', wind2, min_width)
			cv2.setTrackbarPos('max_width', wind2, max_width)
			cv2.setTrackbarPos('min_width', wind2, min_height)
			cv2.setTrackbarPos('max_width', wind2, max_height)
			cv2.setTrackbarPos('vac', wind2, vac)
		except:
			pass
	
	# применяем цветовой фильтр
	thresh = cv2.inRange(hsv, (h1, s1, v1), (h2, s2, v2))

	h_min = np.array((h1, s1, v1), np.uint8)
	h_max = np.array((h2, s2, v2), np.uint8)

	contours, hierarchy = cv2.findContours(
		thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # Нахождение контуров

	for cnt in contours:
		x1, y1, w1, h1 = cv2.boundingRect(cnt)  # получение первых точек
		Areab = cv2.contourArea(cnt)

		X2 = x1 + w1  # Получение 2-ой х
		Y2 = y1 + h1  # Получение 2-ой у

		if Areab > noise:  # Отсеевание шумов

			if min_width <= w1 <= max_width and min_height <= h1 <= max_height:  # сравнивание размеров
				# нахождение центра объекта
				cX, cY = int((x1+X2)/2), int((y1+Y2)/2)

				rect = cv2.minAreaRect(cnt)  # пытаемся вписать прямоугольник
				# поиск четырех вершин прямоугольника
				box = cv2.boxPoints(rect)
				box = np.int0(box)  # округление координат
				areac = int(rect[1][0] * rect[1][1])

				# вычисление координат двух векторов, являющихся сторонам прямоугольника
				edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
				edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

				# выясняем какой вектор больше
				usedEdge = edge1
				if cv2.norm(edge2) > cv2.norm(edge1):
					usedEdge = edge2
				reference = (1, 0)  # горизонтальный вектор, задающий горизонт
				
				if cX < 320:    # Если объект правее центра, то...
					rX = (320-(640-cX))*sm*10
				elif cX >= 320:
					rX = (cX-320)*sm*10
				y = rX  #перевод из пикселей в сантиметры
				x = cY*sm*10
				
				# вычисляем угол между самой длинной стороной прямоугольника и горизонтом
				angle = 180.0 / math.pi * \
					math.acos((reference[0] * usedEdge[0] + reference[1] *
							   usedEdge[1]) / (cv2.norm(reference) * cv2.norm(usedEdge)))

				#Графика
				cv2.putText(img, "%d" % int(angle), (cX, cY),
							cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
				cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
				cv2.circle(img, (cX, cY), 3, (255, 0, 255), -1)
				cv2.rectangle(img, (x1, y1), (X2, Y2), (0, 255, 0), 2)

				print("x=", x, 'Y=', y)

	cv2.imshow('result', img)
	cv2.imshow('BozhePomogiMne', thresh)


cap.release()
cv2.destroyAllWindows()
