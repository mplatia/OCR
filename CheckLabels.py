import cv2
import numpy as  np
import pytesseract
from imutils.object_detection import non_max_suppression

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

img=cv2.imread(r'Imagenes/pliegomitad.jpg',1) # Leer imagen


gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray1, 100, 255)
kernel2 = np.ones((3, 3), np.uint8)
canny = cv2.dilate(canny, kernel2, iterations=1)
cnts, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

contador = 0
puntos =[]
pun = []
cont = 6
for c in cnts:
    epsilon = 0.01 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    area2 = cv2.contourArea(c)
    # if area2 > 104000:
    if area2 > 6500 and area2 < 8000:
        if len(approx) == 4:
            #cv2.drawContours(img, [approx], 0, (0, 0, 255), 2)
            x, y, w, h = cv2.boundingRect(c)
            r=265
            # cv2.rectangle(img, (x- 265, y - 100), (x + w + 230, y + h + 8), (0, 0, 0), 2, cv2.LINE_AA)
            contador = contador + 1
            puntos.append((x, y, w, h, contador))
            print('antes del sort', puntos)
            #puntos.sort(key=lambda r: r[0])
            punt = sorted(puntos, key=lambda r: r[0])

            pun.append(punt)

            print('este es cont antes del if', cont)
            print('antes del if', puntos)
            if contador == cont or contador == 1 or contador == 5 or contador == 85 or contador == 90:

                print('adentro del if', pun)
                print('este es cont', cont)
                cv2.drawContours(img, [approx], 0, (0, 0, 255), 2)
                imgResizei = cv2.resize(img, (1024, 600))
                cv2.imshow("wfb", imgResizei)
                cont = cont + 5
                cv2.waitKey(0)





#imgResizei = cv2.resize(img , (800, 600))
#cv2.imshow("w", imgResizei)

# imgResizeifb = cv2.resize(fin , (1600, 800))
# cv2.imshow("wfb", imgResizeifb)
cv2.waitKey(0)
cv2.destroyWindow()