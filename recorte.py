import cv2
import numpy as np
import pytesseract
from pylibdmtx.pylibdmtx import decode

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

img = cv2.imread(r'Imagenes/p11.jpeg', 1)  # Leer imagen
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convierta la imagen en una imagen en escala de grises
kernel = np.ones((4, 4), np.uint8)  # Kelner
erosion = cv2.erode(gray, kernel, iterations=2)  # Expansión
ditalacion = cv2.dilate(erosion, kernel, iterations=1)  # Dilatacion
ret, thresh = cv2.threshold(ditalacion, 180, 255, cv2.THRESH_BINARY)  # Procesamiento de umbral Método binario
thresh1 = cv2.GaussianBlur(thresh, (3, 3), 0)  # Filtro gaussiano
# imgCanny = cv2.Canny(thresh1, 100,100)
contours, hirearchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Encuentra loscontornos

area = []
contours1 = []

#Detecta el punto y dibuja
for i in contours:
    # area.append(cv2.contourArea(i))
    ver_area = cv2.contourArea(i)

    # if cv2.contourArea(i)>506 and cv2.contourArea(i)<510:   # Calcula el área y elimina las áreas pequeñas
    if cv2.contourArea(i) == 58:  # Calcula el área y elimina las áreas pequeñas
        contours1.append(i)
# Encuentra el centro  y dibuja el número en el punto de coordenadas del centro
for i, j in zip(contours1, range(len(contours1))):
    M = cv2.moments(i)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # if cX == 1308 or cY == 1017:
    if cX == 1354 or cY == 950:
        draw = cv2.drawContours(img, contours1, -1, (0, 0, 0), 2)
        draw1 = cv2.putText(draw, ('este es el punto' + str(j)), (cX, cY), 1, 1.5, (0, 0, 255), 2)

        # l1v = cv2.line(img, (cX, 0), (cX, cY), (0, 0, 0), 4)
        # l1h = cv2.line(img, (0, cY), (cX, cY), (0, 0, 255), 4)

        l2h = cv2.line(img, (0, cY - 55), (cX, cY - 55), (0, 255, 0), 4)
        l3h = cv2.line(img, (0, cY - 259), (cX, cY - 259), (0, 255, 0), 4)
        l4h = cv2.line(img, (0, cY - 461), (cX, cY - 461), (0, 255, 0), 4)
        l5h = cv2.line(img, (0, cY - 664), (cX, cY - 664), (0, 255, 0), 4)
        l6h = cv2.line(img, (0, cY - 855), (cX, cY - 855), (0, 255, 0), 4)

        l2v = cv2.line(img, (cX - 65, 0), (cX - 65, cY), (0, 255, 0), 4)
        l2v = cv2.line(img, (cX - 690, 0), (cX - 690, cY), (0, 255, 0), 4)
        l3v = cv2.line(img, (cX - 1313, 0), (cX - 1313, cY), (0, 255, 0), 4)
    # print('Esta es la j: ', j, 'estas es la x: ', cX, 'esta es la y: ', cY)


# Recorta Indicador
gray1 = cv2.cvtColor(draw1, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray1, 10, 150)
canny = cv2.dilate(canny, None, iterations=1)

cnts, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        #cv2.waitKey(0)




cv2.destroyWindow()
