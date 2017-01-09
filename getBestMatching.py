import cv2
from addPadding import *
from dividingImage import *
from pickleAndUnpickle import *
from testingAndTrainingPaths import *
from settings import *
from definingCharFromImage import *
from skimage.io import sift
from matplotlib import pyplot as plt
import random
import operator


def getBestMatching(path="test2.png"):

    img = cv2.imread(path, 0)
    cv2.imshow('img', img)
    paddedImage = addPadding(img, horizontalPadding, verticalPadding)
    parts = divideImage(paddedImage, n, m)

    keypoints_database = cPickle.load(open("keypoints.p", "rb"))
    ImagePartsKeyPoints_array = []
    for part in parts:
        subImage = getSubImageData(paddedImage, part)
        # cv2.imshow('img2', subImage)
        # cv2.waitKey(0)

        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()
        kp, des = sift.detectAndCompute(subImage, None)
        ImagePartsKeyPoints_array.append([kp, des])
    numberOfMatchingWithEachTrainingCharDict={}
    for charIndex, eachChar in enumerate(keypoints_database):
        for shapeIndex, eachShape in enumerate(eachChar):
            totalNumberOfMatching=0
            shapePartsKeypoints = unpickle_keypoints(
                keypoints_database[charIndex][shapeIndex])  # M*N parts of a training image
            # Comparing each part in the testing image with each part of the current training image
            for i in range(n * m):

                # TODO: MAHER's part
                # print("hh")
                # kp1, des1 = ImagePartsKeyPoints_array[i]
                # kp2, des2 = shapePartsKeypoints[i]
                # if (not kp1 or not kp2):
                #     print("#num of matched is 0")
                #     continue
                # create BFMatcher object
                bf = cv2.BFMatcher()
                # print(des1)
                # print(kp2, des2)
                # matches = bf.knnMatch(des1, des2, 2)  # it return best two matches m and n as DMatch obj
                # print("WRONG")
                # good = []
                # Thr = 0.75
                # for a, b in matches:
                #     if a.distance < Thr * b.distance:  # check if first keypoint m is better than n to take it
                #         good.append([a])
                # print("num of matched", len(good))
                #TODO: assuming that there is (matched) number of keypoints that matched in part i
                matched = random.randint(0, 3)
                totalNumberOfMatching+=matched
            trainingChar = getCharByIndex(charIndex)+" "+getPostionByIndex(shapeIndex)
            numberOfMatchingWithEachTrainingCharDict[str(trainingChar)] = totalNumberOfMatching

    #sorting according to the key:
    # sorted_numberOfMatchingWithEachTrainingCharDict = sorted(numberOfMatchingWithEachTrainingCharDict.items(), key=operator.itemgetter(0))

    #sorting according to the value:
    sorted_numberOfMatchingWithEachTrainingCharDict = sorted(numberOfMatchingWithEachTrainingCharDict.items(), key=operator.itemgetter(1))

    #the sorted becomes array of tuples (key,value)
    # for i,j in sorted_numberOfMatchingWithEachTrainingCharDict:
    #     print(i+":"+str(j))

    return sorted_numberOfMatchingWithEachTrainingCharDict
