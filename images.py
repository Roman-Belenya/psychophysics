from PIL import Image
import numpy as np
import os

img = Image.open('./line_drawings/obj032bat.png')
arr = np.array(img)[:,:,0:3]
arr[arr == 255] = 128

os.mkdir('./images')
for i in range(128):
	temp = np.array(arr)
	temp[temp == 0] = 128 + i
	Image.fromarray(temp).save('./images/' + str(i) + '.png')

