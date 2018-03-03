from psychopy import visual, event, monitors, tools
import numpy as np
from colour_tools import *
from collections import OrderedDict
import json
import sys
sys.path.insert(0, '../')
from tools import load_monitor


class MyStim(visual.grating.GratingStim):

    def __init__(self, **kwargs):

        super(MyStim, self).__init__(**kwargs)

        all_spaces = ['dkl', 'rgb255', 'lms']

        texts = [
            visual.TextStim(win = self.win,
                pos = [self.pos[0], self.pos[1] - (self.size[1] + 50 + i*50)],
                color = 0.2) for i in range(3)
            ]

        self.col_texts = OrderedDict( zip(all_spaces, texts) )

        self.space_text = visual.TextStim(win = self.win,
            text = self.colorSpace,
            pos = [self.pos[0], self.pos[1] + self.size[1] + 50])

        self.dkl2rgb_m = self.win.monitor.getDKL_RGB()
        self.rgb2dkl_m = np.linalg.inv(self.dkl2rgb_m)
        self.lms2rgb_m = self.win.monitor.getLMS_RGB()
        self.rgb2lms_m = np.linalg.inv(self.lms2rgb_m)

        self.colours = OrderedDict( zip(all_spaces, [None]*3) )
        self.update_colours()


    def change_space(self, space):

        if self.colorSpace != space:
            self.colorSpace = space
            self.space_text.text = space
            self.color = self.colours[space]


    def change_colour(self, mag, idx):

        delta = [0, 0, 0]

        if self.colorSpace == 'dkl':
            if idx == 2:
                delta[idx] += mag * 0.01
            else:
                delta[idx] += mag
        elif self.colorSpace == 'lms':
            delta[idx] += mag * 0.01
        else:
            delta[idx] += mag

        self.color += delta
        self.update_colours()


    def update_colours(self):

        self.colours[self.colorSpace] = self.color

        if self.colorSpace == 'dkl':
            self.colours['rgb255'] = dkl2rgb(self.color, self.dkl2rgb_m)
            self.colours['lms'] = rgb2lms(self.colours['rgb255'], self.rgb2lms_m)

        elif self.colorSpace == 'rgb255':
            self.colours['dkl'] = rgb2dkl(self.color, self.rgb2dkl_m)
            self.colours['lms'] = rgb2lms(self.color, self.rgb2lms_m)

        elif self.colorSpace == 'lms':
            self.colours['rgb255'] = lms2rgb(self.color, self.lms2rgb_m)
            self.colours['dkl'] = rgb2dkl(self.colours['rgb255'], self.rgb2dkl_m)

        for key, value in self.colours.items():
            # self.col_texts[key].text = str(np.around(value, 2))
            self.col_texts[key].text = '[ {:.2f} {:.2f} {:.2f} ]'.format(*value)


    def reset_colour(self):

        self.color = [0, 0, 0]
        self.update_colours()


    def round_colour(self):

        if self.colorSpace == 'dkl':
            self.color = np.append(np.around(self.color[0:2], 0), np.around(self.color[2], 2))
        elif self.colorSpace == 'rgb255':
            self.color = np.around(self.color, 0)
        elif self.colorSpace == 'lms':
            self.color = np.around(self.color, 2)

        self.update_colours()


    def unhighlight(self):

        for col_text in self.col_texts.values():
            col_text.color = 0.2


    def highlight(self, space):

        self.unhighlight()
        self.col_texts[space].color = 1


    def draw_all(self):

        self.draw()
        self.space_text.draw()
        for col_text in self.col_texts.values():
            col_text.draw()






class ColourSpaces(object):

    def __init__(self, nStimuli = 2):

        params = json.load(open('../parameters.json', 'rb'))
        mon = load_monitor(params['Monitors'][params['current_monitor']])

        self.win = visual.Window(
            size = [1500, 1024],
            monitor = mon,
            screen = 0,
            fullscr = False,
            allowGUI = False,
            color = 0,
            units = 'pix')

        self.nStimuli = nStimuli

        self.stimuli = [
            MyStim(
                win = self.win,
                tex = None,
                size = self.win.size[1] / (2 * nStimuli),
                pos = [-self.win.size[0] / 2.0 + self.win.size[0] * (i+1) / (nStimuli+1), 0],
                colorSpace = 'dkl',
                color = [-90, 0, 1]) for i in range(nStimuli)
            ]





    def flicker(self):

        stim_idx1 = event.waitKeys(keyList = map(str, range(10)))
        stim_idx1 = int(stim_idx1[0])
        stim_idx2 = event.waitKeys(keyList = map(str, range(10)))
        stim_idx2 = int(stim_idx2[0])

        if stim_idx1 > len(self.stimuli)-1 or stim_idx2 > len(self.stimuli)-1:
            return

        fstim = visual.GratingStim(self.win,
            tex = None,
            mask = 'circle',
            size = self.stimuli[0].size / 2.0,
            pos = [0, 0],
            colorSpace = self.stimuli[stim_idx1].colorSpace)

        self.win.flip()
        frame = 0
        key = None

        col1 = self.stimuli[stim_idx1].color
        sp1 = self.stimuli[stim_idx1].colorSpace
        col2 = self.stimuli[stim_idx2].color
        sp2 = self.stimuli[stim_idx2].colorSpace


        while not key:
            if frame % 1 == 0:
                if np.all(fstim.color == col1):
                    fstim.color = col2
                else:
                    fstim.color = col1
            fstim.draw()
            self.win.flip()
            frame += 1
            key = event.getKeys()



    def main(self):

        for stim in self.stimuli:
            stim.draw_all()
        self.win.flip()

        spaces = ['dkl', 'rgb255', 'lms']
        cur_stim = 0
        cur_space = 0

        decrease_keys = ['a', 's', 'd']
        increase_keys = ['q', 'w', 'e']
        vertical_keys = ['up', 'down']
        horizontal_keys = ['left', 'right']

        delta_mag = 1 # how much to change the colour each time

        while True:

            key, = event.waitKeys()

            if key in horizontal_keys:
                if key == 'left':
                    if cur_stim > 0:
                        self.stimuli[cur_stim].unhighlight()
                        cur_stim -= 1
                elif key == 'right':
                    if cur_stim < len(self.stimuli)-1:
                        self.stimuli[cur_stim].unhighlight()
                        cur_stim += 1

                self.stimuli[cur_stim].highlight(spaces[cur_space])
                self.stimuli[cur_stim].change_space(spaces[cur_space])

            elif key in vertical_keys:
                if key == 'up':
                    if cur_space > 0:
                        cur_space -= 1
                elif key == 'down':
                    if cur_space < 2:
                        cur_space += 1

                self.stimuli[cur_stim].highlight(spaces[cur_space])
                self.stimuli[cur_stim].change_space(spaces[cur_space])


            elif key in increase_keys:
                idx = increase_keys.index(key)
                self.stimuli[cur_stim].change_colour(+delta_mag, idx)

            elif key in decrease_keys:
                idx = decrease_keys.index(key)
                self.stimuli[cur_stim].change_colour(-delta_mag, idx)

            elif key == 'r':
                self.stimuli[cur_stim].reset_colour()

            elif key == 't':
                self.stimuli[cur_stim].round_colour()

            elif key == 'f':
                self.flicker()

            elif key in map(str, range(10)):
                if key == '0':
                    key = '10'
                delta_mag = int(key)

            elif key.startswith('num_'):
                key = key.split('_')[1]
                if key == '0':
                    key = '10'
                delta_mag = int(key)

            elif key in ['return', 'escape']:
                break



            for stim in self.stimuli:
                stim.draw_all()
            self.win.flip()







if __name__ == '__main__':

    cs = ColourSpaces(2)

    try:
        cs.main()
        cs.win.close()
    except:
        cs.win.close()
        raise
