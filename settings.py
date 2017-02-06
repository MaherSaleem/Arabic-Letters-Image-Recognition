horizontalPadding = 30
verticalPadding = 30
n = 3
m = 3

# fontsList = ["AdvertisingBold", "andalus", "Arabic Transparent", "DecoType Naskh", "DecoType Thuluth", "Diwani Letter",
#              "M Unicode Sara", "Simplified Arabic"]

fontsList = ["Simplified Arabic"]
slidingWindowParameters = {
    "winHeight": 30,
    "winWidth": 10,
    "shift": 5,
    "shiftDirection": 1  # 1=>horizontal 0=>vertical
}

constantWindowParameters = {
    "m": m,
    "n": n
}


# ============================================================
# dividingMethod = "constant"
# mn= str(n) if m == n else str(m)+"_"+str(n)
# keyPointsFileName = "keypoints_staticWindow_"+mn+"SAtest.p"
# ============================================================


shiftDirection=""
shiftDirection = "H" if slidingWindowParameters["shiftDirection"] == 1 else "V"


# ============================================================================================================================
#
dividingMethod = "sliding"
keyPointsFileName = "keypoints_slidingWindow_w"+str(slidingWindowParameters["winWidth"])+"_h"+str(slidingWindowParameters["winHeight"])+\
                    "_sh"+str(slidingWindowParameters["shift"])+"_dir"+shiftDirection+"SAtest.p"

# ============================================================================================================================





