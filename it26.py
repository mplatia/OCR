import cv2
import numpy as  np

img=cv2.imread(r'Imagenes/it22.jpeg',1) # Leer imagen
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Convierta la imagen en una imagen en escala de grises
kernel=np.ones((1,1),np.uint8) # Kelner
erosion=cv2.erode(gray,kernel,iterations=1) #Expansión
ditalacion=cv2.dilate(erosion,kernel,iterations=2) #Dilatacion
ret, thresh = cv2.threshold(ditalacion, 100, 255, cv2.THRESH_BINARY_INV) # Procesamiento de umbral Método binario
thresh1 = cv2.GaussianBlur(thresh,(3,3),0)# Filtro gaussiano


black = np.zeros((img.shape[0], img.shape[1], 3), np.uint8) #---black in RGB


# black1 = cv2.rectangle(black,(3760, 50), (3840, 5260),(255, 255, 255), -1)   #--- ROI Vertical
# black1 = cv2.rectangle(black,(150, 0), (3720, 10),(255, 255, 255), -1)   #--- ROI Horizontal
#black4 = cv2.rectangle(black,(100, 2700), (2000, 4100),(255, 255, 255), -1)   #--- ROI Horizontal
black2 = cv2.rectangle(black,(0, 0), (400, 2000),(255, 255, 255), -1)  # --- ROI vertical
# black3 = cv2.rectangle(black2,(3770, 60), (3850, 4200),(255, 255, 255), -1)  # --- ROI vertical
grayb = cv2.cvtColor(black2,cv2.COLOR_BGR2GRAY)               #--- gray
ret,b_mask = cv2.threshold(grayb,150,255, cv2.THRESH_BINARY)                #--- image
fin = cv2.bitwise_and(thresh1,grayb,mask = b_mask)
contours,hirearchy=cv2.findContours(fin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
l1h = cv2.line(img, (0, 50), (400, 50), (0, 255, 255), 10)
l1v = cv2.line(img, (50, 0), (35, 5000), (0, 0, 255), 10)
dy = 170
for l in range(9):
     yy = dy * l
     lh = cv2.line(img, (0, 50 + yy), (400, 50 + yy), (0, 255, 0), 10)


area=[]
contours1=[]

for i in contours:
     # area.append(cv2.contourArea(i))
     ver_area = cv2.contourArea(i)
    # Calcula el área y elimina las áreas pequeñas

     if cv2.contourArea(i)>1000:
        contours1.append(i)

     # print('ver area: ', ver_area)

for i,j in zip(contours1,range(len(contours1))):
    M = cv2.moments(i)
    cX=int(M["m10"]/M["m00"])
    cY=int(M["m01"]/M["m00"])
    draw = cv2.drawContours(img, contours1, -1, (0, 255, 0), 10)
    draw1 =cv2.putText(draw, str(j), (cX, cY), 1,1.5, (0, 0, 0), 5) # Dibujar números en el punto central de coordenadas
    # print('Este es el centroide: ', j,cX ,cY, cv2.contourArea(i) )
    #imgResize = cv2.resize(img,  (1000, 600))
    #cv2.imshow("6 d", imgRe


    imgResizei = cv2.resize(img , (1200, 800))
    cv2.imshow("w", imgResizei)
    cv2.waitKey(0)


imgResizeif = cv2.resize(fin , (600, 400))
cv2.imshow("f", imgResizeif)

cv2.waitKey(0)
cv2.destroyWindow()
