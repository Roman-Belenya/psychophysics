
from psychopy import visual, core, event
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
from functions import *

monitor_fs = 60 # frames/second
flicker_fs = 30 # cycles/second
seconds = 6


cycle = monitor_fs / (flicker_fs * 2) # how many frames there are in a demicycle
# cycle = 1
frame_sec = cycle / float(monitor_fs)

# imgPath = './line_drawings/converted/obj032bat.png'
imgPath = './line_drawings/converted/circle.png'

bwImage = prepare_image(imgPath, fg_colour = -1, bg_colour = 1)

red, _ = change_colour(bwImage, dim = 0, by = 2)
green, _ = change_colour(bwImage, dim = 1, by = 1)

# red = change_colour(bwImage, dim = 0, by = (222/127.5))
# green = change_colour(bwImage, dim = 1, by = (135/127.5))


win = visual.Window(monitor = 'testMonitor', fullscr = True, units = 'pix', color = [1, 1, 1])
win.refreshThreshold = 1./monitor_fs + 0.004
win.recordFrameIntervals = True

green_stim = visual.GratingStim(win, tex = green, size = (600, 600))
red_stim = visual.GratingStim(win, tex = red, size = (600, 600))


current_stim = green_stim
frame = 0
finished = False

DELTA = 2./256

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
	
	if key:
		if key[0] == 'up':
			delta_red, delta_green = -DELTA, DELTA
		elif key[0] == 'down':
			delta_red, delta_green = DELTA, -DELTA
		elif key[0] == 'escape':
			sys.exit()
		elif key[0] == 'return':
			print 'PRESSED ENTER'
			delta_red, delta_green = 0, 0
			finished = True
		
		red, rlevel = change_colour(red, dim = 0, by = delta_red)
		green, glevel = change_colour(green, dim = 1, by = delta_green)
		
		red_stim.tex = red
		green_stim.tex = green
		
		print 'red = {}; green = {}\n'.format(rlevel, glevel)

	frame += 1
	
win.close()

rlevel = 255 + int((rlevel - 1) * 127.5)
glevel = 255 + int((glevel - 1) * 127.5)

isoImage = np.zeros((600, 600, 3), dtype = np.uint8)

isoImage[:300, :300, 0] = rlevel
isoImage[:300, 300:, 1] = glevel

isoImage[300:, :, 0] = rlevel
isoImage[300:, :, 1] = glevel

Image.fromarray(isoImage).show()

print '\n----------------------'	
print 'END OF TRIALS'
print '{} ms/frame'.format(frame_sec * 1000)
print 'dropped {} frames'.format(win.nDroppedFrames)
print 'red   = {}\ngreen = {}'.format(rlevel, glevel)
print '----------------------'

intervals_ms = np.array(win.frameIntervals) * 1000
plt.plot(intervals_ms)
plt.xlabel('frame N')
plt.ylabel('t (ms)')
plt.show()