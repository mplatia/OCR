import cv2
import numpy as  np
import pytesseract
from pylibdmtx.pylibdmtx import decode
from imutils.object_detection import non_max_suppression

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

img=cv2.imread(r'Imagenes/pliegomitad.jpg',1) # Leer imagen

def dataMat(image, bgr):

    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data = decode(gray_img)
    # print(data)
    for decodedObject in data:
        points = decodedObject.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        # cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        cv2.putText(frame, decodedObject.data.decode("utf-8") , (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,bgr, 2)

        # print("Barcode: {} ".format(decodedObject.data.decode("utf-8")))
        for barcode in data:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y - h), (0, 255, 0), 2)
            cv2.putText(img, str(barcode), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, bgr, 2)
            print(barcode)

gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray1, 100, 255)
kernel2 = np.ones((3, 3), np.uint8)
canny = cv2.dilate(canny, kernel2, iterations=1)
cnts, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
l1v = cv2.line(img, ( 3700,  70), ( 3680, 3000), (0, 0, 0), 8)
l1h = cv2.line(img, (180, 70), (3705,  70), (0, 0, 0), 8)


for c in cnts:
    epsilon = 0.01 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    area2 = cv2.contourArea(c)
    # if area2 > 104000:
    if area2 > 6500 and area2 < 8000:
        if len(approx) == 4:
            # cv2.drawContours(img, [approx], 0, (0, 0, 255), 2)
            x, y, w, h = cv2.boundingRect(c)
            # cv2.rectangle(img, (x- 265, y - 100), (x + w + 230, y + h + 8), (0, 0, 0), 2, cv2.LINE_AA)
            l1v = cv2.line(img, (x - 265, y - 100), (x -265, y + h + 20), (0, 0, 0), 8)
            l1h = cv2.line(img, (x - 265 , y + 100), (x + 320, y + 100), (0, 0, 0), 8)
            frame = img[y:y + h, x:x + w]  # y:y+h, x:x+w
            bgr = (0, 255, 0)
            code = dataMat(frame, bgr)
            #cv2.imshow("w", frame)

            #cv2.waitKey(0)

gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

canny1 = cv2.Canny(gray2, 100, 255)
kernel3 = np.ones((3, 3), np.uint8)
cnts1, hierarchy1 = cv2.findContours(gray2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


# print(contador)
imgResizei = cv2.resize(img , (1600, 800))
cv2.imshow("w", imgResizei)

# imgResizeifb = cv2.resize(fin , (1600, 800))
# cv2.imshow("wfb", imgResizeifb)
cv2.waitKey(0)
cv2.destroyWindow()