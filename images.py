from PIL import Image
import numpy as np
import os

img = Image.open('C:\Users\marotta_admin\Desktop\line drawings\obj032bat.png')
arr = np.array(img)
arr[arr == 255] = 128

os.mkdir('./images')
for i in np.arange(0, 129):
	temp = np.array(arr)
	temp[temp == 0] = 128 + i
	Image.fromarray(temp).save('./images/' + str(i) + '.png')
	