import cv2
import os
import numpy as np

# Initialize
path = 'cardquery'
images = []
cardNames = []
myList = os.listdir(path)
orb = cv2.ORB_create(nfeatures=1000)

# Import images
for card in myList:
    curImg = cv2.imread(f'{path}/{card}', 0)
    blurredImg = cv2.GaussianBlur(curImg, (15,15), 0)
    images.append(blurredImg)
    cardNames.append(os.path.splitext(card)[0])

# Initializes the images of the deck for openCV
def deckInit():
    # Initialize
    path = 'cardquery'
    images = []
    cardNames = []
    myList = os.listdir(path)
    orb = cv2.ORB_create(nfeatures=1000)

    # Import images
    for card in myList:
        curImg = cv2.imread(f'{path}/{card}', 0)
        images.append(curImg)
        cardNames.append(os.path.splitext(card)[0])

# Function to get descriptors
def findDes(images):
    desList = []
    for img in images:
        kp,des = orb.detectAndCompute(img,None)     # Get keypoints and descriptors
        desList.append(des)
    return desList

# Function to find the card id by comparing descriptors
def findID(img, desList, thresh):
    kp2, des2 = orb.detectAndCompute(img,None)
    bf = cv2.BFMatcher()
    matchList = []
    finalIdx = -1
    try:
        for des1 in desList:
            matches = bf.knnMatch(des1, des2, k=2)
            good = []
            for m,n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            matchList.append(len(good))
    except:
        pass
    if len(matchList) != 0:
        if max(matchList) > thresh:
            finalIdx = matchList.index(max(matchList))
    return finalIdx

desList = findDes(images)

# Get camera feed and process
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    ret, img2 = cap.read()
    imgOriginal = img2.copy()
    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)        # Converts image to grayscale

    id = findID(img2, desList, 8)
    if id != -1:
        cv2.putText(imgOriginal, cardNames[id], (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)

    cv2.imshow('frame', imgOriginal)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

