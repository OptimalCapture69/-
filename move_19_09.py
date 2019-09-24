import cv2
import time

from pyzbar import pyzbar

import numpy as np
import math
from os import chdir

# from robodk import*
# from robolink import*

import requests

def vacuum(v):
	requests.get("http://localhost:5002/user/"+v)

start_time = time.time()

print("[o] import: --- %s seconds ---" % (time.time() - start_time))

# RDK = Robolink()
# robot = RDK.Item("KUKA KR 3 R540")
# target = RDK.Item("Target 1")

chdir("C:\\Save")  # перемещение в папку с надстройками
notLoaded = True
while notLoaded:  # Пытаемся получить информацию с Android-приложения
	try:
		get = requests.get("http://localhost:5000").text

		print(get)

		presset = open(get+".py").read()

		print("======SETTINGS======")
		exec(presset)
		print("====================")

		notLoaded = False
	except:
		print("[!] File not found! Get request again...")

rX, cY, z, angle = 400, 0, 300, 0

if __name__ == '__main__':
	def nothing(*arg):
		pass


def cv_size(img):
	return tuple(img.shape[1::-1])


sm = 0.19811320754716982  # pix/sm

cap = cv2.VideoCapture(0)

crange = [0, 0, 0, 0, 0, 0]

while True:
	frame, img = cap.read()
	# преобразуем RGB картинку в HSV модель
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# применяем цветовой фильтр
	thresh = cv2.inRange(hsv, (h1, s1, v1), (h2, s2, v2))
	moments = cv2.moments(thresh, 1)

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
				cX, cY = int((x1+X2)/2), int((y1+Y2)/2)  # нахождение центра объекта

				# Смещение начала координатны X в центер изображения
				if cX < 320:
					rX = (320-(640-cX))*sm*10
				elif cX >= 320:
					rX = (cX-320)*sm*10

				rect = cv2.minAreaRect(cnt)  # пытаемся вписать прямоугольник
				box = cv2.boxPoints(rect)  # поиск четырех вершин прямоугольника
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

				# вычисляем угол между самой длинной стороной прямоугольника и горизонтом
				angle = 180.0 / math.pi * \
					math.acos((reference[0] * usedEdge[0] + reference[1] *
							  usedEdge[1]) / (cv2.norm(reference) * cv2.norm(usedEdge)))

				# X=Y, Y=X из-за того, что в RoboDK пространство повернуто на 90*
				x = cY*sm*10  # Перевод из пикселей в СМ, а затем в ММ
				y = rX
				notLoaded = True
				
				while notLoaded:  # Пытаемся получить информацию с Android-приложения
					try:
						z = requests.get("http://localhost:5001").text
						notLoaded=False
					except:
						print("[!] File not found! Get request again...")

				print('[·]', 'y=', y, 'x=', x, 'z=', z)

				# !---НАЧАЛО УПРАВЛЕНИЯ КУКОЙ---!

				

				#TODO: Вставить координаты точек сброса объектов
				if zone==1:	#Место для: Стеклянной бутылки
					
					vacuum(0)
				elif zone==2: #Пластиквой бутылки

					vacuum(0)
				elif zone==3: #Мягкой игрушки
					
					vacuum(0)
				elif zone==4: #Банки

					vacuum(0)
				elif zone==5: #Пакета

					vacuum(0)
				elif zone==6: #Денегб

					vacuum(0)
				elif zone==7: #Бандероли

					vacuum(0)
				elif zone==8: #Банана
					
					vacuum(0)
				
				quit()

	cv2.imshow('result', img)
	cv2.imshow('BozhePomogiMne', thresh)

cap.release()
cv2.destroyAllWindows()
