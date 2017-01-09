import cv2



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
#=======================================================================================================================


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