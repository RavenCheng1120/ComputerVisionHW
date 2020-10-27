from cv2 import cv2
import numpy as np

def binarize(image):
	for r in range(rows):
		for c in range(columns):
			if image[r,c] < 128:
				image[r,c] = 0
			else:
				image[r,c] = 255

	# cv2.imshow("binary", image)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	return image


#---- first question ----#
def dilation(lena, lenaCopy, inputKernel):
	for r in range(rows):
		for c in range(columns):
			if lena[r,c] == 0:
				continue

			#Go through a 5*5 kernel
			for numRow in range(0,len(inputKernel)):
				if (r+numRow-centerR) >= 0 and (r+numRow-centerR) < rows: #Check row isn't below 0 or larger than 512
					for numCol in range(0,len(inputKernel)):
						if (c+numCol-centerC) >= 0 and (c+numCol-centerC) < columns: #Check column isn't below 0 or larger than 512
								if inputKernel[numRow, numCol] == 255: #Check if the position in this kernel is white, and 
									lenaCopy[r+numRow-centerR, c+numCol-centerC] = 255


	# cv2.imshow("dilation", lenaCopy)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	return lenaCopy



#---- Second question ----#
def erosion(lena, lenaCopy, inputKernel):
	for r in range(rows):
		for c in range(columns):
			flagSame = True
			#Go through a 5*5 kernel
			for numRow in range(0,len(inputKernel)):
				if flagSame == False: #Already have a pixel that don't match
					break
				if (r+numRow-centerR) >= 0 and (r+numRow-centerR) < rows: #Check row isn't below 0 or larger than 512
					for numCol in range(0,len(inputKernel)):
						if (c+numCol-centerC) >= 0 and (c+numCol-centerC) < columns: #Check column isn't below 0 or larger than 512
							if inputKernel[numRow, numCol] == 255: #Check if the position in this kernel is white
								if lena[r+numRow-centerR, c+numCol-centerC] != 255: #Check if the position in the image is white
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


#---- Third question ----#
def opening(lena, lenaCopy):
	lenaCopy = erosion(lena, lenaCopy, kernel)
	lenaCopyCopy = np.zeros(lenaOrigin.shape, np.uint8)
	lenaCopyCopy = lenaCopy.copy()
	lenaCopy = dilation(lenaCopy,lenaCopyCopy, kernel)

	# cv2.imshow("opening", lenaCopy)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	cv2.imwrite("opening.bmp",lenaCopy)


#---- Fourth question ----#
def closing(lena, lenaCopy):
	lenaCopy = dilation(lena,lenaCopy, kernel)
	lenaCopyCopy = np.zeros(lenaOrigin.shape, np.uint8)
	lenaCopyCopy = lenaCopy.copy()
	lenaCopy = erosion(lenaCopy, lenaCopyCopy, kernel)

	# cv2.imshow("closing", lenaCopy)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	cv2.imwrite("closing.bmp",lenaCopy)


#---- Fifth question ----#
def complement(image):
	for r in range(rows):
		for c in range(columns):
			image[r,c] = 255 - image[r,c]
	return image
 


def hitMiss(lena, lenaCopy):
	lenaCopy = erosion(lena, lenaCopy, kernel_J)

	# Reverse the image and make a copy of it
	lena = complement(lena)
	lenaReverseCopy = np.zeros(lenaOrigin.shape, np.uint8)
	lenaReverseCopy = lena.copy()

	# Erosion for the reversed image and disjoint kernel
	lenaReverseCopy = erosion(lena,lenaReverseCopy, disjointKernel)
	
	for r in range(rows):
		for c in range(columns):
			if lenaCopy[r,c] == 255 and lenaCopy[r,c] == lenaReverseCopy[r,c]:
				lena[r,c] = 255
			else:
				lena[r,c] = 0

	# cv2.imshow("hitMiss", lena)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	cv2.imwrite("hitMiss.bmp",lena)



if __name__ == '__main__':
	#---- preprocessing ----#
	lenaOrigin = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
	rows, columns = lenaOrigin.shape[:2]
	lenaOrigin = binarize(lenaOrigin)
	kernel = np.array([[0,255,255,255,0],[255,255,255,255,255],[255,255,255,255,255],[255,255,255,255,255],[0,255,255,255,0]])
	centerR = 2
	centerC = 2
	lenaOriginCopy = np.zeros(lenaOrigin.shape, np.uint8)
	lenaOriginCopy = lenaOrigin.copy()

	#---- First ----#
	lenaOriginCopy = dilation(lenaOrigin, lenaOriginCopy, kernel)
	cv2.imwrite("dilation.bmp",lenaOriginCopy)

	#---- Second ----#
	lenaOriginCopy = lenaOrigin.copy()
	lenaOriginCopy = erosion(lenaOrigin, lenaOriginCopy, kernel)
	cv2.imwrite("erosion.bmp", lenaOriginCopy)

	# ---- Third ----#
	lenaOriginCopy = lenaOrigin.copy()
	opening(lenaOrigin, lenaOriginCopy)

	#---- Fourth ----#
	lenaOriginCopy = lenaOrigin.copy()
	closing(lenaOrigin, lenaOriginCopy)

	#---- preprocessing for fifth ----#
	kernel_J = np.zeros([3,3], np.uint8)
	kernel_J[1,0] = 255
	kernel_J[1,1] = 255
	kernel_J[2,1] = 255
	centerR = 1
	centerC = 1

	disjointKernel = np.zeros([3,3], np.uint8)
	disjointKernel[0,1] = 255
	disjointKernel[0,2] = 255
	disjointKernel[1,2] = 255

	#--- Fifth ---#
	lenaOriginCopy = lenaOrigin.copy()
	hitMiss(lenaOrigin, lenaOriginCopy)

