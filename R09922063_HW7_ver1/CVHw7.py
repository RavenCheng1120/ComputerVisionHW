import numpy as np
from cv2 import cv2

###--- Binarize the benchmark image lena ---###
def binary(image):
	for r in range(rows):
		for c in range(columns):
			if image[r,c] < 128:
				image[r,c] = 0
			else:
				image[r,c] = 255
	return image

###--- Downsampling Lena from 512x512 to 64x64 ---###
def downsampling(image, divide, smallImage):
	for r in range(0, rows, divide):
		for c in range(0, columns, divide):
			smallImage[int(r/divide), int(c/divide)] = image[r,c]

###--- Count the Yokoi connectivity number on a downsampled lena using 4-connected ---###
def Yokoi(image):
	copyImage = np.zeros((image.shape[0]+2,image.shape[1]+2), np.uint8)
	for r in range(copyImage.shape[0]):
		for c in range(copyImage.shape[1]):
			if r == 0 or r == copyImage.shape[0]-1:
				continue
			if c == 0 or c == copyImage.shape[1]-1:
				continue
			copyImage[r,c]=image[r-1, c-1]

	resultImage = np.zeros(image.shape, np.uint8)
	for r in range(rows):
		for c in range(columns):
			if image[r,c] == 0:
				continue

			qNum = 0
			sNum = 0
			for h in range(1,5): # 4-connected
				if copyImage[r+1,c+1] != copyImage[r+1+mask[h][0], c+1+mask[h][1]]:
					sNum += 1
				if (copyImage[r+1,c+1] == copyImage[r+1+mask[h][0], c+1+mask[h][1]]) and (copyImage[r+1,c+1] != copyImage[r+1+mask[h+1][0], c+1+mask[h+1][1]] or copyImage[r+1,c+1] != copyImage[r+1+mask[h+5][0], c+1+mask[h+5][1]]):
					qNum += 1

			if qNum == 4:
				resultImage[r,c] = 4
			elif qNum == 3:
				resultImage[r,c] = 3
			elif qNum == 2:	
				resultImage[r,c] = 2
			elif qNum == 1:
				resultImage[r,c] = 1
			elif qNum == 0 and sNum == 0:
				resultImage[r,c] = 5

	resultImage = pairRelation(resultImage)
	return resultImage


###--- pair relationship operator ---###
def pairRelation(YokoiImage):
	for r in range(rows):
		for c in range(columns):
			if YokoiImage[r,c] != 1:
				continue

			for num in range(1,5):
				if (r+mask[num][0]>=0) and (r+mask[num][0]<rows) and (c+mask[num][1]>=0) and (c+mask[num][1]<columns):
					if YokoiImage[r+mask[num][0], c+mask[num][1]] == 1 or YokoiImage[r+mask[num][0], c+mask[num][1]] == 9:
						YokoiImage[r,c] = 9 # Mark as 'p'(Set value = 9)
						break

	return YokoiImage


def thinning(image, markedImage):
	copyImage = np.zeros((image.shape[0]+2,image.shape[1]+2), np.uint8)
	for r in range(copyImage.shape[0]):
		for c in range(copyImage.shape[1]):
			if r == 0 or r == copyImage.shape[0]-1:
				continue
			if c == 0 or c == copyImage.shape[1]-1:
				continue
			copyImage[r,c]=image[r-1, c-1]

	resultImage = np.zeros(image.shape, np.uint8)
	resultImage = image.copy()

	for r in range(rows):
		for c in range(columns):
			# Only do thinning on the 'p' pixel
			if markedImage[r,c] != 9:
				continue

			# Do the Yokoi operation
			qNum = 0
			for h in range(1,5): # 4-connected
				# Check the 4 neighbors and count how many 'q' does this pixel get
				if (copyImage[r+1,c+1] == copyImage[r+1+mask[h][0], c+1+mask[h][1]]) and (copyImage[r+1,c+1] != copyImage[r+1+mask[h+1][0], c+1+mask[h+1][1]] or copyImage[r+1,c+1] != copyImage[r+1+mask[h+5][0], c+1+mask[h+5][1]]):
					qNum += 1

			# Check if the pixel is edge part(q = 1)
			if qNum == 1:
				resultImage[r,c] = 0 # Erase the pixel(i.e. turn it into black pixel)
				copyImage[r+1,c+1] = 0

	return resultImage


if __name__ == '__main__':
	divideTo = 8
	lenaOrigin = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
	rows,columns = lenaOrigin.shape[:2]
	lena = np.zeros((int(lenaOrigin.shape[0]/divideTo), int(lenaOrigin.shape[1]/divideTo)), np.uint8)
	markLena = np.zeros(lena.shape, np.uint8)
	mask = np.array([[0,0],[0,1],[-1,0],[0,-1],[1,0],[1,1],[-1,1],[-1,-1],[1,-1],[0,1]])

	downsampling(binary(lenaOrigin), divideTo, lena)
	rows = int(rows/divideTo)
	columns = int(columns/divideTo)

	markLena = Yokoi(lena)
	markLena = thinning(lena, markLena)

	while not np.array_equal(lena, markLena):
		lena = markLena
		markLena = Yokoi(lena)
		markLena = thinning(lena, markLena)

	# cv2.imshow("Thinning", markLena)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	cv2.imwrite("thinning.bmp", markLena)

