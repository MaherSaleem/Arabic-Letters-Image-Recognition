import os
import numpy as np
import math
import cv2
from skimage.io import sift

"""
Parameters:
 @img: The original image that we want to add padding to
 @wantedHeightPadding: The Height that we want the output image to have after adding the height padding
 @wantedWidthPadding: The Width that we want the output image to have after adding the width padding

This function adds white padding to the sent image in order to make its dimensions
(wantedHeightPadding*wantedWidthPadding).
The difference between the height of the original image and the wanted height is calculated
and then the half of this difference is added to the top & the bottom of the image.
The same is done to the width of the image.

"""
def addPadding(img, wantedHeightPadding, wantedWidthPadding):
    # Getting the original image dimensions
    originalImageHeight, originalImageWidth = img.shape
    WHITE = 255

    # Calculating the difference between the wanted padding & the original padding
    heightPaddingToadd = (wantedHeightPadding - originalImageHeight)
    widthPaddingToadd = (wantedWidthPadding - originalImageWidth)

    # Specifying the padding we want to add to each dimension
    top, bottom = math.ceil(heightPaddingToadd / 2), math.floor(heightPaddingToadd / 2)
    left, right = math.ceil(widthPaddingToadd / 2), math.floor(widthPaddingToadd / 2)

    # Adding the padding as border to the original image
    paddedImage = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=WHITE)
    # cv2.imwrite('padded_pic.png', paddedImage)
    return paddedImage


"""
This function is used to divide the image in n x m parts

@:param(input) img  : denotes that image pixels data
@:param(input) n    : the number of parts we want to divide height
@:param(input) m    : the number of parts we want to divide width

@:return img : the image data is self
@:parts : which an list of dictionaries that contains x and y start and end
    for each division of the image

format of subImages:
    [ {'x': (0, 99), 'y': (0, 99)},
      {'x': (100, 199), 'y': (100, 199)}
      {'x': (200, 299), 'y': (200, 299)} ]

      it could be accessed like this
      subImages[0]['x'] #
      subImages[0]['y']

"""
def divideImage(img , n , m):
    height , width = img.shape
    # print("height is " ,height," width is " , width)
    n_step = height//n
    m_step = width//m

    heightParts = []
    for i in range(n):
        if i == n-1 :# last index
            start_index_n = i*n_step
            end_index_n = height-1
        else:
            start_index_n = i*n_step
            end_index_n = (i+1)*n_step-1
        heightParts.append( (start_index_n , end_index_n))

    widthParts = []
    for i in range(m):
        if i == m-1 :# last index
            start_index_m = i*m_step
            end_index_m = width-1
        else:
            start_index_m = i*m_step
            end_index_m = (i+1)*m_step-1
        widthParts.append( (start_index_m , end_index_m))

    parts = []
    for tuble2 in widthParts:
        for tuble1 in heightParts:
            parts.append({"x" : (tuble1[0] , tuble1[1]) , "y" : (tuble2[0] , tuble2[1])})


    return  parts

def getTrainingImagesPaths(Model="Model(B)",Font = "Simplified Arabic"):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    Model = "Model(B)"
    Font = "Simplified Arabic"
    # newpath = ROOT_DIR + str("\image dataset\PAC-NF\\") + str(Model) + '\\' + str(Font) + '\\'
    newpath = "C:\\Users\Maher\Desktop\PAC-NF\PAC-NF\\" + str(Model) + '\\' + str(Font) + '\\'

    paths = []

    for i in range(1, 30):
        newpath2 = str(newpath) + str(i) + '\\'
        for j in range(1, 5):
            newpath3 = str(newpath2) + str(j) + '\\'
            # print(newpath3)
            if os.path.exists(newpath3):
                newpath4 = str(newpath3) + "n\\"
                newpath5 = str(newpath4) + "1.png"
                paths.append(newpath5)
    return paths

def getSubImageData(img , part):
    print(part)
    x1 ,x2 , y1,y2 =  part['x'][0] , part['x'][1]  , part["y"][0] , part["y"][1]
    return img[x1:x2,y1:y2]





trainingDataPaths = getTrainingImagesPaths()

for path in trainingDataPaths:
    img = cv2.imread(path , 0)
    paddedImage = addPadding(img , 50 , 50)
    n = 3
    m = 3
    parts = divideImage(paddedImage , n,m)
    for part in parts:
        subImage = getSubImageData(paddedImage , part)

        # Initiate SIFT detector
        sift.
        sift = cv2.xfeatures2d.SIFT_create()
        # kp1, des1 = sift.detectAndCompute(subImage, None)
        # print(kp1)
        # print(des1)








