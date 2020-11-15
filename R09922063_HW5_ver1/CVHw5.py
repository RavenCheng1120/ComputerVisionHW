import numpy as np
from cv2 import cv2

#---- first question ----#
def dilation(lena, inputKernel):
	lenaCopy = np.zeros(lena.shape, np.uint8)
	lenaCopy = lena.copy()

	for r in range(rows):
		for c in range(columns):
			localMax = 0
			#Go through a 5*5 kernel
			for numRow in range(len(inputKernel)):
				if (r+numRow-centerR) >= 0 and (r+numRow-centerR) < rows: #Check row isn't below 0 or larger than 512
					for numCol in range(len(inputKernel[0])):
						if (c+numCol-centerC) >= 0 and (c+numCol-centerC) < columns: #Check column isn't below 0 or larger than 512
								if inputKernel[numRow, numCol] == 1 and lena[r+numRow-centerR, c+numCol-centerC] > localMax: 
									localMax = lena[r+numRow-centerR, c+numCol-centerC]

			lenaCopy[r,c] = localMax


	# cv2.imshow("dilation", lenaCopy)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	return lenaCopy


#---- Second question ----#
def erosion(lena, inputKernel):
	lenaCopy = np.zeros(lena.shape, np.uint8)
	lenaCopy = lena.copy()

	for r in range(rows):
		for c in range(columns):
			localMin = 255
			#Go through a 5*5 kernel
			for numRow in range(len(inputKernel)):
				if (r+numRow-centerR) >= 0 and (r+numRow-centerR) < rows: #Check row isn't below 0 or larger than 512
					for numCol in range(len(inputKernel[0])):
						if (c+numCol-centerC) >= 0 and (c+numCol-centerC) < columns: #Check column isn't below 0 or larger than 512
								if inputKernel[numRow, numCol] == 1 and lena[r+numRow-centerR, c+numCol-centerC] < localMin: 
									localMin = lena[r+numRow-centerR, c+numCol-centerC]

			lenaCopy[r,c] = localMin

	# cv2.imshow("erosion", lenaCopy)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	return lenaCopy


#---- Third question ----#
def opening(lena, inputKernel):
	lenaCopy = np.zeros(lena.shape, np.uint8)
	lenaCopy = lena.copy()

	lenaCopy = erosion(lena,inputKernel)
	cv2.imwrite("opening_gray.bmp", dilation(lenaCopy, inputKernel))


#---- Fourth question ----#
def closing(lena, inputKernel):
	lenaCopy = np.zeros(lena.shape, np.uint8)
	lenaCopy = lena.copy()

	lenaCopy = dilation(lena,inputKernel)
	cv2.imwrite("closing_gray.bmp", erosion(lenaCopy, inputKernel))



if __name__ == '__main__':
	lenaOrigin = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
	rows, columns = lenaOrigin.shape[:2]

	kernel = np.array([[0,1,1,1,0],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[0,1,1,1,0]])
	centerR, centerC = 2, 2

	# cv2.imwrite("dilation_gray.bmp", dilation(lenaOrigin, kernel))
	# cv2.imwrite("erosion_gray.bmp", erosion(lenaOrigin, kernel))
	opening(lenaOrigin, kernel)
	closing(lenaOrigin, kernel)

