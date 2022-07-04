import cv2
import numpy as  np
import pytesseract

img=cv2.imread(r'Imagenes/pliego11.jpg',1) # Leer imagen
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Convierta la imagen en una imagen en escala de grises
kernel=np.ones((3,3),np.uint8) # Kelner
erosion=cv2.erode(gray,kernel,iterations=1) #Expansión
ditalacion=cv2.dilate(erosion,kernel,iterations=2) #Dilatacion
ret, thresh = cv2.threshold(ditalacion, 10, 255, cv2.THRESH_BINARY) # Procesamiento de umbral Método binario
thresh1 = cv2.GaussianBlur(thresh,(3,3),0)# Filtro gaussiano

black = np.zeros((img.shape[0], img.shape[1], 3), np.uint8) #---black in RGB


# black1 = cv2.rectangle(black,(3760, 50), (3840, 5260),(255, 255, 255), -1)   #--- ROI Vertical
black1 = cv2.rectangle(black,(150, 50), (1800, 100),(255, 255, 255), -1)   #--- ROI Horizontal
black2 = cv2.rectangle(black1,(40, 100), (80, 4200),(255, 255, 255), -1)  # --- ROI vertical
black3 = cv2.rectangle(black1,(2030, 100), (2045, 4200),(255, 255, 255), -1)  # --- ROI vertical
grayb = cv2.cvtColor(black3,cv2.COLOR_BGR2GRAY)               #--- gray
ret,b_mask = cv2.threshold(grayb,120,255, 0)                #--- image
fin = cv2.bitwise_and(erosion,grayb,mask = b_mask)
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
    draw1=cv2.putText(draw, str(j), (cX, cY), 1,1.5, (0, 0, 0), 5) # Dibujar números en el punto central de coordenadas
    #l1v = cv2.line(img, (cX , cY), (cX, 11000), (0, 0, 255), 5)
    # larribah = cv2.line(img, (131, 72), (3790, 62), (0, 255, 0), 8)
    # labajoh = cv2.line(img, (3779, 5168), (124, 5197), (0, 0, 0), 8)

    # dy = 190
    # dy1= 190
    # for l in range(14):
    #     yy = dy * l
    #     yy1 = dy1 * l
    #     lh = cv2.line(img, (131, 72 + yy), (3790, 62 + yy) , (0, 0, 255), 8)
    #     lh2 = cv2.line(img, (124, 5185 - yy), (3779, 5168 - yy), (255, 0, 0), 8)

        #l1v = cv2.line(img, (cX, 0), (cX, cY), (0, 255, 0), 4)
        # l2h = cv2.line(img, (1600, 1110), (244, 1100), (0, 0, 0), 4)
        # l1v = cv2.line(img, (305, 200), (305, 1120), (0, 0, 0), 4)
        # l2v = cv2.line(img, (930, 200), (930, 1120), (0, 0, 0), 4)
        # l3v = cv2.line(img, (1550, 200), (1550, 1120), (0, 0, 0), 4)
    # print('Este es el centroide: ', j,cX ,cY, cv2.contourArea(i) )
    # imgResize = cv2.resize(img, (600, 800))
    # cv2.imshow("6 d", imgResize)





# imgResize = cv2.resize(img, (640, 800))
# cv2.imshow("6 d", imgResize)

imgResize = cv2.resize(fin, (800, 1000))
cv2.imshow("6 d", imgResize)

imgResize1 = cv2.resize(black3 , (800, 1000))
cv2.imshow("6 draw", imgResize1)
imgResizei = cv2.resize(img , (800, 1000))
cv2.imshow("w", imgResizei)
cv2.waitKey(0)
cv2.destroyWindow()
