import psychopy
from psychopy import visual, core, event
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from glob import glob
from functions import *
import random

i = 5 # current picture number
pics = glob('./line_drawings/converted/*.png')
colour_delta = 2./256

#  1    x          2
# --- = - ;   x = --- 
# 256   2         256

keys = ['f', 'j'] # f = detected

n_trials = 20
n_catch_trials = int(0.25 * n_trials)
catch_trials_idcs = np.random.choice(n_trials, n_catch_trials)


win = visual.Window(monitor = 'testMonitor', fullscr = True, units = 'pix', color = [0, 0, 0])

text = visual.TextStim(win = win, color = 1)
text.text = 'Press any button'
text.draw()
win.flip()
event.waitKeys()

fixation = visual.GratingStim(win, size = 10, pos = [0,0], sf = 0, mask = 'circle')

img = prepare_image(pics[i])
foreground = img == -1
img[~foreground] = 0
img[foreground] = 0


stim = visual.GratingStim(win, tex = img, size = 600, units = 'pix')

clock = core.Clock()

for trial in range(n_trials):

	clock.reset()
	
	fixation.draw()
	win.flip()
	while clock.getTime() < 1:
		pass
		
	if trial not in catch_trials_idcs:
		stim.draw()
	win.flip()		
	while clock.getTime() < 2.5:
		pass

	text.text = 'f = detected\nj = did not detect'
	text.draw()
	win.flip()
	key = event.waitKeys(keyList = keys)

	if 'f' in key:
		img[foreground] -= colour_delta
	elif 'j' in key:
		img[foreground] += colour_delta
	
	stim.tex = img
	

win.close()