import tkinter as tk
from tkinter import *
import cv2
from PIL import Image
from PIL import ImageTk
import imutils
import pytesseract
import numpy as np
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


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




def findEncodings(images):
    global img
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeList.append(img)
    return encodeList



def visualizar():
    global cap
    if cap is not None:
        timer = cv2.getTickCount()
        ret, img = cap.read()
        boxes = pytesseract.image_to_data(img)
        for a,b in enumerate(boxes.splitlines()):
            if a != 0:
                b = b.split()
                if len(b) == 12 and (b[11] == '202702' or b[11] == '820022' or b[11] == 'B20022' or b[11] == '|T27-7YS' or b[11] == 'IT27-7YS' or b[11] == 'Integron®' ):
                    x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                    cv2.putText(img, b[11], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 255), 2)

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        # cv2.putText(img, str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20,230,20), 2);
        if ret == True:
            img = imutils.resize(img, width=900)
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
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
    visualizar()

lblVideo = Label(root)
lblVideo.place(x=450, y=15)
btn = Button(root, text="Iniciar",image= photoimages, compound=LEFT, command=iniciar)
btn.grid(column=0, row=0, padx=5, pady=5)
btn1 = Button(root, text="Cerrar", image= photoimages, compound=LEFT, command=fin)
btn1.grid(column=1, row=0, padx=5, pady=5)
root.title('CheckGene')
root.mainloop()
