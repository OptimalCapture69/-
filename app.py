import cv2
import time
from pyzbar import pyzbar
import numpy as np
import math
from robodk import*
from robolink import*

RDK = Robolink()
robot = RDK.Item("KUKA KR 3 R540")


rX, cY, z, angle = 400, 0, 300, 0


if __name__ == '__main__':
	def nothing(*arg):
		pass

def cv_size(img):
	return tuple(img.shape[1::-1])

sm=0.10824742268041238         
dpi=21     #Размер QR кода в сантиметрах

cap = cv2.VideoCapture(1)


crange = [0,0,0, 0,0,0]
while True:
	frame, img = cap.read()
	# преобразуем RGB картинку в HSV модель
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
	cv2.circle(img, (0, 0), 3, (255, 0, 255), -1)
	h1 = 7
	s1 = 26
	v1 = 70
	h2 = 47
	s2 = 255
	v2 = 154
	
	noise = 250

	min_height = 218
	min_width = 141
	
	max_height = 265
	max_width = 181
	
	# применяем цветовой фильтр
	thresh = cv2.inRange(hsv, (h1, s1, v1), (h2, s2, v2))
	moments = cv2.moments(thresh, 1)  

	

	h_min = np.array((h1, s1, v1), np.uint8)
	h_max = np.array((h2, s2, v2), np.uint8)

	contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #Нахождение контуров
	
	for cnt in contours:
		
		x1, y1, w1, h1 = cv2.boundingRect(cnt) #получение первых точек
		Areab = cv2.contourArea(cnt)

		X2=x1 + w1  #Получение 2-ой х
		Y2=y1 + h1  #Получение 2-ой у

		if Areab > noise: #Отсеевание шумов
		
			if min_width <= w1 <= max_width and min_height <= h1 <= max_height: #сравнивание размеров
				cX, cY = int((x1+X2)/2), int((y1+Y2)/2) #нахождение центра объекта
				print(cX)
				
				#Смещение координатной плоскости 
				if cX < 320:    # Если объект правее центра, то...
					rX=(320-(640-cX))*sm*10
					print(rX)
					print("Right")
				elif cX >= 320:
					rX=(cX-320)*sm*10
					print(rX)
					print("Left")

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
				y=rX
				x=cY
				#x *= -1
				z = 400
				#z *= -1
				z2 = 300
				print(y,x)
				target = RDK.AddTarget("T1")
				target.setAsCartesianTarget()
				target.setJoints([0,0,0,0,0,0])
				target.setPose(KUKA_2_Pose([x,y,z,130.560,-45.890,180.000]))
				robot.MoveJ(target)
				joints = robot.Joints().list()
				print(angle)
				joints[5] = angle
				robot.MoveJ(joints)
				
				t1 = RDK.AddTarget("t1")
				tp = t1.Pose()
				tp[2,3]=z
				pause(2)
				t1.setPose(tp)
				robot.MoveJ(t1)
				pause(2)
				tp[2,3] = tp[2,3]+200
				z2 =500 
				target.setPose(KUKA_2_Pose([x,y,z2,130.560,-45.890,180.000]))
				robot.MoveJ(target)
				t1.Delete()
				target.Delete()
				quit()
	#тк в рободк не правельное пространство, для будущего удобства меняем оси
	#cv2.imshow('hSv', hsv)
	#cv2.imshow('result', img)
	#cv2.imshow('BozhePomogiMne', thresh)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		quit()
cap.release()
cv2.destroyAllWindows()
