

import cv2
image = cv2.imread(r'Imagenes/pliegomitad.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gauss = cv2.GaussianBlur(gray, (7, 7), 0)
canny = cv2.Canny(gauss, 0, 60)
# canny = cv2.Canny(gray, 0, 50)
canny = cv2.dilate(canny, None, iterations=1)
canny = cv2.erode(canny, None, iterations=1)
# _, th = cv2.threshold(canny, 0, 50, cv2.THRESH_BINARY_INV)
#_,cnts,_ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# OpenCV 3
cnts,_ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# OpenCV 4
# cv2.drawContours(gray, cnts, -1, (0,255,0), 2)


for c in cnts:
  epsilon = 0.01*cv2.arcLength(c,True)
  approx = cv2.approxPolyDP(c,epsilon,True)
  area = cv2.contourArea(c)
  x, y, w, h = cv2.boundingRect(approx)
  recorte = image[y:y + h, x:x + w]  # y:y+h, x:x+w

  if len(approx)>10:
      if area > 5000 and area < 6000:
        M = cv2.moments(c)
        if (M["m00"] == 0): M["m00"] = 1
        x1 = int(M["m10"] / M["m00"])
        y1 = int(M['m01'] / M['m00'])
        # print(area)
        # cv2.putText(image,'Circulo', (x,y-5),1,1.5,(0,0,0),2)

        b = image.item(y1, x1, 0)
        g = image.item(y1, x1, 1)
        r = image.item(y1, x1, 2)

        print(r, g, b)
        cv2.drawContours(image, [approx], 0, (0,0,0),5)
        imgResizei = cv2.resize(recorte, (800, 400))
        cv2.imshow('image',imgResizei)
        cv2.waitKey(0)


