import cv2
import numpy as np
import textdetection

def nothing(x):
    pass

# Set-ExecutionPolicy Unrestricted -Scope Process
# .\mtgvenv\Scripts\activate

# Identification
# Isolate the name and cost
# Estimate corner points of contour
# Transform the card into flattened image
# Take snippet of image

# Get the camera feed
cap = cv2.VideoCapture(0)

cv2.namedWindow("Parameters")
cv2.createTrackbar("minThreshold", "Parameters", 24, 255, nothing)
cv2.createTrackbar("maxThreshold", "Parameters", 50, 255, nothing)

while True:
    ret, img = cap.read()
    imgOrig = img.copy()                                                            # Save an unaltered version of the original

    # Detection
    
    # Image Pre-processing
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                 # Convert to Greyscale
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 0)                                   # Blurs the image
    valThresh, imgthresh = cv2.threshold(imgBlur, 160, 255, cv2.THRESH_BINARY)      # Thresholds the image
    
    # edge and contour detection
    threshold1 = cv2.getTrackbarPos("minThreshold", "Parameters")
    threshold2 = cv2.getTrackbarPos("maxThreshold", "Parameters")
    imgCanny = cv2.Canny(imgBlur, threshold1, threshold2)
    imgDilated = cv2.dilate(imgCanny, (1,1), iterations=2)
    
    contours, hierarchy = cv2.findContours(imgDilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # How many cards are in the image
    # print("Cards in the image:", len(contours))

    cv2.imshow('frame', imgOrig)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()