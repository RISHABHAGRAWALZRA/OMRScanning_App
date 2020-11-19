import cv2
import numpy as np


def rectContours(contours):
    rectCont = []
    for i in contours:
        area = cv2.contourArea(i)
        # print("Area", area)

        if 800 < area < 640000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if len(approx == 4):
                rectCont.append(i)
    rectCont = sorted(rectCont, key=cv2.contourArea, reverse=True)
    return rectCont


def contourPoints(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    return approx


def reorder(myPoints):
    # print(myPoints)
    # print(myPoints.shape)
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    # print(myPoints)
    # print(add)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]  # [w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)]  # [h,0]
    return myPointsNew


def wrapping(height, width, AnswerContour, imgResized):
    pt1 = np.float32(AnswerContour)
    pt2 = np.float32([[0, 0], [400, 0], [0, height // 2], [400, height // 2]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgWrapedColored = cv2.warpPerspective(imgResized, matrix, (400, height // 2))

    # ApplyThreshold

    imgWrapedGreyAnswer = cv2.cvtColor(imgWrapedColored, cv2.COLOR_BGR2GRAY)
    imgThresholdAnswer = cv2.threshold(
        imgWrapedGreyAnswer, 180, 255, cv2.THRESH_BINARY_INV
    )[1]
    return imgThresholdAnswer


def splitAnswer(img):
    rows = np.array_split(img, 5, 0)
    boxes = []
    for r in range(len(rows)):
        cols = np.array_split(rows[r], 4, 1)
        for box in range(len(cols)):
            boxes.append(cols[box])
    return boxes


def splitEnrollment(img):
    rows = np.array_split(img, 10, 0)
    boxes = []
    for r in range(len(rows)):
        cols = np.array_split(rows[r], 8, 1)
        for box in range(len(cols)):
            boxes.append(cols[box])
    return boxes


def splitTest(img):
    rows = np.array_split(img, 10, 0)
    boxes = []
    for r in range(len(rows)):
        cols = np.array_split(rows[r], 5, 1)
        for box in range(len(cols)):
            boxes.append(cols[box])
    return boxes