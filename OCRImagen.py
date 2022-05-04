import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab
import time
from pylibdmtx import pylibdmtx
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'






img = cv2.imread('Imagenes/p6.jpeg', cv2.IMREAD_UNCHANGED)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



##############################################
##### Detecting Words  ######
##############################################
# #[   0          1           2           3           4          5         6       7       8        9        10       11 ]
# #['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text']
boxes = pytesseract.image_to_data(img)
for a,b in enumerate(boxes.splitlines()):
        # print(b)
        if a!=0:
            b = b.split()
            print(b)
            # ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            # msg = pylibdmtx.decode(thresh)
            # print(msg)

            # if len(b)==12 and (b[11] == '202702' or b[11] == '820022' or  b[11] == '|T27-7YS' or b[11] == 'Integron®') :
            if len(b) == 12:

                x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                cv2.putText(img,b[11],(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)
                cv2.rectangle(img, (x,y), (x+w, y+h), (50, 50, 255), 2)
imgr = cv2.resize(img,(500,800))
cv2.imshow('img', imgr)
cv2.waitKey(0)