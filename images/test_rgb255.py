from psychopy import visual, core
import glob
from PIL import Image
import numpy as np


pics = glob.glob('./images/line_drawings/*.png')

def get_fg_mask(img_path):
		# returns psyhopy mask of black pixel locations
		# 1 = transparent, -1 = opaque
    
		img = np.flip(np.array(Image.open(img_path)), 0)
		fg = from_rgb(img[:,:,0]) * -1

		return fg
		
def from_rgb(value):
	assert np.all(value >= 0) and np.all(value <= 255), 'Invalid value'
	
	return value / 127.5 - 1


win = visual.Window(
	monitor = 'labBENQ',
	colorSpace = 'rgb255',
	color = 128,
	units = 'pix')
	
stim = visual.GratingStim(
	win = win,
	tex = None,
	mask = None,
	size = (300, 300),
	colorSpace = 'rgb255',
	color = 150)
	
	
for i in range(10):
	stim.tex = pics[i]
	stim.mask = get_fg_mask(pics[i])
	stim.draw()
	win.flip()
	core.wait(0.5)
	