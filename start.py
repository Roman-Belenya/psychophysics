from experiment_part import *
import json
from psychopy import visual, core
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

# exp1 = ContrastDetection(win, **params['ContrastDetection'])
# exp2 = IsoluminanceDetection(win, **params['IsoluminanceDetection'])

# exp1.main_sequence()
# exp2.main_sequence()

# exp = ExperimentPart(win, **params['Global'])
# exp.fixation_cross.draw()
# exp.win.flip()
# core.wait(2)
# exp.win.close()

exp = FreeChoiceExperiment(win, **params['FreeChoiceExperiment'])
exp.make_images_sequence()