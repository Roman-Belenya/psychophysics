import numpy as np
import glob
import os
from psychopy import visual, core, event
from tools import *
import sys

np.random.seed(1)

class ExperimentPart(object):

	def __init__(self, win, **params):

		for name, value in params.items():
			setattr(self, name, value)

		self.win = win
		self.images = glob.glob(self.images_path + '/*.png')
		self.responses = []
		# self.keys = [self.pos_key, self.neg_key, 'escape']

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


	def export_results():
		pass


class ContrastDetection(ExperimentPart):


	def __init__(self, win, **params):

		super(ContrastDetection, self).__init__(win = win, **params)

		# self.stim.color = invert(self.grey)
		self.stim.color = self.grey


		seq = [1]*(self.n_trials - 3) + [0]*self.n_catch_trials # 1=trial, 0=catch trial
		np.random.shuffle(seq) # randomise the seq array
		self.trial_seq = [1, 1, 1] + seq

		self.keys = [self.pos_key, self.neg_key, 'escape']

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
			# self.stim.tex = img
			self.stim.mask = fg
			# self.stim.color = invert(self.grey)
			self.stim.color = self.grey


			#Run the trial
			core.wait(self.stim_pre_delay)
			self.run_trial(clock, kind)
			core.wait(self.stim_post_delay)

			# Get the response
			response, increment = self.get_response()
			self.responses.append( (i, kind, self.grey, response) )
			print self.responses[-1]
			if response == 'stop':
				break

			# Adjust grey if experimental trial
			if kind == 1:
				self.grey += increment * self.colour_delta





class IsoluminanceDetection(ExperimentPart):

	def __init__(self, win, **params):

		super(IsoluminanceDetection, self).__init__(win=win, **params)

		self.fix_col = np.array(self.fix_col)
		self.var_col_lo = np.array(self.var_col_lo)
		self.var_col_hi = np.array(self.var_col_hi)
		self.col_delta = np.array(self.col_delta)

		self.keys = [self.up_key, self.down_key, 'escape', 'return']

		self.done = visual.TextStim(
			win = self.win,
			colorSpace = 'rgb255',
			color = 255,
			text = 'done',
			pos = (0, 0),
			alignHoriz = 'center',
			alignVert = 'center')



	def run_trial(self, colour):
		'''colour is the colour to be changed in the trial'''

		frame = 0
		half_cycle = self.monitor_fs / (2.0 * self.flicker_fs)

		while True:
			if frame % half_cycle == 0:
				if np.all(self.stim.color == self.fix_col):
					self.stim.color = colour
				else:
					self.stim.color = self.fix_col
			self.stim.draw()
			self.win.flip()
			frame += 1

			ans = event.getKeys(keyList = self.keys)
			if ans:
				ans, = ans # unpack from the list
				if ans == 'up':
					colour = change_colour(colour, self.col_delta)
				elif ans == 'down':
					colour = change_colour(colour, -1*self.col_delta)
				elif ans == 'return':
					print colour
					return colour
				elif ans == 'escape':
					# skip to the next trial, do not increment trial no
					sys.exit()


 
	def run_block(self, kind, images_seq):

		if kind == 'up':
			text = self.instructions_text_up
			colour = self.var_col_lo
		elif kind == 'down':
			text = self.instructions_text_down
			colour = self.var_col_hi
		self.show_instructions(text)

		values = []

		for i in range(self.n_trials):

			img = images_seq[i]
			fg = get_fg_mask(img)
			self.stim.mask = fg

			iso_colour = self.run_trial(colour)

			values.append(iso_colour)

			self.done.draw()
			self.win.flip()
			core.wait(1)

		avg_colour = np.around(np.mean(values, axis = 0), 0)
		return avg_colour


	def main_sequence(self):
	
		self.show_instructions(self.instructions_text)

		assert len(self.blocks_seq) == self.n_blocks

		images_seq = np.random.choice(self.images, size = self.n_trials, replace = False)

		for i, kind in zip(range(self.n_blocks), self.blocks_seq):

			np.random.shuffle(images_seq)
			avg_col = self.run_block(kind, images_seq)
			self.responses.append((i, kind, avg_col))
			print self.responses[-1]

