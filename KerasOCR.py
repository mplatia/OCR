import keras_ocr
import cv2
import matplotlib.pyplot as plt

pipeline = keras_ocr.pipeline.Pipeline()

img = [keras_ocr.tools.read(img) for img in ['tr.png, trgn.png']]


plt.figure(figsize = (10,20))
plt.imshow(img[0])
plt.show()
plt.figure(figsize = (10,20))
plt.imshow(img[1])
plt.show()

