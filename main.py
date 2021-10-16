from PIL import Image, ImageDraw, ImageFont
from sys import argv
import numpy as np
import cv2
import math as ma
import os
import time

import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize, suppress=True)

##for i in range(50):
##    for j in range(50):
##        print(round(test[i][j]/255), end=' ')
##    print()

min=0.7839419607843138

chrArr = [[-1, 0]]*256
chrArr = np.array(chrArr, dtype=np.double)
chrArr = np.full_like(chrArr, -1.0)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def char_image(char):
    # Get an image with a char drawn on it.
    # font = ImageFont.truetype("NotoSansThai-Regular.ttf", 40)
    font = ImageFont.truetype("verdana.ttf", 40)
    image = Image.new('RGB', (50, 50), (255, 255, 255))
    drawer = ImageDraw.Draw(image)
    drawer.text((0,0), char, font=font, fill=(0, 0, 0))
    image = image.convert('L')
    return image

def calMin(num):
    min=1
    minChr=0
    for i in range(round(num/2),num):
        imgChr = np.array(char_image(chr(i)))
        ##print(chr(i), np.mean(imgChr)/255)

        if(min > np.mean(imgChr)/255):
            min = np.mean(imgChr)/255
            minChr = i
        if((i % 1000) == 0):
            print(i/num, chr(minChr))
            
    return min

##min = calMin(130047)

def calMap(chrArr, min, num):
    scale=1-min
    for i in range(32,num):
        imgChr = np.array(char_image(chr(i)))
        grayVal = (((np.mean(imgChr)/255)-min)/(1-min))*255
        if(abs(round(grayVal) - chrArr[round(grayVal)][1]) > abs(grayVal - round(grayVal))):
##            print(chrArr, i/num, chrArr[round(grayVal)][1], grayVal)
            chrArr[round(grayVal)] = [i, grayVal]
##            print(chrArr, i/num, chrArr[round(grayVal)][1], grayVal)
        elif((i % 2500) == 0):
            print(i/num)
    i = 0
    while(i < chrArr.shape[0]):
        if chrArr[i][0] == -1:
            chrArr = numpy.delete(chrArr,i,0)
        elif chrArr[i][0] == 0:
            chrArr = numpy.delete(chrArr,i,0)
        else:
            i += 1
            
    chrArr = numpy.delete(chrArr,1,1)
    
    return chrArr

##chrArr = calMap(chrArr, min, round(130047*0.5151983513652756))
chrArr = calMap(chrArr, min, round(1024))

hight = 2**8
weight = round(hight * 2)

ASCII_CHARS = chrArr

print(chrArr)

cap = cv2.VideoCapture(0)

if not (cap.isOpened()):
    print("Could not open video device")

buf2 = np.empty((1080, 1920, 3), np.dtype('uint8'))
buf1 = np.empty((1080, 1920), np.dtype('uint8'))
buf = np.empty((hight, weight), np.dtype('uint8'))

fc = 0
ret = True

while (True):
    ret, buf2 = cap.read()
    buf1 = cv2.cvtColor(buf2, cv2.COLOR_BGR2GRAY)
    buf = cv2.resize(buf1, (weight, hight), interpolation = cv2.INTER_AREA)
    # print(buf)

    for i in range(hight):
        for j in range(weight):
            # print((buf[i][j]/255)*(ASCII_CHARS.shape[0]-1))
            print(chr(round(ASCII_CHARS[round((buf[i][j]/255)*(ASCII_CHARS.shape[0]-1))][0])), end =' ')
        print()

    time.sleep(5)
    os.system('cls')
    fc += 1

cap.release()

os.system('BRAKE')
