import os
import sys

from constructTrainingArray import *
from getBestMatching import *
from testingAndTrainingPaths import *


def getMeasurements(aboveThresholdArray, ImagePath):
    Char, position = getCharWithPositionFromPath(ImagePath)
    charString = getCharByIndex(int(Char) - 1) + " " + getPostionByIndex(int(position)-1)
    TP = 0
    for key in aboveThresholdArray:
        if charString in key:
            TP+=1

    return TP
#=======================================================================================================================

keyPointsFileName = "keypoints_staticWindow_1.p"
# constructTrainingArray(keyPointsFileName, "constant")

testingPaths = getTestingImagesPaths()

thresholdForNumberOfMatchedKeypoints = 7
TP=0
for testingImagePathArray in testingPaths[:3]:
    for testingImagePath in testingImagePathArray:
        print("#"*50)
        Char, position = getCharWithPositionFromPath(testingImagePath)
        print(getCharByIndex(int(Char) - 1) + " " + getPostionByIndex(int(position)-1), ":")

        #array of tuples: (key,value)
        numberOfMatchingWithEachTrainingCharArray = getBestMatching(testingImagePath, keyPointsFileName)
        CharsWithMatchingAboveThreshold={}
        for key,value in numberOfMatchingWithEachTrainingCharArray:
            if value >=thresholdForNumberOfMatchedKeypoints:
                CharsWithMatchingAboveThreshold[key]=value
        print(CharsWithMatchingAboveThreshold)

        TP+=getMeasurements(CharsWithMatchingAboveThreshold.keys(),testingImagePath)

print(TP)
