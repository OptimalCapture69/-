import cv2
import time

from pyzbar import pyzbar

import numpy as np
import math
from os import chdir

#from robodk import*
#from robolink import*

import requests

import time

start_time = time.time()

print("import: --- %s seconds ---" % (time.time() - start_time))

#RDK = Robolink()
#robot = RDK.Item("KUKA KR 3 R540")
#target = RDK.Item("Target 1")

chdir("C:\\Save")
notLoaded = True
while notLoaded:
    get=requests.get("http://localhost:5000").text
    print(get)
    print("open url: --- %s seconds ---" % (time.time() - start_time))
    try:
        presset=open(get+".py").read()
        print(presset)
        exec(presset)
        notLoaded=False
    except:
        print("File not found! Try")

print("[fin] open url: --- %s seconds ---" % (time.time() - start_time))

rX, cY, z, angle = 400, 0, 300, 0

if __name__ == '__main__':
	def nothing(*arg):
		pass

def cv_size(img):
	return tuple(img.shape[1::-1])

sm=0.19811320754716982     #pix/sm

cap = cv2.VideoCapture(0)

crange = [0,0,0, 0,0,0]

while True:
	frame, img = cap.read()
	# преобразуем RGB картинку в HSV модель
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )



	# применяем цветовой фильтр
	thresh = cv2.inRange(hsv, (h1, s1, v1), (h2, s2, v2))
	moments = cv2.moments(thresh, 1)

	h_min = np.array((h1, s1, v1), np.uint8)
	h_max = np.array((h2, s2, v2), np.uint8)

	contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #Нахождение контуров
	
	for cnt in contours:
		
		x1, y1, w1, h1 = cv2.boundingRect(cnt) #получение первых точек
		Areab = cv2.contourArea(cnt)

		X2=x1 + w1	#Получение 2-ой х
		Y2=y1 + h1	#Получение 2-ой у

		if Areab > noise: #Отсеевание шумов
		
			if min_width <= w1 <= max_width and min_height <= h1 <= max_height: #сравнивание размеров
				cX, cY = int((x1+X2)/2), int((y1+Y2)/2) #нахождение центра объекта
				
				#Смещение координатной плоскости 
				if cX < 320:
					rX=(320-(640-cX))*sm*10
				elif cX >= 320:
					rX=(cX-320)*sm*10

				rect = cv2.minAreaRect(cnt) # пытаемся вписать прямоугольник
				box = cv2.boxPoints(rect) # поиск четырех вершин прямоугольника
				box = np.int0(box) # округление координат
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
				angle = 180.0 / math.pi * math.acos((reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv2.norm(reference) * cv2.norm(usedEdge)))

				x=cY*sm*10
				y=rX

				print('y=',y, 'x=',x)

#				x *= -1
#				z *= -1

#				approach = target.Pose()*transl(x,y,z)
#				robot.MoveJ(approach)
#				quit()

	cv2.imshow('result', img)
	cv2.imshow('BozhePomogiMne', thresh)

	if cv2.waitKey(10) & 0xFF == ord('q'):
		quit()

cap.release()
cv2.destroyAllWindows()