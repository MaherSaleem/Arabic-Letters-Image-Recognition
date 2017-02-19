from printDataBase import *
import xlsxwriter


def noOfKeypoints(keypoints_database,filename):
    if os.path.isfile(filename):
        os.remove(filename)
    headers = ["Character","Position","Font"]
    # print(keypoints_database)

    workbook = xlsxwriter.Workbook(filename + '.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 10, 20)

    format2 = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#8DB4E2'})
    row=0
    for index, head in enumerate(headers):
        worksheet.write(row, index, head, format2)
    row+=1

    for fontIndex, eachFont in enumerate(keypoints_database):

        for charIndex, eachChar in enumerate(eachFont):

            for shapeIndex, eachShape in enumerate(eachChar):
                sum = 0
                shapePartsKeypoints = unpickle_keypoints(
                    keypoints_database[fontIndex][charIndex][shapeIndex])  # M*N parts of a training image

                trainingChar = getFontNameByIndex(fontIndex) + "-" + getCharByIndex(charIndex) + " " + getPostionByIndex(
                    shapeIndex)

                for i in range(len(shapePartsKeypoints)):
                    kp2, des2 = shapePartsKeypoints[i]
                    sum += len(kp2)

                # print(len(shapePartsKeypoints))
                format3 = workbook.add_format({
                    'bold': 1,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter',
                    'bg_color': '#D9D9D9'})
                # file.write(str(trainingChar) +"\n" + str(sum) + "\n\n")
                worksheet.write(row, 0, getFontNameByIndex(fontIndex), format3)
                worksheet.write(row, 1, getPostionByIndex(shapeIndex), format3)
                worksheet.write(row, 2, getCharByIndex(charIndex), format3)
                worksheet.write(row, 3, sum, format3)

                row+=1

    workbook.close()
