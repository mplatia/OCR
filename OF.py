import cv2
import numpy as  np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

img=cv2.imread(r'Imagenes/IMG.jpg',1) # Leer imagen
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Convierta la imagen en una imagen en escala de grises
kernel=np.ones((1,1),np.uint8) # Kelner
erosion=cv2.erode(gray,kernel,iterations=2) #Expansión
ditalacion=cv2.dilate(erosion,kernel,iterations=2) #Dilatacion
ret, thresh = cv2.threshold(ditalacion, 170, 255, cv2.THRESH_BINARY_INV)
# Procesamiento de umbral Método binario
thresh1 = cv2.GaussianBlur(thresh,(1,1),0)# Filtro gaussiano

black = np.zeros((img.shape[0], img.shape[1], 3), np.uint8) #---black in RGB


# black1 = cv2.rectangle(black,(3760, 50), (3840, 5260),(255, 255, 255), -1)   #--- ROI Vertical
black1 = cv2.rectangle(black,(100, 50), (3600, 200),(255, 255, 255), -1)   #--- ROI Horizontal
#black4 = cv2.rectangle(black,(100, 2700), (2000, 4100),(255, 255, 255), -1)   #--- ROI Horizontal
# black2 = cv2.rectangle(black1,(0, 100), (40, 4200),(255, 255, 255), -1)  # --- ROI vertical
# black3 = cv2.rectangle(black2,(3770, 60), (3850, 4200),(255, 255, 255), -1)  # --- ROI vertical
grayb = cv2.cvtColor(black1,cv2.COLOR_BGR2GRAY)               #--- gray
ret,b_mask = cv2.threshold(grayb,10,255, cv2.THRESH_BINARY)                #--- image
fin = cv2.bitwise_and(thresh,grayb,mask = b_mask)
contours,hirearchy=cv2.findContours(fin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

area=[]
contours1=[]

boxes1 = pytesseract.image_to_data(fin)
for a, b in enumerate(boxes1.splitlines()):
    if a != 0:
        #print(a)
        b = b.split()
    dy = 190
    for l in range(1, 16):
        if len(b) == 12 and b[11] == 'Integron®':
        # if len(b) == 12:
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
            print(x)
            # cv2.putText(img, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(img, (x - 270, y + 165), (x + w + 225, y + h - 50), (0, 0, 0), 5)
            #cv2.rectangle(img, (x - 270, y + 180), (x + w + 245, y + h - 50), (0, 0, 0), 5)
            yy = dy * l
            cv2.rectangle(img, (x - 270, y + 165 + yy), (x + w + 225, y + h - 50 + yy), (0, 0, 0), 5)

def ordenar_puntos(puntos):
    n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()

    y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1])

    x1_order = y_order[:2]
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])

    x2_order = y_order[2:4]
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])

    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray1, 100, 255)
kernel2=np.ones((3,3),np.uint8)
canny = cv2.dilate(canny, kernel2, iterations=1)
cnts, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
palabras = []
for c in cnts:
    epsilon = 0.01 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    area2 = cv2.contourArea(c)
    if area2 > 104000:
        if len(approx) == 4:
            cv2.drawContours(img, [approx], 0, (0, 0, 255), 2)
            puntos = ordenar_puntos(approx)
            p1 = cv2.circle(img, tuple(puntos[0]), 7, (255, 0, 0), 2)
            p2 = cv2.circle(img, tuple(puntos[1]), 7, (0, 255, 0), 2)
            p3 = cv2.circle(img, tuple(puntos[2]), 7, (0, 0, 255), 2)
            p4 = cv2.circle(img, tuple(puntos[3]), 7, (255, 255, 0), 2)
            # imgResizei = cv2.resize(img, (1600, 800))
            # cv2.imshow("w", imgResizei)
            # cv2.waitKey(0)

        xr, yr, wr, hr = cv2.boundingRect(c)
        if x != 0 and y != 0:
            recorte = img[yr:yr + hr, xr:xr + wr]  # y:y+h, x:x+w
            # imgResizere = cv2.resize(recorte, (680, 316))
            # recorteOCR = cv2.resize(recorte , None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
            recorteOCR = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((1, 1), np.uint8)
            recorteOCR = cv2.dilate(recorteOCR, kernel, iterations=1)
            recorteOCR = cv2.erode(recorteOCR, kernel, iterations=1)
            cv2.threshold(cv2.GaussianBlur(recorteOCR, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            cv2.threshold(cv2.bilateralFilter(recorteOCR, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            cv2.threshold(cv2.medianBlur(recorteOCR, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            cv2.adaptiveThreshold(cv2.GaussianBlur(recorteOCR, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 31, 2)

            cv2.adaptiveThreshold(cv2.bilateralFilter(recorteOCR, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 31, 2)

            cv2.adaptiveThreshold(cv2.medianBlur(recorteOCR, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
            #imgResize = cv2.resize(recorte, (800, 600))
            #recortegris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
            grayr = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)

            boxes = pytesseract.image_to_data(recorteOCR)
            for ar, br in enumerate(boxes.splitlines()):
                if ar != 0:
                    br = br.split()
                    # if len(br) == 12:
                    #     print(br)
                    # # #if len(b) == 12 and (b[11] == 'Integron®' or b[11] == '|T27-7YS' or b[11] == '2027-02' or b[11] == '820022'):
                    if len(br) == 12 and (
                            br[11] == 'Integron®' or br[11] == '1T27-7YS' or br[11] == '|T27-7YS' or br[11] == '1127-7YS' or  br[11] == 'IT27-7YS' or br[11] == '2027-02' or br[11] == '820022' or br[
                        11] == '2027.02' or br[11] == '202702'
                            or br[11] == '2027' or br[11] == 'B20022' or br[11] == '820022' or br[11] == '620022' or br[11] == 's20022'):
                        x1, y1, w1, h1 = int(br[6]), int(br[7]), int(br[8]), int(br[9])
                        cv2.putText(recorte, br[11], (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
                        cv2.rectangle(recorte, (x1, y1), (x1 + w1, y1 + h1), (50, 50, 255), 2)

                        # cv2.imshow("wor ", imgResizere)
                        cv2.imshow("wr", recorte)
                        cv2.waitKey(0)



imgResizei = cv2.resize(img , (1600, 800))
cv2.imshow("w", imgResizei)

imgResizeifb = cv2.resize(fin , (1600, 800))
cv2.imshow("wfb", imgResizeifb)
cv2.waitKey(0)
cv2.destroyWindow()