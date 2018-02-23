from psychopy import visual, event, monitors, tools
import numpy as np
from colour_tools import *
from collections import OrderedDict

def main():
    win = visual.Window(size = [500, 500])
    ms = MyStim(win = win, tex = None, size = 100, pos = [0, 0])
    return win, ms


class MyStim(visual.grating.GratingStim):

    def __init__(self, **kwargs):

        super(MyStim, self).__init__(**kwargs)

        all_spaces = ['dkl', 'rgb255', 'lms']

        self.col_texts = OrderedDict( zip(all_spaces, [visual.TextStim(self.win) for i in range(3)]) )
        for i, col_text in enumerate(self.col_texts.values()):
            col_text.pos = [self.pos[0], self.pos[1] - (self.size[1] + 50 + i*50)]

        self.colours = OrderedDict( zip(all_spaces, [None]*3) )
        self.update_colours()

        self.space_text = visual.TextStim(win = self.win,
            text = self.colorSpace,
            pos = [self.pos[0], self.pos[1] + self.size[1] + 50])

        self.dkl2rgb_m = self.win.monitor.getDKL_RGB()
        self.rgb2dkl_m = np.linalg.inv(self.dkl2rgb_m)
        self.lms2rgb_m = self.win.monitor.getLMS_RGB()
        self.rgb2lms_m = np.linalg.inv(self.lms2rgb_m)


    def change_colour(self, space, delta):

        if self.colorSpace != space:
            self.colorSpace = space
            self.space_text.text = space
            self.color = self.colours[space]

        self.color += delta


    def update_colours(self):

        if self.colorSpace == 'dkl':
            self.colours['dkl'] = self.color
            self.colours['rgb255'] = dkl2rgb(self.color, self.dkl2rgb_m)
            self.colours['lms'] = rgb2lms(self.colours['rgb255'], self.rgb2lms_m)

        elif self.colorSpace == 'rgb255':
            self.colours['rgb255'] = self.color
            self.colours['dkl'] = rgb2dkl(self.color, self.rgb2dkl_m)
            self.colours['lms'] = rgb2lms(self.color, self.rgb2lms_m)

        elif self.colorSpace == 'lms':
            self.colours['lms'] = self.color
            self.colours['rgb255'] = lms2rgb(self.color, self.lms2rgb_m)
            self.colours['dkl'] = rgb2dkl(self.colours['rgb255'], self.rgb2dkl_m)

        for key, value in self.colours.items():
            self.col_texts[key].text = str(np.around(value, 2))


    def highlight(self, space):
        for col_text in self.col_texts.values():
            col_text.color = 0.2
        self.col_texts[space].color = 1





class ColourSpaces(object):

    def __init__(self, nStimuli = 2):

        self.mon = monitors.Monitor('LabDell')
        self.mon.setCurrent('experiment')

        self.win = visual.Window(
            size = [1024, 1024],
            monitor = self.mon,
            screen = 0,
            fullscr = False,
            allowGUI = False,
            color = 0,
            units = 'pix')

        self.nStimuli = nStimuli

        self.stimuli = [
            visual.GratingStim(
            win = self.win,
            tex = None,
            colorSpace = 'dkl') for i in range(nStimuli)
            ]

        for i, stim in enumerate(self.stimuli):
            stim.color = [90, 0, 1]
            stim.size = self.win.size[0] / (2*len(self.stimuli))
            stim.pos = [-self.win.size[0] / 2.0 + self.win.size[0] * (i+1) / (len(self.stimuli)+1), 0]


        self.colours = []
        for i in range(3): # 3 colour spaces: dkl, rgb255, lms
            self.colours.append([visual.TextStim(self.win) for k in range(len(self.stimuli))])

        for i, cols in enumerate(self.colours):
            for k, col in enumerate(cols):
                col.text = 'hi'
                col.pos = [self.stimuli[k].pos[0], -50 - self.stimuli[k].size[1] - i * 50]


        self.spaces = [visual.TextStim(self.win) for i in range(len(self.stimuli))]

        for i, space in enumerate(self.spaces):
            space.pos = [self.stimuli[i].pos[0], 50 + self.stimuli[k].size[1]]


        self.dkl2rgb_m = self.mon.getDKL_RGB()
        self.rgb2dkl_m = np.linalg.inv(self.dkl2rgb_m)
        self.lms2rgb_m = self.mon.getLMS_RGB()
        self.rgb2lms_m = np.linalg.inv(self.lms2rgb_m)


    def draw_all(self):

        for stim in self.stimuli:
            stim.draw()
        for row in self.colours:
            for col in row:
                col.draw()
        for space in self.spaces:
            space.draw()


    def highlight_col(self, col):

        for row in self.colours:
            for colour in row:
                colour.color = 0.2
        self.colours[col[0]][col[1]].color = 1


    def calculate_cols(self, stim):

        if stim.colorSpace == 'rgb255':
            rgb = stim.color
            dkl = self.rgb2dkl(rgb)
            lms = self.rgb2lms(rgb)
        elif stim.colorSpace == 'dkl':
            dkl = stim.color
            rgb = self.dkl2rgb(dkl)
            lms = self.rgb2lms(rgb)
        elif stim.colorSpace == 'lms':
            lms = stim.color
            rgb = self.lms2rgb(lms)
            dkl = self.rgb2dkl(rgb)

        return dkl, rgb, lms


    def set_cols(self, stim, idx):
        cols = self.calculate_cols(stim)
        for i, row in enumerate(self.colours):
            row[idx].text = str(np.around(cols[i]))


    def main(self):

        cc = [0, 0] # current colour [space, stim]

        spaces = ['dkl', 'rgb255', 'lms']

        decrease_keys = ['a', 's', 'd']
        increase_keys = ['q', 'w', 'e']
        vertical_keys = ['up', 'down']
        horizontal_keys = ['left', 'right']

        self.set_cols(self.stimuli[cc[1]], cc[1])

        while True:

            key, = event.waitKeys()

            if key in horizontal_keys:
                if key == 'left':
                    if cc[1] > 0:
                        cc[1] -= 1
                elif key == 'right':
                    if cc[1] < len(self.stimuli)-1:
                        cc[1] += 1
                self.highlight_col(cc)

            elif key in vertical_keys:
                if key == 'up':
                    if cc[0] > 0:
                        cc[0] -= 1
                elif key == 'down':
                    if cc[0] < len(self.colours)-1:
                        cc[0] += 1
                self.highlight_col(cc)


            elif key in increase_keys:
                if self.stimuli[cc[1]].colorSpace != spaces[cc[0]]:
                    cols = self.calculate_cols(self.stimuli[cc[1]])
                    self.stimuli[cc[1]].colorSpace = spaces[cc[0]]
                    self.stimuli[cc[1]].color = cols[cc[0]]
                    self.spaces[cc[1]].text = spaces[cc[0]]

                idx = increase_keys.index(key)
                self.stimuli[cc[1]].color[idx] += 1
                self.set_cols(self.stimuli[cc[1]], cc[1])

            elif key in decrease_keys:
                if self.stimuli[cc[1]].colorSpace != spaces[cc[0]]:
                    cols = self.calculate_cols(self.stimuli[cc[1]])
                    self.stimuli[cc[1]].colorSpace = spaces[cc[0]]
                    self.stimuli[cc[1]].color = cols[cc[0]]
                    self.spaces[cc[1]].text = spaces[cc[0]]

                idx = decrease_keys.index(key)
                self.stimuli[cc[1]].color[idx] -= 1
                self.set_cols(self.stimuli[cc[1]], cc[1])


            else:
                break

            self.draw_all()
            self.win.flip()







if __name__ == '__main__':

    cs = ColourSpaces(3)

    try:

        cs.draw_all()
        cs.win.flip()
        cs.main()
        cs.win.close()
    except:
        cs.win.close()
        raise
