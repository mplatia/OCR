import cv2
import numpy as  np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

img=cv2.imread(r'C:\Users\Maxi\Desktop\proyectosCV\OCR\Imagenes\p123.jpeg',1) # Leer imagen
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Convierta la imagen en una imagen en escala de grises
kernel=np.ones((8,8),np.uint8) # Kelner
erosion=cv2.erode(gray,kernel,iterations=2) #Expansión
ditalacion=cv2.dilate(erosion,kernel,iterations=1) #Dilatacion
ret, thresh = cv2.threshold(ditalacion, 180, 255, cv2.THRESH_BINARY) # Procesamiento de umbral Método binario
thresh1 = cv2.GaussianBlur(thresh,(5,5),0)# Filtro gaussiano


black = np.zeros((img.shape[0], img.shape[1], 3), np.uint8) #---black in RGB

black1 = cv2.rectangle(black,(300, 200), (200, 1100),(255, 255, 255), -1)   #--- ROI
black2 = cv2.rectangle(black1,(300, 200), (600, 300),(255, 255, 255), -1) # (500, 200), (200, abajo)
grayb = cv2.cvtColor(black2,cv2.COLOR_BGR2GRAY)               #--- gray
ret,b_mask = cv2.threshold(grayb,127,255, 0)                #--- image
fin = cv2.bitwise_and(thresh1,grayb,mask = b_mask)
contours,hirearchy=cv2.findContours(fin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

area=[]
contours1=[]
for i in contours:
     # area.append(cv2.contourArea(i))
     ver_area = cv2.contourArea(i)
    # Calcula el área y elimina las áreas pequeñas
     if cv2.contourArea(i)> 300 and cv2.contourArea(i)< 1300:
         contours1.append(i)

     #print('ver area: ', ver_area)


# Encuentra el centro  y dibuja el número en el punto de coordenadas del centro
for i,j in zip(contours1,range(len(contours1))):
    M = cv2.moments(i)
    cX=int(M["m10"]/M["m00"])
    cY=int(M["m01"]/M["m00"])
    draw = cv2.drawContours(img, contours1, -1, (0, 0, 255), 2)
    draw1=cv2.putText(draw, str(j), (cX, cY), 1,1.5, (0, 0, 0), 2) # Dibujar números en el punto central de coordenadas
    l1h = cv2.line(img, (1600, cY), (cX, cY), (0, 0, 0), 4)
    l2h = cv2.line(img, (1600, 1110), (244, 1100), (0, 0, 0), 4)
    l1v = cv2.line(img, (305, 200), (305, 1120), (0, 0, 0), 4)
    l2v = cv2.line(img, (930, 200), (930, 1120), (0, 0, 0), 4)
    l3v = cv2.line(img, (1550, 200), (1550, 1120), (0, 0, 0), 4)
    #print('Esta es la j: ', j,cX ,cY )
gray1 = cv2.cvtColor(draw1, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray1, 10, 150)
canny = cv2.dilate(canny, None, iterations=1)

cnts, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in cnts:
    area2 = cv2.contourArea(c)
    #print(area2)
    if area2 > 118075 and area2 < 158075 :
        x, y, w, h = cv2.boundingRect(c)
        if x != 0 and y != 0:
            recorte = draw1[y:y + h, x:x + w]  # y:y+h, x:x+w
            imgResize = cv2.resize(recorte, (800, 600))
            image_norm = cv2.rotate(recorte, cv2.ROTATE_180)
            boxes = pytesseract.image_to_data(image_norm)
            for a, b in enumerate(boxes.splitlines()):
                if a != 0:
                    b = b.split()
                    print(b)
                    # if len(b) == 12 and (b[11] == 'Integron®' or b[11] == '|T27-7YS'):
                    if len(b) == 12 and (b[11] == 'Integron®' or b[11] == '|T27-7YS'):
                        x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                        cv2.putText(recorte, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
                        cv2.rectangle(image_norm, (x, y), (x + w, y + h), (50, 50, 255), 2)

            cv2.imshow("recorte con OCR", image_norm)
            cv2.waitKey(0)
#Mostrar imágenes

imgResize = cv2.resize(draw1,(800,600))
#imgResizef = cv2.resize(fin,(800,600))
#imgResize2 = cv2.resize(black2,(800,600))


#cv2.imshow("2 Erosion",imgResizef)
#cv2.imshow("3 Dilatacion",imgResize2)
#cv2.imshow("4 Thresh",thresh)
#cv2.imshow("5 thresh1",thresh1)
#imgResizer = cv2.resize(roi,(100,700))
#cv2.imshow("roi",imgResizer)
cv2.imshow("6 draw",imgResize)


cv2.waitKey(0)
cv2.destroyWindow()
