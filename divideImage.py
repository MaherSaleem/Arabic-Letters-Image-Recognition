import cv2
import numpy as np
import image_slicer

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
def divide(img , n , m):
    height , width = img.shape
    # print("height is " ,height," width is " , width)
    n_step = height//n
    m_step = width//m

    heightParts = []
    for i in range(n):
        if i == n-1 :# last index
            start_index_n = i*n_step
            end_index_n = height-1
        else:
            start_index_n = i*n_step
            end_index_n = (i+1)*n_step-1
        heightParts.append( (start_index_n , end_index_n))

    widthParts = []
    for i in range(m):
        if i == m-1 :# last index
            start_index_m = i*m_step
            end_index_m = width-1
        else:
            start_index_m = i*m_step
            end_index_m = (i+1)*m_step-1
        widthParts.append( (start_index_m , end_index_m))

    parts = []
    for tuble2 in widthParts:
        for tuble1 in heightParts:
            parts.append({"x" : (tuble1[0] , tuble1[1]) , "y" : (tuble2[0] , tuble2[1])})


    return img, parts



img = cv2.imread('sample.png', 0)
n=3
m=3
img , parts = divide(img , n , m)
part = parts[0]
for part in parts:
    x1 ,x2 , y1,y2 =  part['x'][0] ,part['x'][1]  , part["y"][0] , part["y"][1]
    cv2.imshow('im' ,img[x1:x2,y1:y2] )
    cv2.waitKey(0)
