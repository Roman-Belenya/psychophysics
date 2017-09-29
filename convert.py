# Convert line drawings in gif format to RGB png files to manipulate colours
from PIL import Image
import numpy as np
import os
import glob


imgs = glob.glob('./line_drawings/*.gif')

out_path = './line_drawings/converted_alpha'
if not os.path.isdir(out_path):
	os.mkdir(out_path)

for img in imgs:
    path, filename = os.path.split(img)
    file, ext = os.path.splitext(filename)
    Img = Image.open(img).convert('RGBA').resize((512, 512), Image.NEAREST)

    rgba = np.array(Img)

    if len(np.unique(rgba)) > 2:
        raise Exception('image {} has {} colour levels'.format(img, len(np.unique(m))))

    bg = np.zeros([512, 512, 4], dtype = np.bool)
    bg[:,:,3] = (rgba[:,:,0] == 255) # this is white background

    rgba[bg] = 0 # make white region fully transparent (0)

    Img_converted = Image.fromarray(rgba)

    dest = os.path.join(out_path, file + '.png')
    Img_converted.save(dest, 'PNG')
    print img
