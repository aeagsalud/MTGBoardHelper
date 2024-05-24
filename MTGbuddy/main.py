import cv2
import numpy as np


def nothing(x):
    pass

# Image Pre-processing for contour/edge detection
def imageProc(imgInput):
    imgGray = cv2.cvtColor(imgInput, cv2.COLOR_BGR2GRAY)                                # Convert to Greyscale
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 0)                                       # Blurs the image
    valThresh, imgthresh = cv2.threshold(imgBlur, 160, 255, cv2.THRESH_BINARY)          # Thresholds the image

    imgPreproc = imgthresh
    return imgPreproc

# Filter contours to only count cards
def cardFilter(imgProcessed):
    # edge and contour detection
    imgCanny = cv2.Canny(imgProcessed, threshold1, threshold2)                        # Edge detection
    imgDilated = cv2.dilate(imgCanny, (1,1), iterations=1)                            # Thickens edges
    
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Check if no contours detected
    if len(contours) == 0:
        return [], []

    cardHash = np.zeros(len(contours), dtype=int)
    cardposData = []

    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        perim = cv2.arcLength(contours[i], True)
        epsilon = 0.01 * perim
        approx = cv2.approxPolyDP(contours[i], epsilon, True)
        rectX, rectY, rectW, rectH = cv2.boundingRect(approx)
        cardposData.append((rectX, rectY, rectW, rectH))

        if ((area > areaMin) and (area < areamax)):                                 # Check if the area is within limits
            if (len(approx) == 4):                                                  # Check if the polygon has 4 vertices (rectangle)
                cardHash[i] = 1
                cv2.rectangle(img, (rectX, rectY), (rectX + rectW, rectY + rectH), (0, 0, 255), 5)

    return contours, cardHash, cardposData

def isTapped(cardHash, cardposData, img):
    for i in range(len(cardposData)):
        # Initialize variables
        rectW = cardposData[i][1]
        rectH = cardposData[i][2]

        if (cardHash[i] == 1):
            print(rectW, rectH)
            if (rectW > rectH):
                cv2.putText(img, 'untapped', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            else:
                cv2.putText(img, 'tapped', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


# Set-ExecutionPolicy Unrestricted -Scope Process
# .\mtgvenv\Scripts\activate

# Identification
# Isolate the name and cost
# Estimate corner points of contour
# Transform the card into flattened image
# Take snippet of image

# Get the camera feed
cap = cv2.VideoCapture(0)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cv2.namedWindow("Parameters")
cv2.createTrackbar("minThreshold", "Parameters", 24, 255, nothing)
cv2.createTrackbar("maxThreshold", "Parameters", 50, 255, nothing)
cv2.createTrackbar("areaMin", "Parameters", 50, 900, nothing)
cv2.createTrackbar("areaMax", "Parameters", 120000, 120000, nothing)

while True:
    ret, img = cap.read()
    imgOrig = img.copy()                                                            # Save an unaltered version of the original
    
    # Get parameters from trackbars
    threshold1 = cv2.getTrackbarPos("minThreshold", "Parameters")
    threshold2 = cv2.getTrackbarPos("maxThreshold", "Parameters")
    areaMin = cv2.getTrackbarPos("areaMin", "Parameters")
    areamax = cv2.getTrackbarPos("areaMax", "Parameters")

    # ---Detection---
    # Image Pre-processing
    imgPreproc = imageProc(img)
    
    # edge and contour detection
    contours, cardHash, cardposData = cardFilter(imgPreproc)
    # isTapped(cardHash, cardposData, img)

    cardNum = np.count_nonzero(cardHash)
    # How many cards are in the image
    # print("Cards in the image:", len(contours))

    cv2.imshow("preproc", imgPreproc)
    cv2.imshow("Output", img)

    # print("number of cards:", cardNum)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
