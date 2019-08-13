import cv2
import time
from pyzbar import pyzbar
import numpy as np

cv2.namedWindow( "color" )
cv2.namedWindow( "size" )


if __name__ == '__main__':
    def nothing(*arg):
        pass

def cv_size(img):
	return tuple(img.shape[1::-1])

sm=0         
dpi=4.655     #Размер QR кода в сантиметрах

cap = cv2.VideoCapture(1)


cv2.createTrackbar('h1', 'color', 0, 255, nothing)
cv2.createTrackbar('s1', 'color', 0, 255, nothing)
cv2.createTrackbar('v1', 'color', 0, 255, nothing)
cv2.createTrackbar('h2', 'color', 255, 255, nothing)
cv2.createTrackbar('s2', 'color', 255, 255, nothing)
cv2.createTrackbar('v2', 'color', 255, 255, nothing)
cv2.createTrackbar('noise', 'size', 0, 100, nothing)

cv2.createTrackbar('min_height', 'size', 0, 500, nothing)
cv2.createTrackbar('min_width', 'size', 0, 500, nothing)

cv2.createTrackbar('max_height', 'size', 0, 500, nothing)
cv2.createTrackbar('max_width', 'size', 0, 500, nothing)

crange = [0,0,0, 0,0,0]

while True:
	frame, img = cap.read()
	# преобразуем RGB картинку в HSV модель
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
	
	h1 = cv2.getTrackbarPos('h1', 'color')
	s1 = cv2.getTrackbarPos('s1', 'color')
	v1 = cv2.getTrackbarPos('v1', 'color')
	h2 = cv2.getTrackbarPos('h2', 'color')
	s2 = cv2.getTrackbarPos('s2', 'color')
	v2 = cv2.getTrackbarPos('v2', 'color')
	noise = cv2.getTrackbarPos('noise', 'size')
	min_height = cv2.getTrackbarPos('min_height', 'size')
	min_width = cv2.getTrackbarPos('min_width', 'size')
	max_height = cv2.getTrackbarPos('max_height', 'size')
	max_width = cv2.getTrackbarPos('max_width', 'size')
	# применяем цветовой фильтр
	thresh = cv2.inRange(hsv, (h1, s1, v1), (h2, s2, v2))
	moments = cv2.moments(thresh, 1)
	for barcode in pyzbar.decode(img): # ищем QR-коды на кадре:
		x, y, w, h = barcode.rect # координаты и размеры QR-кода
		cx, cy = x + w // 2, y + h // 2 # координаты его центра
		data = barcode.data.decode('utf-8') # данные QR-кода
		
		if data == "1":
			sm=dpi/w
		print(data)
		print(sm*dpi)
		print(sm*w)
		# граффика
		cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
		cv2.putText(img, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	
	h_min = np.array((h1, s1, v1), np.uint8)
	h_max = np.array((h2, s2, v2), np.uint8)

	contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	
	for cnt in contours:
		x1, y1, w1, h1 = cv2.boundingRect(cnt)
		Areab = cv2.contourArea(cnt)
		X2=x1 + w1
		Y2=y1 + h1
		if Areab > noise:
			print(w1, h1, min_width, max_width, min_height, max_height)
			if min_width <= w1 <= max_width and min_height <= h1 <= max_height:
				cv2.rectangle (img, (x1, y1), (X2, Y2), (0,255,0), 2)
				print("!\n"*10)
			print(sm*w1) #a
		if cv2.waitKey(10) & 0xFF == ord('q'):
			quit()
	cv2.imshow('result', img)
	cv2.imshow('trash', thresh)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		quit()

cap.release()
cv2.destroyAllWindows()