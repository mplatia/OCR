import cv2
import numpy as np

# src = cv2.imread(r"Imagenes/p6.jpeg")  # Leer foto
# ROI = np.zeros(src.shape,
#                np.uint8)  # Cree una matriz vacía vacía del mismo tamaño que la imagen original para el almacenamientoROIInformación
#
# gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)  # Escala de grises
# ret, binary = cv2.threshold(gray,
#                            0, 255,
#                            cv2.THRESH_BINARY_INV | cv2.THRESH_TRIANGLE)  # Binarización adaptativa
#
# contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Buscar todos los contornos, cada información de contornos se almacena en la matriz de contornos
#
# for cnt in range(len(contours)):  # Procesar cada contorno en función de la cantidad de contornos
#     # Aproximación de contorno, los principios específicos deben estudiarse en profundidad
#     epsilon = 0.01 * cv2.arcLength(contours[cnt], True)
#     approx = cv2.approxPolyDP(contours[cnt], epsilon,
#                              True)  # Guardar la información de vértice del resultado de aproximación
#     # El número de vértices determina la forma del contorno
#     # Calcular la posición del centro del contorno
#     mm = cv2.moments(contours[cnt])
#     if mm['m00'] != 0:
#         cx = int(mm['m10'] / mm['m00'])
#         cy = int(mm['m01'] / mm['m00'])
#         color = src[cy][cx]
#         color_str = "(" + str(color[0]) + ", " + str(color[1]) + ", " + str(color[2]) + ")"
#         p = cv2.arcLength(contours[cnt], True)
#         area = cv2.contourArea(contours[cnt])
#
#         # Analizar geometría
#         corners = len(approx)
#         if corners == 3 and (color[2] >= 150 or color[
#             0] >= 150) and area > 1000:  # Una serie de condiciones de juicio son ajustadas por las características del proyecto
#             cv2.drawContours(ROI, contours, cnt, (255, 255, 255),-1)  # AROIDibuje un contorno en el lienzo vacío y llénelo de blanco (el último parámetro es el ancho de la línea del contorno, si es un número negativo, llenará directamente el área)
#             imgroi = ROI & src  # ROIY la imagen original para filtrar la imagen originalROIzona
#             cv2.imshow("ROI", imgroi)
#             # cv2.imwrite(r"ROI.jpg")
#
#         if corners >= 10 and (color[2] >= 150 or color[0] >= 150) and area > 1000:
#             cv2.drawContours(ROI, contours, cnt, (255, 255, 255), -1)
#             imgroi = ROI & src
#             cv2.imshow("ROI", imgroi)
#             # cv2.imwrite(r"ROI.jpg")
#
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()


