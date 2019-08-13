import cv2
import time
from pyzbar import pyzbar

cap = cv2.VideoCapture(0)
frame = cap.read()
try:
    frame_sizeX=frame.cv2.CAP_PROP_FRAME_HEIGHT   #Получение высоты кадра
    frame_sizeY=frame.cv2.CAP_PROP_FRAME_WIDTH    #Получение широты кадра
except:
    print("ERROR: cant get size of cam")
QR_size=15 # размер QR-кода в сантиметрах
QRs=False

QR1=False
QR2=False
QR3=False
QR4=False


while True:
    frame, img = cap.read()
    while QRs != True:
        for barcode in pyzbar.decode(img): # ищем QR-коды на кадре:
            x, y, w, h = barcode.rect # координаты и размеры QR-кода
            cx, cy = x + w // 2, y + h // 2 # координаты его центра
            data = barcode.data.decode('utf-8') # данные QR-кода
            print(data)
            # граффика
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            try:
                for i in int(data):

                    if QR1 and QR2 and QR3 and QR4 == True: QRs=True
            except:
                print("not all")


    cv2.imshow('result', img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()