import os
import math
import cv2
import _pickle as cPickle

from PIL.ImageFilter import MedianFilter
from scipy.fftpack._fftpack import destroy_dct2_cache
from skimage.io import sift


def getTestingImagesPaths(Model="Model(B)", Font="Simplified Arabic"):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    Model = "Model(B)"
    Font = "Simplified Arabic"
    # newpath = ROOT_DIR + str("\image dataset\PAC-NF\\") + str(Model) + '\\' + str(Font) + '\\'
    newpath = "C:\\Users\Maher\Desktop\PAC-NF\PAC-NF\\" + str(Model) + '\\' + str(Font) + '\\'

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






#=======================================================================================================================

"""
Parameters:
 @img: The original image that we want to add padding to
 @wantedHeightPadding: The Height that we want the output image to have after adding the height padding
 @wantedWidthPadding: The Width that we want the output image to have after adding the width padding

This function adds white padding to the sent image in order to make its dimensions
(wantedHeightPadding*wantedWidthPadding).
The difference between the height of the original image and the wanted height is calculated
and then the half of this difference is added to the top & the bottom of the image.
The same is done to the width of the image.

"""


def addPadding(img, wantedHeightPadding, wantedWidthPadding):
    # Getting the original image dimensions
    originalImageHeight, originalImageWidth = img.shape
    WHITE = 255

    # Calculating the difference between the wanted padding & the original padding
    heightPaddingToadd = (wantedHeightPadding - originalImageHeight)
    widthPaddingToadd = (wantedWidthPadding - originalImageWidth)

    # Specifying the padding we want to add to each dimension
    top, bottom = math.ceil(heightPaddingToadd / 2), math.floor(heightPaddingToadd / 2)
    left, right = math.ceil(widthPaddingToadd / 2), math.floor(widthPaddingToadd / 2)

    # Adding the padding as border to the original image
    paddedImage = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=WHITE)
    # cv2.imwrite('padded_pic.png', paddedImage)
    return paddedImage


def slidingWindow(img, winWidth, winHeight, shift, shiftDirection=0):
    imgHeight, imgWidth = img.shape
    assert winWidth <= imgWidth

    parts = []
    i = 0
    nextXEnd = 0
    while nextXEnd <= imgWidth:
        x_start = i * shift
        x_end = i * shift + winWidth
        y_start = (imgHeight - winHeight) // 2
        y_end = winHeight - (imgHeight - winHeight) // 2
        if shiftDirection == 0:  # vertical
            parts.append({"x": (x_start, x_end), "y": (y_start, y_end)})

            # just draw it
            x1, x2, y1, y2 = x_start, x_end, y_start, y_end,
            cv2.imshow('im', img[x1:x2, y1:y2])
            cv2.waitKey(0)
        else:  # horizantal
            parts.append({"x": (y_start, y_end), "y": (x_start, x_end)})

            # just draw it
            x1, x2, y1, y2 = y_start, y_end, x_start, x_end,
            cv2.imshow('im', img[x1:x2, y1:y2])
            cv2.waitKey(0)

        print((x_start, x_end, y_start, y_end))
        i += 1
        nextXEnd = ((i + 1) * shift + winWidth)

    # for last part
    x_start = i * shift
    x_end = imgWidth - 1
    y_start = (imgHeight - winHeight) // 2
    y_end = winHeight - (imgHeight - winHeight) // 2
    parts.append({"x": (x_start, x_end), "y": (y_start, y_end)})
    print(parts)
    return parts


"""
This function is used to divide the image in n x m parts

@:param(input) img  : denotes that image pixels data
@:param(input) n    : the number of parts we want to divide height
@:param(input) m    : the number of parts we want to divide width

@:return img : the image data is self
@:parts : which an list of dictionaries that contains x and y start and end
    for each division of the image

format of subImages:
    [ {'x': (0, 99), 'y': (0, 99)},
      {'x': (100, 199), 'y': (100, 199)}
      {'x': (200, 299), 'y': (200, 299)} ]

      it could be accessed like this
      subImages[0]['x'] #
      subImages[0]['y']

"""


def divideImage(img, n, m):
    height, width = img.shape
    # print("height is " ,height," width is " , width)
    n_step = height // n
    m_step = width // m

    heightParts = []
    for i in range(n):
        if i == n - 1:  # last index
            start_index_n = i * n_step
            end_index_n = height - 1
        else:
            start_index_n = i * n_step
            end_index_n = (i + 1) * n_step - 1
        heightParts.append((start_index_n, end_index_n))

    widthParts = []
    for i in range(m):
        if i == m - 1:  # last index
            start_index_m = i * m_step
            end_index_m = width - 1
        else:
            start_index_m = i * m_step
            end_index_m = (i + 1) * m_step - 1
        widthParts.append((start_index_m, end_index_m))

    parts = []
    for tuble2 in widthParts:
        for tuble1 in heightParts:
            parts.append({"x": (tuble1[0], tuble1[1]), "y": (tuble2[0], tuble2[1])})

    return parts


def getTrainingImagesPaths(Model="Model(B)", Font="Simplified Arabic"):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    Model = "Model(B)"
    Font = "Simplified Arabic"
    # newpath = ROOT_DIR + str("\image dataset\PAC-NF\\") + str(Model) + '\\' + str(Font) + '\\'
    newpath = "C:\\Users\Maher\Desktop\PAC-NF\PAC-NF\\" + str(Model) + '\\' + str(Font) + '\\'

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

                    pathsForOneChar.append(newpath5)
        pathsAlph.append(pathsForOneChar)
    return pathsAlph


def getSubImageData(img, part):
    x1, x2, y1, y2 = part['x'][0], part['x'][1], part["y"][0], part["y"][1]
    # cv2.imshow('im', img[x1:x2, y1:y2])
    # cv2.waitKey(0)

    return img[x1:x2, y1:y2]


def pickle_keypoints(keypoints, descriptors):
    i = 0
    temp_array = []
    for point in keypoints:
        temp = [point.pt, point.size, point.angle, point.response, point.octave, point.class_id, descriptors[i]]
        i += 1
        temp_array.append(temp)
    return temp_array


"""
This code unpickels for 1 shape(1 image)
"""


def unpickle_keypoints(shape):
    total = []
    try:
        for sub in shape:
            # if sub is None:
            #     continue
            keypoints = []
            descriptors = []
            for point in sub:
                temp_feature = cv2.KeyPoint(x=point[0][0], y=point[0][1], _size=point[1], _angle=point[2],
                                            _response=point[3], _octave=point[4], _class_id=point[5])
                temp_descriptor = point[6]
                keypoints.append(temp_feature)
                descriptors.append(list(temp_descriptor))
            total.append([keypoints, descriptors])
    except:
        pass
    return total


def storeToFile(fileName, temp_array):
    cPickle.dump(temp_array, open(fileName, "wb"))


def constructTrainingArray():
    trainingDataPaths = getTrainingImagesPaths()
    temp_array = []
    i = 0
    for eachChar in trainingDataPaths:
        j = 0
        listForChar = []
        for eachShape in eachChar:
            listForShape = []
            img = cv2.imread(eachShape, 0)
            # cv2.imshow('img'+str(i),img)
            # cv2.waitKey(0)
            paddedImage = addPadding(img, horizontalPadding, verticalPadding)
            # cv2.imshow('img'+str(i+1),paddedImage)
            # cv2.waitKey(0)

            # n = 3
            # m = 3
            parts = divideImage(paddedImage, n, m)
            ImagePartsKeyPoints_array = []
            for part in parts:
                subImage = getSubImageData(paddedImage, part)
                # Initiate SIFT detector
                sift = cv2.xfeatures2d.SIFT_create()
                kp1, des1 = sift.detectAndCompute(subImage, None)
                temp = pickle_keypoints(kp1, des1)
                listForShape.append(temp)
                # listForShape.append([kp1,des1])
                # Initiate ORB detector
                # orb = cv2.ORB_create()
                # find the keypoints and descriptors with ORB
                # kp1, des1 = orb.detectAndCompute(subImage, None)
            listForChar.append(listForShape)
        temp_array.append(listForChar)
    # print(temp_array[0][1])
    storeToFile("keypoints.p", temp_array)


# print(des1)
print("=" * 300)

# constructTrainingArray()






def getBestMatching(path="test2.png"):
    img = cv2.imread(path, 0)
    cv2.imshow('img', img)
    paddedImage = addPadding(img, horizontalPadding, verticalPadding)
    parts = divideImage(paddedImage, n, m)

    keypoints_database = cPickle.load(open("keypoints.p", "rb"))
    ImagePartsKeyPoints_array = []
    for part in parts:
        subImage = getSubImageData(paddedImage, part)
        # cv2.imshow('img2', subImage)
        # cv2.waitKey(0)
        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()
        kp, des = sift.detectAndCompute(subImage, None)
        ImagePartsKeyPoints_array.append([kp, des])

    for charIndex, eachChar in enumerate(keypoints_database):
        for shapeIndex, eachShape in enumerate(eachChar):
            shapePartsKeypoints = unpickle_keypoints(
                keypoints_database[charIndex][shapeIndex])  # 9 parts of a training image
            print()
            for i in range(n * m):
                print("hh")
                kp1, des1 = ImagePartsKeyPoints_array[i]
                kp2, des2 = shapePartsKeypoints[i]
                if (not kp1 or not kp2):
                    print("#num of matched is 0")
                    continue
                # create BFMatcher object
                bf = cv2.BFMatcher()
                # print(des1)
                print(kp2, des2)
                matches = bf.knnMatch(des1, des2, 2)  # it return best two matches m and n as DMatch obj
                print("WRONG")
                good = []
                Thr = 0.75
                for a, b in matches:
                    if a.distance < Thr * b.distance:  # check if first keypoint m is better than n to take it
                        good.append([a])
                print("num of matched", len(good))
                ###############################################


def getCharByIndex(index):
    if index == 27 :return "ي"
    if index > 1:
        index +=1
    if index > 19:
        index +=6
    return chr(ord("ا") + index)

def getPostionByIndex(index):
    postions = ["البداية" , "الوسط" , "النهاية" , "منعزل"]
    return postions[index]

# for i in range(0,50):
#     print( getCharByIndex(i) , getPostionByIndex(2))
n = 1
m = 1
horizontalPadding = 30
verticalPadding = 30
# constructTrainingArray()
#
getBestMatching()
# ok = getTestingImagesPaths()
# for i in ok:
#     print(i)
# img_ = cv2.imread("out.png" , 0)
# cv2.imshow('img', img_)
# slidingWindow(img_,100,280 , 10,shiftDirection=1           )
# cv2.waitKey(0)











# keypoints_database = cPickle.load(open("keypoints.p", "rb"))
# print(keypoints_database)






# print(keypoints_database[1][2])
# t = unpickle_keypoints(keypoints_database[1][2])
# print("+++++++++++++\n"  ,t)
# print(keypoints_database[1])
# tot =[]
# tot =  unpickle_keypoints(keypoints_database[1])
# print(tot)
# kp1, desc1 = unpickle_keypoints(keypoints_database[1])
# print(len(unpickle_keypoints(keypoints_database[0])))
