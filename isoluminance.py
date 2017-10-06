
from psychopy import visual, core, event
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
from functions import *

'''
10 Hz = 6 frames/cycle
15 Hz = 4 frames/cycle. change colour every second frame
30 Hz = 2 frames/cycle. change colour every frame
'''

monitor_fs = 60 # frames/second
flicker_fs = 30 # cycles/second

cycle = monitor_fs / (flicker_fs * 2) # how many frames there are in a demicycle


# imgPath = './line_drawings/converted/obj032bat.png'
imgPath = './line_drawings/converted/circle.png'

fg = get_fg_mask(imgPath)

red = np.array([225, 0, 0])
green = np.array([0, 0, 0])

win = visual.Window(
	monitor = 'testMonitor', 
	fullscr = True, 
	units = 'pix', 
	colorSpace = 'rgb255',
	color = [255, 255, 255])
	
win.refreshThreshold = 1./monitor_fs + 0.004
win.recordFrameIntervals = True

stim = visual.GratingStim(
	win = win, 
	tex = imgPath, 
	size = (300, 300),
	mask = fg,
	colorSpace = 'rgb255',
	color = red,
	phase = 0.5
	)


frame = 0
finished = False
delta = np.array([0, 5, 0])


while not finished:
	if frame % cycle == 0:
		if np.all(stim.color == red):
			stim.color = green
		else:
			stim.color = red
	stim.draw()
	win.flip()
	
	key = event.getKeys()
	
	if key:
		key, = key
		if key == 'up':
			green = change_colour(green, delta)
		elif key == 'down':
			green = change_colour(green, -delta)
		elif key == 'escape':
			sys.exit()
		elif key == 'return':			
			finished = True
		else:
			try:
				ans = int(key)
				if ans == 0:
					ans = 10
				cycle = ans
				frame = 0
			except:
				pass
			
	frame += 1
	
win.close()


isoImage = np.zeros((600, 600, 3), dtype = np.uint8)

isoImage[:300, :300, 0] = red[0]
isoImage[:300, 300:, 1] = green[1]

isoImage[300:, :, 0] = red[0]
isoImage[300:, :, 1] = green[1]

Image.fromarray(isoImage).show()

print '\n----------------------'	
print 'END OF TRIALS'
print 'dropped {} frames'.format(win.nDroppedFrames)
print 'red   = {}\ngreen = {}'.format(red, green)
print '----------------------'

intervals_ms = np.array(win.frameIntervals) * 1000
plt.plot(intervals_ms)
plt.xlabel('frame N')
plt.ylabel('t (ms)')
plt.show()