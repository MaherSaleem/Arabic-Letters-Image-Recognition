import time
from getBestMatching import *
from testingAndTrainingPaths import *
from noOfkeyPoints import *
from measurements import *
import shutil


def applyTesting(testingFont, keyPointsFileName, dividingMethod, constantWindowParameters, slidingWindowParameters ):

    start_time =time.time()
    keypoints_database = cPickle.load(open(databaseFolderName+keyPointsFileName, "rb"))

    databaseSize = getDatabaseSize(keypoints_database)

    # Simplified Arabic
    # Tahoma
    testingPaths = getTestingImagesPaths(Model="Model(B)", Font=testingFont)

    # thresholdForNumberOfMatchedKeypoints = 7

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

    # print("DIVIDING METHOD: "+dividingMethod)

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
            trainingFontListSize=getTrainingFontsNumber()

            TP, TN, FP, FN, existf = getMeasurementsForFamilies(CharsWithMatchingAboveThreshold.keys(), testingImagePath,
                                                                trainingFontListSize,
                                                        databaseSize)

            familiesMeasurements["totalTP"] += TP
            familiesMeasurements["totalTN"] += TN
            familiesMeasurements["totalFN"] += FN
            familiesMeasurements["totalFP"] += FP
            familiesMeasurements["totalExist"] += existf

            TP, TN, FP, FN, exist = getMeasurements(CharsWithMatchingAboveThreshold.keys(), testingImagePath, trainingFontListSize,
                                             databaseSize)
            normalMeasurements["totalTP"] += TP
            normalMeasurements["totalTN"] += TN
            normalMeasurements["totalFN"] += FN
            normalMeasurements["totalFP"] += FP
            normalMeasurements["totalExist"] += exist
            # print("#"*50)
    end_time = time.time()
# ==============================================================================================================================================================
    folderName=""

    if dividingMethod == "sliding":

        shiftDirection = ""
        shiftDirection = "H" if slidingWindowParameters["shiftDirection"] == 1 else "V"

        folderName = "H" + str(slidingWindowParameters['winHeight']) + "_W" + str(
            slidingWindowParameters['winWidth']) + "_Sh" \
                 + str(slidingWindowParameters['shift']) + "_Dir" + shiftDirection



    else:
        folderName = "M" + str(constantWindowParameters['m']) + "_N" + str(constantWindowParameters['n'])
    path = "numberOfKeypoints/" + dividingMethod+"/"

    if not os.path.exists(path):
        os.makedirs(path)

    else:
        shutil.rmtree(path)
        os.makedirs(path)

    # NoOfkeyPointsFileName = "noOfKeypoints_"+dividingMethod+"_"+folderName
    #
    noOfKeypoints(keypoints_database, path+folderName)

    executionTime = end_time - start_time
    print("NORMAL MEASUREMENTS:(databaseSize="+str(databaseSize)+")")
    a, r, p = evaluateResults(normalMeasurements["totalTP"], normalMeasurements["totalTN"], normalMeasurements["totalFP"], normalMeasurements["totalFN"])
    print("total number of existence: ", normalMeasurements["totalExist"])
    print("total number of tests: ", str(totalTests))
    aOfEx = normalMeasurements["totalExist"]/totalTests
    print("\n\n accuracy of exist = ", aOfEx)
    print("#"*30)
    executionTime = float("{0:.5f}".format(executionTime))

    # excelFileName=path+"/normalMeasurements"
    # writeToexcelFile(excelFileName,normalMeasurements,a, r, p, aOfEx, executionTime)
    normalMeasurementsToWrite = [normalMeasurements["totalTP"], normalMeasurements["totalTN"], normalMeasurements["totalFP"], normalMeasurements["totalFN"], a,r,p,aOfEx,executionTime]



    print("MEASUREMENTS FOR FAMILIES:")
    a, r, p = evaluateResults(familiesMeasurements["totalTP"], familiesMeasurements["totalTN"], familiesMeasurements["totalFP"], familiesMeasurements["totalFN"])

    print("total number of existence: ", familiesMeasurements["totalExist"])
    print("total number of tests: ", totalTests)
    aOfEx = familiesMeasurements["totalExist"]/totalTests
    print("\naccuracy of exist = ", aOfEx)

    print("\nTOTAL EXECUTION TIME : %s seconds" % executionTime)
    print("\n")
    print("="*30)

    familiesMeasurementsToWrite = [familiesMeasurements["totalTP"], familiesMeasurements["totalTN"], familiesMeasurements["totalFP"], familiesMeasurements["totalFN"], a, r, p, aOfEx,executionTime]

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


    return normalMeasurementsToWrite,familiesMeasurementsToWrite










    # printdataBase(dataBaseName=keyPointsFileName , verbos=False)
