from psychopy import visual, event, monitors, tools
import numpy as np
from copy import deepcopy


class ColourSpaces(object):

    def __init__(self):

        self.mon = monitors.Monitor('LabDell')
        self.mon.setCurrent('no_gamma')

        self.win = visual.Window(
            size = [1024, 1024],
            monitor = self.mon,
            screen = 0,
            fullscr = False,
            allowGUI = False,
            color = 0,
            units = 'pix')

        stim1 = visual.GratingStim(
            win = self.win,
            tex = None,
            size = 255,
            pos = [-200, 0],
            colorSpace = 'dkl')
        stim1.color = [90, 0, 1]

        stim2 = visual.GratingStim(
            win = self.win,
            tex = None,
            size = 255,
            pos = [200, 0],
            colorSpace = 'dkl')
        stim2.color = [90, 0, 1]

        self.stimuli = [stim1, stim2]

        self.colours = np.array([
            # Left stimulus             Right stimulus
            [visual.TextStim(self.win), visual.TextStim(self.win)], # dkl
            [visual.TextStim(self.win), visual.TextStim(self.win)], # rgb255
            [visual.TextStim(self.win), visual.TextStim(self.win)]  # lms
            ])

        for i, (left, right) in enumerate(self.colours):
            left.text = right.text = 'hi!'
            left.pos[0] = -200
            right.pos[0] = 200
            left.pos[1] = right.pos[1] = -200 + i * -50

        space1 = visual.TextStim(
            win = self.win,
            pos = [-200, 200])

        space2 = visual.TextStim(
            win = self.win,
            pos = [200, 200])

        self.spaces = [space1, space2]

        # self.dkl2rgb_m = self.mon.getDKL_RGB()
        # self.rgb2dkl_m = np.linalg.inv(self.dkl2rgb_m)
        # self.lms2rgb_m = self.mon.getLMS_RGB()
        # self.rgb2lms_m = np.linalg.inv(self.lms2rgb_m)


    def draw_all(self):

        for stim in self.stimuli:
            stim.draw()
        for col1, col2 in self.colours:
            col1.draw()
            col2.draw()
        for space in self.spaces:
            space.draw()


    def highlight_col(self, col):

        for col1, col2 in self.colours:
            col1.color = col2.color = 0.2
        self.colours[col[0]][col[1]].color = 1


    def cart2sph(self, dklCart):

        z,y,x = dklCart

        radius = np.sqrt(x**2 + y**2 + z**2)
        azimuth = np.arctan2(x, y)
        if azimuth < 0:
            azimuth += 2 * np.pi
        azimuth *= (180 / np.pi)
        elevation = np.arctan(float(z) / np.sqrt(x**2 + y**2)) * (180 / np.pi)

        return np.array([elevation, azimuth, radius])


    def dkl2rgb(dkl):
        rgb = tools.colorspacetools.dkl2rgb(dkl, self.dkl2rgb_m)
        return (rgb + 1) * 127.5

    def lms2rgb(lms):
        rgb = tools.colorspacetools.lms2rgb(lms, self.lms2rgb_m)
        return (rgb + 1) * 127.5

    def rgb2dkl(rgb):
        rgb = rgb / 127.5 - 1
        dkl = np.dot(self.rgb2dkl_m, rgb)
        return self.cart2sph(dkl)

    def rgb2lms(rgb):
        rgb = rgb / 127.5 - 1
        lms = tools.colorspacetools.rgb2lms(rgb, self.rgb2lms_m)
        return lms


    def main(self):

        cc = [0, 0] # current colour [space, stim]

        spaces = ['dkl', 'rgb255', 'lms']

        decrease_keys = ['a', 's', 'd']
        increase_keys = ['q', 'w', 'e']
        vertical_keys = ['up', 'down']
        horizontal_keys = ['left', 'right']

        while True:

            key, = event.waitKeys()

            if key in horizontal_keys:
                if key == 'left':
                    if cc[1] > 0:
                        cc[1] -= 1
                elif key == 'right':
                    if cc[1] < 1:
                        cc[1] += 1

            elif key in vertical_keys:
                if key == 'up':
                    if cc[0] > 0:
                        cc[0] -= 1
                elif key == 'down':
                    if cc[0] < 2:
                        cc[0] += 1

                self.stimuli[cc[1]].colorSpace = spaces[cc[0]]
                self.spaces[cc[1]].text = spaces[cc[0]]

            else:
                break

            self.highlight_col(cc)
            self.draw_all()
            self.win.flip()







if __name__ == '__main__':
    cs = ColourSpaces()

    cs.draw_all()
    cs.win.flip()

    cs.main()
