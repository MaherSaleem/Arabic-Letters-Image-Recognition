import os
import math
import cv2
import _pickle as cPickle
import numpy as np
from settings import *
import re
from pickleAndUnpickle import *




#starts from 0 => 'ا'
def getCharByIndex(index):

    if index == 27: return "ي"
    if index > 1:
        index += 1
    if index > 19:
        index += 6
    return chr(ord("ا") + index)


def getCharWithPositionFromPath (path):
    regex = r".*\\(\d*)\\(\d)\\."

    # test_str = "C:\\Users\\Maher\\Desktop\\PAC-NF\\PAC-NF\\Model(B)\\Simplified Arabic\\15\\3\\n"
    matches = re.match(regex, path)
    # print("char is ", matches.group(1))
    # print("position is ", matches.group(2))
    return matches.group(1), matches.group(2)

def getPostionByIndex(index):

    postions = ["منعزل" , "البداية" , "الوسط" , "النهاية"]
    return postions[index]

def getIndexByPosition(position):
    postions = ["منعزل" , "البداية" , "الوسط" , "النهاية"]
    return postions.index(position)

def getFontNameByIndex(index):

    name = ["AdvertisingBold" , "andalus" , "Arabic Transparent" ,
            "DecoType Naskh" , "DecoType Thuluth" , "Diwani Letter",
            "M Unicode Sara" , "Simplified Arabic" , "Tahoma" ,"Traditional Arabic"]
    return name[index]


def printFont(font ,fontIndex, verbos ):
    print("#" * 130)
    print("#        " , getFontNameByIndex(fontIndex)  )
    print("#" * 130)
    for charIndex , char in enumerate(font):
        printChar(charIndex , char , verbos)
    print("#" * 130)


def printChar(charIndex,char , verbos):
    for shapeIndex, shape in enumerate(char):
        printShape(shapeIndex , shape,charIndex,char , verbos)


def printShape(shapeIndex, shape , charIndex,char,verbos):
    print("<<Char is ", getCharByIndex(charIndex), " ", getPostionByIndex(shapeIndex), ">>")
    shape = unpickle_keypoints(shape)
    for partIndex, part in enumerate(shape):
        keypoints, description = shape[partIndex]
        print("  <<part number", partIndex, ">>")
        print("      this part contains", len(shape[partIndex][1]), "keypoints")
        if verbos: print("      keypoints :", keypoints)
        if verbos: print("      description : ", description)
    print("=" * 100)



"""
Verbos is used to enable or disable printing the keypoints and description
"""


def printdataBase(dataBaseName="keypoints.p" , verbos=True):

    keypoints_database = cPickle.load(open(databaseFolderName+dataBaseName, "rb"))
    # for fontIndex, font in enumerate(keypoints_database): # TODO enable that later
    font = keypoints_database
    # printFont(font , 7 , verbos) # 7 is simplified arabic index


    for fontIndex , font in enumerate(keypoints_database):
        print("#" * 130)
        print("font is " , getFontNameByIndex(fontIndex))
        print("#        " , getFontNameByIndex(fontIndex) , )
        print("#" * 130)
        #font = keypoints_database
        for charIndex , char in enumerate(font):
            for shapeIndex , shape in enumerate(char):
                pos , shape = shape
                print("<<Char is " , getCharByIndex(charIndex) , " " , getPostionByIndex(shapeIndex) , ">>" )
                shape = unpickle_keypoints(shape)
                for partIndex , part in enumerate(shape):
                    keypoints , description = shape[partIndex]
                    print("  <<part number" , partIndex , ">>")
                    print("      this part contains" , len(shape[partIndex][1]) , "keypoints")
                    if verbos : print("      keypoints :" , keypoints)
                    if verbos : print("      description : " , description)
                print("="*100)
    print("#" * 130)

# printdataBase(dataBaseName="keypoints_staticWindow_1SA.p" , verbos=False)
# print(getPostionByIndex(0))

