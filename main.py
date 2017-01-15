import os
import sys

from constructTrainingArray import *
from getBestMatching import *
from testingAndTrainingPaths import *
from measurements import *


keyPointsFileName = "keypoints_staticWindow_1.p"
fontsList = ["AdvertisingBold", "andalus", "Arabic Transparent", "DecoType Naskh", "DecoType Thuluth", "Diwani Letter",
             "M Unicode Sara", "Simplified Arabic"]

slidingWindowParameters = {
    "winWidth": 5,
    "winHeight": 5,
    "shift": 10,
    "shiftDirection": 0
}

constantWindowParameters = {
    "m": m,
    "n": n
}

# constructTrainingArray(fontsList, keyPointsFileName, "constant", constantWindowParameters, slidingWindowParameters)

keypoints_database = cPickle.load(open(keyPointsFileName, "rb"))

databaseSize = getDatabaseSize(keypoints_database)


testingPaths = getTestingImagesPaths(Model="Model(B)", Font="Tahoma")

thresholdForNumberOfMatchedKeypoints = 7

normalMeasurements = {
    "totalTP": 0,
    "totalTN": 0,
    "totalFP": 0,
    "totalFN": 0
}
familiesMeasurements = {
    "totalTP": 0,
    "totalTN": 0,
    "totalFP": 0,
    "totalFN": 0
}

print("\n\ncalculating measurements for the testing dataset...")
for testingImagePathArray in testingPaths:
    # print(testingImagePathArray)
    for testingImagePath in testingImagePathArray:
        # print(testingImagePath)
        Char, position = getCharWithPositionFromPath(testingImagePath)
        # print(getCharByIndex(int(Char) - 1) + " " + getPostionByIndex(int(position)-1), ":")

        #array of tuples: (key,value)
        numberOfMatchingWithEachTrainingCharArray = getBestMatching(testingImagePath, keypoints_database, "constant",
                                                                    constantWindowParameters, slidingWindowParameters)
        CharsWithMatchingAboveThreshold={}
        for key,value in numberOfMatchingWithEachTrainingCharArray:
            if value >=thresholdForNumberOfMatchedKeypoints:
                CharsWithMatchingAboveThreshold[key]=value
        # print(CharsWithMatchingAboveThreshold)

        TP, TN, FP, FN = getMeasurements(CharsWithMatchingAboveThreshold.keys(), testingImagePath, len(fontsList), databaseSize)
        familiesMeasurements["totalTP"] += TP
        familiesMeasurements["totalTN"] += TN
        familiesMeasurements["totalFN"] += FN
        familiesMeasurements["totalFP"] += FP

        TP, TN, FP, FN = getMeasurementsForFamilies(CharsWithMatchingAboveThreshold.keys(), testingImagePath, len(fontsList),
                                                    databaseSize)
        normalMeasurements["totalTP"] += TP
        normalMeasurements["totalTN"] += TN
        normalMeasurements["totalFN"] += FN
        normalMeasurements["totalFP"] += FP

print("NORMAL MEASUREMENTS:(databaseSize="+str(databaseSize)+")")
evaluateResults(normalMeasurements["totalTP"], normalMeasurements["totalTN"], normalMeasurements["totalFP"], normalMeasurements["totalFN"])
print("#"*30)
print("MEASUREMENTS FOR FAMILIES:")
evaluateResults(familiesMeasurements["totalTP"], familiesMeasurements["totalTN"], familiesMeasurements["totalFP"], familiesMeasurements["totalFN"])








# Char = getFontNameByIndex(2)+"-"+getCharByIndex(2)+" "+getPostionByIndex(2)
# print(Char)
# trainingChar = str(Char).split("-")[1].split(" ")[0]
# print(trainingChar)
# trainingGroupIndex = getGroupbyChar(trainingChar)
# print(trainingGroupIndex)
