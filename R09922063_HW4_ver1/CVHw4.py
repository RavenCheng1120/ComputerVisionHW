from cv2 import cv2
import numpy as np

def binarize():
	for r in range(rows):
		for c in range(columns):
			if lenaOrigin[r,c] < 128:
				lenaOrigin[r,c] = 0
			else:
				lenaOrigin[r,c] = 255

	# cv2.imshow("binary", lenaOrigin)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()


### first question ###
def dilation(lena, lenaCopy):
	for r in range(rows):
		for c in range(columns):
			# If this pixel is black, skip it
			if lena[r,c] == 0:
				continue

			#Go through a 5*5 kernel
			for numRow in range(-2,3):
				if (r+numRow) >= 0 and (r+numRow) < rows: #Check row isn't below 0 or larger than 512
					for numCol in range(-2,3):
						if (c+numCol) >= 0 and (c+numCol) < columns: #Check column isn't below 0 or larger than 512
							if lena[r+numRow, c+numCol] == 0 and lenaCopy[r+numRow, c+numCol] == 0: #The chosen pixel is black, then turn it to the corresponding color
								lenaCopy[r+numRow, c+numCol] = kernel[2+numRow, 2+numCol]


	# cv2.imshow("dilation", lenaCopy)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	return lenaCopy



### Second question ###
def erosion(lena, lenaCopy):
	for r in range(rows):
		for c in range(columns):
			# If this pixel is black, skip it
			if lena[r,c] == 0:
				continue

			flagSame = True
			#Go through a 3*5 kernel. First and last row of the kernel will be examine later.
			for numRow in range(-1,2):
				if flagSame == False:
					break
				if (r+numRow) >= 0 and (r+numRow) < rows: #Check row isn't below 0 or larger than 512
					for numCol in range(-2,3):
						if (c+numCol) >= 0 and (c+numCol) < columns: #Check column isn't below 0 or larger than 512
							if lena[r+numRow, c+numCol] != kernel[2+numRow, 2+numCol]:
								flagSame = False
								break

			if (r-2) >= 0:
				for numCol in range(-1,2):
					if (c+numCol) >= 0 and (c+numCol) < columns:
						if lena[r-2,c+numCol] != kernel[0, 2+numCol]:
							flagSame = False
							break
			if (r+2 < rows):
				for numCol in range(-1,2):
					if (c+numCol) >= 0 and (c+numCol) < columns:
						if lena[r+2,c+numCol] != kernel[4, 2+numCol]:
							flagSame = False
							break

			if flagSame == True:
				lenaCopy[r,c] = 255
			else:
				lenaCopy[r,c] = 0

	# cv2.imshow("erosion", lenaCopy)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	return lenaCopy


### Third question ###
def opening(lena, lenaCopy):
	lenaCopy = erosion(lena, lenaCopy)
	lenaCopyCopy = np.zeros(lenaOrigin.shape, np.uint8)
	lenaCopyCopy = lenaCopy.copy()
	lenaCopy = dilation(lenaCopy,lenaCopyCopy)

	# cv2.imshow("opening", lenaCopy)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	cv2.imwrite("opening.bmp",lenaCopy)


### Fourth question ###
def closing(lena, lenaCopy):
	lenaCopy = dilation(lena,lenaCopy)
	lenaCopyCopy = np.zeros(lenaOrigin.shape, np.uint8)
	lenaCopyCopy = lenaCopy.copy()
	lenaCopy = erosion(lenaCopy, lenaCopyCopy)

	# cv2.imshow("closing", lenaCopy)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	cv2.imwrite("closing.bmp",lenaCopy)


def complement(image):
	for r in range(rows):
		for c in range(columns):
			if image[r,c] == 0:
				image[r,c] = 255
			else:
				image[r,c] = 0
	return image


### Fifth question ###
def hitMiss(lena, lenaCopy):
	lenaCopy = erosion(lena, lenaCopy)

	lena = complement(lena)
	lenaCopyCopy = np.zeros(lenaOrigin.shape, np.uint8)
	lenaCopyCopy = lena.copy()

	# Erosion
	for r in range(rows):
		for c in range(columns):
			if lena[r,c] == 0:
				continue

			flagSame = True
			if (r-2) >= 0:
				for numCol in range(-2,3,4):
					if (c+numCol) >= 0 and (c+numCol) < columns:
						if lena[r-2,c+numCol] != kernel[0, 2+numCol]:
							flagSame = False
							break
			if (r+2 < rows):
				for numCol in range(-2,3,4):
					if (c+numCol) >= 0 and (c+numCol) < columns:
						if lena[r+2,c+numCol] != kernel[4, 2+numCol]:
							flagSame = False
							break

			if flagSame == True:
				lenaCopyCopy[r,c] = 255
			else:
				lenaCopyCopy[r,c] = 0


	for r in range(rows):
		for c in range(columns):
			if lena[r,c] == 255 and lena[r,c] == lenaCopyCopy[r,c]:
				lenaCopy[r,c] = 255
			else:
				lenaCopy[r,c] = 0

	# cv2.imshow("hitMiss", lenaCopy)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	cv2.imwrite("hitMiss.bmp",lenaCopy)


if __name__ == '__main__':
	lenaOrigin = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
	rows, columns = lenaOrigin.shape[:2]
	binarize()
	kernel = np.array([[0,255,255,255,0],[255,255,255,255,255],[255,255,255,255,255],[255,255,255,255,255],[0,255,255,255,0]])

	lenaOriginCopy = np.zeros(lenaOrigin.shape, np.uint8)
	lenaOriginCopy = lenaOrigin.copy()
	# lenaOriginCopy = dilation(lenaOrigin, lenaOriginCopy)
	# cv2.imwrite("dilation.bmp",lenaOriginCopy)

	# lenaOriginCopy = lenaOrigin.copy()
	# lenaOriginCopy = erosion(lenaOrigin, lenaOriginCopy)
	# cv2.imwrite("erosion.bmp", lenaOriginCopy)

	# lenaOriginCopy = lenaOrigin.copy()
	# opening(lenaOrigin, lenaOriginCopy)

	# lenaOriginCopy = lenaOrigin.copy()
	# closing(lenaOrigin, lenaOriginCopy)

	disjointKernel = np.zeros([5,5], np.uint8)
	disjointKernel[0,0] = 255
	disjointKernel[0,4] = 255

	lenaOriginCopy = lenaOrigin.copy()
	hitMiss(lenaOrigin, lenaOriginCopy)

