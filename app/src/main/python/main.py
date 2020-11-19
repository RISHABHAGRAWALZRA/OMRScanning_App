import cv2
import numpy as np
import base64
import utilities
import os
import io
import PIL.Image as Image

def startScanning(data):
    path = data
    width = 800
    height = 950
    questions = 5
    choices = 4

    print(path)
    print("hello",os.listdir("sdcard1"))

    #img = np.asarray(data, dtype="uint8")
    #img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    #img  = Image.open(io.BytesIO(data))
    # img = np.asarray(img)
    # decode_data = base64.b64decode(data)
    # np_data = np.fromstring(decode_data,np.uint8)
    # img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
    #cv2.imshow("image",img)
    #cv2.waitKey(0)
    #img = cv2.imread(os.path.abspath(path));

    img = cv2.imread(path)
    print(type(img),img.shape)
    #print(img.shape)
    imgResized = cv2.resize(img, (width, height))

    imgContours = cv2.resize(img, (width, height)).copy()
    # imgAnswerContours = cv2.resize(img, (width, height)).copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)

    # v = np.median(imgGray)
    # sigma = 0.33
    # lower = int(max(0, (1.0 - sigma) * v))
    # upper = int(min(200, (1.0 + sigma) * v))
    # for i in range(10, 100, 10):
    # cv2.imshow("Original", img)
    imgCanny = cv2.Canny(imgBlur, 10, 50)
    imgCanny2 = cv2.resize(imgCanny, (width, height))
    # st = str(i)

    contours, hierarchy = cv2.findContours(
        imgCanny2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 5)
    # fetchin answer Contours
    rectangleCont = utilities.rectContours(contours)
    #print(len(rectangleCont))
    EnrollmentContour = utilities.contourPoints(rectangleCont[0])
    TestidContour = utilities.contourPoints(rectangleCont[1])
    Answer1Contour = utilities.contourPoints(rectangleCont[2])
    Answer2Contour = utilities.contourPoints(rectangleCont[3])
    Answer3Contour = utilities.contourPoints(rectangleCont[4])
    Answer4Contour = utilities.contourPoints(rectangleCont[5])
    Answer5Contour = utilities.contourPoints(rectangleCont[6])
    # checking Correct
    # cv2.drawContours(imgAnswerContours, EnrollmentContour, -1, (0, 255, 0), 2)
    # cv2.drawContours(imgAnswerContours, TestidContour, -1, (0, 255, 0), 2)
    # cv2.drawContours(imgAnswerContours, Answer1Contour, -1, (0, 255, 0), 2)
    # cv2.drawContours(imgAnswerContours, Answer2Contour, -1, (255, 0, 0), 2)
    # cv2.drawContours(imgAnswerContours, Answer3Contour, -1, (255, 0, 0), 2)
    # cv2.drawContours(imgAnswerContours, Answer4Contour, -1, (255, 0, 0), 2)
    # cv2.drawContours(imgAnswerContours, Answer5Contour, -1, (255, 0, 0), 2)
    # cv2.imshow("Countor", imgAnswerContours)
    Answer1Contour = utilities.reorder(Answer1Contour)
    Answer2Contour = utilities.reorder(Answer2Contour)
    Answer3Contour = utilities.reorder(Answer3Contour)
    Answer4Contour = utilities.reorder(Answer4Contour)
    Answer5Contour = utilities.reorder(Answer5Contour)
    Answer5Contour = utilities.reorder(Answer5Contour)
    EnrollmentContour = utilities.reorder(EnrollmentContour)
    TestidContour = utilities.reorder(TestidContour)

    imgThresholdAnswer16_20 = utilities.wrapping(
        height, width, Answer1Contour, imgResized
    )
    imgThresholdAnswer21_25 = utilities.wrapping(
        height, width, Answer2Contour, imgResized
    )
    imgThresholdAnswer6_10 = utilities.wrapping(
        height, width, Answer3Contour, imgResized
    )
    imgThresholdAnswer11_15 = utilities.wrapping(
        height, width, Answer4Contour, imgResized
    )
    imgThresholdAnswer1_5 = utilities.wrapping(
        height, width, Answer5Contour, imgResized
    )
    imgThresholdEnroll = utilities.wrapping(
        height, width, EnrollmentContour, imgResized
    )
    imgThresholdTestId = utilities.wrapping(height, width, TestidContour, imgResized)
    imgThresholdAnswerArray = [
        imgThresholdAnswer1_5,
        imgThresholdAnswer6_10,
        imgThresholdAnswer11_15,
        imgThresholdAnswer16_20,
        imgThresholdAnswer21_25,
    ]

    enrollBoxes = utilities.splitEnrollment(imgThresholdEnroll)
    # i = 0
    # for image in enrollBoxes:
    #     i += 1
    #     cv2.imshow(str(i), image)
    enrollNumber = ""

    row = 0
    col = 0
    pixelMatrix = np.zeros((10, 8))
    for image in enrollBoxes:
        totalPixel = cv2.countNonZero(image)
        if(totalPixel>800):
            pixelMatrix[row][col] = 1
        col += 1
        if col == 8:
            row += 1
            col = 0
    for c in range(8):
        for r in range(10):
            if pixelMatrix[r][c] == 1:
                enrollNumber += str((r + 1) % 10)

    testIdBoxes = utilities.splitTest(imgThresholdTestId)

    testId = ""
    row = 0
    col = 0
    pixelMat = np.zeros((10, 5))
    for image in testIdBoxes:
        totalPixel = cv2.countNonZero(image)
        if totalPixel > 1000:
            pixelMat[row][col] = 1
        col += 1
        if col == 5:
            row += 1
            col = 0
    for c in range(5):
        for r in range(10):
            if pixelMat[r][c] == 1:
                testId += str((r + 1) % 10)
    QuestionNumber = 1
    responseSet = dict()
    for answers in imgThresholdAnswerArray:
        boxes = utilities.splitAnswer(answers)
        pixelMatrix = np.zeros((questions, choices))
        countR = 0
        countC = 0
        for image in boxes:
            totalPixel = cv2.countNonZero(image)
            if not (QuestionNumber in responseSet):
                responseSet[QuestionNumber] = []
            if totalPixel > 2600:
                pixelMatrix[countR][countC] = 1
                responseSet[QuestionNumber].append(chr(ord("A") + countC))
            countC += 1
            if countC == choices:
                countR += 1
                QuestionNumber += 1
                countC = 0
    finalResponse = {
        "EnrollmentNumber": int(enrollNumber),
        "TestId": int(testId),
        "AnswerSubmitted": responseSet,
    }
    return finalResponse
    # cv2.imshow("Boxes at 21", boxes[0])


