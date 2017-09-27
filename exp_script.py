import psychopy
from psychopy import visual, core, event
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from glob import glob
from functions import *
import random
import sys
import time

i = 5 # current picture number
pics = glob('./line_drawings/converted/*.png')
# colour_delta = 2./256
colour_delta = 0.005

#  1    x          2
# --- = - ;   x = ---
# 256   2         256

keys = ['f', 'j', 'escape'] # f = detected

responses = []
lum_values = []

n_trials = 10
n_catch_trials = int(0.25 * n_trials)
catch_trials_idcs = np.random.choice(n_trials, n_catch_trials)

img = prepare_image(pics[i])
fg_colour = 0

win = visual.Window(monitor = 'testMonitor', fullscr = True, units = 'pix', colorSpace = 'rgb')
win.color = [0, 0, 0]

framerate = win.getActualFrameRate(nIdentical = 20, nMaxFrames = 200, nWarmUpFrames = 20, threshold = 1)
print 'framerate is {}'.format(framerate)

start_text = visual.TextStim(win = win, color = 1)
start_text.text = 'Press any button to start'
detect_text = visual.TextStim(win, color = 1, pos = (-200, 0), alignHoriz = 'center', alignVert = 'center')
detect_text.text = 'F = detected'
not_detect_text = visual.TextStim(win, color = 1, pos = (200, 0), alignHoriz = 'center', alignVert = 'center')
not_detect_text.text = 'J = not detected'

stim = visual.GratingStim(win, size = 512, units = 'pix')



start_text.draw()
win.flip()
event.waitKeys()
clock = core.Clock()

for trial in range(n_trials):

	stim.tex = prepare_image(np.random.choice(pics), fg_colour)

	win.flip()
	core.wait(1)

	stim.draw(); win.flip()
	clock.reset()
	while clock.getTime() < 1.5:
		pass
	win.flip()
	core.wait(0.5)

	detect_text.color = 1
	not_detect_text.color = 1
	detect_text.draw()
	not_detect_text.draw()
	win.flip()
	key = event.waitKeys(keyList = keys)

	lum_values.append(fg_colour)

	if key[0] == 'f':
		fg_colour -= colour_delta
		detect_text.color = -0.7
		responses.append(1)

	elif key[0] == 'j':
		fg_colour += colour_delta
		not_detect_text.color = -0.7
		responses.append(0)

	elif key[0] == 'escape':
		break

	detect_text.draw()
	not_detect_text.draw()
	win.flip()
	core.wait(1)


start_text.text = 'Done! Press any button to quit'
start_text.draw()
win.flip()
event.waitKeys()

win.close()

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.plot(responses)
ax1.set_title('Responses')

ax2 = fig.add_subplot(122)
ax2.plot(lum_values)
ax2.axhline(np.mean(lum_values), c = 'red')
ax2.set_title('Luminance')

plt.show()
