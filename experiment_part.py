import numpy as np
from psychopy import visual, core, event

np.random.seed(1)

class ExperimentPart(object):

	def __init__(self, **kwargs):
		for name, value in kwargs.items():
			setattr(self, name, value)
		
		

class ContrastDetection(ExperimentPart):

	def __init__(self, win):
		
		super(ContrastDetection, self).__init__(win)
		
		self.n_trials = 20
		self.n_catch_trials = 5
		seq = [1]*(self.n_trials - 3) + [0]*self.n_catch_trials # 1=trial, 0=catch trial
		np.random.shuffle(seq) # randomise the seq array
		self.trial_sequence = [1, 1, 1] + seq
		
		self.grey_value = 128
		self.colour_delta = 1
		
		self.responses = []
		
		
	def show_instructions(self):
		pass
		
	def run_trial(self):
		pass
		
	def wait_response(self):
		pass
		
	def main_sequence(self):
		pass