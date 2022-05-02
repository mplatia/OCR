import cv2
import numpy as  np





img=cv2.imread(r'Imagenes/p9.jpeg',1) # Leer imagen
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Convierta la imagen en una imagen en escala de grises
kernel=np.ones((4,4),np.uint8) # Kelner
erosion=cv2.erode(gray,kernel,iterations=2) #Expansión
ditalacion=cv2.dilate(erosion,kernel,iterations=1) #Dilatacion
ret, thresh = cv2.threshold(ditalacion, 180, 255, cv2.THRESH_BINARY) # Procesamiento de umbral Método binario
thresh1 = cv2.GaussianBlur(thresh,(3,3),0)# Filtro gaussiano
# imgCanny = cv2.Canny(thresh1, 100,100)
contours,hirearchy=cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)# Encuentra loscontornos

area=[]
contours1=[]
for i in contours:
     # area.append(cv2.contourArea(i))
     ver_area = cv2.contourArea(i)


     # if cv2.contourArea(i)>506 and cv2.contourArea(i)<510:   # Calcula el área y elimina las áreas pequeñas
     if cv2.contourArea(i)>10:  # Calcula el área y elimina las áreas pequeñas
        contours1.append(i)
        print('ver area: ', ver_area)
print(len(contours1)-1) #Calcular la cantidad de dominios conectados

draw=cv2.drawContours(img,contours1,-1,(0,0,0),2) #Representar dominios conectados
draw1=cv2.putText(draw, str('Puntos encontrados: ')+ str(len(contours1)), (10, 50), 1,1.5, (0, 255, 0), 2)
# Encuentra el centro  y dibuja el número en el punto de coordenadas del centro
for i,j in zip(contours1,range(len(contours1))):


	M = cv2.moments(i)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])

	if cX == 1308 or cY == 1017:
	    draw1=cv2.putText(draw1, ('este es el punto'+ str(j)), (cX, cY), 1,1.5, (0, 0, 255), 2)
        print('Esta es la j: ', j, 'estas es la x: ', cX, 'esta es la y: ', cY)



#Mostrar imágenes
imgResize = cv2.resize(draw1,(600,800))
# cv2.imshow("1 gris",gray)
#cv2.imshow("2 Erosion",erosion)
#cv2.imshow("3 Dilatacion",ditalacion)
#cv2.imshow("4 Thresh",thresh)
#cv2.imshow("5 thresh1",thresh1)
cv2.imshow("6 draw",imgResize)


cv2.waitKey()
cv2.destroyWindow()
