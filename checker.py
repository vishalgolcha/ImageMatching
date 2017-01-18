from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob
import os


# im=[]
# im=glob.glob("/home/v_g/Desktop/data/Modi2/*.png")
# im.extend(glob.glob("/home/v_g/Desktop/data/Modi2/*.cms"))
# im.extend(glob.glob("/home/v_g/Desktop/data/Modi2/*.jpg"))
# im.extend(glob.glob("/home/v_g/Desktop/data/Modi2/*.jpeg"))

#make a dict 
ima={}
path=r"/home/v_g/Desktop/checker/"
# path="/home/ubuntu/imtag/modi/"
os.chdir(path)
im = os.listdir(path)

print im 

for i in range(len(im)):
	ima[im[i]]=i

lol={}
for i in range(len(im)):
	lol[i]=i
# print ima


def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err
 
def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
 	return s



dim=(100,100)

for j in range(len(im)):
	# if lol[j]==j:
	# print im[i]
	# print im[i+1]

	original = cv2.imread(str("/home/v_g/Desktop/checker/01pp.jpg"))
	contrast = cv2.imread(str(im[j]))
	# shopped = cv2.imread("virat.jpg")
	 
	original1 = cv2.resize(original, dim, interpolation = cv2.INTER_AREA)
	contrast1 = cv2.resize(contrast, dim, interpolation = cv2.INTER_AREA)
	# shopped1 = cv2.resize(original, dim, interpolation = cv2.INTER_AREA) 

	# convert the images to grayscale
	original = cv2.cvtColor(original1, cv2.COLOR_BGR2GRAY)
	contrast = cv2.cvtColor(contrast1, cv2.COLOR_BGR2GRAY)
	# shopped = cv2.cvtColor(shopped1, cv2.COLOR_BGR2GRAY)

	k= compare_images(original, contrast, "Original vs. Contrast")
	print im[j][2:]
	print k
		# if(k>=0.9):
		# 	lol[j]=i

# for i in range(len(im)):
# 	print im[i]
# 	print " "
# 	print lol[i]
# 	print "\n"

count=0
for i in range(len(im)):
	if lol[i]!=i:
		count+=1
print count 