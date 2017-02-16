horizontalPadding = 30
verticalPadding = 30
# n = 3
# m = 3
databaseFolderName = "databases/"


def getTrainingFontsNumber():

    return len(fontsList)


#  [keyPointsFileName, dividingMethod, constantWindowParameters, slidingWindowParameters]
def getSlidingWindowSettings(string):#H_W_Sh_Dir
    settings = str(string).split('_')
    H = int(settings[0])
    W = int(settings[1])
    Sh = int(settings[2])
    Dir = int(settings[3])

    slidingWindowParameters = {
        "winHeight": H,
        "winWidth": W,
        "shift": Sh,
        "shiftDirection": Dir  # 1=>horizontal 0=>vertical
    }

    shiftDirection = ""
    shiftDirection = "H" if slidingWindowParameters["shiftDirection"] == 1 else "V"

    dividingMethod = "sliding"
    keyPointsFileName = "keypoints_slidingWindow_w" + str(slidingWindowParameters["winWidth"]) + "_h" + str(
        slidingWindowParameters["winHeight"]) + \
                        "_sh" + str(slidingWindowParameters["shift"]) + "_dir" + shiftDirection + ".p"

    settingsArray = [keyPointsFileName, dividingMethod, [], slidingWindowParameters]

    return settingsArray


def getConstantWindowSettings(string):
    settings = str(string).split('_')
    m = int(settings[0])
    n = int(settings[1])

    constantWindowParameters = {
        "m": m,
        "n": n
    }


    # ============================================================
    dividingMethod = "constant"
    mn= str(n) if m == n else str(m)+"_"+str(n)
    keyPointsFileName = "keypoints_staticWindow_"+mn+".p"
    # ============================================================

    settingsArray = [keyPointsFileName, dividingMethod, constantWindowParameters, []]

    return settingsArray


# ============================================================================================================================


constantWindows = ["1_1","2_2","3_3","4_4"] #m_n
# slidingWindows = ["30_10_5_1","30_15_5_1","30_5_2_1","30_5_3_1","30_10_5_0","30_15_5_0","30_5_2_0","30_5_3_0"] #H_W_Sh_Dir
slidingWindows = ["30_10_5_1","30_15_5_1","30_10_5_0","30_15_5_0"] #H_W_Sh_Dir

# slidingWindows = []
# constantWindows = ["1_1"]
fontsList = ["AdvertisingBold", "andalus", "Arabic Transparent", "DecoType Naskh", "DecoType Thuluth", "Diwani Letter",
             "M Unicode Sara", "Simplified Arabic"]

testingFont = "Tahoma"

# fontsList = ["Simplified Arabic"]


# array that contains array of settings, each array consists of
#  [keyPointsFileName, dividingMethod, constantWindowParameters, slidingWindowParameters]
constantTestingSettings = []
allTestingSettings =[ ]
for i in constantWindows:
    allTestingSettings.append(getConstantWindowSettings(i))
    # constantTestingSettings.append(getConstantWindowSettings(i))

slidingTestingSettings = []
for i in slidingWindows:
    allTestingSettings.append(getSlidingWindowSettings(i))
    # slidingTestingSettings.append(getSlidingWindowSettings(i))





