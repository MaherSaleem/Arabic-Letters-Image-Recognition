import cv2
from addPadding import *
from dividingImage import *
from pickleAndUnpickle import *
from testingAndTrainingPaths import *
from settings import *
from printDataBase import *
from skimage.io import sift
from matplotlib import pyplot as plt


def constructTrainingArray(fontsList, keyPointsFileName, partitioningType, constantWindowParameters, slidingWindowParameters):

    print("Constructing the database...")
    trainingDataPathsForAllFonts = []
    for font in fontsList:
        trainingDataPathsForOneFont = getTrainingImagesPaths(Font=font)
        trainingDataPathsForAllFonts.append(trainingDataPathsForOneFont)
    listForAllFonts=[]
    i = 0
    for eachFont in trainingDataPathsForAllFonts:
        listForFont = []
        for eachChar in eachFont:
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
                if partitioningType == "constant":
                    parts = divideImage(paddedImage, constantWindowParameters["n"], constantWindowParameters["m"])
                elif partitioningType == "sliding":
                    parts = slidingWindow(paddedImage, slidingWindowParameters["winWidth"]
                                          , slidingWindowParameters["winHeight"],
                                          slidingWindowParameters["shift"],
                                          slidingWindowParameters["shiftDirection"])

                ImagePartsKeyPoints_array = []
                for part in parts:
                    subImage = getSubImageData(paddedImage, part)
                    # Initiate SIFT detector
                    sift = cv2.xfeatures2d.SIFT_create()
                    kp1, des1 = sift.detectAndCompute(subImage, None)
                    temp =  pickle_keypoints(kp1, des1)
                    listForShape.append(temp)
                    # listForShape.append([kp1,des1])
                    # Initiate ORB detector
                    # orb = cv2.ORB_create()
                    # find the keypoints and descriptors with ORB
                    # kp1, des1 = orb.detectAndCompute(subImage, None)
                char, pos = getCharWithPositionFromPath(eachShape)
                listForChar.append((int(pos)-1,listForShape))
            listForFont.append(listForChar)
        listForAllFonts.append(listForFont)
    # print(listForAllFonts[0][1])
    storeToFile(databaseFolderName+keyPointsFileName, listForAllFonts)
    print("Database is successfully constructed.")