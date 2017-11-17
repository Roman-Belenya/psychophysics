from experiment_part import *
import json
from psychopy import visual
from tools import *

with open('parameters.json', 'rb') as f:
	params = json.load(f)

win = visual.Window(
	size = [1920, 1080],
	monitor = 'labBENQ',
	fullscr = True,
	colorSpace = 'rgb255',
	color = 128,
	units = 'deg')

exp1 = ContrastDetection(win, **params['ContrastDetection'])
exp2 = IsoluminanceDetection(win, **params['IsoluminanceDetection'])

exp1.main_sequence()
exp2.main_sequence()

# path = "./images/line_drawings/obj032bat.png"
# fg = get_fg_mask(path)

# stim = visual.ImageStim(
# 	win = win,
# 	image = path,
# 	mask = None,
# 	units = 'deg',
# 	size = 5,
# 	colorSpace = 'rgb255',
# 	color = inverse_colour(0))

# stim.draw()
# win.flip()
# event.waitKeys()
# win.close()
