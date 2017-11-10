import numpy as np
import glob
import os
from psychopy import visual, core, event
from tools import *

np.random.seed(1)

class ExperimentPart(object):

	def __init__(self, win, **params):

		for name, value in params.items():
			setattr(self, name, value)

		self.win = win
		self.images = glob.glob(self.images_path + '/*.png')
		self.responses = []
		self.keys = [self.pos_key, self.neg_key, 'escape']

		self.instructions = visual.TextStim(
			win = self.win,
			colorSpace = 'rgb255',
			color = 255,
			text = '',
			pos = (0, 0))

		# self.instructions = visual.TextBox(
		# 	window = self.win,
		# 	color_space = 'rgb255',
		# 	font_color = [255]*3,
		# 	text = 'ahaha',
		# 	size = (2,2),
		# 	grid_horz_justification='center', grid_vert_justification='center',
		# 	pos = (0, 0))

		self.press_any = visual.TextStim(
			win = self.win,
			colorSpace = 'rgb255',
			color = 255,
			text = 'Press any button to continue',
			pos = (0, -10))

		self.stim = visual.ImageStim(
			win = self.win,
			image = None,
			mask = None,
			units = 'deg',
			size = 5,
			colorSpace = 'rgb255',
			color = 0)


	def show_instructions(self, text):

		self.instructions.text = text
		# self.instructions.setText('these are my instructions')
		self.instructions.draw()
		self.press_any.draw()
		self.win.flip()
		event.waitKeys()


class ContrastDetection(ExperimentPart):


	def __init__(self, win, **params):

		super(ContrastDetection, self).__init__(win = win, **params)

		# self.stim.color = invert(self.grey_value)
		self.stim.color = self.grey_value


		seq = [1]*(self.n_trials - 3) + [0]*self.n_catch_trials # 1=trial, 0=catch trial
		np.random.shuffle(seq) # randomise the seq array
		self.trial_seq = [1, 1, 1] + seq

		self.positive = visual.TextStim(
			win = self.win,
			colorSpace = 'rgb255',
			color = 255,
			text = '{} = detected'.format(self.pos_key.upper()),
			pos = (-7, 0),
			alignHoriz = 'center',
			alignVert = 'center')

		self.negative = visual.TextStim(
			win = self.win,
			colorSpace = 'rgb255',
			color = 255,
			text = '{} = not detected'.format(self.neg_key.upper()),
			pos = (7, 0),
			alignHoriz = 'center',
			alignVert = 'center')


	def run_trial(self, clock, kind):

		if kind == 1: # if is experimental trial
			self.stim.draw()
		self.win.flip()
		clock.reset()
		while clock.getTime() <= self.stim_latency:
			pass
		self.win.flip()


	def get_response(self):

		self.positive.color = 255
		self.negative.color = 255

		self.positive.draw()
		self.negative.draw()
		self.win.flip()
		key = event.waitKeys(keyList = self.keys)

		if key[0] == self.pos_key:
			response = 1
			increment = -self.colour_delta
			self.positive.color = 150

		elif key[0] == self.neg_key:
			response = 0
			increment = self.colour_delta
			self.negative.color = 150

		elif key[0] == 'escape':
			response = 'stop'
			increment = None

		self.positive.draw()
		self.negative.draw()
		self.win.flip()

		return response, increment


	def main_sequence(self):

		self.show_instructions(self.instructions_text)
		clock = core.Clock()
		core.wait(1)

		image_seq = np.random.choice(self.images, size = self.n_trials, replace = False)
		# i = trial number, trial = type (1=exp, 0=catch)
		for i, kind in zip(range(self.n_trials), self.trial_seq):

			# Process the image
			img = image_seq[i]
			fg = get_fg_mask(img)
			self.stim.tex = img
			self.stim.mask = fg
			# self.stim.color = invert(self.grey_value)
			self.stim.color = self.grey_value


			#Run the trial
			core.wait(self.stim_pre_delay)
			self.run_trial(clock, kind)
			core.wait(self.stim_post_delay)

			# Get the response
			response, increment = self.get_response()
			self.responses.append( (i, kind, self.grey_value, response) )
			print self.responses[-1]
			if response == 'stop':
				break

			# Adjust grey if experimental trial
			if kind == 1:
				self.grey_value += increment * self.colour_delta





class IsoluminanceDetection(ExperimentPart):

	def __init__(self, win, **params):

		super(IsoluminanceDetection, self).__init__(win=win, **params)

		self.positive.text = '{} = flickered'.format(self.pos_key.upper())
		self.negative.text = '{} = not flickered'.format(self.neg_key.upper())
		self.red = np.array(self.red)
		self.green = np.array(self.green)
		self.stim.color = self.red


	def run_trial(self, clock):

		frame = 0
		half_cycle = self.monitor_fs / (2.0 * self.flicker_fs)
		clock.reset()

		while clock.getTime() < self.stim_latency:
			if frame % half_cycle == 0:
				if np.all(self.stim.color == self.red):
					self.stim.color = self.green
				else:
					self.stim.color == self.red
			self.stim.draw()
			self.win.flip()


	def main_sequence(self):
		self.show_instructions(self.instructions_text)
		clock = core.Clock()
		core.wait(1)
