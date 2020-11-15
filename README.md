# ComputerVisionHW
Main website of the CV class: http://cv2.csie.ntu.edu.tw/CV/index.html  
This repo is for the NTU CSIE computer vision class in 2020 fall.

## HW1
Basic Image Manipulation  
1. upside-down lena.bmp
2. right-side-left lena.bmp
3. diagonally flip lena.bmp
4. rotate lena.bmp 45 degrees clockwise
5. shrink lena.bmp in half
6. binarize lena.bmp at 128 to get a binary image

## HW2
Basic Image Manipulation  
1. a binary image (threshold at 128)
2. a histogram
3. 4-connected components(regions with + at centroid, bounding box)

## HW3
Histogram Equalization  
1. original image and its histogram
2. image with intensity divided by 3 and its histogram
3. image after applying histogram equalization to (b) and its histogram

## HW4
Mathematical Morphology - Binary Morphology  
Use a 3-5-5-5-3 kernel for question 1 to 4.  
1. Dilation
2. Erosion
3. Opening
4. Closing
5. Hit-and-miss transform (use a 3x3 kernel from textbook)

## HW5
Write programs which do gray-scale morphology on a gray-scale image(lena.bmp):  
1. Dilation
2. Erosion
3. Opening
4. Closing
Please use the octogonal 3-5-5-5-3 kernel. (which is actually taking the local maxima or local minima respectively).  

## HW6
Write a program which counts the Yokoi connectivity number on a downsampled image(lena.bmp).  
Downsampling Lena from 512x512 to 64x64: Binarize the benchmark image lena as in HW2, then using 8x8 blocks as a unit, take the topmost-left pixel as the downsampled data.  
Count the Yokoi connectivity number on a downsampled lena using 4-connected.  
Result of this assignment is a 64x64 matrix.  

## HW7
Write a program which does thinning on a downsampled image (lena.bmp).  
Downsampling Lena from 512x512 to 64x64: Binarize the benchmark image lena as in HW2, then using 8x8 blocks as a unit, take the topmost-left pixel as the downsampled data.  
You have to use 4-connected neighborhood detection.  
