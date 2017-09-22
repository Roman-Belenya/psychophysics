from psychopy import visual, core, event
from PIL import Image
import numpy as np
import time
import os

def convert_image(img):
	img = img/127.5 - 1
	return img

if not os.path.isdir('./flicker_images'):
	os.mkdir('./flicker_images')


monitor_fs = 60 # Hz
flicker_fs = 15

phase = monitor_fs / (flicker_fs * 2)

img = Image.open('./line_drawings/converted/obj032bat.png')
green_img = np.array(img)
red_img = green_img.copy()

green_img[:,:,1] = 255
red_img[:,:,0] = 255

Image.fromarray(red_img).save('./flicker_images/red.png')
Image.fromarray(green_img).save('./flicker_images/green.png')
# g = convert_image(green_img)
# r = convert_image(red_img)

win = visual.Window(monitor = 'testMonitor', fullscr = True, units = 'pix', color = [1, 1, 1])

green_bitmap = visual.ImageStim(win, image = './flicker_images/green.png', name = 'green')
red_bitmap = visual.ImageStim(win, image = './flicker_images/red.png', name = 'red')

current_bitmap = green_bitmap


for frame in range(300):
	if frame % phase == 0:
		print frame
		if current_bitmap == green_bitmap:
			current_bitmap = red_bitmap
		else:
			current_bitmap = green_bitmap
	current_bitmap.draw()
	win.flip()
	
win.close()