import cv2
import numpy as  np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

img=cv2.imread(r'Imagenes/pliego1.jpg',1) # Leer imagen
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Convierta la imagen en una imagen en escala de grises
kernel=np.ones((1,1),np.uint8) # Kelner
erosion=cv2.erode(gray,kernel,iterations=1) #Expansión
ditalacion=cv2.dilate(erosion,kernel,iterations=2) #Dilatacion
ret, thresh = cv2.threshold(ditalacion, 190, 255, cv2.THRESH_BINARY_INV) # Procesamiento de umbral Método binario
thresh1 = cv2.GaussianBlur(thresh,(3,3),0)# Filtro gaussiano


black = np.zeros((img.shape[0], img.shape[1], 3), np.uint8) #---black in RGB


# black1 = cv2.rectangle(black,(3760, 50), (3840, 5260),(255, 255, 255), -1)   #--- ROI Vertical
black1 = cv2.rectangle(black,(150, 0), (3720, 10),(255, 255, 255), -1)   #--- ROI Horizontal
#black4 = cv2.rectangle(black,(100, 2700), (2000, 4100),(255, 255, 255), -1)   #--- ROI Horizontal
black2 = cv2.rectangle(black1,(0, 100), (40, 4200),(255, 255, 255), -1)  # --- ROI vertical
black3 = cv2.rectangle(black2,(3770, 60), (3850, 4200),(255, 255, 255), -1)  # --- ROI vertical
grayb = cv2.cvtColor(black3,cv2.COLOR_BGR2GRAY)               #--- gray
ret,b_mask = cv2.threshold(grayb,190,255, cv2.THRESH_BINARY)                #--- image
fin = cv2.bitwise_and(thresh1,grayb,mask = b_mask)
contours,hirearchy=cv2.findContours(fin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

area=[]
contours1=[]

for i in contours:
     # area.append(cv2.contourArea(i))
     ver_area = cv2.contourArea(i)
    # Calcula el área y elimina las áreas pequeñas
     if cv2.contourArea(i)>10:
        contours1.append(i)

     # print('ver area: ', ver_area)


# Encuentra el centro  y dibuja el número en el punto de coordenadas del centro
for i,j in zip(contours1,range(len(contours1))):

    M = cv2.moments(i)
    cX=int(M["m10"]/M["m00"])
    cY=int(M["m01"]/M["m00"])
    draw = cv2.drawContours(img, contours1, -1, (0, 0, 255), 2)
    draw1 =cv2.putText(draw, str(j), (cX, cY), 1,1.5, (0, 0, 0), 5) # Dibujar números en el punto central de coordenadas
    l1v = cv2.line(draw1, (cX , cY), (cX, 11000), (0, 0, 0), 10)
    l1h = cv2.line(draw1, (150, cY + 15), (cX, cY), (0, 0, 0), 10)
    # print('Este es el centroide: ', j,cX ,cY, cv2.contourArea(i) )
    #imgResize = cv2.resize(img,  (1000, 600))
    #cv2.imshow("6 d", imgResize)
    #cv2.waitKey(0)
gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray1, 110, 130)
kernel2=np.ones((3,3),np.uint8)
canny = cv2.dilate(canny, kernel2, iterations=1)

# imgResizec = cv2.resize(canny , (1000, 600))
# cv2.imshow("w", imgResizec)
def ordenar_puntos(puntos):
    n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()

    y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1])

    x1_order = y_order[:2]
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])

    x2_order = y_order[2:4]
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])

    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]
indicador = 0
tabla = []
palabras = []
lista_comparar = ['Integron®', '|T27-7YS', '2027-02' ]
cnts, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in cnts:
    epsilon = 0.01 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    area2 = cv2.contourArea(c)
    # print(area2)
    #if area2 > 90000 and area2 < 15076650:
    if area2 > 101450 and area2 < 225080:
        # print(len(approx))
        if len(approx) == 4:
            cv2.drawContours(img, [approx], 0, (0, 0, 255), 5)
            puntos = ordenar_puntos(approx)
            p1 = cv2.circle(draw1, tuple(puntos[0]), 7, (255, 0, 0), 2)
            p2 = cv2.circle(draw1, tuple(puntos[1]), 7, (0, 255, 0), 2)
            p3 = cv2.circle(draw1, tuple(puntos[2]), 7, (0, 0, 255), 2)
            p4 = cv2.circle(draw1, tuple(puntos[3]), 7, (255, 255, 0), 2)

        x, y, w, h = cv2.boundingRect(c)
        if x != 0 and y != 0:
            recorte = draw1[y:y + h, x:x + w]  # y:y+h, x:x+w
            indicador = indicador+1
            #imgResize = cv2.resize(recorte, (800, 600))
            # recortegris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
            boxes = pytesseract.image_to_data(recorte)
            for a, b in enumerate(boxes.splitlines()):
                if a != 0:
                    b = b.split()
                    #if len(b) == 12 and (b[11] == 'Integron®' or b[11] == '|T27-7YS' or b[11] == '2027-02'):
                    #if len(b) == 12 and (b[11] == 'Integron®' or b[11] == '|T27-7YS' or b[11] == '2027-02' or b[11] == '820022'):
                    if len(b) == 12 and (
                            b[11] == 'Integron®' or b[11] == '|T27-7YS' or b[11] == '2027-02' or b[11] == '820022' or b[
                        11] == '2027.02' or b[11] == '02'
                            or b[11] == '2027' or b[11] == 'B20022'):
                        # print(b)
                        nob = indicador, b[11], x,y,w,h
                        palabras.append(nob)
                        # print(palabras)
                        # if b[11] == 'Integron®':
                        #     # print('arriba:',b)
                        x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                        cv2.putText(recorte, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
                        cv2.rectangle(recorte, (x, y), (x + w, y + h), (50, 50, 255), 2)
                            # atributos = indicador, 'Integron®', x,y,w,h
                        #     # break
                        #     # tabla.append(atributos)
                        #     if b[11] == '|T27-7YS':
                        #         # print('arriba:',b)
                        #         x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                        #         cv2.putText(recorte, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
                        #         cv2.rectangle(recorte, (x, y), (x + w, y + h), (50, 50, 255), 2)
                        #         atributos = indicador, 'Integron®', 'IT27-7YS',  x, y, w, h
                        #         break
                        #         # tabla.append(atributos)
                        # if len(b) == 11:
                        #     atributos = indicador, 'no tiene IT27-7YS'

            # tabla.append(atributos)
            # print(palabras)

            # imgResize = cv2.resize(draw1, (600, 800))
            # cv2.imshow("6 dd", recorte)
            # cv2.waitKey(0)

# [item for item in palabras if item[1] == lista_comparar[0]]
for i in range(len(palabras)):
    for p in range(len(lista_comparar)):
        # print(len(lista_comparar))
        # print('Indicador', palabras[i][0], 'pcom: ', lista_comparar[p] , 'palabras[i][1]: ', palabras[p][1])
        if lista_comparar[p] ==  palabras[p][1]:
            print('EN EL INDICADOR: ', palabras[i][0], 'SE ENCONTRARON LAS PALABRAS:',  palabras[i][1])
            break
        if lista_comparar[p] !=  palabras[p][1]:
            print('EN EL INDICADOR: ', palabras[i][0], 'NO SE ENCONTRARON LAS PALABRAS:', lista_comparar[p])
            break
# imgResize = cv2.resize(img, (640, 800))
# cv2.imshow("6 d", imgResize)

# imgResize = cv2.resize(fin, (500, 700))
# cv2.imshow("6 d", imgResize)
#
# imgResize1 = cv2.resize(grayb , (500, 700))
# cv2.imshow("6 grayb", imgResize1)
imgResizei = cv2.resize(img , (800, 600))
cv2.imshow("w", imgResizei)
cv2.waitKey(0)
cv2.destroyWindow()
