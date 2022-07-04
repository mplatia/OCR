import numpy as np
import cv2
from pylibdmtx import pylibdmtx

image = cv2.imread('Imagenes/p6.jpeg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# imgResizeO = cv2.resize(image,(800,249))
cv2.imshow("Orig", image)
cv2.waitKey(0)
# equalize lighting
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
gray = clahe.apply(gray)

# edge enhancement
edge_enh = cv2.Laplacian(gray, ddepth = cv2.CV_8U,
                         ksize = 3, scale = 1, delta = 0)
# imgResizeE = cv2.resize(edge_enh,(800,249))
cv2.imshow("Edges", edge_enh)
cv2.waitKey(0)

# bilateral blur, which keeps edges
blurred = cv2.bilateralFilter(edge_enh, 13, 50, 50)

# use simple thresholding. adaptive thresholding might be more robust
(_, thresh) = cv2.threshold(blurred, 55, 255, cv2.THRESH_BINARY_INV)

cv2.imshow("Thresholded", thresh)
cv2.waitKey(0)


msg2 = pylibdmtx.decode(thresh)

print(msg2)



