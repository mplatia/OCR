import cv2
import numpy as  np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

img=cv2.imread(r'Imagenes/pliego.jpg',1) # Leer imagen
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Convierta la imagen en una imagen en escala de grises
kernel=np.ones((1,1),np.uint8) # Kelner
erosion=cv2.erode(gray,kernel,iterations=1) #Expansión
ditalacion=cv2.dilate(erosion,kernel,iterations=2) #Dilatacion
ret, thresh = cv2.threshold(ditalacion, 180, 255, cv2.THRESH_BINARY_INV) # Procesamiento de umbral Método binario
thresh1 = cv2.GaussianBlur(thresh,(3,3),0)# Filtro gaussiano



black = np.zeros((img.shape[0], img.shape[1], 3), np.uint8) #---black in RGB

black1 = cv2.rectangle(black,(200, 100), (600, 4000),(255, 255, 255), -1)   #--- ROI Vertical1

# xb1 , xb2 = 200 , 600
# yb1 , yb2 = 100 , 200
# black1 = cv2.rectangle(black,(xb1, yb1), (xb2, yb2),(255, 255, 255), -1)
# dist= 200

# for r in range(28):
    # xr = dist * r
    # roi = cv2.rectangle(black,(xb1, yb1 + xr), (xb2, yb2 + xr),(255, 255, 255), -1)  # --- ROI horizontal3
# black3 = cv2.rectangle(black,(3700, 0), (3850, 200),(255, 255, 255), -1)  # --- ROI horizontal2
# black4 = cv2.rectangle(black3,(0, 5180), (230, 5280),(255, 255, 255), -1)  # --- ROI horizontal4
grayb = cv2.cvtColor(black1,cv2.COLOR_BGR2GRAY)               #--- gray
ret,b_mask = cv2.threshold(grayb,10,255, 0)                #--- image
fin = cv2.bitwise_and(thresh1,grayb,mask = b_mask)
contours,hirearchy=cv2.findContours(fin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

boxes = pytesseract.image_to_data(fin)
for a, b in enumerate(boxes.splitlines()):
    if a != 0:
        # print(a)
        b = b.split()
        # print(b)
        if len(b) == 12:
            # if len(b) == 12:
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
            cv2.putText(fin, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
            nob = y-25
            nob1 = y - 35
            l1h = cv2.line(img, (0, nob), (3800, nob1 ), (0, 0, 0), 6)
            dx = 188
            dx2 = 190
            dy = 620
            for l in range(28):
                xx = dx * l
                xx1 = dx2 * l
                yy = dy * l
                #lh = cv2.line(img, (0, nob + xx), (4000, nob + xx1 ), (0, 0, 0), 6)


# # Encuentra el centro  y dibuja el número en el punto de coordenadas del centro
# for i,j in zip(contours1,range(len(contours1))):
#     M = cv2.moments(i)
#     cX=int(M["m10"]/M["m00"])
#     cY=int(M["m01"]/M["m00"])
#     draw = cv2.drawContours(img, contours1, -1, (0, 0, 255), 2)
#     draw1=cv2.putText(draw, str(j), (cX, cY), 1,1.5, (0, 255, 0), 50) # Dibujar números en el punto central de coordenadas
#
#     xv3, xv4 = 173, 148
#     yv3 , yv4 = 5221, 21
#
#     l1v = cv2.line(img,  (xv3, yv3), (xv4 , yv4), (0, 0, 255), 10)
#     l2v = cv2.line(img, (3707, 5222), (3708, 9), (0, 255, 255), 10)
#
#
#     xh1 , xh2 = 131 , 3747
#     yh1 , yh2 = 72 , 62
#     l1h = cv2.line(img, (xh1, yh1), (xh2, yh2), (0, 0, 0), 10)
#     l2h = cv2.line(img, (120, 5186), (3767, 5168), (255, 0, 0), 10)
#
#     dx = 194
#     dy = 620
# for l in range(26):
#     xx = dx * l
#     yy = dy * l
#     lh = cv2.line(img, (xh1, yh1 + xx), (xh2, yh2 + xx), (0, 0, 0), 10)
#     lv = cv2.line(img, (xv3 + yy, yv3), (xv4 + yy, yv4), (0, 0, 0), 10)
#
# gray1 = cv2.cvtColor(draw1, cv2.COLOR_BGR2GRAY)
# canny = cv2.Canny(gray1, 10, 150)
# kernel2=np.ones((4,4),np.uint8)
# canny = cv2.dilate(canny, kernel2, iterations=2)
#
# cnts, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# for c in cnts:
#     area2 = cv2.contourArea(c)
#     if area2 > 90000 and area2 < 15076650:
#         print(area2)
#         x, y, w, h = cv2.boundingRect(c)
#         if x != 0 and y != 0:
#             recorte = draw1[y:y + h, x:x + w]  # y:y+h, x:x+w
#             #imgResize = cv2.resize(recorte, (800, 600))
#             boxes = pytesseract.image_to_data(recorte)
#             for a, b in enumerate(boxes.splitlines()):
#                 if a != 0:
#                     print(a)
#                     b = b.split()
#                     print(b)
#                     if len(b) == 12 and (b[11] == 'Integron®' or b[11] == '|T27-7YS' or b[11] == '2027-02'):
#                     #if len(b) == 12:
#                         x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
#                         cv2.putText(recorte, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
#                         cv2.rectangle(recorte, (x, y), (x + w, y + h), (50, 50, 255), 2)
#
#         cv2.imshow("recorte con OCR", recorte)
#         cv2.waitKey(0)
    # print('Esta es la j: ', j,cX ,cY, 'AREA: ', cv2.contourArea(i) )
    # imgResizeH = cv2.resize(img, (500, 650))
    # cv2.imshow("recorte con OCR", imgResizeH)
    # cv2.waitKey(0)


imgResize1 = cv2.resize(fin,(600,700))
imgResize = cv2.resize(img,(600,800))
cv2.imshow("6 d",imgResize)
cv2.imshow("6 draw",imgResize1)


cv2.waitKey(0)

cv2.destroyWindow()
