from psychopy import visual, event, monitors, tools
import numpy as np


class ColoursGrid(object):

    def __init__(self, master):

        self.master = master


        self.colours = np.array([
            [visual.TextStim(master.win, pos=[-200, -200]), visual.TextStim(master.win, pos=[200, -200])],
            [visual.TextStim(master.win, pos=[-200, -250]), visual.TextStim(master.win, pos=[200, -250])],
            [visual.TextStim(master.win, pos=[-200, -300]), visual.TextStim(master.win, pos=[200, -300])],
            ])



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

        self.stim1 = visual.GratingStim(
            win = self.win,
            tex = None,
            size = 255,
            pos = [-200, 0],
            colorSpace = 'dkl')
        self.stim1.color = [90, 0, 1]

        self.stim2 = visual.GratingStim(
            win = self.win,
            tex = None,
            size = 255,
            pos = [200, 0],
            colorSpace = 'dkl')
        self.stim2.color = [90, 0, 1]

        self.colours1 = np.array([
            visual.TextStim(win = self.win, pos = [-200, -200]),
            visual.TextStim(win = self.win, pos = [-200, -250]),
            visual.TextStim(win = self.win, pos = [-200, -300]) ])

        self.colours2 = np.array([
            visual.TextStim(win = self.win, pos = [200, -200]),
            visual.TextStim(win = self.win, pos = [200, -250]),
            visual.TextStim(win = self.win, pos = [200, -300]) ])


    def draw_all(self):

        for c1, c2 in zip(self.colours1, self.colours2):
            c1.draw()
            c2.draw()
        self.stim1.draw()
        self.stim2.draw()


    def main(self):

        current_stim = self.stim1
        current_space = 0 # 0 = dkl, 1 = rgb255, 2 = lms

        while True:

            key, = event.waitKeys()

            if key == 'left':
                current_stim = self.stim1
                self.colours1[current_space].color = 1






if __name__ == '__main__':
    cs = ColourSpaces()

    cs.draw_all()
    cs.win.flip()

    event.waitKeys()
