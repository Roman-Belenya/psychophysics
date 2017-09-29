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

    m = np.array(Img)

    if len(np.unique(m)) > 2:
        raise Exception('image {} has {} colour levels'.format(img, len(np.unique(m))))

    mask = np.zeros([512, 512, 4], dtype = np.bool)
    mask[:,:,3] = (m[:,:,0] == 255) # this is white background

    m[mask] = 0

    Img_converted = Image.fromarray(m)

    dest = os.path.join(out_path, file + '.png')
    Img_converted.save(dest, 'PNG')
    print img
