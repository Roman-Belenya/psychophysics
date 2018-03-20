from psychopy import visual, event, monitors, tools
import numpy as np
from colour_tools import *
from collections import OrderedDict
import json
import sys
sys.path.insert(0, '../')
from tools import load_monitor
from scipy.io import loadmat
import csv


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
            size = [1000, 1000],
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



class ColourRepresentations(object):


    def __init__(self,
        phosphors = './test_calib/spectrum_after.dat',
        fundamentals = './2deg_StockmanSharpe.csv'):

        self.fundamentals_mat = loadmat(r"C:\Program Files\MATLAB\colour_toolbox\fundamentals_ss.mat")['fundamentals']
        self.phosphors_mat = loadmat(r"C:\Program Files\MATLAB\colour_toolbox\phosphors.mat")['phosphors']

        self.fundamentals = self.load_fundamentals(fundamentals)
        self.phosphors = self.load_phosphors(phosphors)

        self.all_spaces = ['rgb', 'lms', 'dkl']
        self.colours = OrderedDict( zip(self.all_spaces, [None]*3) )
        self.colours['rgb'] = np.zeros(3)
        self.current_space = 'rgb'
        self.update_colours()


    def change_colour(self, idx, mag):

        delta = np.zeros(3)

        if self.current_space == 'dkl':
            if idx == 2:
                delta[idx] += mag * 0.01
            else:
                delta[idx] += mag
        elif self.current_space == 'lms':
            delta[idx] += mag * 0.01
        else:
            delta[idx] += mag

        self.colours[self.current_space] += delta
        self.update_colours()


    def change_space(self, space):

        if space in range(3):
            self.current_space = self.all_spaces[space]
        elif type(space) is str:
            self.current_space = space


    def update_colours(self):

        if self.current_space == 'rgb':
            rgb = self.colours['rgb']
            lms = self.rgb2lms(rgb)
            dkl_cart = self.lms2dkl(lms)
            dkl = self.dkl_cart2sph(dkl_cart)

        elif self.current_space == 'lms':
            lms = self.colours['lms']
            rgb = self.lms2rgb(lms)
            dkl_cart = self.lms2dkl(lms)
            dkl = self.dkl_cart2sph(dkl_cart)

        elif self.current_space == 'dkl':
            dkl = self.colours['dkl']
            dkl_cart = self.dkl_sph2cart(dkl)
            lms = self.dkl2lms(dkl_cart)
            rgb = self.lms2rgb(lms)
            print rgb

        self.colours['rgb'] = rgb
        self.colours['lms'] = lms
        self.colours['dkl'] = dkl


    def reset_colour(self):

        self.colours[self.current_space] = np.zeros(3)
        self.update_colours()


    def round_colour(self):

        cur_c = self.colours[self.current_space]

        if self.current_space == 'dkl':
            round_c = np.append(np.around(cur_c[0:2], 0), np.around(cur_c[2], 2))
        elif self.current_space == 'rgb':
            round_c = np.around(cur_c, 0)
        elif self.current_space == 'lms':
            round_c = np.around(cur_c, 2)

        self.colours[self.current_space] = round_c
        self.update_colours()


    def load_fundamentals(self, file):

        with open(file, 'rb') as f:
            reader = csv.reader(f)
            rows = np.array([map(float, row) for row in reader])

        mask = np.logical_and(390 <= rows[:,0], rows[:,0] <= 780)
        return rows[mask, 1:]


    def load_phosphors(self, file):

        rows = []
        record = False
        with open(file, 'rb') as f:
            for row in f:
                if row.startswith('380'):
                    record = True
                if record:
                    row_floats = map(float, row.rstrip().split('\t'))
                    rows.append(row_floats)

        rows = np.array(rows)
        mask = np.logical_and(390 <= rows[:,0], rows[:,0] <= 780)

        return rows[mask, 1:]


    def rgb2lms(self, rgb255):

        rgb1 = np.array(rgb255) / 255.0
        rgbTOlms = np.dot(self.fundamentals.T, self.phosphors)
        lms = np.dot(rgbTOlms, rgb1)
        return lms


    def lms2rgb(self, lms):

        rgbTOlms = np.dot(self.fundamentals.T, self.phosphors)
        lmsTOrgb = np.linalg.inv(rgbTOlms)
        rgb1 = np.dot(lmsTOrgb, lms)
        rgb255 = rgb1 * 255.0
        return rgb255


    def lms2dkl(self, lms_t):

        lms_b = self.rgb2lms([128,128,128])
        lms_t = np.array(lms_t)
        lms_diff = lms_b - lms_t
        B = np.array([
            [1, 1, 0],
            [1, -lms_b[0]/lms_b[1], 0],
            [-1, -1, (lms_b[0] + lms_b[1]) / lms_b[2]]
            ])
        B_inv = np.linalg.inv(B)

        lum = B_inv[:,0]
        chro_LM = B_inv[:,1]
        chro_S = B_inv[:,2]

        lum_pooled = np.linalg.norm(lum / lms_b)
        chro_LM_pooled = np.linalg.norm(chro_LM / lms_b)
        chro_S_pooled = np.linalg.norm(chro_S / lms_b)

        lum_unit = lum / lum_pooled
        chro_LM_unit = chro_LM / chro_LM_pooled
        chro_S_unit = chro_S / chro_S_pooled

        lum_norm = np.dot(B, lum_unit)
        chro_LM_norm = np.dot(B, chro_LM_unit)
        chro_S_norm = np.dot(B, chro_S_unit)

        D_const = np.array([
            [1 / lum_norm[0], 0, 0],
            [0, 1 / chro_LM_norm[1], 0],
            [0, 0, 1 / chro_S_norm[2]]
            ])

        T = np.dot(D_const, B)
        dkl_rad = np.dot(T, lms_diff)

        return dkl_rad


    def dkl2lms(self, dkl_rad):

        lms_b = self.rgb2lms([128, 128, 128])
        dkl_rad = np.array(dkl_rad)

        B = np.array([
            [1, 1, 0],
            [1, -lms_b[0]/lms_b[1], 0],
            [-1, -1, (lms_b[0] + lms_b[1]) / lms_b[2]]
            ])
        B_inv = np.linalg.inv(B)

        lum = B_inv[:,0]
        chro_LM = B_inv[:,1]
        chro_S = B_inv[:,2]

        lum_pooled = np.linalg.norm(lum / lms_b)
        chro_LM_pooled = np.linalg.norm(chro_LM / lms_b)
        chro_S_pooled = np.linalg.norm(chro_S / lms_b)

        lum_unit = lum / lum_pooled
        chro_LM_unit = chro_LM / chro_LM_pooled
        chro_S_unit = chro_S / chro_S_pooled

        lum_norm = np.dot(B, lum_unit)
        chro_LM_norm = np.dot(B, chro_LM_unit)
        chro_S_norm = np.dot(B, chro_S_unit)

        D_const = np.array([
            [1 / lum_norm[0], 0, 0],
            [0, 1 / chro_LM_norm[1], 0],
            [0, 0, 1 / chro_S_norm[2]]
            ])

        T = np.dot(D_const, B)
        T_inv = np.linalg.inv(T)

        lms_diff = np.dot(T_inv, dkl_rad)
        lms_t = lms_b - lms_diff

        return lms_t


    def dkl_cart2sph(self, dkl_rad):

        isolum_len = np.sqrt(dkl_rad[1]**2 + dkl_rad[2]**2)

        if isolum_len == 0:
            elevation_rad = np.arctan(dkl_rad[0] / 1e-9)
        else:
            elevation_rad = np.arctan(dkl_rad[0] / isolum_len)

        if dkl_rad[1] > -1e-6 and dkl_rad[1] < 1e-6 and dkl_rad[2] > -1e-6 and dkl_rad[2] < 1e-6:
            azimuth_rad = 0
            radius = np.sqrt(dkl_rad[0]**2)
        else:
            azimuth_rad = np.arctan(-dkl_rad[2] / dkl_rad[1])
            radius = isolum_len

        if dkl_rad[1] > 0 and dkl_rad[2] > 0:
            azimuth_deg = azimuth_rad * 180 / np.pi + 180
        elif dkl_rad[1] > 0 and dkl_rad[2] < 0:
            azimuth_deg = azimuth_rad * 180 / np.pi + 180
        elif dkl_rad[1] < 0 and dkl_rad[2] < 0:
            azimuth_deg = azimuth_rad * 180 / np.pi + 360
        else:
            azimuth_deg = azimuth_rad * 180 / np.pi

        elevation_deg = -elevation_rad * 180 / np.pi
        dkl_deg = np.array([elevation_deg, azimuth_deg, radius])

        return dkl_deg


    def dkl_sph2cart(self, dkl_sph):

        elevation_deg = dkl_sph[0]
        azimuth_deg = dkl_sph[1]
        radius = dkl_sph[2]

        azimuth_rad = np.radians(azimuth_deg)
        elevation_rad = np.radians(elevation_deg)

        if elevation_deg in [-90, 90]:
            lum = radius
            chro_LM = 0
            chro_S = 0
        else:
            lum =     radius * np.sin(elevation_rad)
            chro_LM = radius * np.cos(azimuth_rad) * np.cos(elevation_rad)
            chro_S =  radius * np.sin(azimuth_rad) * np.cos(elevation_rad)

        dkl_rad = np.array([lum, chro_LM, chro_S])

        return dkl_rad


    def dkl_sph2rgb(self, dkl_sph):

        dkl_cart = self.dkl_sph2cart(dkl_sph)
        lms = self.dkl2lms(dkl_cart)
        rgb = self.lms2rgb(lms)

        return lms

    def rgb2dkl_sph(self, rgb):

        lms = self.rgb2lms(rgb)
        dkl_cart = self.lms2dkl(lms)
        dkl_sph = self.dkl_cart2sph(dkl_cart)

        return dkl_sph







if __name__ == '__main__':

    cs = ColourSpaces(2)

    try:
        cs.main()
        cs.win.close()
    except:
        cs.win.close()
        raise
