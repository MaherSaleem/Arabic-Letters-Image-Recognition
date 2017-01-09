import re

def getCharByIndex(index):
    if index == 27 :return "ي"
    if index > 1:
        index +=1
    if index > 19:
        index +=6
    return chr(ord("ا") + index)

def getPostionByIndex(index):
    postions = ["منعزل" ,"البداية" , "الوسط" ,  "النهاية"]
    return postions[index]


def getCharWithPositionFromPath (path):
    regex = r".*\\(\d*)\\(\d)\\."

    # test_str = "C:\\Users\\Maher\\Desktop\\PAC-NF\\PAC-NF\\Model(B)\\Simplified Arabic\\15\\3\\n"
    matches = re.match(regex, path)
    # print("char is ", matches.group(1))
    # print("position is ", matches.group(2))
    return matches.group(1), matches.group(2)