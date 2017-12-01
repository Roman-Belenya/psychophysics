from experiment_part import *
import json
from psychopy import visual, core
from tools import *
import Tkinter as tk

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

# exp = ExperimentPart(win, **params['Global'])
# exp.fixation_cross.draw()
# exp.win.flip()
# core.wait(2)
# exp.win.close()

# exp = FreeChoiceExperiment(win, **params['FreeChoiceExperiment'])
# exp.make_images_sequence()


class Applicaiton(object):
	
	def __init__(self, root):
	
		self.root = root
		self.program_path = os.getcwd()
		self.frame = tk.Frame(root)
		self.frame.grid(row = 0, column = 0, sticky = 'wns', padx=  30, pady = 30)
		
		tk.Label(self.frame, text = 'Participant id', row = 1, column = 0)
		self.subject_id = tk.Entry(self.frame)
		self.subject_id.grid(row = 1, column = 1)
		
	def start_experiment(self):
		pass