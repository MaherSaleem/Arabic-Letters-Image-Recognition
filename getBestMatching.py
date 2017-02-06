import cv2
from addPadding import *
from dividingImage import *
from pickleAndUnpickle import *
from testingAndTrainingPaths import *
from settings import *
from printDataBase import *
from skimage.io import sift
from matplotlib import pyplot as plt
import random
import operator


def getBestMatching(path, keypoints_database, partitioningType, constantWindowParameters, slidingWindowParameters):

    img = cv2.imread(path, 0)
    # cv2.imshow('img', img)
    paddedImage = addPadding(img, horizontalPadding, verticalPadding)
    # parts = divideImage(paddedImage, n, m)
    if partitioningType == "constant":
        parts = divideImage(paddedImage, constantWindowParameters["n"], constantWindowParameters["m"])
    elif partitioningType == "sliding":
        parts = slidingWindow(paddedImage, slidingWindowParameters["winWidth"]
                              , slidingWindowParameters["winHeight"],
                              slidingWindowParameters["shift"],
                              slidingWindowParameters["shiftDirection"])

    # keypoints_database = cPickle.load(open(keyPointsFile, "rb"))
    ImagePartsKeyPoints_array = []
    for part in parts:
        subImage = getSubImageData(paddedImage, part)
        # cv2.imshow('img2', subImage)
        # cv2.waitKey(0)

        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()
        kp, des = sift.detectAndCompute(subImage, None)
        ImagePartsKeyPoints_array.append([kp, des])
    ln=0
    for i in ImagePartsKeyPoints_array: # query parts
        ln+=len(i[0])
    # print(ImagePartsKeyPoints_array)


    # print("# of query KP: ",ln)
    numberOfMatchingWithEachTrainingCharDict={}
    for fontIndex, eachFont in enumerate(keypoints_database):
        for charIndex, eachChar in enumerate(eachFont):
            for shapeIndex, eachShape in enumerate(eachChar):
                totalNumberOfMatching=0
                pos , eachShape = eachShape
                shapePartsKeypoints = unpickle_keypoints(
                    keypoints_database[fontIndex][charIndex][shapeIndex][1])  # M*N parts of a training image
                # Comparing each part in the testing image with each part of the current training image

                matchesBetweeenQueryAndTraining = comparePartsBetweenQueryAndTraining(ImagePartsKeyPoints_array,shapePartsKeypoints)
                # print(matchesBetweeenQueryAndTraining)

                trainingChar = getFontNameByIndex(fontIndex)+"-"+getCharByIndex(charIndex)+" "+getPostionByIndex(pos)
                numberOfMatchingWithEachTrainingCharDict[str(trainingChar)] = matchesBetweeenQueryAndTraining
    arrayOfMaxForEachPart = [0]*len(ImagePartsKeyPoints_array)#size of number of parts
    for trainingChar,trainingPartsKeypointArray in numberOfMatchingWithEachTrainingCharDict.items():
        for index ,value in enumerate(trainingPartsKeypointArray):
            if value>arrayOfMaxForEachPart[index]:
                arrayOfMaxForEachPart[index] = value

    dictForYesNo = {}
    for trainingChar, trainingPartsKeypointArray in numberOfMatchingWithEachTrainingCharDict.items():
        for index ,value in enumerate(trainingPartsKeypointArray):
            if value == arrayOfMaxForEachPart[index]:
                if trainingChar in dictForYesNo.keys():
                    dictForYesNo[trainingChar] +=1
                    # print("meho")
                else:
                    dictForYesNo[trainingChar] = 1



    #sorting according to the key:
    # sorted_numberOfMatchingWithEachTrainingCharDict = sorted(dictForYesNo.items(), key=operator.itemgetter(0))

    #sorting according to the value:
    sorted_numberOfMatchingWithEachTrainingCharDict = sorted(dictForYesNo.items(), key=operator.itemgetter(1))

    # the sorted becomes array of tuples (key,value)
    # for i,j in sorted_numberOfMatchingWithEachTrainingCharDict:
    #     print(i+":"+str(j))

    return sorted_numberOfMatchingWithEachTrainingCharDict



def comparePartsBetweenQueryAndTraining(QueryParts,TrainingParts):
    # print("%"*50)
    # print(QueryParts)
    # print("+"*50)
    # print(TrainingParts)
    # print("="*50)

    matchArray=[]
    for i in range(len(QueryParts)):

        # TODO: MAHER's part
        kp1, des1 = QueryParts[i]
        kp2, des2 = TrainingParts[i]  # from training data
        if (not kp1 or not kp2):
            # print("#num of matched is 0")  # since no keypoints
            continue

        des2 = np.array(des2)

        # create BFMatcher object
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)  # it return best two matches m and n as DMatch obj
        good = []
        Thr = 0.75
        for twoMatched in matches:
            if len(twoMatched) == 1:  # one best match
                a = twoMatched[0]
                good.append([a])
            else:
                a, b = twoMatched
                if a.distance < Thr * b.distance:  # check if first keypoint m is better than n to take it
                    good.append([a])
        # print("num of matched", len(good))

        # TODO: assuming that there is (matched) number of keypoints that matched in part i
        # matched = random.randint(0, 3)
        matched = len(good)
        # totalNumberOfMatching += matched
        matchArray.append(matched)
    # print(matchArray)
    return matchArray

