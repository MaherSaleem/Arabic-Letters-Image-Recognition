import os
import sys
import time
from constructTrainingArray import *
from getBestMatching import *
from testingAndTrainingPaths import *
from measurements import *
from noOfkeyPoints import *
from applyTesting import *


algorithm="SIFT"
measurementPath = "measurements_excel/"+algorithm+"/"

if not os.path.exists(measurementPath):
    os.makedirs(measurementPath)

allNormalMeasurementsToWrite_constant={}
allFamiliesMeasurementsToWrite_constant={}
allNormalMeasurementsToWrite_sliding = {}
allFamiliesMeasurementsToWrite_sliding = {}

for settings in allTestingSettings:
    keyPointsFileName = settings[0]
    dividingMethod = settings[1]
    constantWindowParameters = settings[2]
    slidingWindowParameters = settings[3]

    if dividingMethod == "sliding":

        shiftDirection = ""
        shiftDirection = "H" if slidingWindowParameters["shiftDirection"] == 1 else "V"

        string = "H=" + str(slidingWindowParameters['winHeight']) + ", W=" + str(
            slidingWindowParameters['winWidth']) + ", Sh=" \
                 + str(slidingWindowParameters['shift']) + ", Dir=" + shiftDirection



    else:
        string = "M=" + str(constantWindowParameters['m']) + ", N=" + str(constantWindowParameters['n'])





    print("Method: " + dividingMethod)
    print("Settings: " + string + "\n")

    normalMeasurementsToWrite = []
    familiesMeasurementsToWrite = []

    # constructTrainingArray(fontsList, keyPointsFileName, dividingMethod, constantWindowParameters, slidingWindowParameters)
    normalMeasurementsToWrite, familiesMeasurementsToWrite = applyTesting(testingFont, keyPointsFileName, dividingMethod, constantWindowParameters, slidingWindowParameters)

    if dividingMethod == "sliding":
        allNormalMeasurementsToWrite_sliding[string] = normalMeasurementsToWrite
        allFamiliesMeasurementsToWrite_sliding[string] = familiesMeasurementsToWrite

    elif dividingMethod == "constant":
        allNormalMeasurementsToWrite_constant[string] = normalMeasurementsToWrite
        allFamiliesMeasurementsToWrite_constant[string] = familiesMeasurementsToWrite


# if not os.path.exists("measurements_excel/"+dividingMethod):
#     os.makedirs("measurements_excel/"+dividingMethod)

# print(allNormalMeasurementsToWrite_constant)
writeToexcelFile(measurementPath+"constant",allNormalMeasurementsToWrite_constant,allFamiliesMeasurementsToWrite_constant)
writeToexcelFile(measurementPath+"sliding",allNormalMeasurementsToWrite_sliding,allFamiliesMeasurementsToWrite_sliding)







