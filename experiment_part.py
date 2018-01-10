import psychopy
from psychopy import visual, core, event
import numpy as np
import glob
import os
from tools import *
from my_image import MyImage
import sys
from itertools import product
import csv
import shutil
import datetime

np.random.seed(1)

class ExperimentPart(object):

    def __init__(self, win, id, params):

        for name, value in params.items():
            if type(value) is list:
                    value = np.array(value)
            setattr(self, name, value)

        self.datetime = datetime.datetime.now()

        self.win = win
        self.id = id
        self.images = [os.path.abspath(img) for img in glob.glob(os.path.join(self.images_dir, '*.png'))]
        self.responses = []
        self.colheaders = []
        self.finished = False

        self.instructions = visual.TextStim(
            win = self.win,
            colorSpace = 'rgb255',
            color = 255,
            text = '',
            pos = (0, 0))

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
            size = self.stim_size,
            colorSpace = 'rgb255')

        self.fixation_cross = visual.GratingStim(
            win = self.win,
            tex = None,
            mask = 'cross',
            size = 1,
            units = 'deg',
            colorSpace = 'rgb255',
            color = 135)

    def __str__(self):
        return self.__class__.__name__


    def show_instructions(self, text):

        self.instructions.text = text
        # self.instructions.setText('these are my instructions')
        self.instructions.draw()
        self.press_any.draw()
        self.win.flip()
        key = event.waitKeys()
        if key[0] == 'escape':
            return False
        return True


    def export_results(self, filename, *extralines):

        with open(filename, 'wb') as f:
            writer = csv.writer(f, delimiter = '\t')

            writer.writerow( ['Experiment:', str(self)] )
            writer.writerow( ['Date:', self.datetime.strftime('%d %B %Y')] )
            writer.writerow( ['Time:', self.datetime.strftime('%H:%M:%S')] )
            for line in extralines:
                writer.writerow(line)
            writer.writerow('')
            writer.writerow( self.colheaders )

            for line in self.responses:
                writer.writerow(line)



class ContrastDetection(ExperimentPart):

    def __init__(self, win, id, params):

        super(ContrastDetection, self).__init__(win, id, params)

        self.stim.color = self.bg_grey
        self.keys = [self.pos_key, self.neg_key, 'escape']
        self.colheaders = ['#', 'Kind', 'Grey_value', 'Response']

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


    @property
    def output_col(self):
        if not self.responses:
            return [999]*3
        # take average of positive responses to exprimental trials (exclude catch)
        values = [i[2] for i in self.responses if i[1] and i[3]]
        if not values:
            return [None, None, None]
  
        return np.mean(values, axis = 0).tolist()


    def run_trial(self, clock, kind):

        if kind == 1: # if is experimental trial
            self.stim.draw()
        self.win.flip()
        clock.reset()
        while clock.getTime() <= self.t_stim:
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
            response, increment = ('stop', None)

        self.positive.draw()
        self.negative.draw()
        self.win.flip()

        return response, increment


    def main_sequence(self):

        start = self.show_instructions(self.instructions_text)
        if not start:
            return

        clock = core.Clock()
        core.wait(1)
                
        i = 0
        detects = 0 # number of times they detected the image when kind == 1
        
        while detects < self.n_trials:
            
            if i < 5:
                kind = 1
            else:
                kind = np.random.choice([0, 1], p = [self.p_catch, 1 - self.p_catch])
                
            # Process the image
            if kind:
                img = np.random.choice(self.images)
                fg = get_fg_mask(img)
                self.stim.mask = fg
                self.stim.color = self.fg_grey

            #Run the trial
            core.wait(self.t_prestim)
            self.run_trial(clock, kind)
            core.wait(self.t_poststim)

            # Get the response
            response, increment = self.get_response()
            if response == 'stop':
                break

            self.responses.append( (i, kind, list(self.fg_grey), response) )
            print self.responses[-1]

            # Adjust grey if experimental trial
            if kind:
                self.fg_grey += increment
                if response:
                    detects += 1
            i += 1
            

        core.wait(2)
        self.finished = True





class IsoluminanceDetection(ExperimentPart):

    def __init__(self, win, id, params):

        super(IsoluminanceDetection, self).__init__(win, id, params)

        self.keys = [self.up_key, self.down_key, 'escape', 'return']
        self.colheaders = ['#', 'Kind', 'Colour']

        self.done = visual.TextStim(
            win = self.win,
            colorSpace = 'rgb255',
            color = 255,
            text = 'Done!',
            pos = (0, 0),
            alignHoriz = 'center',
            alignVert = 'center')

    @property
    def output_col(self):
        if not self.responses:
            return [999]*3
        values = [i[2] for i in self.responses]
        return np.mean(values, axis = 0).tolist()


    def run_trial(self, colour):
        '''colour is the colour to be changed in the trial'''

        frame = 0
        half_cycle = self.monitor_fs / (2.0 * self.flicker_fs) # how much frames each image lasts for during flickering

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
                if ans[0] == 'up':
                    colour = change_colour(colour, self.col_delta)
                elif ans[0] == 'down':
                    colour = change_colour(colour, -1*self.col_delta)
                elif ans[0] == 'return':
                    return colour
                elif ans[0] == 'escape':
                    return 'stop'



    def run_block(self, kind, images_seq):

        if kind == 'up':
            text = self.instructions_text_up
            colour = self.var_col_lo
        elif kind == 'down':
            text = self.instructions_text_down
            colour = self.var_col_hi
        self.show_instructions(text)

        for i in range(self.n_trials):

            img = images_seq[i]
            fg = get_fg_mask(img)
            self.stim.mask = fg

            core.wait(self.t_prestim)
            iso_col = self.run_trial(colour)
            if np.any(iso_col == 'stop'):
                return
            self.responses.append( (i, kind, list(iso_col)) )
            print self.responses[-1]

            self.win.flip()
            core.wait(self.t_poststim)


    def main_sequence(self):

        start = self.show_instructions(self.instructions_text)
        if not start:
            return

        for i, kind in enumerate(self.blocks_seq):

            # get new images on block 0, 2, 4 ...
            if i % 2 == 0:
                images_seq = np.random.choice(self.images, size = self.n_trials, replace = False)
            np.random.shuffle(images_seq)
            self.run_block(kind, images_seq)

        core.wait(2)
        self.finished = True



class FreeChoiceExperiment(ExperimentPart):

    def __init__(self, win, id, params):

        super(FreeChoiceExperiment, self).__init__(win, id, params)

        self.stim.colorSpace = 'rgb' # back to default, would show inverted colours with rgb255
        self.keylist = [self.left_key, self.right_key, 'escape']

        self.colheaders = ['#', 'Condition', 'Stimulus', 'Responce', 'Latency']

        self.left_resp = visual.TextStim(
            win = self.win,
            colorSpace = 'rgb255',
            color = 255,
            pos = [-3, -8])

        self.right_resp = visual.TextStim(
            win = self.win,
            colorSpace = 'rgb255',
            color = 255,
            pos = [3, -8])

        self.question = visual.TextStim(
            win = self.win,
            colorSpace = 'rgb255',
            color = 255,
            text = self.question_text,
            pos = (0, -5))


    def define_colours(self, col_dict):

        for name, value in col_dict.items():
            setattr(self, name, value)


    def make_images(self):

        out_dir = os.path.join('.', self.id, 'stimuli')
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)

        for img_path in self.images:
            img = MyImage(img_path, out_dir)
            img.apply_colours(self.fg_col, self.bg_col, self.fg_grey, self.bg_grey)



    def make_images_sequence(self):

        names = [os.path.split(os.path.splitext(i)[0])[1] for i in self.images]
        perm = list(product(self.conditions, names))
        perm = perm * self.n_trials
        np.random.shuffle(perm)

        with open(self.seq_file, 'wb') as f:
            writer = csv.writer(f)
            for line in perm:
                writer.writerow(line)


    def read_images_sequence(self, file):

        seq = []
        out_dir = os.path.join('.', self.id, 'stimuli')

        with open(file, 'rb') as f:
            reader = csv.reader(f)
            for cond, stim in reader:
                path = os.path.join(self.images_dir, stim + '.png')
                img = MyImage(path, out_dir)
                seq.append((cond, img))

        return seq


    def run_trial(self, kind, clock, image):

        if kind == 'parvo':
            self.stim.setImage(image.parvo_path)
        elif kind == 'magno':
            self.stim.setImage(image.magno_path)
        elif kind == 'unbiased':
            self.stim.setImage(image.unbiased_path)

        # Randomly associate global and local letters with left/right response
        left_letter, right_letter = np.random.choice([image.global_letter, image.local_letter], size = 2, replace = False)
        
        self.left_resp.color = 255
        self.right_resp.color = 255
        
        # Get rid of "num_" if needed
        lk = self.left_key.split('_')[-1]
        rk = self.right_key.split('_')[-1]
        
        self.left_resp.text = '{} = {}'.format(lk, left_letter.upper())
        self.right_resp.text = '{} = {}'.format(rk, right_letter.upper())

        event.clearEvents()
        key = None

        self.fixation_cross.draw()
        self.win.flip()
        clock.reset()
        while clock.getTime() < self.t_fix:
            pass

        self.stim.draw()
        self.win.flip()
        clock.reset() # starts counting time from here

        while clock.getTime() < self.t_stim:
            if not key:
        		key = event.getKeys(keyList = self.keylist, timeStamped = clock)

        if not key:
            self.question.draw()
            self.left_resp.draw()
            self.right_resp.draw()
            self.win.flip()
            key = event.waitKeys(keyList = self.keylist, timeStamped = clock)

        key, = key
        latency = key[1]
        if key[0] == self.left_key:
            response = image.get_response_type(left_letter)
            self.left_resp.color = 150
        elif key[0] == self.right_key:
            response = image.get_response_type(right_letter)
            self.right_resp.color = 150
        elif key[0] == 'escape':
            response = 'stop'

        self.question.draw()
        self.left_resp.draw()
        self.right_resp.draw()
        self.win.flip()

        return response, latency


    def main_sequence(self):

        start = self.show_instructions(self.instructions_text)
        if not start:
            return

        clock = core.Clock()
        core.wait(1)

        self.make_images()
        images_seq = self.read_images_sequence(self.seq_file)
        n = 0

        for cond, img in images_seq:

            # Run trial
            core.wait(self.t_prestim)
            resp, lat = self.run_trial(cond, clock, img)
            if resp == 'stop':
                break
            core.wait(self.t_poststim)
            self.responses.append( (n, cond, img.name, resp, lat) )
            print self.responses[-1]
            n += 1


        core.wait(2)
        self.finished = True



