
from psychopy import visual, core, event
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time
import os

monitor_fs = 60 # frames/second
flicker_fs = 15 # cycles/second
seconds = 6

# r  |----|    |----|    |----|    |
# g  |    |----|    |----|    |----|

#    |--cycle--|


assert flicker_fs * 2 <= monitor_fs, 'Too high flicker fs'

cycle = monitor_fs / (flicker_fs * 2) # how many frames there are in a cycle
frame_sec = cycle / float(monitor_fs)

green, red = prepare_image('./line_drawings/converted/obj032bat.png')
# green, red = prepare_image('./line_drawings/converted/obj010fishtank.png')

win = visual.Window(monitor = 'testMonitor', fullscr = True, units = 'pix', color = [1, 1, 1])
win.refreshThreshold = 1./monitor_fs + 0.004

green_stim = visual.ImageStim(win, image = green, size = (600, 600), name = 'green')
red_stim = visual.ImageStim(win, image = red, size = (600, 600), name = 'red')

current_stim = green_stim

t0 = time.time()
win.recordFrameIntervals = True
for frame in range(seconds * monitor_fs):
	if frame % cycle == 0: # eg frame 4, 8, 16, 20, ...
		print frame
		if current_stim == green_stim:
			current_stim = red_stim
		else:
			current_stim = green_stim
	current_stim.draw()
	win.flip()
win.close()

print '---------\n'	
print '{} seconds'.format(time.time() - t0)
print '{} ms/frame'.format(frame_sec * 1000)
print 'dropped {} frames'.format(win.nDroppedFrames)
print '\n----------'

intervals_ms = np.array(win.frameIntervals) * 1000
plt.plot(intervals_ms)
plt.xlabel('frame N')
plt.ylabel('t (ms)')
plt.show()
