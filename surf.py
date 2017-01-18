import cv2 
from matplotlib import pyplot as plt
img =cv2.imread('dg.jpg',0)
# img=cv2.SURF(400)
surf= cv2.xfeatures2d.SURF_create()
kp1,des1= surf.detectAndCompute(img,None)
img2 = cv2.drawKeypoints(img,kp1,None,(255,0,0),4)
plt.imshow(img2),plt.show()

# surf= cv2.xfeatures2d.SURF_create()
# surf.setHessianThreshold
# upright not working
# print surf.descriptorSize()