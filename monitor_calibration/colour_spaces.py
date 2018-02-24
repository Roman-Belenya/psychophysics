from psychopy import visual, event, monitors, tools
import numpy as np
from colour_tools import *
from collections import OrderedDict


class MyStim(visual.grating.GratingStim):

    def __init__(self, **kwargs):

        super(MyStim, self).__init__(**kwargs)

        all_spaces = ['dkl', 'rgb255', 'lms']

        self.col_texts = OrderedDict( zip(all_spaces, [visual.TextStim(self.win) for i in range(3)]) )
        for i, col_text in enumerate(self.col_texts.values()):
            col_text.pos = [self.pos[0], self.pos[1] - (self.size[1] + 50 + i*50)]

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


    def change_colour(self, delta):

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
            self.col_texts[key].text = str(np.around(value, 2))


    def unhighlight(self):

        for col_text in self.col_texts.values():
            col_text.color = 0.2


    def hightlight(self, space):

        self.unhighlight()
        self.col_texts[space].color = 1


    def draw_all(self):

        self.draw()
        self.space_text.draw()
        for col_text in self.col_texts:
            col_text.draw()






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
            MyStim(
            win = self.win,
            tex = None,
            colorSpace = 'dkl') for i in range(nStimuli)
            ]

        for i, stim in enumerate(self.stimuli):
            stim.color = [90, 0, 1]
            stim.size = self.win.size[0] / (2*len(self.stimuli))
            stim.pos = [-self.win.size[0] / 2.0 + self.win.size[0] * (i+1) / (len(self.stimuli)+1), 0]


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
                    if cur_space < 3:
                        cur_space += 1

                self.stimuli[cur_stim].highlight(spaces[cur_space])
                self.stimuli[cur_stim].change_space(spaces[cur_space])


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

            for stim in self.stimuli:
                stim.draw_all()
            self.win.flip()







if __name__ == '__main__':

    cs = ColourSpaces(3)

    try:
        cs.main()
        cs.win.close()
    except:
        cs.win.close()
        raise
