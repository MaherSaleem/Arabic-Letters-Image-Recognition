import cv2
import _pickle as cPickle



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

#=======================================================================================================================


def unpickle_keypoints(shape):
    total = []
    try:
        sumOfKey = 0
        for sub in shape:
            # if sub is None:
            #     continue
            keypoints = []
            descriptors = []
            for point in sub:
                temp_feature = cv2.KeyPoint(x=point[0][0], y=point[0][1], _size=point[1], _angle=point[2],
                                            _response=point[3], _octave=point[4], _class_id=point[5])
                temp_descriptor = point[6]
                # sumOfKey +=
                keypoints.append(temp_feature)
                descriptors.append(list(temp_descriptor))
            total.append([keypoints, descriptors])
    except:
        pass
    return total

#=======================================================================================================================


def storeToFile(fileName, temp_array):
    cPickle.dump(temp_array, open(fileName, "wb"))