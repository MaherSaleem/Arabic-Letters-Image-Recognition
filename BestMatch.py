import cv2


def getBestMatching(path="test2.png"):

    img = cv2.imread(path, 0)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    paddedImage = addPadding(img, horizontalPadding, verticalPadding)
    # cv2.imshow('img',paddedImage)
    # cv2.waitKey(0)
    parts = divideImage(paddedImage, n, m)

    keypoints_database = cPickle.load(open("keypoints.p", "rb"))
    ImagePartsKeyPoints_array = []
    i = 0
    for part in parts:
        print("part is ", i)
        subImage = getSubImageData(paddedImage, part)
        cv2.imshow('img2', subImage)
        cv2.waitKey(0)

        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(subImage, None)
        # print(des1)
        # finding the best match between the input image and the training data

        # create BFMatcher object
        bf = cv2.BFMatcher()

        # Match descriptors.
        for charIndex, eachChar in enumerate(keypoints_database):
            print(eachChar)
            for shapeIndex, eachShape in enumerate(eachChar):
                shapePartsKeypoints = unpickle_keypoints(keypoints_database[charIndex][shapeIndex])
                kp2, des2 = shapePartsKeypoints[i]
                matches = bf.knnMatch(des1, des2, k=2)  # it return best two matches m and n as DMatch obj
                good = []
                for a, b in matches:
                    if a.distance < 0.75 * b.distance:  # check if first keypoint m is better than n to take it
                        good.append([a])

                print("num of matched", len(good))

        i += 1

