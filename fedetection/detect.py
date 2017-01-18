import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('/home/v_g/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/v_g/opencv/data/haarcascades/haarcascade_eye.xml')

# face_cascade = cv2.CascadeClassifier('/home/ubuntu/opencv-2.4.13/data/haarcascades/haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('/home/ubuntu/opencv-2.4.13/data/haarcascades/haarcascade_eye.xml')

img = cv2.imread('mod.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)


for (x,y,w,h) in faces:
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	roi_gray = gray[y:y+h, x:x+w]
	roi_color = img[y:y+h, x:x+w]
	eyes = eye_cascade.detectMultiScale(roi_gray)
	for (ex,ey,ew,eh) in eyes:
		cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

print len(faces)
# cv2.imwrite("detected2.jpg",img)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()