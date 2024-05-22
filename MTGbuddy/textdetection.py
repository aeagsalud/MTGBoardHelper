import cv2
import easyocr
import matplotlib.pyplot as plt

def readText(img):
    reader = easyocr.Reader(['en'], gpu=True)
    text_ = reader.readtext(img)
    for t in text_:
        print(t)
        bbox, text, score = t
        print(text)
        # cv2.rectangle(img, bbox[0], bbox[2], (0,255,0), 4)

image_path = 'C:/Users/aeggs/Documents/personalProjs/MTGbuddy/dtk-178-colossodon-yearling.jpg'

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    imgOrig = img.copy()    

    readText(img)

    cv2.imshow('frame', img)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()