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


def noOfKeypoints(keypoints_database,filename):
    file = open(filename, "w",encoding='utf-8')
    for fontIndex, eachFont in enumerate(keypoints_database):

        for charIndex, eachChar in enumerate(eachFont):

            for shapeIndex, eachShape in enumerate(eachChar):

                shapePartsKeypoints,totalNoOfkeypoitns = unpickle_keypoints(
                    keypoints_database[fontIndex][charIndex][shapeIndex])  # M*N parts of a training image

                trainingChar = getFontNameByIndex(fontIndex) + "-" + getCharByIndex(charIndex) + " " + getPostionByIndex(
                    shapeIndex)
                file.write(str(trainingChar) +"\n" + str(totalNoOfkeypoitns)+"\n\n")
