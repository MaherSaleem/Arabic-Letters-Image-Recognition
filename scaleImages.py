import cv2
import numpy as np
import math

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


img = cv2.imread('a.png', 0)
paddedimage = addPadding(img, 50, 50)
