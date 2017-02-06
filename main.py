import os
import sys
import time
from constructTrainingArray import *
from getBestMatching import *
from testingAndTrainingPaths import *
from measurements import *
from noOfkeyPoints import *




constructTrainingArray(fontsList, keyPointsFileName, dividingMethod, constantWindowParameters, slidingWindowParameters)


start_time =time.time()
keypoints_database = cPickle.load(open(keyPointsFileName, "rb"))

databaseSize = getDatabaseSize(keypoints_database)


testingPaths = getTestingImagesPaths(Model="Model(B)", Font="Simplified Arabic")

thresholdForNumberOfMatchedKeypoints = 7

normalMeasurements = {
    "totalTP": 0,
    "totalTN": 0,
    "totalFP": 0,
    "totalFN": 0,
    "totalExist": 0
}
familiesMeasurements = {
    "totalTP": 0,
    "totalTN": 0,
    "totalFP": 0,
    "totalFN": 0,
    "totalExist": 0
}

print("DIVIDING METHOD: "+dividingMethod)

# totalexist=0
totalTests=0
print("\n\ncalculating measurements for the testing dataset...")
for testingImagePathArray in testingPaths:
    # print(testingImagePathArray)
    for testingImagePath in testingImagePathArray:
        totalTests+=1
        # print(testingImagePath)
        Char, position = getCharWithPositionFromPath(testingImagePath)
        # print("testing char: ",getCharByIndex(int(Char) - 1) + " " + getPostionByIndex(int(position)-1), ":")

        #array of tuples: (key,value)
        numberOfMatchingWithEachTrainingCharArray = getBestMatching(testingImagePath, keypoints_database, dividingMethod,
                                                                    constantWindowParameters, slidingWindowParameters)
        # print(numberOfMatchingWithEachTrainingCharArray)

        max=0
        for _,value in numberOfMatchingWithEachTrainingCharArray:
            # print(value)
            if value>max:
                max = value
        # if max==0:
        #     continue
        thresholdForNumberOfMatchedKeypoints = max
        # print(max)
        # print(thresholdForNumberOfMatchedKeypoints)
        CharsWithMatchingAboveThreshold={}
        for key,value in numberOfMatchingWithEachTrainingCharArray:
            if value >=thresholdForNumberOfMatchedKeypoints:
                CharsWithMatchingAboveThreshold[key]=value
        # print(CharsWithMatchingAboveThreshold)
        # for char in CharsWithMatchingAboveThreshold:
        #     print(char)

        TP, TN, FP, FN, existf = getMeasurementsForFamilies(CharsWithMatchingAboveThreshold.keys(), testingImagePath,
                                                    len(fontsList),
                                                    databaseSize)

        familiesMeasurements["totalTP"] += TP
        familiesMeasurements["totalTN"] += TN
        familiesMeasurements["totalFN"] += FN
        familiesMeasurements["totalFP"] += FP
        familiesMeasurements["totalExist"] += existf

        TP, TN, FP, FN, exist = getMeasurements(CharsWithMatchingAboveThreshold.keys(), testingImagePath, len(fontsList),
                                         databaseSize)
        normalMeasurements["totalTP"] += TP
        normalMeasurements["totalTN"] += TN
        normalMeasurements["totalFN"] += FN
        normalMeasurements["totalFP"] += FP
        normalMeasurements["totalExist"] += exist
        # print("#"*50)
end_time = time.time()

executionTime = end_time - start_time
print("NORMAL MEASUREMENTS:(databaseSize="+str(databaseSize)+")")
evaluateResults(normalMeasurements["totalTP"], normalMeasurements["totalTN"], normalMeasurements["totalFP"], normalMeasurements["totalFN"])
print("total number of existence: ", normalMeasurements["totalExist"])
print("total number of tests: ", str(totalTests))
print("\n\n accuracy of exist = ", normalMeasurements["totalExist"]/totalTests)
print("#"*30)
print("MEASUREMENTS FOR FAMILIES:")
evaluateResults(familiesMeasurements["totalTP"], familiesMeasurements["totalTN"], familiesMeasurements["totalFP"], familiesMeasurements["totalFN"])

print("total number of existence: ", familiesMeasurements["totalExist"])
print("total number of tests: ", totalTests)
print("\naccuracy of exist = ", familiesMeasurements["totalExist"]/totalTests)

print("\nTOTAL EXECUTION TIME : %s seconds" % executionTime)

# write some measurements to a file

# filename = "executionTime_normalAccExistence_familiesAccExistenceFile.txt"
# with open(filename, 'a') as out:
#     if dividingMethod == "constant":
#         method = str(constantWindowParameters["m"])+"X"+str(constantWindowParameters["n"])
#     else:
#         method = str(slidingWindowParameters["winHeight"])+", "+str(slidingWindowParameters["winWidth"])+", "+\
#                  str(slidingWindowParameters["shift"])+str(shiftDirection)
#     out.write(method+"\nExecutionTime: " +
#               str(executionTime) + "\nNORMAL existence Accuracy: " + str(normalMeasurements["totalExist"]/totalTests)+
#               "\nFAMILIES existence Accuracy: " + str(familiesMeasurements["totalExist"] / totalTests)+"\n"+"#"*30+"\n")
#








# NoOfkeyPointsFileName = "noOfKeypoints_staticWindow_3.txt"
#
# noOfKeypoints(keypoints_database,NoOfkeyPointsFileName)


# printdataBase(dataBaseName=keyPointsFileName , verbos=False)










# Char = getFontNameByIndex(2)+"-"+getCharByIndex(2)+" "+getPostionByIndex(2)
# print(Char)
# trainingChar = str(Char).split("-")[1].split(" ")[0]
# print(trainingChar)
# trainingGroupIndex = getGroupbyChar(trainingChar)
# print(trainingGroupIndex)
