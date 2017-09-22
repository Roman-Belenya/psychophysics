from psychopy import visual, core, event
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt; plt.ion()
import time
import os

def convert_image(img):
	img = img/127.5 - 1
	return np.flip(img, 0) # for some reason, flips the matrix vertically

# if not os.path.isdir('./flicker_images'):
# 	os.mkdir('./flicker_images')

def change_colour(image, dim = 0, by = 10):
    img = image.copy()
    mask = img[:,:,dim] == 0 # select all balck pixels
    img[mask] += by
    return img


monitor_fs = 60 # Hz
flicker_fs = 15
seconds = 5

assert flicker_fs * 2 <= monitor_fs, 'Too high flicker fs'

phase = monitor_fs / (flicker_fs * 2)

img = Image.open('./line_drawings/converted/obj032bat.png')
green_img = np.array(img)
red_img = green_img.copy()

green_img[:,:,1] = 255 # insert max values into green channel
red_img[:,:,0] = 255

# Image.fromarray(red_img).save('./flicker_images/red.png')
# Image.fromarray(green_img).save('./flicker_images/green.png')
g = convert_image(green_img)
r = convert_image(red_img)

win = visual.Window(monitor = 'testMonitor', fullscr = True, units = 'pix', color = [1, 1, 1])
win.recordFrameIntervals = True
win.refreshThreshold = 1/60. + 0.004


# green_bitmap = visual.ImageStim(win, image = './flicker_images/green.png', name = 'green')
# red_bitmap = visual.ImageStim(win, image = './flicker_images/red.png', name = 'red')

green_bitmap = visual.ImageStim(win, image = g, size = (600, 600), name = 'green')
red_bitmap = visual.ImageStim(win, image = r, size = (600, 600), name = 'red')

current_bitmap = green_bitmap

t0 = time.time()
for frame in range(seconds * monitor_fs):
	if frame % phase == 0:
		print frame
		if current_bitmap == green_bitmap:
			current_bitmap = red_bitmap
		else:
			current_bitmap = green_bitmap
	current_bitmap.draw()
	win.flip()
print '{} seconds'.format(time.time() - t0)
print 'dropped {} frames'.format(win.nDroppedFrames)

win.close()

plt.plot(win.frameIntervals)
plt.show()
