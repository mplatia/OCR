import cv2
import numpy as  np
import pytesseract
from imutils.object_detection import non_max_suppression

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

img=cv2.imread(r'Imagenes/pliegomitad.jpg',1) # Leer imagen
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
kernel2 = np.ones((3, 3), np.uint8)
canny = cv2.dilate(canny, kernel2, iterations=1)
cnts, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
for c in cnts:
    epsilon = 0.01 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    area2 = cv2.contourArea(c)
    # if area2 > 104000:
    if area2 > 6500 and area2 < 8000:
        if len(approx) == 4:
            cv2.drawContours(img, [approx], 0, (0, 0, 255), 2)
            puntos = ordenar_puntos(approx)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img, (x- 265, y - 100), (x + w + 230, y + h + 5), (0, 0, 0), 5, cv2.LINE_AA)

gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

canny1 = cv2.Canny(gray2, 100, 255)
kernel3 = np.ones((3, 3), np.uint8)
cnts1, hierarchy1 = cv2.findContours(gray2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for c1 in cnts1:
    xr, yr, wr, hr = cv2.boundingRect(c1)
    area3 = cv2.contourArea(c1)
    print(area3)
    if x != 0 and y != 0:
        if (area3 > 95000):
            recorte = gray2[yr:yr + hr, xr:xr + wr]  # y:y+h, x:x+w
            model = cv2.dnn.readNet(r'C:\Users\Maxi\Desktop\proyectosCV\CursoOCR\frozen_east_text_detection.pb')
            recorte2 = cv2.cvtColor(recorte, cv2.COLOR_GRAY2BGR)
            # ## Prepare the image
            # use multiple of 32 to set the new img shape
            height, width, _ = recorte2.shape
            new_height = (height // 32) * 32
            new_width = (width // 32) * 32
            print(new_height, new_width)

            # get the ratio change in width and height
            h_ratio = height / new_height
            w_ratio = width / new_width
            print(h_ratio, w_ratio)

            blob = cv2.dnn.blobFromImage(recorte2, 1, (new_width, new_height), (123.68, 116.78, 103.94), True, False)
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

            img_copy = recorte2.copy()


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
                        if len(br) == 12 and br[11] == 'Integron®' :
                            # if len(br) == 12 and (br[11] == 'Integron' or br[11] == '1T27-7YS' or br[11] == '|T27-7YS' or br[11] == '1127-7YS'
                            #         or br[11] == 'IT27-7YS' or br[11] == '2027-02' or br[11] == '820022' or
                            #         br[11] == '2027.02' or br[11] == '202702'
                            #         or br[11] == '2027' or br[11] == 'B20022' or br[11] == '820022' or br[11] == '620022' or
                            #         br[11] == 's20022'):
                            print(br[11])
                            x1, y1, w1, h1 = int(br[6]), int(br[7]), int(br[8]), int(br[9])
                            cv2.rectangle(img_copy, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

                            cv2.putText(img_copy, br[11], (x1, y1 + 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
                            cv2.imshow("w", img_copy)
                            cv2.waitKey(0)


imgResizei = cv2.resize(img , (1600, 800))
cv2.imshow("w", imgResizei)

# imgResizeifb = cv2.resize(fin , (1600, 800))
# cv2.imshow("wfb", imgResizeifb)
cv2.waitKey(0)
cv2.destroyWindow()