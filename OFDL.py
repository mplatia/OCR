import cv2
import numpy as  np
import pytesseract
from imutils.object_detection import non_max_suppression

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

img=cv2.imread(r'Imagenes/pliegomitad.jpg',1) # Leer imagen
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Convierta la imagen en una imagen en escala de grises
kernel=np.ones((1,1),np.uint8) # Kelner
erosion=cv2.erode(gray,kernel,iterations=2) #Expansión
ditalacion=cv2.dilate(erosion,kernel,iterations=2) #Dilatacion
ret, thresh = cv2.threshold(ditalacion, 170, 255, cv2.THRESH_BINARY_INV)
# Procesamiento de umbral Método binario
thresh1 = cv2.GaussianBlur(thresh,(1,1),0)# Filtro gaussiano

black = np.zeros((img.shape[0], img.shape[1], 3), np.uint8) #---black in RGB


black1 = cv2.rectangle(black,(100, 50), (3600, 200),(255, 255, 255), -1)   #--- ROI Horizontal
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
            # cv2.putText(img, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(img, (x - 270, y + 167), (x + w + 225, y + h - 50), (0, 0, 0), 2)
            #cv2.rectangle(img, (x - 270, y + 180), (x + w + 245, y + h - 50), (0, 0, 0), 5)
            yy = dy * l
            cv2.rectangle(img, (x - 270, y + 167 + yy), (x + w + 225, y + h - 50 + yy), (0, 0, 0), 5)

gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray1, 100, 255)
kernel2 = np.ones((3, 3), np.uint8)
canny = cv2.dilate(canny, kernel2, iterations=1)
cnts, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
palabras = []
def ordenar_puntos(puntos):
    n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()

    y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1])

    x1_order = y_order[:2]
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])

    x2_order = y_order[2:4]
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])

    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]
for c in cnts:
    epsilon = 0.01 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    area2 = cv2.contourArea(c)


    # if area2 > 104000:
    if area2 > 3250:
        if len(approx) == 4:
            print(area2)
            cv2.drawContours(img, [approx], 0, (0, 0, 255), 2)
            puntos = ordenar_puntos(approx)
            p1 = cv2.circle(img, tuple(puntos[0]), 7, (255, 0, 0), 2)
            p2 = cv2.circle(img, tuple(puntos[1]), 7, (0, 255, 0), 2)
            p3 = cv2.circle(img, tuple(puntos[2]), 7, (0, 0, 255), 2)
            p4 = cv2.circle(img, tuple(puntos[3]), 7, (255, 255, 0), 2)
            imgResizei = cv2.resize(img, (1600, 800))
            cv2.imshow("w", imgResizei)
            cv2.waitKey(0)

        xr, yr, wr, hr = cv2.boundingRect(c)
        if x != 0 and y != 0:
            recorte = img[yr:yr + hr, xr:xr + wr]  # y:y+h, x:x+w
            model = cv2.dnn.readNet(r'C:\Users\Maxi\Desktop\proyectosCV\CursoOCR\frozen_east_text_detection.pb')
            # ## Prepare the image
            # use multiple of 32 to set the new img shape
            height, width, _ = recorte.shape
            new_height = (height // 32) * 32
            new_width = (width // 32) * 32
            print(new_height, new_width)

            # get the ratio change in width and height
            h_ratio = height / new_height
            w_ratio = width / new_width
            print(h_ratio, w_ratio)

            blob = cv2.dnn.blobFromImage(recorte, 1, (new_width, new_height), (123.68, 116.78, 103.94), True, False)
            model.setInput(blob)

            model.getUnconnectedOutLayersNames()

            (geometry, scores) = model.forward(model.getUnconnectedOutLayersNames())
            # ## Post-Processing
            # <img src="OCR_EAST12.png" width=700 height=400 />
            rectangles = []
            confidence_score = []
            for i in range(geometry.shape[2]):
                for j in range(0, geometry.shape[3]):

                    if scores[0][0][i][j] < 0.1:
                        continue

                    bottom_x = int(j * 4 + geometry[0][1][i][j])
                    bottom_y = int(i * 4 + geometry[0][2][i][j])

                    top_x = int(j * 4 - geometry[0][3][i][j])
                    top_y = int(i * 4 - geometry[0][0][i][j])

                    rectangles.append((top_x, top_y, bottom_x, bottom_y))
                    confidence_score.append(float(scores[0][0][i][j]))
            # use Non-max suppression to get the required rectangles
            fin_boxes = non_max_suppression(np.array(rectangles), probs=confidence_score, overlapThresh=0.5)

            img_copy = recorte.copy()

            for (x1, y1, x2, y2) in fin_boxes:
                x1 = int(x1 * w_ratio)
                y1 = int(y1 * h_ratio)
                x2 = int(x2 * w_ratio)
                y2 = int(y2 * h_ratio)

                # segment = img_copy[y1:y2 + 4, x1:x2 + 2, :]
                segment = img_copy[y1:y2, x1:x2, :]

                segment_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
                ret, thresh2 = cv2.threshold(segment_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                text = pytesseract.image_to_data(thresh2, config=r"--psm 1")
                for ar, br in enumerate(text.splitlines()):
                    if ar != 0:
                        br = br.split()
                        if len(br) == 12:
                        # if len(br) == 12 and (br[11] == 'Integron' or br[11] == '1T27-7YS' or br[11] == '|T27-7YS' or br[11] == '1127-7YS'
                        #         or br[11] == 'IT27-7YS' or br[11] == '2027-02' or br[11] == '820022' or
                        #         br[11] == '2027.02' or br[11] == '202702'
                        #         or br[11] == '2027' or br[11] == 'B20022' or br[11] == '820022' or br[11] == '620022' or
                        #         br[11] == 's20022'):
                            print(br[11])
                            x1, y1, w1, h1 = int(br[6]), int(br[7]), int(br[8]), int(br[9])
                            cv2.rectangle(img_copy,(x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

                            cv2.putText(img_copy, br[11], (x1, y1 + 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
                            cv2.imshow("w", img_copy)
                            cv2.waitKey(0)



imgResizei = cv2.resize(img , (1600, 1000))
cv2.imshow("w", imgResizei)

# imgResizeifb = cv2.resize(fin , (1600, 800))
# cv2.imshow("wfb", imgResizeifb)
cv2.waitKey(0)
cv2.destroyWindow()