import numpy as np
import glob
import os
from psychopy import visual, core, event
from PIL import Image

np.random.seed(1)

class ExperimentPart(object):

	def __init__(self, win):
		self.win = win
		
		self.instructions = visual.TextStim(
			win = self.win,
			colorSpace = 'rgb255',
			color = [255, 255, 255],
			text = 'a',
			pos = (0, 0))
		
		self.press_any = visual.TextStim(
			win = self.win,
			colorSpace = 'rgb255',
			color = [255, 255, 255],
			text = 'Press any button to continue',
			pos = (0, -100))
			
	def show_instructions(self, text):
	
		self.instructions.text = text
		self.instructions.draw()
		self.press_any.draw()
		self.win.flip()
		event.waitKeys()
		
		
	def from_rgb(self, value):
		assert np.all(value >= 0) and np.all(value <= 255), 'Invalid value'
		
		return value / 127.5 - 1
		
		
	def to_rgb(self, value):
		assert np.all(value >= -1) and np.all(value <= 1), 'Invalid value in {}'.format(np.unique(value))

		v = 255 + np.around((value - 1) * 127.5)
		return int(v)
			
			
	def get_fg_mask(self, img_path):
		# returns psyhopy mask of black pixel locations
		# 1 = transparent, -1 = opaque
    
		img = np.flip(np.array(Image.open(img_path)), 0)
		fg = self.from_rgb(img[:,:,0]) * -1

		return fg
		

class ContrastDetection(ExperimentPart):

	def __init__(self, win, **params):
		
		super(ContrastDetection, self).__init__(win=win)
		
		for name, value in params.items():
			setattr(self, name, value)
		
		seq = [1]*(self.n_trials - 3) + [0]*self.n_catch_trials # 1=trial, 0=catch trial
		np.random.shuffle(seq) # randomise the seq array
		self.trial_seq = [1, 1, 1] + seq
		
		self.keys = [self.detect_key, self.not_detect_key, 'escape']
		self.responses = []
		
		self.images = glob.glob(self.images_path + '/*.png')
		
		self.instructions = visual.TextStim(
			win = self.win,
			color = [255, 255, 255],
			text = self.instructions)
			
		self.detect = visual.TextStim(
			win = self.win,
			colorSpace = 'rgb255',
			color = [255, 255, 255],
			text = 'F = detected',
			pos = (-200, 0),
			alignHoriz = 'center',
			alignVert = 'center')
		
		self.not_detect = visual.TextStim(
			win = self.win,
			colorSpace = 'rgb255',
			color = [255, 255, 255],
			text = 'J = not detected',
			pos = (200, 0),
			alignHoriz = 'center',
			alignVert = 'center')
			
		self.stim = visual.GratingStim(
			win = self.win,
			tex = None,
			mask = None,
			size = (300, 300),
			colorSpace = 'rgb255',
			color = self.grey_value,
			phase = 0.5)
		
		
	def run_trial(self, clock):
	
		self.stim.draw()
		self.win.flip()
		clock.reset()
		while clock.getTime() <= self.stim_latency:
			pass
		self.win.flip()
		
		
	def get_response(self):
	
		self.detect.color = 255
		self.not_detect.color = 255
		
		self.detect.draw()
		self.not_detect.draw()
		self.win.flip()
		key = event.waitKeys(keyList = self.keys)
		
		if key[0] == self.detect_key:
			response = 'detect'
			increment = -1
			self.detect.color = 150
		
		elif key[0] == self.not_detect_key:
			response = 'not_detect'
			increment = 1
			self.not_detect.color = 150
			
		elif key[0] == 'escape':
			response = 'stop'
			increment = None
			
		self.detect.draw()
		self.not_detect.draw()
		self.win.flip()
		
		return response, increment
			
		
	def main_sequence(self):
	
		self.show_instructions(self.instructions_text)
		clock = core.Clock()
		core.wait(1)
		
		# i = trial number, trial = type (1=exp, 0=catch)
		for i, kind in zip(range(self.n_trials), self.trial_seq):
		
			# Process the image
			img = str(np.random.choice(self.images)) # strange error here if left without str
			fg = self.get_fg_mask(img)
			self.stim.tex = img
			self.stim.mask = fg
			self.stim.color = self.grey_value
			
			#Run the trial
			core.wait(self.stim_pre_delay)
			self.run_trial(clock)
			core.wait(self.stim_post_delay)
			
			# Get the response
			response, increment = self.get_response()
			self.responses.append( (i, kind, self.grey_value, response) )
			if response == 'stop':
				return
				
			# Adjust grey if experimental trial
			if kind:
				self.grey_value += increment * self.colour_delta
				print self.grey_value
		
			
		