import numpy as np
from cv2 import cv2
import random
import math
import statistics
import CVHw5 as morphology

def snrCalculate(sImage, nImage):
	summaryS, summaryN = 0, 0
	for r in range(rows):
		for c in range(columns):
			summaryS += int(sImage[r,c])
			summaryN += (int(nImage[r,c]) - int(sImage[r,c]))
	meanS = summaryS/(rows*columns)
	meanN = summaryN/(rows*columns)

	summaryVS, summaryVN = 0, 0
	for r in range(rows):
		for c in range(columns):
			summaryVS += ((int(sImage[r,c]) - meanS) ** 2)
			summaryVN += ((int(nImage[r,c]) - int(sImage[r,c]) - meanN) ** 2)
	vs = summaryVS/(rows*columns)
	vn = summaryVN/(rows*columns)
	return (20 * math.log10(math.sqrt(vs)/math.sqrt(vn)))


def gaussianNoise(image, amplitude):
	lenaCopy = np.zeros(image.shape, np.uint8)
	lenaCopy = image.copy()
	for r in range(rows):
		for c in range(columns):
			noiseOutput = int(lenaCopy[r,c]) + (amplitude * random.gauss(0,1))
			if noiseOutput > 255:
				noiseOutput = 255
			lenaCopy[r,c] = noiseOutput

	print("gaussian Noise", amplitude," SNR = ", snrCalculate(image,lenaCopy))
	return lenaCopy


def saltAndPepperNoise(image, threshold):
	lenaCopy = np.zeros(image.shape, np.uint8)
	lenaCopy = image.copy()
	for r in range(rows):
		for c in range(columns):
			randomNumber = random.uniform(0,1)
			if randomNumber < threshold:
				lenaCopy[r,c] = 0
			elif randomNumber > (1-threshold):
				lenaCopy[r,c] = 255

	print("salt And Pepper", threshold," SNR = ", snrCalculate(image,lenaCopy))
	return lenaCopy


def boxFilter(width, height, originImg):
	lenaCopy = np.zeros(originImg.shape, np.uint8)
	lenaCopy = originImg.copy()
	paddingTop = int(height/2)
	paddingLeft = int(width/2)
	image = cv2.copyMakeBorder(originImg,paddingTop,paddingTop,paddingLeft,paddingLeft,cv2.BORDER_REPLICATE)
	for r in range(paddingTop,rows+paddingTop):
		for c in range(paddingLeft,columns+paddingLeft):
			summary = 0
			for h in range(-paddingTop,paddingTop+1):
				for w in range(-paddingLeft,paddingLeft+1):
					summary += image[r+h, c+w]
			lenaCopy[r-paddingTop,c-paddingLeft] = summary/(width*height)

	print("box Filter", width, "x" ,height," SNR = ", snrCalculate(lena,lenaCopy))
	return lenaCopy


def medianFilter(width, height, originImg):
	lenaCopy = np.zeros(originImg.shape, np.uint8)
	lenaCopy = originImg.copy()
	paddingTop = int(height/2)
	paddingLeft = int(width/2)
	image = cv2.copyMakeBorder(originImg,paddingTop,paddingTop,paddingLeft,paddingLeft,cv2.BORDER_REPLICATE)
	for r in range(paddingTop,rows+paddingTop):
		for c in range(paddingLeft,columns+paddingLeft):
			pixelList = []
			for h in range(-paddingTop,paddingTop+1):
				for w in range(-paddingLeft,paddingLeft+1):
					pixelList.append(image[r+h, c+w])
			lenaCopy[r-paddingTop,c-paddingLeft] = statistics.median(pixelList)

	print("median Filter", width, "x" ,height," SNR = ", snrCalculate(lena,lenaCopy))
	return lenaCopy



if __name__ == '__main__':
	lena = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
	rows,columns = lena.shape[:2]
	kernel = np.array([[0,1,1,1,0],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[0,1,1,1,0]])
	centerR, centerC = 2, 2

	### Generate Gaussian Noise images
	gaussianNoise10 = gaussianNoise(lena, 10)
	gaussianNoise30 = gaussianNoise(lena, 30)
	cv2.imwrite("gaussianNoise10.bmp", gaussianNoise10)
	cv2.imwrite("gaussianNoise30.bmp", gaussianNoise30)

	### Generate Salt and Pepper Noise images
	saltAndPepperNoise005 = saltAndPepperNoise(lena, 0.05)
	saltAndPepperNoise010 = saltAndPepperNoise(lena, 0.1)
	cv2.imwrite("saltAndPepperNoise005.bmp", saltAndPepperNoise005)
	cv2.imwrite("saltAndPepperNoise010.bmp", saltAndPepperNoise010)
	
	### Box Filter 3x3 on the four images
	cv2.imwrite("box33Gaussian10.bmp", boxFilter(3,3,gaussianNoise10))
	cv2.imwrite("box33Gaussian30.bmp", boxFilter(3,3,gaussianNoise30))
	cv2.imwrite("box33Salt005.bmp", boxFilter(3,3,saltAndPepperNoise005))
	cv2.imwrite("box33Salt010.bmp", boxFilter(3,3,saltAndPepperNoise010))

	### Box Filter 5x5 on the four images
	cv2.imwrite("box55Gaussian10.bmp", boxFilter(5,5,gaussianNoise10))
	cv2.imwrite("box55Gaussian30.bmp", boxFilter(5,5,gaussianNoise30))
	cv2.imwrite("box55Salt005.bmp", boxFilter(5,5,saltAndPepperNoise005))
	cv2.imwrite("box55Salt010.bmp", boxFilter(5,5,saltAndPepperNoise010))

	### Median Filter 3x3 on the four images
	cv2.imwrite("median33Gaussian10.bmp", medianFilter(3,3,gaussianNoise10))
	cv2.imwrite("median33Gaussian30.bmp", medianFilter(3,3,gaussianNoise30))
	cv2.imwrite("median33Salt005.bmp", medianFilter(3,3,saltAndPepperNoise005))
	cv2.imwrite("median33Salt010.bmp", medianFilter(3,3,saltAndPepperNoise010))

	### Median Filter 5x5 on the four images
	cv2.imwrite("median55Gaussian10.bmp", medianFilter(5,5,gaussianNoise10))
	cv2.imwrite("median55Gaussian30.bmp", medianFilter(5,5,gaussianNoise30))
	cv2.imwrite("median55Salt005.bmp", medianFilter(5,5,saltAndPepperNoise005))
	cv2.imwrite("median55Salt010.bmp", medianFilter(5,5,saltAndPepperNoise010))

	# tempImage = morphology.closing(morphology.opening(gaussianNoise10, kernel), kernel)
	# print("open-close SNR = ", snrCalculate(lena,tempImage))
	# cv2.imwrite("openingClosingGaussian10.bmp", tempImage)
	# tempImage = morphology.opening(morphology.closing(gaussianNoise10, kernel), kernel)
	# print("close-open SNR = ", snrCalculate(lena,tempImage))
	# cv2.imwrite("ClosingopeningGaussian10.bmp", tempImage)

	# tempImage = morphology.closing(morphology.opening(gaussianNoise30, kernel), kernel)
	# print("open-close SNR = ", snrCalculate(lena,tempImage))
	# cv2.imwrite("openingClosingGaussian30.bmp", tempImage)
	# tempImage = morphology.opening(morphology.closing(gaussianNoise30, kernel), kernel)
	# print("close-open SNR = ", snrCalculate(lena,tempImage))
	# cv2.imwrite("ClosingopeningGaussian30.bmp", tempImage)

	# tempImage = morphology.closing(morphology.opening(saltAndPepperNoise005, kernel), kernel)
	# print("open-close SNR = ", snrCalculate(lena,tempImage))
	# cv2.imwrite("openingClosingSalt005.bmp", tempImage)
	# tempImage = morphology.opening(morphology.closing(saltAndPepperNoise005, kernel), kernel)
	# print("close-open SNR = ", snrCalculate(lena,tempImage))
	# cv2.imwrite("ClosingopeningSalt005.bmp", tempImage)

	# tempImage = morphology.closing(morphology.opening(saltAndPepperNoise010, kernel), kernel)
	# print("open-close SNR = ", snrCalculate(lena,tempImage))
	# cv2.imwrite("openingClosingSalt010.bmp", tempImage)
	# tempImage = morphology.opening(morphology.closing(saltAndPepperNoise010, kernel), kernel)
	# print("close-open SNR = ", snrCalculate(lena,tempImage))
	# cv2.imwrite("ClosingopeningSalt010.bmp", tempImage)
