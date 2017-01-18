import cv2
import numpy as np

img = cv2.imread('vk.jpg')
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#extracts SIFT features from images
sift = cv2.xfeatures2d.SIFT_create()
kp = sift.detect(gray,None)

img=cv2.drawKeypoints(gray,kp,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imwrite('sift_keypoints3.jpg',img)


# client id 6yD_bZpNzBi8n0LWQZltZV8Grp8lOd5qqOaCRjFR

# client -secret pT9ZaL1dizrU6dAbNuSyPgb_4L2H1dHIXly0j0Zd

# 1HLztKpOZK8jrewj0KaYwwauMyKBqn

# result = clarifai_api.tag_images(open('/home/v_g/Desktop/trump.jpg', 'rb'))
