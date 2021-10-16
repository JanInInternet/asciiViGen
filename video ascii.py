import cv2
import numpy as np
import math as ma
import os
from PIL import Image

hight = 2**9
weight = round(hight * 2.5)

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", ".", " "]

cap = cv2.VideoCapture(0)

if not (cap.isOpened()):
    print("Could not open video device")

buf2 = np.empty((480, 640, 3), np.dtype('uint8'))
buf1 = np.empty((480, 640), np.dtype('uint8'))
buf = np.empty((hight, weight), np.dtype('uint8'))

fc = 0
ret = True

while (True):
    ret, buf2 = cap.read()
    buf1 = cv2.cvtColor(buf2, cv2.COLOR_BGR2GRAY)
    buf = cv2.resize(buf1, (weight, hight), interpolation = cv2.INTER_AREA)

    for i in range(hight):
        for j in range(weight):
            print(ASCII_CHARS[ma.floor((buf[i][j]/255)*11)], end ='')
        print()
    os.system('cls')
    fc += 1

cap.release()

os.system('BRAKE')
