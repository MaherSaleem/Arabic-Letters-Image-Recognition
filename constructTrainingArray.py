import cv2
from addPadding import *
from dividingImage import *
from pickleAndUnpickle import *
from testingAndTrainingPaths import *
from settings import *
from skimage.io import sift
from matplotlib import pyplot as plt






def constructTrainingArray():
    trainingDataPaths = getTrainingImagesPaths()
    temp_array = []
    i = 0
    for eachChar in trainingDataPaths:
        j = 0
        listForChar = []
        for eachShape in eachChar:
            listForShape = []
            img = cv2.imread(eachShape, 0)
            # cv2.imshow('img'+str(i),img)
            # cv2.waitKey(0)
            paddedImage = addPadding(img, horizontalPadding, verticalPadding)
            # cv2.imshow('img'+str(i+1),paddedImage)
            # cv2.waitKey(0)

            parts = divideImage(paddedImage, n, m)
            ImagePartsKeyPoints_array = []
            for part in parts:
                subImage = getSubImageData(paddedImage, part)
                # Initiate SIFT detector
                sift = cv2.xfeatures2d.SIFT_create()
                kp1, des1 = sift.detectAndCompute(subImage, None)
                temp = pickle_keypoints(kp1, des1)
                listForShape.append(temp)
                # listForShape.append([kp1,des1])
                # Initiate ORB detector
                # orb = cv2.ORB_create()
                # find the keypoints and descriptors with ORB
                # kp1, des1 = orb.detectAndCompute(subImage, None)
            listForChar.append(listForShape)
        temp_array.append(listForChar)
    # print(temp_array[0][1])
    storeToFile("keypoints.p", temp_array)