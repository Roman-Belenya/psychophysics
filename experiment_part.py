# -*- coding: utf-8 -*-

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
import logging


logger = logging.getLogger(__name__)

np.random.seed(1)

class ExperimentPart(object):

    def __init__(self, win, _id, params):

        for name, value in params.items():
            if type(value) is list:
                    value = np.array(value)
            setattr(self, name, value)

        self.datetime = datetime.datetime.now()

        self.win = win
        self.id = _id
        self.images = glob.glob(os.path.join(self.images_dir, '*.png'))
        self.responses = []
        self.colheaders = []
        self.finished = False
        self.clock = core.Clock()

        # self.instructions = visual.TextStim(
        #     win = self.win,
        #     colorSpace = 'rgb255',
        #     color = 255,
        #     text = '',
        #     pos = (0, 0))
        # self.instructions.wrapWidth = 30

        self.instructions = visual.ImageStim(win = self.win)

        # self.press_space = visual.TextStim(
        #     win = self.win,
        #     colorSpace = 'rgb255',
        #     color = 255,
        #     text = 'Press the space bar to continue',
        #     pos = (0, -10))

        self.stim = visual.ImageStim(
            win = self.win,
            units = 'deg',
            size = self.stim_size,
            colorSpace = 'rgb255',
            interpolate = True)

        # self.fixation_cross = visual.GratingStim(
        #     win = self.win,
        #     tex = None,
        #     mask = 'cross',
        #     size = 1,
        #     units = 'deg',
        #     colorSpace = 'rgb255',
        #     color = 135)

        fix_img = './images/fixation_cross.png'
        self.fixation_cross = visual.ImageStim(
            win = self.win,
            size = 3.42,
            colorSpace = 'rgb255',
            color = 135)
        self.fixation_cross.mask = get_fg_mask(fix_img)

        logger.info('creating {}'.format(str(self)))

    def __str__(self):
        return self.__class__.__name__


    # def show_instructions(self, text):

    #     self.instructions.text = text
    #     self.instructions.draw()
    #     # self.press_space.draw()
    #     self.win.flip()
    #     key = event.waitKeys(keyList = ['escape', 'space'])
    #     if key[0] == 'escape':
    #         return False
    #     return True

    def show_instructions(self, img):

        self.instructions.image = img
        self.instructions.draw()
        self.win.flip()
        key = event.waitKeys(keyList = ['escape', 'space'])
        if key[0] == 'escape':
            return False
        return True

    def export_results(self, filename, *extralines):

        while os.path.isfile(filename):
            name, ext = os.path.splitext(filename)
            filename = name + '_new' + ext

        with open(filename, 'wb') as f:
            if '.csv' in filename:
                delimiter = ','
            else:
                delimiter = '\t'

            writer = csv.writer(f, delimiter = delimiter)

            writer.writerow( ['Experiment:', str(self)] )
            writer.writerow( ['Participant:', self.id] )
            writer.writerow( ['Date:', self.datetime.strftime('%d %B %Y')] )
            exp_time = datetime.datetime.now()
            writer.writerow( ['Time:', self.datetime.strftime('%H:%M:%S'), exp_time.strftime('%H:%M:%S')] )

            for line in extralines:
                writer.writerow(line)
            writer.writerow('')
            writer.writerow( self.colheaders )

            for line in self.responses:
                writer.writerow(line)

        logger.info('exported file {}'.format(filename))



class ContrastDetection(ExperimentPart):

    def __init__(self, win, _id, params):

        super(ContrastDetection, self).__init__(win, _id, params)

        self.stim.color = self.bg_grey
        self.keys = [self.pos_key, self.neg_key, 'escape']
        self.colheaders = ['#', 'Condition', 'Stimulus', 'GreyValue', 'Response']

        self.positive = visual.TextStim(
            win = self.win,
            colorSpace = 'rgb255',
            color = 255,
            text = '→  detected'.decode('UTF-8'),
            pos = (7, 0))

        self.negative = visual.TextStim(
            win = self.win,
            colorSpace = 'rgb255',
            color = 255,
            text = 'not detected  ←'.decode('UTF-8'),
            pos = (-7, 0))


    @property
    def output_col(self):
        if not self.responses:
            return [999]*3
        # take average of positive responses to exprimental trials (exclude catch)
        values = [i[3] for i in self.responses if i[1] and i[4]]
        if not values:
            return [None, None, None]

        return np.mean(values, axis = 0).tolist()


    def run_trial(self, kind):

        self.win.flip()
        core.wait(self.t_prestim)

        if kind == 1: # if is experimental trial
            self.stim.draw()
        self.win.flip()
        self.clock.reset()
        while self.clock.getTime() <= self.t_stim:
            pass
        self.win.flip()
        core.wait(self.t_poststim)

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

        core.wait(1)
        self.positive.color = 255
        self.negative.color = 255

        return response, increment


    def main_sequence(self):

        start = self.show_instructions(self.instructions_img)
        print self.instructions.image
        if not start:
            logger.info('did not start experiment')
            return

        logger.info('started experiment')
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
            response, increment = self.run_trial(kind)
            if response == 'stop':
                logger.info('broke from the experiment')
                break

            self.responses.append( (i, kind, os.path.split(img)[1], list(self.fg_grey), response) )
            logger.info('ran trial: {}'.format(self.responses[-1]))

            # Adjust grey if experimental trial
            if kind:
                self.fg_grey += increment
                if response:
                    detects += 1
            i += 1

        self.win.flip()
        core.wait(2)
        self.finished = True



class IsoluminanceDetection(ExperimentPart):

    def __init__(self, win, _id, params):

        super(IsoluminanceDetection, self).__init__(win, _id, params)

        self.keys = [self.up_key, self.down_key, 'escape', 'return']
        self.colheaders = ['#', 'Condition', 'Stimulus', 'IsoColour']


    @property
    def output_col(self):
        if not self.responses:
            return [999]*3
        values = [i[3] for i in self.responses]
        return np.mean(values, axis = 0).tolist()


    def run_trial(self, colour):
        '''colour is the colour to be changed in the trial (var_col_lo or var_col_hi)'''

        half_cycle = self.win.monitor.refresh_rate / (2.0 * self.flicker_fs) # how many frames each image lasts during flickering (e.g. green 2 frames -> red 2 frames)
        frame = 0
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

        start = self.show_instructions(text)
        if not start:
            logger.info('did not start the block {}'.format(kind))
            return
        logger.info('started block {}'.format(kind))

        for i, img in enumerate(images_seq):

            self.stim.mask = get_fg_mask(img)

            core.wait(self.t_prestim)
            iso_col = self.run_trial(colour)
            self.win.flip()
            core.wait(self.t_poststim)

            if np.any(iso_col == 'stop'):
                return
            self.responses.append( (i, kind, os.path.split(img)[1], list(iso_col)) )
            logger.info('ran trial: {}'.format(self.responses[-1]))



    def main_sequence(self):

        start = self.show_instructions(self.instructions_img)
        if not start:
            logger.info('did not start the experiment')
            return
        logger.info('started the experiment')

        for i, kind in enumerate(self.blocks_seq):
            # get new images on block 0, 2, 4 ...
            if i % 2 == 0:
                images_seq = np.random.choice(self.images, size = self.n_trials, replace = False)
            np.random.shuffle(images_seq)
            self.run_block(kind, images_seq)

        self.win.flip()
        core.wait(2)
        self.finished = True



class FreeChoiceExperiment(ExperimentPart):

    def __init__(self, win, _id, colours_dict, params):

        super(FreeChoiceExperiment, self).__init__(win, _id, params)

        self.colours_dict = colours_dict
        self.check_colours_dict()

        self.stim.colorSpace = 'rgb' # back to default, would show inverted colours with rgb255
        self.colheaders = ['#', 'Condition', 'Stimulus', 'Response', 'Latency']

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

        # self.question = visual.TextStim(
        #     win = self.win,
        #     colorSpace = 'rgb255',
        #     color = 255,
        #     text = self.question_text,
        #     pos = (0, -5))


    def check_colours_dict(self):
        try:
            assert set(self.colours_dict.keys()) == set(['bg_grey', 'fg_grey', 'bg_col', 'fg_col'])
            for value in self.colours_dict.values():
                for v in value:
                    assert 0 <= v <= 255
        except Exception as e:
            logger.exception('bad colours dict: {}'.format(self.colours_dict))
            raise


    def make_images_seq_file(self):

        conditions = ['magno', 'parvo', 'unbiased']
        names = [os.path.split(os.path.splitext(i)[0])[1] for i in self.images]
        perm = list(product(conditions, names)) * self.n_trials
        np.random.shuffle(perm)

        with open(self.seq_file, 'wb') as f:
            writer = csv.writer(f)
            for line in perm:
                writer.writerow(line)


    def load_images_sequence(self):
        '''returns a sequence with MyImage objects. images are created here when encounered for the first time'''

        logger.info('loading trial sequence from {}'.format(self.seq_file))
        seq = []

        with open(self.seq_file, 'rb') as f:
            reader = csv.reader(f)

            for cond, stim in reader: # cond = 'magno', stim = 'Hs'
                path = os.path.join(self.images_dir, stim + '.png')
                img = MyImage(path, cond, self.colours_dict)
                seq.append(img)
        return seq


    def run_trial(self, img):

        self.stim.image = img.make_image()
        event.clearEvents()
        key = None

        # Randomly associate global and local letters with left/right response. Local/global letters can randomly appear on the left/right (4 possible combinations)
        # left = local, left = global, right = local, right = global
        left_letter, right_letter = np.random.choice([img.global_letter, img.local_letter], size = 2, replace = False)

        # Get rid of "num_" if needed (to display on screen)
        # lk = self.left_key.split('_')[-1]
        # rk = self.right_key.split('_')[-1]

        self.left_resp.text = '{}  ←'.format(left_letter.upper()).decode('UTF-8')
        self.right_resp.text = '→  {}'.format(right_letter.upper()).decode('UTF-8')

        self.fixation_cross.draw()
        self.win.flip()
        self.clock.reset()
        while self.clock.getTime() < self.t_fix:
            pass

        self.win.flip()
        core.wait(self.t_prestim)

        self.stim.draw()
        self.win.flip()
        self.clock.reset() # starts counting time from here

        while self.clock.getTime() < self.t_stim:
            if not key:
                key = event.getKeys(keyList = self.keylist, timeStamped = self.clock)

        if not key:
            # self.question.draw()
            self.left_resp.draw()
            self.right_resp.draw()
            self.win.flip()
            key = event.waitKeys(keyList = self.keylist, timeStamped = self.clock)

        key, = key
        latency = key[1]
        if key[0] == self.left_key:
            response = img.get_response_type(left_letter)
            self.left_resp.color = 150
        elif key[0] == self.right_key:
            response = img.get_response_type(right_letter)
            self.right_resp.color = 150
        elif key[0] == 'escape':
            response = 'stop'

        # self.question.draw()
        self.left_resp.draw()
        self.right_resp.draw()
        self.win.flip()

        core.wait(self.t_poststim)

        # Reset the colours of the answer options
        self.left_resp.color = 255
        self.right_resp.color = 255

        return response, latency


    def main_sequence(self):

        self.keylist = [self.left_key, self.right_key, 'escape']

        start = self.show_instructions(self.instructions_img)
        if not start:
            logger.info('did not start the experiment')
            return
        logger.info('started the experiment')

        images_seq = self.load_images_sequence()
        core.wait(1)

        for n, img in enumerate(images_seq):
            resp, lat = self.run_trial(img)
            if resp == 'stop':
                logger.info('stopped experiment')
                break
            self.responses.append( (n, img.cond, img.name, resp, lat) )
            logger.info('ran trial {}'.format(self.responses[-1]))

        self.win.flip()
        core.wait(2)
        self.finished = True



class DividedAttentionExperiment(FreeChoiceExperiment):

    def run_trial(self, img):

        self.stim.image = img.make_image()

        self.fixation_cross.draw()
        self.win.flip()
        self.clock.reset()
        while self.clock.getTime() < self.t_fix:
            pass

        self.win.flip()
        core.wait(self.t_prestim)

        self.stim.draw()
        self.win.flip()
        self.clock.reset()
        key = event.waitKeys(keyList = self.keylist, timeStamped = self.clock)

        key, = key
        latency = key[1]
        if key[0] == self.pos_key:
            response = 1
        elif key[0] == self.neg_key:
            response = 0
        elif key[0] == 'escape':
            response = 'stop'

        self.win.flip()
        core.wait(self.t_poststim)

        return response, latency


    def make_practice_images_sequence(self):

        seq = []
        for image in self.images: # only include unbiased images in practice trials
            img = MyImage(image, 'unbiased', self.colours_dict)
            seq.append(img)
        seq *= self.n_practice_trials # how many times each image should be repeated
        np.random.shuffle(seq)
        return seq


    def run_block(self, kind, imgs_seq):

        start = self.show_instructions(self.instructions_text_block)
        if not start:
            logger.info('did not start block {}'.format(kind))
            return
        logger.info('started block {}'.format(kind))
        core.wait(1)

        for i, img in enumerate(imgs_seq):
            resp, lat = self.run_trial(img)
            if resp == 'stop':
                logger.info('stopped block {}'.format(kind))
                return
            correct = img.has_letter(self.target_letter) == resp # this var tells whether the resp was correct or not
            self.responses.append( (i, kind, img.cond, img.name, resp, correct, lat) )
            logger.info('ran trial {}'.format(self.responses[-1]))

        logger.info('finished block {}'.format(kind))


    def main_sequence(self):

        self.colheaders = ['#', 'BlockType', 'Condition', 'Stimulus', 'Response', 'Correct', 'Latency']
        self.keylist = [self.pos_key, self.neg_key, 'escape']

        start = self.show_instructions(self.instructions_img)
        if not start:
            logger.info('did not start the experiment')
            return
        logger.info('started the experiment')

        blocks_seq = ['practice'] * self.n_practice_blocks + ['experimental'] * self.n_blocks
        practice_imgs_seq = self.make_practice_images_sequence()
        imgs_seq = self.load_images_sequence()

        for i, block in enumerate(blocks_seq):
            if block == 'practice':
                seq = practice_imgs_seq
            elif block == 'experimental':
                seq = imgs_seq

            # reverse the order of trials (the same as seq[::-1])
            if i > 0:
                seq = reversed(seq)
            self.run_block(block, seq)

        self.win.flip()
        core.wait(2)
        self.finished = True


class SelectiveAttentionExperiment(DividedAttentionExperiment):

    def run_trial(self, img):

        self.stim.image = img.make_image()

        left_letter, right_letter = np.random.choice([img.global_letter, img.local_letter], size = 2, replace = False)
        self.left_resp.text = '{}  ←'.format(left_letter.upper()).decode('UTF-8')
        self.right_resp.text = '→  {}'.format(right_letter.upper()).decode('UTF-8')

        self.fixation_cross.draw()
        self.win.flip()
        self.clock.reset()
        while self.clock.getTime() < self.t_fix:
            pass

        self.win.flip()
        core.wait(self.t_prestim)

        self.stim.draw()
        self.left_resp.draw()
        self.right_resp.draw()
        self.win.flip()
        self.clock.reset()
        key = event.waitKeys(keyList = self.keylist, timeStamped = self.clock)

        key, = key
        latency = key[1]
        if key[0] == self.left_key:
            response = img.get_response_type(left_letter)
            self.left_resp.color = 150
        elif key[0] == self.right_key:
            response = img.get_response_type(right_letter)
            self.right_resp.color = 150
        elif key[0] == 'escape':
            response = 'stop'

        self.stim.draw()
        self.left_resp.draw()
        self.right_resp.draw()
        self.win.flip()

        self.left_resp.color = 255
        self.right_resp.color = 255
        core.wait(self.t_poststim)

        return response, latency


    def run_block(self, kind, imgs_seq):

        if kind[1] == 'local':
            txt = self.instructions_img_local
        elif kind[1] == 'global':
            txt = self.instructions_img_global

        start = self.show_instructions(txt)
        if not start:
            logger.info('did not start block {}'.format(kind))
            return
        logger.info('started block {}'.format(kind))
        core.wait(1)

        for i, img in enumerate(imgs_seq):
            resp, lat = self.run_trial(img)
            if resp == 'stop':
                logger.info('stopped block {}'.format(kind))
                return
            self.responses.append( (i, '-'.join(kind), img.cond, img.name, resp, lat) )
            logger.info('ran trial {}'.format(self.responses[-1]))

        logger.info('finished block {}'.format(kind))


    def main_sequence(self):

        self.colheaders = ['#', 'BlockType', 'Condition', 'Stimulus', 'Response', 'Latency']
        self.keylist = [self.left_key, self.right_key, 'escape']

        # start = self.show_instructions(self.instructions_text)
        # if not start:
        #     logger.info('did not start the experiment')
        #     return
        logger.info('started the experiment')

        total_blocks = self.n_practice_blocks + self.n_blocks
        if self.local_first:
            cond_seq = ['local' if i%2==0 else 'global' for i in range(total_blocks)]
        else:
            cond_seq = ['global' if i%2==0 else 'local' for i in range(total_blocks)]
        type_seq = ['practice'] * self.n_practice_blocks + ['experimental'] * self.n_blocks
        blocks_seq = zip(type_seq, cond_seq) # (practice, global), (experimental, local) etc.
        logger.info('made blocks sequence: {}'.format(blocks_seq))

        practice_imgs_seq = self.make_practice_images_sequence()
        imgs_seq = self.load_images_sequence()

        for i, block in enumerate(blocks_seq):
            if block[0] == 'practice':
                seq = practice_imgs_seq
            elif block[0] == 'experimental':
                seq = imgs_seq

            if i > 0:
                seq = reversed(seq)
            self.run_block(block, seq)

        self.win.flip()
        core.wait(2)
        self.finished = True



#                           ExperimentPart
#                _______________|________________________
#               |               |                       |
#   ContrastDetection   IsoluminanceDetection   FreeChoiceExperiment
#                                                       |
#                                               DividedAttentionExperiment
#                                                       |
#                                               SelectiveAttentionExperiment

