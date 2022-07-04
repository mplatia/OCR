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

Lista = []

def dataMat(recorte, bgr):
    global code
    # image = cv2.imread('Imagenes/p6.jpeg', cv2.IMREAD_UNCHANGED);
    gray_img = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    data = decode(gray_img)
    # print(data)
    # for decodedObject in data:
    #     # points = decodedObject.rect
    #     # pts = np.array(points, np.int32)
    #     # pts = pts.reshape((-1, 1, 2))
    #     # cv2.polylines(image, [pts], True, (0, 255, 0), 3)
    #
    #     cv2.putText(recorte, decodedObject.data.decode("utf-8") , (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,bgr, 2)

        # print("Barcode: {} ".format(decodedObject.data.decode("utf-8")))
    for barcode in data:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        x1, y1, w1, h1 = barcode.rect
        print('barcode: ', x1, y1, w1, h1)
        cv2.rectangle(recorte, (x1, w1), (x1+w1, w1+h1), (0, 255, 0), 2)
        print('x1:',x1, 'y1:',w1)
        print ('x1 + w1',x1 + w1,'w1+h1: ', w1+h1)
        # cv2.putText(recorte, str(barcode), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, bgr, 2)
        cv2.imshow("recorte con OCR", recorte)
        cv2.waitKey(0)
        # print(barcode)
        # print(len(barcode))


def ocr():
    print('holaaa')

for c in cnts:
    # epsilon = 0.01 * cv2.arcLength(c, True)
    # approx = cv2.approxPolyDP(c, epsilon, True)
    # area2 = cv2.contourArea(c)

    x, y, w, h = cv2.boundingRect(c)


    if  x != 0 and y != 0:
        # print(x, y, w, h)
        recorte = draw1[y:y+h, x:x+w]# y:y+h, x:x+w
        imgResize = cv2.resize(draw1, (1260, 860))
        boxes = pytesseract.image_to_data(recorte)
        for a, b in enumerate(boxes.splitlines()):
             # print(b)
            if a != 0:
                b = b.split()
                print(b)
                 # if len(b)==12 and (b[11] == '202702' or b[11] == '820022' or  b[11] == '|T27-7YS' or b[11] == 'Integron®') :
                if len(b) == 12 and (b[11] == 'Integron®' or  b[11] == '|T27-7YS'):
                    x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                    cv2.putText(recorte, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
                    cv2.rectangle(recorte , (x, y), (x + w, y + h), (50, 50, 255), 2)
        bgr = (0,255,0)

        #cv2.imshow("recorte con OCR", recorte)
        # code = dataMat(recorte, bgr)

        #cv2.waitKey(0)



                        # recorte = draw1[692:895, 665:1289] #y:y+h, x:x+w


# Mostrar imágenes
imgResize = cv2.resize(draw1,(800,600))
cv2.imshow("draw1", imgResize)
cv2.waitKey(0)
cv2.destroyWindow()
