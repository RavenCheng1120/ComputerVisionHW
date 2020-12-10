from cv2 import cv2
import numpy as np
import math

def Roberts(originImg, rows, columns, threshold):
	image = np.zeros(originImg.shape, np.uint8)
	imageBordered = cv2.copyMakeBorder(originImg, 0, 1, 0, 1, cv2.BORDER_REFLECT) # Extend image borders

	for r in range(rows):
		for c in range(columns):
			r1 = int(imageBordered[r+1,c+1]) - int(imageBordered[r,c])
			r2 = int(imageBordered[r+1,c]) - int(imageBordered[r,c+1])
			gradient = math.sqrt(r1**2 + r2**2)
			if gradient >= threshold:
				image[r,c] = 0
			else:
				image[r,c] = 255

	# cv2.imshow("Roberts", image)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	return image


def Prewitt(originImg, rows, columns, threshold, mask_1, mask_2):
	image = np.zeros(originImg.shape, np.uint8)
	imageBordered = cv2.copyMakeBorder(originImg, 1, 1, 1, 1, cv2.BORDER_REFLECT)
	maskRows = len(mask_1)
	maskColumns = len(mask_1[0])

	for r in range(rows):
		for c in range(columns):
			p1, p2 = 0, 0
			for maskR in range(maskRows):
				for maskC in range(maskColumns):
					p1 += int(imageBordered[r+maskR-1, c+maskC-1]) * mask_1[maskR][maskC]
					p2 += int(imageBordered[r+maskR-1, c+maskC-1]) * mask_2[maskR][maskC]
			gradient = math.sqrt(p1**2 + p2**2)
			if gradient >= threshold:
				image[r,c] = 0
			else:
				image[r,c] = 255

	cv2.imshow("Prewitt", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return image


def compass(originImg, rows, columns, threshold, mask):
	image = np.zeros(originImg.shape, np.uint8)
	borderImg = cv2.copyMakeBorder(originImg, 1, 1, 1, 1, cv2.BORDER_REFLECT)

	for r in range(rows):
		for c in range(columns):
			imageList = [borderImg[r-1,c-1], borderImg[r-1,c] , borderImg[r-1,c+1], borderImg[r,c+1] ,borderImg[r+1,c+1], borderImg[r+1,c], borderImg[r+1,c-1] , borderImg[r,c-1]]
			maxK = 0
			for offset in range(8):
				tempSum = 0
				for num in range(8):
					tempSum += imageList[num] * mask[(num+offset)%8]
				if tempSum > maxK:
					maxK = tempSum

			if maxK >= threshold:
				image[r,c] = 0
			else:
				image[r,c] = 255

	cv2.imshow("Compass", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return image


def NevatiaBabu(originImg, rows, columns, threshold, mask_1, mask_2):
	image = np.zeros(originImg.shape, np.uint8)
	borderImg = cv2.copyMakeBorder(originImg, 2, 2, 2, 2, cv2.BORDER_REPLICATE)
	mask_3 = arrayClockwise(mask_1)
	mask_4 = arrayClockwise(mask_2)
	mask_6 = arrayFlip(mask_4)
	mask_5 = arrayClockwise(mask_6)

	for r in range(rows):
		for c in range(columns):
			maxK = 0
			for num in range(6):
				tempsum = 0
				for maskN in range(len(mask_1)):
					for maskC in range(len(mask_1[0])):
						if num == 0:
							tempsum += int(borderImg[r+maskN-2,c+maskC-2]) * mask_1[maskN,maskC]
						elif num == 1:
							tempsum += int(borderImg[r+maskN-2,c+maskC-2]) * mask_2[maskN,maskC]
						elif num == 2:
							tempsum += int(borderImg[r+maskN-2,c+maskC-2]) * mask_6[maskN,maskC]
						elif num == 3:
							tempsum += int(borderImg[r+maskN-2,c+maskC-2]) * mask_3[maskN,maskC]
						elif num == 4:
							tempsum += int(borderImg[r+maskN-2,c+maskC-2]) * mask_4[maskN,maskC]
						elif num == 5:
							tempsum += int(borderImg[r+maskN-2,c+maskC-2]) * mask_5[maskN,maskC]
				if tempsum > maxK:
					maxK = tempsum

			if maxK >= threshold:
				image[r,c] = 0
			else:
				image[r,c] = 255

	cv2.imshow("NevatiaBabu", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return image



#--- Functions for mask array changing operation ---#
def arrayClockwise(maskArray):
	return np.rot90(maskArray, 3)

def arrayFlip(maskArray):
    return np.fliplr(maskArray)


if __name__ == '__main__':
	lena = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
	lenaRows, lenaColumns = lena.shape[:2]

	### Roberts operator
	cv2.imwrite("Roberts.bmp", Roberts(lena, lenaRows, lenaColumns, 25))

	### Prewitt edge detector
	setMask1 = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])
	setMask2 = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
	cv2.imwrite("Prewitt.bmp", Prewitt(lena, lenaRows, lenaColumns, 55, setMask1, setMask2))

	### Sobel edge detector
	setMask1 = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
	setMask2 = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
	cv2.imwrite("Sobel.bmp", Prewitt(lena, lenaRows, lenaColumns, 60, setMask1, setMask2))

	### Frei and Chen gradient operator
	setMask1 = np.array([[-1,-math.sqrt(2),-1],[0,0,0],[1,math.sqrt(2),1]])
	setMask2 = np.array([[-1,0,1],[-math.sqrt(2),0,math.sqrt(2)],[-1,0,1]])
	cv2.imwrite("FreiChen.bmp", Prewitt(lena, lenaRows, lenaColumns, 40, setMask1, setMask2))

	### Kirsch compass operator
	listMask = np.array([-3,-3,5,5,5,-3,-3,-3])
	cv2.imwrite("Kirsch.bmp", compass(lena, lenaRows, lenaColumns, 135, listMask))

	### Robinson
	listMask = np.array([-1,0,1,2,1,0,-1,-2])
	cv2.imwrite("Robinson.bmp", compass(lena, lenaRows, lenaColumns, 43, listMask))

	### Nevatia-Babu 5×5 operator
	setMask1 = np.array([[100,100,100,100,100], [100,100,100,100,100], [0,0,0,0,0], [-100,-100,-100,-100,-100], [-100,-100,-100,-100,-100]])
	setMask2 = np.array([[100,100,100,100,100], [100,100,100,78,-32], [100,92,0,-92,-100], [32,-78,-100,-100,-100], [-100,-100,-100,-100,-100]])
	cv2.imwrite("NevatiaBabu.bmp", NevatiaBabu(lena, lenaRows, lenaColumns, 12500, setMask1, setMask2))
	