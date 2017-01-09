import os
import cv2

from definingCharFromImage import *

def getTrainingImagesPaths(Model="Model(B)", Font="Simplified Arabic"):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    Model = "Model(B)"
    Font = "Simplified Arabic"
    # newpath = ROOT_DIR + str("\image dataset\PAC-NF\\") + str(Model) + '\\' + str(Font) + '\\'
    # newpath = "C:\\Users\Maher\Desktop\PAC-NF\PAC-NF\\" + str(Model) + '\\' + str(Font) + '\\'
    newpath = "C:\\Users\zeiad\Desktop\gam3a\Image Processing\\arabic characters Project\\training data\Model(B)" + '\\' + str(Font) + '\\'

    pathsAlph = []

    for i in range(1, 30):
        pathsForOneChar = []

        newpath2 = str(newpath) + str(i) + '\\'
        for j in range(1, 5):

            newpath3 = str(newpath2) + str(j) + '\\'
            # print(newpath3)
            imageIndex = 2
            if os.path.exists(newpath3):
                if os.listdir(newpath3):

                    newpath4 = str(newpath3) + "n\\"

                    while (1):
                        newpath5 = str(newpath4) + str(imageIndex) + ".png"
                        img = cv2.imread(newpath5, 0)
                        if (img.shape[0] > 30 or img.shape[1] > 30):
                            imageIndex += 1
                        else:
                            break
                    # print(newpath5)
                    # getCharWithPositionFromPath(newpath5)
                    pathsForOneChar.append(newpath5)
        pathsAlph.append(pathsForOneChar)
    return pathsAlph

#=======================================================================================================================

def getTestingImagesPaths(Model="Model(B)", Font="Simplified Arabic"):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    Model = "Model(B)"
    Font = "Simplified Arabic"
    # newpath = ROOT_DIR + str("\image dataset\PAC-NF\\") + str(Model) + '\\' + str(Font) + '\\'
    # newpath = "C:\\Users\Maher\Desktop\PAC-NF\PAC-NF\\" + str(Model) + '\\' + str(Font) + '\\'
    newpath = "C:\\Users\zeiad\Desktop\gam3a\Image Processing\\arabic characters Project\\training data\Model(B)" + '\\' + str(Font) + '\\'

    pathsAlph = []
    charTypes = [ "b","i", "bi"]

    for i in range(1, 30):
        pathsForOneChar = []

        newpath2 = str(newpath) + str(i) + '\\'
        for j in range(1, 5):

            newpath3 = str(newpath2) + str(j) + '\\'
            # print(newpath3)
            imageIndex = 2
            if os.path.exists(newpath3):
                if  os.listdir(newpath3) :
                    for i,type in enumerate(charTypes):
                        newpath4 = str(newpath3) + str(type) + "\\"
                        # print(newpath4)
                        while (1):
                            newpath5 = str(newpath4) +str(i+1)+ str(imageIndex) + ".png"

                            img = cv2.imread(newpath5, 0)
                            if (img.shape[0] > 30 or img.shape[1] > 30):
                                imageIndex += 1
                            else:
                                break
                        # print(newpath5)
                        pathsForOneChar.append(newpath5)
        pathsAlph.append(pathsForOneChar)
    return pathsAlph



#=======================================================================================================================

def getSubImageData(img, part):
    x1, x2, y1, y2 = part['x'][0], part['x'][1], part["y"][0], part["y"][1]
    # cv2.imshow('im', img[x1:x2, y1:y2])
    # cv2.waitKey(0)

    return img[x1:x2, y1:y2]
