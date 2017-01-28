from printDataBase import *


def noOfKeypoints(keypoints_database,filename):
    file = open(filename, "w",encoding='utf-8')
    for fontIndex, eachFont in enumerate(keypoints_database):

        for charIndex, eachChar in enumerate(eachFont):

            for shapeIndex, eachShape in enumerate(eachChar):
                sum = 0
                shapePartsKeypoints = unpickle_keypoints(
                    keypoints_database[fontIndex][charIndex][shapeIndex])  # M*N parts of a training image

                trainingChar = getFontNameByIndex(fontIndex) + "-" + getCharByIndex(charIndex) + " " + getPostionByIndex(
                    shapeIndex)

                for i in range(len(shapePartsKeypoints)):
                    kp2, des2 = shapePartsKeypoints[i]
                    sum += len(kp2)
                file.write(str(trainingChar) +"\n" + str(sum)+"\n\n")