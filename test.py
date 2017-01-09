import re

regex = r".*\\(\d*)\\(\d)\\."

test_str = "C:\\Users\\Maher\\Desktop\\PAC-NF\\PAC-NF\\Model(B)\\Simplified Arabic\\15\\3\\n"
matches = re.match(regex,test_str)
print("char is " ,matches.group(1))
print("position is " , matches.group(2))



# import numpy as np
# import cv2
# from matplotlib import pyplot as plt
#
# #
# # img1 = cv2.imread('test2.png',0)          # queryImage
# # path2 = "C:\\Users\zeiad\Desktop\gam3a\Image Processing\\arabic characters Project\\sourceCode\\training data\\Model(B)" + \
# #         '\\' + "Simplified Arabic" + '\\' + str(4) + '\\' + str(3) + '\\' + "n" + '\\' + "2.png"
# # img2 = cv2.imread(path2,0) # trainImage
#
# img1=cv2.imread("sbT.png",0)
# img2=cv2.imread("sbTT.png",0)
# cv2.imshow('img',img2)
# cv2.waitKey(0)
# # Initiate SIFT detector
# orb = cv2.ORB_create()
#
# # find the keypoints and descriptors with SIFT
# kp1, des1 = orb.detectAndCompute(img1,None)
# kp2, des2 = orb.detectAndCompute(img2,None)
# # create BFMatcher object
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#
# # Match descriptors.
# matches = bf.match(des1,des2)
#
# # Sort them in the order of their distance.
# matches = sorted(matches, key = lambda x:x.distance)
#
# # Draw first 10 matches.
# img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10], None, flags=2)
#
# plt.imshow(img3),plt.show()