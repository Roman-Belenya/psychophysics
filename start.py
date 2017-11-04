from experiment_part import *
import json
from psychopy import visual

with open('parameters.json', 'rb') as f:
	params = json.load(f)

win = visual.Window(
	monitor = 'labBENQ',
	fullscr = True,
	colorSpace = 'rgb255',
	color = 128,
	units = 'pix')

exp = ContrastDetection(win, **params['ContrastDetection'])
exp.main_sequence()