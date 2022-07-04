import tkinter as tk
from tkinter import *
import cv2
from PIL import Image
from PIL import ImageTk
from PIL import ImageGrab
import imutils
import pytesseract
import numpy as np
import os
from pylibdmtx.pylibdmtx import decode


pytesseract.pytesseract.\
    tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


def fin():
    root.destroy()

def guardar():
    print ("El usuario es ", e1.get())
    print("Se encuentra en Fase ", e2.get())
    print ("OP es ", e3.get())
    limpiar_var()

def limpiar_var():
    e1.delete(0, 'end')
    e2.delete(0, 'end')
    e3.delete(0, 'end')

root = Tk()
root.state('zoomed')
root.title("TerraProg")
root.geometry("600x600")

p1 = PhotoImage(file=r'trgn.png')
root.iconphoto(False, p1)


bg = PhotoImage(file=r'tr.png')
photoimagebg = bg.subsample(1, 1)


label1 = Label(root, image=photoimagebg)
label1.place(x=0, y=0)

root['bg'] = 'white'


tk.Label(root, text="Usuario").grid(column=0, row=1)
tk.Label(root, text="Fase").grid(column=1, row=1)
tk.Label(root, text="Número de OP").grid(column=2, row=1)

e1 = tk.Entry(root)
e2 = tk.Entry(root)
e3 = tk.Entry(root)

e1.grid(column=0, row=2, padx=5, pady=5)
e2.grid(column=1, row=2, padx=5, pady=5)
e3.grid(column=2, row=2, padx=5, pady=5)


photo = PhotoImage(file = r'trgn.png')
photoimages = photo.subsample(30, 30)

def dataMat(image, bgr):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data = decode(gray_img)
    # print(data)
    for decodedObject in data:
        points = decodedObject.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        # cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        # cv2.putText(img, decodedObject.data.decode("utf-8") , (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,bgr, 2)

        # print("Barcode: {} ".format(decodedObject.data.decode("utf-8")))
        for barcode in data:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            x, y, w, h = barcode.rect
            cv2.rectangle(img, (x, y), (x + w, y - h), (0, 255, 0), 2)
            cv2.putText(img, str(barcode), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, bgr, 2)
            print(barcode)
            # print(len(barcode))


def visualizar():
    global cap
    global img
    global code
    if cap is not None:
        timer = cv2.getTickCount()
        ret, img = cap.read()
        if ret == True:
            bgr = (0, 255, 0)
            code = dataMat(img, bgr)
            img = imutils.resize(img, width=900)
            frame1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame1)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)

        else:
            lblVideo.image = ""
            cap.release()





def iniciar():
    global cap
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)
    img = visualizar()

lblVideo = Label(root)
lblVideo.place(x=450, y=15)
btn = Button(root, text="Iniciar",image= photoimages, compound=LEFT, command=iniciar)
btn.grid(column=0, row=0, padx=5, pady=5)
btn1 = Button(root, text="Cerrar", image= photoimages, compound=LEFT, command=fin)
btn1.grid(column=1, row=0, padx=5, pady=5)
root.title('CheckGene')
root.mainloop()
