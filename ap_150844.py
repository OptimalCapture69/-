import cv2

if __name__ == '__main__':
    def nothing(*arg):
        pass

cv2.namedWindow( "size" )

cv2.createTrackbar('min_height', 'size', 0, 500, nothing)
cv2.createTrackbar('min_width', 'size', 0, 500, nothing)

cv2.createTrackbar('max_height', 'size', 0, 500, nothing)

while 1:
	min_height = cv2.getTrackbarPos('min_height', 'size')
	min_width = cv2.getTrackbarPos('min_width', 'size')
	
	max_height = cv2.getTrackbarPos('max_height', 'size')
	max_width = cv2.getTrackbarPos('max_width', 'size')
	w1, h1 = 100, 200
	if min_width <= w1 <= max_width and min_height <= h1 <= max_height:
		print(True)