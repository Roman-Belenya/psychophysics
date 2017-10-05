
from psychopy import visual, core, event
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
from functions import *

monitor_fs = 60 # frames/second
flicker_fs = 1 # cycles/second
seconds = 6


cycle = monitor_fs / (flicker_fs * 2) # how many frames there are in a demicycle
frame_sec = cycle / float(monitor_fs)

# imgPath = './line_drawings/converted/obj032bat.png'
imgPath = './line_drawings/converted/circle.png'

bwImage = prepare_image(imgPath, fg_colour = -1, bg_colour = 1)

# red = change_colour(bwImage, dim = 0, by = 2)
# green = change_colour(bwImage, dim = 1, by = 2)

red = change_colour(bwImage, dim = 0, by = (222/127.5))
green = change_colour(bwImage, dim = 1, by = (135/127.5))


win = visual.Window(monitor = 'testMonitor', fullscr = True, units = 'pix', color = [1, 1, 1])

green_stim = visual.GratingStim(win, tex = green, size = (600, 600))
red_stim = visual.GratingStim(win, tex = red, size = (600, 600))



current_stim = green_stim
frame = 0
finished = False
print cycle

while not finished:
	if frame % cycle == 0:
		# print frame
		if current_stim == green_stim:
			current_stim = red_stim
		else:
			current_stim = green_stim
	current_stim.draw()
	win.flip()
	
	
	key = event.getKeys()
	if 'up' in key:
		red = change_colour(red, dim = 0, by = 0.01)
		red_stim.tex = red
		frame = 0
		print np.unique(red)[1]
	elif 'down' in key:
		red = change_colour(red, dim = 0, by = -0.01)
		red_stim.tex = red
		frame = 0
		print np.unique(red)[1]
	elif 'escape' in key:
		finished = True
	
	frame += 1
	
win.close()