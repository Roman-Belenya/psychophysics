# Convert line drawings in gif format to RGB png files to manipulate colours
from PIL import Image
import numpy as np
import os
import glob


imgs = glob.glob('./line_drawings/*.gif')

out_path = './line_drawings/converted'
if not os.path.isdir(out_path):
	os.mkdir(out_path)

for img in imgs:
    path, filename = os.path.split(img)
    file, ext = os.path.splitext(filename)
    Img = Image.open(img)
	
    dest = os.path.join(out_path, file + '.png')
    Img.resize((600, 600)).convert('RGB').save(dest, 'PNG')
    print img
