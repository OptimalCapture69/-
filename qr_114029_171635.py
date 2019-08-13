import cv2
import time
from pyzbar import pyzbar
import numpy as np

cv2.namedWindow( "settings" )

if __name__ == '__main__':
    def nothing(*arg):
        pass

def cv_size(img):
	return tuple(img.shape[1::-1])

sm=0         
dpi=4.655     #Размер QR кода в сантиметрах

cap = cv2.VideoCapture(1)


cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
cv2.createTrackbar('noise', 'settings', 0, 100, nothing)

cv2.createTrackbar('min_height', 'settings', 0, 100, nothing)
cv2.createTrackbar('min_width', 'settings', 0, 100, nothing)

cv2.createTrackbar('max_height', 'settings', 0, 100, nothing)
cv2.createTrackbar('max_width', 'settings', 0, 100, nothing)

crange = [0,0,0, 0,0,0]

while True:
	frame, img = cap.read()
	# преобразуем RGB картинку в HSV модель
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
	
	h1 = cv2.getTrackbarPos('h1', 'settings')
	s1 = cv2.getTrackbarPos('s1', 'settings')
	v1 = cv2.getTrackbarPos('v1', 'settings')
	h2 = cv2.getTrackbarPos('h2', 'settings')
	s2 = cv2.getTrackbarPos('s2', 'settings')
	v2 = cv2.getTrackbarPos('v2', 'settings')
	noise = cv2.getTrackbarPos('noise', 'settings')
	min_height = cv2.getTrackbarPos('min_height', 'settings')
	min_width = cv2.getTrackbarPos('min_width', 'settings')
	max_height = cv2.getTrackbarPos('max_height', 'settings')
	max_width = cv2.getTrackbarPos('max_width', 'settings')
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
		HOfObj=x1 + w1
		WOfObj=y1 + h1
		if Areab > noise:
			if HOfObj > height and WOfObj > width
			cv2.rectangle (img, (x1, y1), (HOfObj, WOfObj), (0,255,0), 2)
			print(sm*w1)

	cv2.imshow('result', img)
	cv2.imshow('hsv', hsv)
	cv2.imshow('trash', thresh)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		quit()

cap.release()
cv2.destroyAllWindows()