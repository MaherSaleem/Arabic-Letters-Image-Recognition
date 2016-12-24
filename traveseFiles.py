import os
import cv2

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
Model = "Model(B)"
Font = "Simplified Arabic"
newpath = ROOT_DIR + str("\image dataset\PAC-NF\\") + str(Model) + '\\' + str(Font) + '\\'

pathes = []

for i in range(1, 3):
    newpath2 = str(newpath) + str(i) + '\\'
    for j in range(1, 5):
        newpath3 = str(newpath2) + str(j) + '\\'
        # print(newpath3)
        if os.path.exists(newpath3):
            newpath4 = str(newpath3) + "n\\"
            newpath5 = str(newpath4) + "1.png"
            print(newpath5)
            pathes.append(newpath5)
