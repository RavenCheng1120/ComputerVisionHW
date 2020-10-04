import numpy as np
from cv2 import cv2

def upsideDown():
    lenaCopy = np.zeros(lena.shape,np.uint8)
    lenaCopy = lena.copy()
    for c in range(columns):
        for r in range(rows):
            lenaCopy[r,c] = lena[rows-r-1,c]
        
    #<-- Show image -->
    # cv2.imshow("upside-down", lenaCopy)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #<-- Save image -->
    cv2.imwrite("answer1.bmp",lenaCopy)


def rightLeft():
    lenaCopy = np.zeros(lena.shape,np.uint8)
    lenaCopy = lena.copy()
    for r in range(rows):
        for c in range(columns):
            lenaCopy[r,c] = lena[r,columns-c-1]
    
    #<-- Show image -->
    # cv2.imshow("right-side-left", lenaCopy)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #<-- Save image -->
    cv2.imwrite("answer2.bmp",lenaCopy)


def diagonalFlip():
    lenaCopy = np.zeros(lena.shape,np.uint8)
    lenaCopy = lena.copy()
    for r in range(rows):
        for c in range(columns):
            lenaCopy[r,c] = lena[c,r]

    #<-- Show image -->
    # cv2.imshow("diagonally flip", lenaCopy)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #<-- Save image -->
    cv2.imwrite("answer3.bmp",lenaCopy)


if __name__ == '__main__':
    lena = cv2.imread('lena.bmp')
    rows,columns = lena.shape[:2]
    # upsideDown()
    # rightLeft()
    # diagonalFlip()