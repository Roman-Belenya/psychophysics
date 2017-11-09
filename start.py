from experiment_part import *
import json
from psychopy import visual
from tools import *

with open('parameters.json', 'rb') as f:
	params = json.load(f)

win = visual.Window(
	monitor = 'labBENQ',
	fullscr = True,
	colorSpace = 'rgb255',
	color = 128,
	units = 'deg')

# exp = ContrastDetection(win, **params['ContrastDetection'])
# exp.main_sequence()

path = "C:\Users\marotta_admin\Desktop\psychophysics-exp\images\line_drawings\obj032bat.png"
fg = get_fg_mask(path)

stim = visual.ImageStim(
	win = win, 
	image = path,
	mask = None,
	units = 'deg',
	size = 5,
	colorSpace = 'rgb255',
	color = inverse_colour(0))

stim.draw()
win.flip()
event.waitKeys()
win.close()