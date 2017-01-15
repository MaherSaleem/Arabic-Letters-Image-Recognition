from printDataBase import *


def getDatabaseSize(keypoints_database):

    databaseSize=0
    for  eachFont in keypoints_database:
        for  eachChar in eachFont:
            for eachShape in eachChar:
                databaseSize +=1
    return databaseSize

#=======================================================================================================================


#starts from 0 => 'ا'
def getGroupbyIndex(index):
    groups = [
        (1,2,3), #ba
        (4,5,6), # 7a
        (7,8), #dal
        (9,10),#ra
        (11,12),#seen
        (13,14), # sad
        (15,16),#ta2
        (17,18),#3een
        (19 , 20)#fa
    ]
    for groupIndex,group in enumerate(groups):
        if index in group:
            return groupIndex
    return -1 # there is no group


#=======================================================================================================================


def getGroupbyChar(char):
    groups = [
        (1,2,3), #ba
        (4,5,6), # 7a
        (7,8), #dal
        (9,10),#ra
        (11,12),#seen
        (13,14), # sad
        (15,16),#ta2
        (17,18),#3een
        (19 , 20)#fa
    ]
    for groupIndex,group in enumerate(groups):
        if char in [getCharByIndex(index) for index in group ]:
            return groupIndex
    return -1


# #tesing groups
# for i in range(0,28):
#     print( i ,getCharByIndex(i) , getGroupbyIndex(i))

#=======================================================================================================================

def accuracy(TP , TN , FP , FN):
    return (TP + TN)/(TP + TN + FP + FN)


def precision(TP , FP):
    return (TP)/(TP + FP)


def recall(TP , FN):
    return TP/(TP+FN)


def f_mesure(p,r):
    return (2*p *r)/(p+r)


def evaluateResults(TP , TN , FP , FN):
    print("=== Confusion Matrix ===")
    print("TP=", TP , "FN=" , FN)
    print("FP=", FP , "TN=" , TN)
    print("=======================")
    a = accuracy(TP,TN,FP,FN)
    r = recall(TP,FN)
    p = precision(TP,FP)
    print("Accuracy = " , a )
    print("Recall  =" , r)
    print("Precision = " , p )
    return a,r,p # returned if they needed in any stage

# evaluateResults(50,20,30,10)

#=======================================================================================================================

# The array we send to this function will contain all the characters with number of matched keypoints above our threshold
# which represents the best matched characters


def getMeasurementsForFamilies(aboveThresholdArray, ImagePath, numberOfFonts, DataSetLength ):

    Char, position = getCharWithPositionFromPath(ImagePath)
    charString = getCharByIndex(int(Char) - 1) + " " + getPostionByIndex(int(position)-1)
    testingGroupIndex = getGroupbyIndex(int(Char)-1)
    TP = 0
    # TP will be the number of entries in the array that are axactly the same as the query image (eventhough different font type)
    for key in aboveThresholdArray:
        trainingChar = str(key).split("-")[1].split(" ")[0]
        trainingGroupIndex = getGroupbyChar(trainingChar)
        if testingGroupIndex == trainingGroupIndex == -1:
            continue
        if testingGroupIndex == trainingGroupIndex:
            TP +=1
    # FP will be the rest of the entries in the previous array
    FP = len(aboveThresholdArray)-TP

    # FN = (number of fonts in the training set) - TP
    FN = numberOfFonts - TP

    # TN = total number of testing dataset - (TP + FP + FN)
    TN = DataSetLength - (TP + FP + FN)

    return TP, TN, FP, FN
#=======================================================================================================================


def getMeasurements(aboveThresholdArray, ImagePath, numberOfFonts, DataSetLength ):

    Char, position = getCharWithPositionFromPath(ImagePath)
    charString = getCharByIndex(int(Char) - 1) + " " + getPostionByIndex(int(position)-1)
    TP = 0
    # TP will be the number of entries in the array that are axactly the same as the query image (eventhough different font type)
    for key in aboveThresholdArray:
        if charString in key:
            TP += 1

    # FP will be the rest of the entries in the previous array
    FP = len(aboveThresholdArray)-TP

    # FN = (number of fonts in the training set) - TP
    FN = numberOfFonts - TP

    # TN = total number of testing dataset - (TP + FP + FN)
    TN = DataSetLength - (TP + FP + FN)

    return TP, TN, FP, FN

#=======================================================================================================================