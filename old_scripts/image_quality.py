from psychopy import visual, event
from PIL import Image, ImageFilter
import os
import glob
import numpy as np

blur = 1
interp = True

win = visual.Window(
    size = [500, 500],
    monitor = 'labDell',
    screen = 0,
    fullscr = False,
    allowGUI = False,
    colorSpace = 'rgb255',
    color = 100,
    units = 'deg')

image_dir = r'C:\Users\marotta_admin\Desktop\images'

stim = visual.ImageStim(
    win = win,
    size = [7.84, 9.26],
    units = 'deg',
    interpolate = interp)

text = visual.TextStim(
    win = win,
    colorSpace = 'rgb255',
    color = 255,
    pos = (0, -7),
    antialias = True)

imgs = glob.glob(os.path.join(image_dir, '*.png'))
current_img = 0

while True:
    img = Image.open(imgs[current_img])
    print np.unique(np.array(img))
    img = img.filter(ImageFilter.GaussianBlur(radius = blur))
    stim.image = img
    text.text = os.path.split(imgs[current_img])[1]
    stim.draw()
    text.draw()
    win.flip()
    key = event.waitKeys()
    if key[0] == 'left':
        if current_img > 0:
            current_img -= 1
            stim.image = imgs[current_img]
    elif key[0] == 'right':
        if current_img < len(imgs) - 1:
            current_img += 1
            stim.image = imgs[current_img]
    elif key[0] == 'escape':
        break


win.close()
