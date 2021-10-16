import numpy as np
import math as ma
from PIL import Image

hight = 128
weight = round(hight * 2.5)

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", ".", " "]

img_arr = np.array(Image.open('cat.jpg').resize((weight,hight)).convert('L'))
Image.fromarray(img_arr).save('r_cat.jpg')
print("After resizing:",img_arr.shape)

maxImg = np.amax(img_arr)
minImg = np.amin(img_arr)

print(maxImg, minImg)

step = 5

for i in range(hight):
    for j in range(weight):
            print(ASCII_CHARS[ma.floor((img_arr[i][j]/maxImg)*11)], end ='')

    print()

while True:
    pass
