from cv2 import cv2
import numpy as np

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


	f = open("result.txt", 'w')
	for r in range(rows):
		for c in range(columns):
			if resultImage[r,c] == 0:
				f.write("  ")
			else:
				f.write(str(resultImage[r,c]))
				f.write(" ")
		f.write('\n')
	f.close()



if __name__ == '__main__':
	divideTo = 8
	lenaOrigin = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
	rows,columns = lenaOrigin.shape[:2]
	lena = np.zeros((int(lenaOrigin.shape[0]/divideTo), int(lenaOrigin.shape[1]/divideTo)), np.uint8)
	mask = np.array([[0,0],[0,1],[-1,0],[0,-1],[1,0],[1,1],[-1,1],[-1,-1],[1,-1],[0,1]])

	downsampling(binary(lenaOrigin), divideTo, lena)
	rows = int(rows/divideTo)
	columns = int(columns/divideTo)

	Yokoi(lena)
