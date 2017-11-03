from psychopy import visual, core, event
import numpy as np
from PIL import Image
from functions import prepare_image

path = '/home/roman/Desktop/psychophysics/line_drawings/converted/obj069cactus.png'

img, fg = prepare_image(path, 0)

win = visual.Window(monitor = 'testMonitor', fullscr = True, units = 'pix', color = [0, 0, 0])


stim = visual.GratingStim(win, tex = img, size = 512)
colourDelta = (2./256) / 16
lum = 0

event.waitKeys()
for frame in range(128*16):
    stim.draw()
    win.flip()
    key = event.getKeys()
    if 'space' in key:
        break
    lum += colourDelta
    img[fg] = lum
    stim.tex = img

print 'luminance threshold is {}'.format(lum)
win.close()
