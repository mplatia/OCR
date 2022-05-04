import cv2
import numpy as np

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
for i in contours:
    # area.append(cv2.contourArea(i))
    ver_area = cv2.contourArea(i)

    # if cv2.contourArea(i)>506 and cv2.contourArea(i)<510:   # Calcula el área y elimina las áreas pequeñas
    if cv2.contourArea(i) == 58:  # Calcula el área y elimina las áreas pequeñas
        contours1.append(i)
        print('ver area: ', ver_area)
# Encuentra el centro  y dibuja el número en el punto de coordenadas del centro
for i, j in zip(contours1, range(len(contours1))):
    M = cv2.moments(i)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # if cX == 1308 or cY == 1017:
    if cX == 1354 or cY == 950:
        draw1 = cv2.putText(img, ('este es el punto' + str(j)), (cX, cY), 1, 1.5, (0, 0, 255), 2)

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


# contrar puntos

def ordenar_puntos(puntos):
    n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()

    y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1])

    x1_order = y_order[:2]
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])

    x2_order = y_order[2:4]
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])

    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]


gray1 = cv2.cvtColor(draw1, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray1, 10, 150)
canny = cv2.dilate(canny, None, iterations=1)

cnts, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in cnts:
    epsilon = 0.01 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    area2 = cv2.contourArea(c)
    # print('area2', area2)

    if area2 > 124891:

        if len(approx) == 4:
            cv2.drawContours(draw1, [approx], 0, (0, 0, 0), 2)

            puntos = ordenar_puntos(approx)

        p1 = cv2.circle(draw1, tuple(puntos[0]), 7, (255, 0, 0), 2)
        p2 = cv2.circle(draw1, tuple(puntos[1]), 7, (0, 255, 0), 2)
        p3 = cv2.circle(draw1, tuple(puntos[2]), 7, (0, 0, 255), 2)
        p4 = cv2.circle(draw1, tuple(puntos[3]), 7, (255, 255, 0), 2)
        print(tuple(puntos[0]),puntos[1],puntos[2],puntos[3])

# Mostrar imágenes
imgResize = cv2.resize(draw1, (1260, 860))
cv2.imshow("6 draw", imgResize)
cv2.waitKey()
cv2.destroyWindow()
