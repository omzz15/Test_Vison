import cv2
import numpy as np
import json
from tkinter import *

path = "C:\Development\Robotics\FRC\Test_Vision\ML\Cone_Data\cone.jpg" # f'{img_path}\{img_name}'

def get_img():
    img = cv2.imread(path)
    img = cv2.resize(img, (540,960))
    return img

def on_update(val):
    img = get_img()
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, (hLow.get(), sLow.get(), vLow.get()), (hHigh.get(), sHigh.get(), vHigh.get()))
    cv2.imshow("mask", mask)
    #get contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #show contours
    img = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    cv2.imshow("image w/ contours", img)

def on_save():
    data = {}
    data["HSV_low"] = [hLow.get(), sLow.get(), vLow.get()]
    data["HSV_high"] = [hHigh.get(), sHigh.get(), vHigh.get()]
    #write lower and upper bounds to json file
    with open("C:\Development\Robotics\FRC\Test_Vision\ML\Cone_Data\color_data.json", "w") as f:
        json.dump(data, f)

root = Tk()
#set window size
root.geometry("500x400")

length = 500

hLow = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="H Low", length= length, command=on_update)
hLow.pack()
hHigh = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="H High", length= length, command=on_update)
hHigh.pack()
sLow = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="S Low", length= length, command=on_update)
sLow.pack()
sHigh = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="S High", length= length, command=on_update)
sHigh.pack()
vLow = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="V Low", length= length, command=on_update)
vLow.pack()
vHigh = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="V High", length= length, command=on_update)
vHigh.pack()
button = Button(root, text="Save", command=on_save)
button.pack()

cv2.imshow("image", get_img())

root.mainloop()

cv2.destroyAllWindows()