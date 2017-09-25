import psychopy
from psychopy import visual, core, event
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from glob import glob
from functions import *

current_lum = 128
i = 5 # current picture number
pics = glob('./line_drawings/converted/*.png')


win = visual.Window(monitor = 'testMonitor', fullscr = True, units = 'pix', color = [1, 1, 1])

text = visual.TextStim(win = win, color = [0, 0, 0])
text.text = 'Press any button'
text.draw()
win.flip()
event.waitKeys()


img = prepare_image(pics[i])
nonwhite = img != 1
print np.unique(img)
img[~nonwhite] = 0
img[nonwhite] = -1
print np.unique(img)

img_stim = visual.ImageStim(win, image = img, colorSpace = 'rgb', size = [600, 600], units = 'pix')

img_stim.draw()
win.flip()

core.wait(2)

win.close()