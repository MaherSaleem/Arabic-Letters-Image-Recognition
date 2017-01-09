import os
import sys

from constructTrainingArray import *
from getBestMatching import *
from definingCharFromImage import *
from testingAndTrainingPaths import *


def getMeasurements(aboveThresholdArray, ImagePath):
    Char, position = getCharWithPositionFromPath(ImagePath)
    charString = getCharByIndex(int(Char) - 1) + " " + getPostionByIndex(int(position)-1)
    TP = 0
    if charString in aboveThresholdArray:
        TP = 1

    return TP
#=======================================================================================================================


# constructTrainingArray()

testingPaths = getTestingImagesPaths()

thresholdForNumberOfMatchedKeypoints = 3
TP=0
for testingImagePathArray in testingPaths:
    for testingImagePath in testingImagePathArray:
        #array of tuples: (key,value)
        numberOfMatchingWithEachTrainingCharArray = getBestMatching(testingImagePath)
        CharsWithMatchingAboveThreshold={}
        for key,value in numberOfMatchingWithEachTrainingCharArray:
            if value >=thresholdForNumberOfMatchedKeypoints:
                CharsWithMatchingAboveThreshold[key]=value

        TP+=getMeasurements(CharsWithMatchingAboveThreshold,testingImagePath)

print(TP)


















# keypoints_database = cPickle.load(open("keypoints.p", "rb"))
# print(keypoints_database)

# print(keypoints_database[1][2])
# t = unpickle_keypoints(keypoints_database[1][2])
# print("+++++++++++++\n"  ,t)
# print(keypoints_database[1])
# tot =[]
# tot =  unpickle_keypoints(keypoints_database[1])
# print(tot)
#kp1, desc1 = unpickle_keypoints(keypoints_database[1])
# print(len(unpickle_keypoints(keypoints_database[0])))