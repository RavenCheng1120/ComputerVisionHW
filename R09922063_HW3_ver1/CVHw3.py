from cv2 import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def drawHistogram():
	histData = []
	for r in range(rows):
		for c in range(columns):
			histData.append(lena[r,c,2])

	n, bins, patches = plt.hist(x=histData, bins=256)
	plt.title(r'Histogram')
	plt.savefig("answer1.png")
	plt.show()


def dividedHistogram():
	for r in range(rows):
		for c in range(columns):
			lenaCopy[r,c,0] = int(math.floor(lena[r,c,0]/3))
			lenaCopy[r,c,1] = int(math.floor(lena[r,c,0]/3))
			lenaCopy[r,c,2] = int(math.floor(lena[r,c,0]/3))
			histDivided.append(lenaCopy[r,c,0])

	# cv2.imshow("Divide by 3", lenaCopy)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	# cv2.imwrite("answer2_1.bmp",lenaCopy)

	# n, bins, patches = plt.hist(x=histDivided, bins=256)
	# plt.title(r'Histogram')
	# plt.xlim(0,255)
	# plt.savefig("answer2_2.png")
	# plt.show()


def equalization():
	histData = []
	pmf = np.zeros(256, dtype = int)
	cdf = np.zeros(256, dtype = int)
	cdfMin = 1000
	for count in range(len(histDivided)):
		pmf[histDivided[count]] += 1

	previous = pmf[0]
	for count in range(256):
		if pmf[count] != 0:
			if cdfMin > pmf[count]:
				cdfMin = pmf[count]
			cdf[count] = previous + pmf[count]
			previous = cdf[count]

	for r in range(rows):
		for c in range(columns):
			temp = lenaCopy[r,c,0]
			for i in range(3):
				lenaCopy[r,c,i]= math.floor((cdf[temp] - cdfMin)/(rows*columns-cdfMin)*255)
			histData.append(lenaCopy[r,c,0])

	# cv2.imshow("Image", lenaCopy)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	cv2.imwrite("answer3_1.bmp",lenaCopy)

	n, bins, patches = plt.hist(x=histData, bins=256)
	plt.title(r'Histogram')
	plt.xlim(0,255)
	plt.savefig("answer3_2.png")
	plt.show()


if __name__ == '__main__':
	lena = cv2.imread('lena.bmp')
	rows,columns = lena.shape[:2]
	lenaCopy = np.zeros(lena.shape,np.uint8)
	lenaCopy = lena.copy()
	histDivided = []

	# drawHistogram()
	dividedHistogram()
	equalization()