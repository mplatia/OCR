import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab
import time
import matplotlib.pyplot as plt


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
img = cv2.imread('Imagenes/pliego71.jpg')

gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray1, 10, 255)
kernel2=np.ones((1,1),np.uint8)
canny = cv2.dilate(canny, kernel2, iterations=1)
#############################################
#### Detecting Characters  ######
#############################################
boxes = pytesseract.image_to_data(gray1)
for a, b in enumerate(boxes.splitlines()):
    if a != 0:
        #print(a)
        b = b.split()
        print(b)
        if len(b) == 12 and (b[11] == 'Integron®' or b[11] == '|T27-7YS' or b[11] == '2027-02' or b[11] == '820022' or b[11] == '2027.02'  or b[11] == '02'
                             or b[11] == '2027' or b[11] == 'B20022'):

        # if len(b) == 12:
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
            cv2.putText(img, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

imgResizei = cv2.resize(img , (1600, 800))
cv2.imshow('img', imgResizei)
# cv2.imshow('canny', canny)
# plt.figure(figsize = (10,20))
# plt.imshow(img)
# plt.show()

cv2.waitKey(0)


