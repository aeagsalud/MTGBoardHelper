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
    blurredImg = cv2.GaussianBlur(curImg, (11,11), 0)
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
# Note: thresh is deciding the minimum matchList value acceptable
def findID(img, thresh):
    desList = findDes(images)
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
            cv2.imshow("training image", images[finalIdx])
    return finalIdx
