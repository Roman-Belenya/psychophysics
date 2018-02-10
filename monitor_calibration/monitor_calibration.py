from psychopy import monitors, visual, event
import numpy as np
import csv

class MonitorCalibration(object):

    def __init__(self, mon_name, calib_name):


        self.mon = monitors.Monitor(mon_name)

        if calib_name in self.mon.calibNames:
            self.mon.setCurrent(calib_name)
            print 'loaded {}'.format(calib_name)
        else:
            self.mon.newCalib(calibName = calib_name)
            self.mon.setCurrent(calib_name)
            self.mon.setDistance(40)
            self.mon.setWidth(52)
            self.mon.setSizePix([1920, 1200])
            self.mon.setLineariseMethod(4)
            print 'created ne calib'

        self.levels = map(int, np.linspace(0, 255, 16))
        self.lums = []
        self.gamma_grid = []

        self.wavelengths = []
        self.power = []
        self.dkl2rgb = []
        self.lms2rgb = []

        self.win = visual.Window(
            size = [1920, 1200],
            monitor = self.mon,
            screen = 0,
            fullscr = True,
            colorSpace = 'rgb255',
            color = 128,
            units = 'pix')
        self.minimise()

        self.target = visual.GratingStim(
            win = self.win,
            tex = None,
            colorSpace = 'rgb255',
            color = [0,0,0],
            size = 256)

        self.curr_colour = visual.TextStim(
            win = self.win,
            pos = (0, -500),
            colorSpace = 'rgb255',
            color = 255)

        self.curr_calib = visual.TextStim(
            win = self.win,
            colorSpace = 'rgb255',
            color = 0)

    def minimise(self):
        self.win.winHandle.minimize()
        # self.win.winHandle.set_fullscreen(False)
        self.win.flip()

    def maximise(self):
        self.win.winHandle.maximize()
        # self.win.winHandle.set_fullscreen(True)
        self.win.flip()

    def measure_lums(self, chans = ['l', 'r', 'g', 'b']):

        self.maximise()

        for chan in chans:
            self.curr_calib.text = chan
            self.curr_calib.draw()
            self.win.flip()
            event.waitKeys()

            i = 0
            while True:

                tc = self.levels[i]

                if chan == 'r':
                    self.target.color = [tc, 0, 0]
                elif chan == 'g':
                    self.target.color = [0, tc, 0]
                elif chan == 'b':
                    self.target.color = [0, 0, tc]
                elif chan == 'l':
                    self.target.color = [tc] * 3
                else:
                    return

                self.curr_colour.text = '{}/{}: {}'.format(i+1, len(self.levels), str(self.target.color))

                self.target.draw()
                self.curr_colour.draw()
                self.win.flip()

                key = event.waitKeys(keyList = ['left', 'right', 'return'])
                if key[0] == 'left' and i > 0:
                    i -= 1
                elif key[0] == 'right' and i < len(self.levels) - 1:
                    i += 1
                elif key[0] == 'return':
                    self.win.flip()
                    break

        self.minimise()


    def get_lum(self, filename):

        lum = []
        with open(filename, 'rb') as f:
            for i, line in enumerate(f):
                if i > 1:
                    line = line.split('\t')
                    lum.append(float(line[1]))

        if len(lum) != len(self.levels):
            raise Exception('too many measurements in {}'.format(filename))

        return lum


    def get_gamma(self, lums):

        if len(lums) != 4:
            raise Exception('need 4 lum measurements')

        gamma_grid = []
        for chan in lums:
            model = monitors.GammaCalculator(inputs = self.levels,
                lums = chan, eq = 4)
            gamma_grid.append([model.min, model.max, model.gamma, model.a, model.b, model.k])

        return gamma_grid


    def measure_cols(self):

        self.maximise()

        cols = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

        for col in cols:
                self.target.color = col
                self.target.draw()
                self.win.flip()
                event.waitKeys()

        self.minimise()


    def get_spectrum(self, filename):

        waves = []
        power = []

        with open(filename, 'rb') as f:
            for i, line in enumerate(f):
                try:
                    line = map(float, line.split('\t'))
                except:
                    print line
                    continue

                waves.append(line[0])
                power.append(line[1:])

        power = np.transpose(power).tolist()
        if len(power) != 3:
            raise Exception('need 3 spectra')

        return waves, power


    def get_dkl2rgb(self):

        assert all([len(self.wavelengths) == len(i) for i in self.power])

        return monitors.makeDKL2RGB(self.wavelengths, self.power)

    def get_lms2rgb(self):

        assert all([len(self.wavelengths) == len(i) for i in self.power])

        return monitors.makeLMS2RGB(self.wavelengths, self.power)

    def save_matrix(self, name, matrix):
        with open(name, 'wb') as f:
            writer = csv.writer(f)
            for line in matrix:
                writer.writerow(line)

    def test_lums(self):

        self.maximise()

        cols = [[0, 0, 0], [128, 128, 128], [255, 255, 255]]

        for col in cols:
                self.target.color = col
                self.target.draw()
                self.win.flip()
                event.waitKeys()

        self.minimise()



# if __name__ == 'monitor_calibration':
#     c = MonitorCalibration('test', 'ha')

