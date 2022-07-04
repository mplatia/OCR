from pylibdmtx.pylibdmtx import decode
import cv2
import numpy as np

def dataMat(image, bgr):
    # image = cv2.imread('Imagenes/p6.jpeg', cv2.IMREAD_UNCHANGED);
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data = decode(gray_img)
    # print(data)
    for decodedObject in data:
        points = decodedObject.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        # cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        cv2.putText(frame, decodedObject.data.decode("utf-8") , (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,bgr, 2)

        # print("Barcode: {} ".format(decodedObject.data.decode("utf-8")))
        for barcode in data:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y - h), (0, 255, 0), 2)
            cv2.putText(frame, str(barcode), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, bgr, 2)
            print(barcode)
            # print(len(barcode))

bgr = (0, 255, 0)

frame = cv2.imread('Imagenes/bp.png')#CAP
code = dataMat(frame, bgr)
# print(code)
imgr = cv2.resize(frame, (800, 600))
cv2.imshow('Data Matrix reader', imgr)
code = cv2.waitKey(0)