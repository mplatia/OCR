import numpy as np
import cv2
from pylibdmtx import pylibdmtx

if __name__ == '__main__':

    image = cv2.imread('Imagenes/p11.jpeg', cv2.IMREAD_UNCHANGED);

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret,thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    msg = pylibdmtx.decode(thresh)
    for i in range(len(msg)):
        print(msg[i].data)
        print(str(msg[i].data, "utf-8"))  # removes the b'... formatting
        print(msg[i].rect.left)
        print(msg[i].rect.top)
        print(msg[i].rect.width)
        print(msg[i].rect.height)
        cv2.rectangle(image, (msg[i].rect.left, msg[i].rect.top ),(  msg[i].rect.width, msg[i].rect.height), (50, 50, 255), 2)
    imgr = cv2.resize(image, (800, 600))
    cv2.imshow("Resultado DataMatrix", imgr)
    print(msg)
    cv2.waitKey(0)

