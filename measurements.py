from printDataBase import *
import xlsxwriter

def getDatabaseSize(keypoints_database):

    databaseSize=0
    for  eachFont in keypoints_database:
        for  eachChar in eachFont:
            for eachShape in eachChar:
                databaseSize +=1
    return databaseSize

#=======================================================================================================================


#starts from 0 => 'ا'
def getGroupbyIndex(index , querySahpe=0 , testShape=0):


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
    grpIdx=-1
    grpLen=1

    for groupIndex,group in enumerate(groups):
        if index in group:
            # print(group)
            grpIdx,grpLen= groupIndex, len(group)
            break

    if querySahpe != testShape: return -1, grpLen

    return grpIdx, grpLen # there is no group


#=======================================================================================================================


def getGroupbyChar(char , querySahpe=0 , testShape=0):
    if querySahpe != testShape :return -1

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
    print("Accuracy = " ,"{0:.3f}".format(a))
    print("Recall  =" ,"{0:.3f}".format(r) )
    print("Precision = " , "{0:.3f}".format(p) )
    return float("{0:.3f}".format(a)),float("{0:.3f}".format(r)),float("{0:.3f}".format(p)) # returned if they needed in any stage

# evaluateResults(50,20,30,10)

#=======================================================================================================================

# The array we send to this function will contain all the characters with number of matched keypoints above our threshold
# which represents the best matched characters


def getMeasurementsForFamilies(aboveThresholdArray, ImagePath, numberOfFonts, DataSetLength ):

    Char, position = getCharWithPositionFromPath(ImagePath)#returns position from the path 1=> 'ا'
    charString = getCharByIndex(int(Char) - 1) + " " + getPostionByIndex(int(position)-1)

    exist = 0
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    if len(aboveThresholdArray)<1 :
        return TP, TN, FP, FN, exist
    # TP will be the number of entries in the array that are axactly the same as the query image (eventhough different font type)
    for key in aboveThresholdArray:
        charWithPosition=str(key).split("-")[1].split(" ")
        trainingChar = charWithPosition[0]
        trainingPositionString = charWithPosition[1]
        trainingPositionIndex=getIndexByPosition(trainingPositionString)
        # print((int(position)-1))

        trainingGroupIndex = getGroupbyChar(trainingChar)
        testingGroupIndex, groupSize = getGroupbyIndex(int(Char) - 1, querySahpe = trainingPositionIndex, testShape=(int(position)-1))
        # print(testingGroupIndex)
        # print(charWithPosition, trainingPositionIndex,trainingGroupIndex,"-------", charString, str(int(position) - 1),testingGroupIndex)
        #print(charWithPosition,trainingGroupIndex)
        # print(trainingGroupIndex,testingGroupIndex)
        # print("training char:",trainingChar)
        if testingGroupIndex == -1 and trainingGroupIndex == -1:
            continue
        if testingGroupIndex == trainingGroupIndex:
            TP +=1
            exist = 1
            # print(charWithPosition,"----",charString, testingGroupIndex)
    # FP will be the rest of the entries in the previous array
    FP = len(aboveThresholdArray)-TP

    # FN = (number of fonts in the training set) - TP
    FN = numberOfFonts * groupSize - TP
    # if FN <0:
    #     print(TP,numberOfFonts * groupSize)

    # TN = total number of testing dataset - (TP + FP + FN)
    TN = DataSetLength - (TP + FP + FN)

    return TP, TN, FP, FN, exist
#=======================================================================================================================


def getMeasurements(aboveThresholdArray, ImagePath, numberOfFonts, DataSetLength ):

    Char, position = getCharWithPositionFromPath(ImagePath)
    charString = getCharByIndex(int(Char) - 1) + " " + getPostionByIndex(int(position)-1)
    TP = 0
    exist=0
    # TP will be the number of entries in the array that are axactly the same as the query image (eventhough different font type)
    for key in aboveThresholdArray:
        if charString in key:
            TP += 1
            exist=1

    # FP will be the rest of the entries in the previous array
    FP = len(aboveThresholdArray)-TP

    # FN = (number of fonts in the training set) - TP
    FN = numberOfFonts - TP

    # TN = total number of testing dataset - (TP + FP + FN)
    TN = DataSetLength - (TP + FP + FN)
    # if exist ==0:
    #     print(charString)
    #     print(aboveThresholdArray)
    return TP, TN, FP, FN , exist

#=======================================================================================================================


def writeToexcelFile(fileName,allNormalMeasurementsToWrite,allFamiliesMeasurementsToWrite):

    if os.path.isfile(fileName):
        os.remove(fileName)
    # Create a workbook and add a worksheet.
    headers = ["TP","TN","FP","FN","Accuracy","Recall","Precision","accuracy of existence", "executionTime"]
    workbook = xlsxwriter.Workbook(fileName+'.xlsx')
    worksheet = workbook.add_worksheet()


    #drawing the header:
    row = 0
    worksheet.set_column(0, 4, 20)
    normalFamily="Normal"
    for i in range(0,2):

        merge_format = workbook.add_format({
            'bold': 1,
            'border':1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color' : '#963636'})
        format2 = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#8DB4E2'})
        format3 = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#D9D9D9'})
        format4 = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#F2F2F2'})

        worksheet.write(row,0,"Using SIFT",merge_format)
        # merge_format.set_bg_color('#8DB4E2')
        worksheet.merge_range(row, 1, row, len(headers), normalFamily,format2)
        row+=1
        # merge_format.set_bg_color('#D9D9D9')
        worksheet.write(row, 0, "Description",format3)
        for index,head in enumerate(headers):
            worksheet.write(row, 1+index, head, format3)

        row+=1
        if i ==1:
            tmp = allFamiliesMeasurementsToWrite
        else:
            tmp = allNormalMeasurementsToWrite
        for key, measurement in tmp.items(): #measurement is one row
            col=0
            worksheet.write(row, col, key, format3)
            col+=1

            # measurements = measurement[0]
            # a = measurement[1]
            # r = measurement[2]
            # p = measurement[3]
            # aOfEx = measurement[4]
            # exTime = measurement[5]

            for measure in measurement:
                worksheet.write(row, col, measure,format4)
                col+=1
            row+=1


        row+=3
        normalFamily="Families"


    workbook.close()
