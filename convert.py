from PIL import Image
import numpy as np
import os
import glob

# imgs = glob.glob('./line_drawings/*.gif')
imgs = os.listdir('./line_drawings')
path = './line_drawings/converted'
os.mkdir(path)

for i in imgs:
    name, ext = os.path.splitext(i)
    img = Image.open('./line_drawings/' + i)
    if img.size != (300,300): print 'unequal size !'
    dest = os.path.join(path, name + '.png')
    img.resize((600, 600)).save(dest)
    print i
