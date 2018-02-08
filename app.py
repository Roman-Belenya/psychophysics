import psychopy
from psychopy import monitors
import Tkinter as tk
import logging
from experiment_part import *
import json
from tools import *
import tkFileDialog
from tkMessageBox import showwarning, showinfo, askyesno
import subprocess
import unittest

DIRS = ['./data', './logs']
for DIR in DIRS:
    if not os.path.isdir(DIR):
        os.mkdir(DIR)

time = datetime.datetime.strftime(datetime.datetime.now(), '%d-%b-%Y %H-%M-%S,%f')
logging.basicConfig(filename = os.path.join('./logs', time + '.log'),
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(funcName)s: %(message)s',
    filemode = 'a')
logger = logging.getLogger(__name__)


class PopupEntries(object):

    def __init__(self, master, def_grey = True, def_col = True):

        self.master = master
        self.top = tk.Toplevel(master.root, padx = 20, pady = 20)
        self.top.focus_set()
        self.top.grab_set()
        self.top.title('Define colours')
        self.def_grey = def_grey
        self.def_col = def_col
        self.finished = False


        self.grey_vars = {'r': tk.IntVar(),
                          'g': tk.IntVar(),
                          'b': tk.IntVar()}

        self.col_vars = {'r': tk.IntVar(),
                  'g': tk.IntVar(),
                  'b': tk.IntVar()}

        entry_params = {'width': 3, 'relief': tk.FLAT, 'justify': tk.CENTER}
        grid_params = {'padx': 5, 'pady': 5}

        for i, n in enumerate(['R', 'G', 'B']):
            tk.Label(self.top, text = n).grid(row = 0, column = i+1, sticky = 'WE', pady = 5)

        if def_grey:
            tk.Label(self.top, text = 'Contrast (FG grey):').grid(row = 1, column = 0, sticky = 'E', pady = 5)
            for i, col in enumerate(['r', 'g', 'b']):
                tk.Entry(self.top,
                    textvariable = self.grey_vars[col],
                    **entry_params).grid(row = 1, column = i+1, **grid_params)

        if def_col:
            tk.Label(self.top, text = 'Isoluminance (BG col):').grid(row = 2, column = 0, sticky = 'E', pady = 5)
            for i, col in enumerate(['r', 'g', 'b']):
                tk.Entry(self.top,
                    textvariable = self.col_vars[col],
                    **entry_params).grid(row = 2, column = i+1, **grid_params)

        tk.Button(self.top,
            text = 'OK',
            command = self.ok,
            width = 5,
            relief = tk.GROOVE).grid(row = 3, column = 1, columnspan = 3, pady = (15, 0))

        tk.Button(self.top,
            text = 'Load colours',
            command = self.load_colours,
            width = 10,
            relief = tk.GROOVE).grid(row = 3, column = 0, pady = (15,0))


    def ok(self):

        try:
            grey = [self.grey_vars['r'].get(), self.grey_vars['g'].get(), self.grey_vars['b'].get()]
            col = [self.col_vars['r'].get(), self.col_vars['g'].get(), self.col_vars['b'].get()]
            for arr in [grey, col]:
                assert all(0 <= i <= 255 for i in arr)
        except AssertionError:
            showwarning('Entry', 'Incorrect value')
            return

        if self.def_grey:
            self.master.colours['fg_grey'] = grey
            logger.info('defining fg_grey by hand: {}'.format(grey))

        if self.def_col:
            self.master.colours['bg_col'] = col
            logger.info('defining bg_col by hand: {}'.format(col))


        self.finished = True
        self.top.grab_release()
        self.top.destroy()

    def load_colours(self):

        file = tkFileDialog.askopenfilename(filetypes = [('json files', '.json')])
        if not file:
            return
        with open(file, 'rb') as f:
            d = json.load(f)

        try:
            for name, value in zip(['r', 'g', 'b'], d['bg_col']):
                self.col_vars[name].set(value)
            for name, value in zip(['r', 'g', 'b'], d['fg_grey']):
                self.grey_vars[name].set(value)

        except Exception:
            showwarning('File error', 'Bad colours file')
            logger.exception('bad colours.json file: {}'.format(file))
            return


class Application(object):

    def __init__(self, root):

        self.root = root
        self.root.resizable(width = False, height = False)
        self.root.title('Psychophysics')
        self.frame = tk.Frame(root)
        self.frame.grid(row = 0, column = 0, sticky = 'wns', padx=  30, pady = 30)

        # Check parameters file
        if not os.path.isfile('./parameters.json'):
            showwarning('Parameters', 'Missing parameters file')
            logger.warning('missing parameters file')
            return
        self.params = self.load_params('./parameters.json')

        # Check monitor viewing distane
        mon = monitors.Monitor(self.params['monitor_name'])
        if mon.getDistance() != self.params['viewing_distance']:
            mon.setDistance(self.params['viewing_distance'])
            mon.saveMon()
            logger.info('updated monitor viewing distance: {} cm'.format(mon.getDistance))

        self.colours = {
            'bg_grey': self.params['ContrastDetection']['bg_grey'],
            'fg_grey': None,
            'bg_col': None,
            'fg_col': self.params['IsoluminanceDetection']['fix_col']
            }

        # Participant's id entry
        self.id = tk.StringVar()
        self.id.set("Participant's id")
        self.id_entry = tk.Entry(self.frame,
            textvariable = self.id,
            justify = tk.CENTER,
            relief = tk.FLAT,
            width = 15)
        self.id_entry.grid(row = 0, column = 0, padx = 10, pady = (0, 20))


        # Checkbuttons
        self.contrast_var = tk.IntVar()
        tk.Checkbutton(
            self.frame,
            text = 'Contrast detection',
            variable = self.contrast_var).grid(row = 1, column = 0, sticky = 'W')

        self.isolum_var = tk.IntVar()
        tk.Checkbutton(
            self.frame,
            text = 'Isoluminance deteciton',
            variable = self.isolum_var).grid(row = 2, column = 0, sticky = 'W', pady = (0, 5))

        self.free_var = tk.IntVar()
        tk.Checkbutton(
            self.frame,
            text = 'Free choice',
            variable = self.free_var).grid(row = 3, column = 0, sticky = 'W')

        self.divided_var = tk.IntVar()
        tk.Checkbutton(
            self.frame,
            text = 'Divided attention',
            variable = self.divided_var).grid(row = 4, column = 0, sticky = 'W')

        self.selective_var = tk.IntVar()
        tk.Checkbutton(
            self.frame,
            text = 'Selective attention',
            variable = self.selective_var).grid(row = 5, column = 0, sticky = 'W')

        # Buttons
        self.tests_button = tk.Button(self.frame,
            text = 'Run tests',
            command = self.run_tests,
            height = 2,
            width = 10,
            relief = tk.GROOVE)
        self.tests_button.grid(row = 6, column = 0, columnspan = 2, sticky = 'EW', pady = (20, 0))

        self.start_button = tk.Button(self.frame,
            text = 'Start experiment',
            command = self.start_experiment,
            height = 2,
            width = 10,
            relief = tk.GROOVE)
        self.start_button.grid(row = 7, column = 0, columnspan = 2, sticky = 'EW', pady = (10, 0))

        logger.info('started app')




    def start_experiment(self):

        np.random.seed(1)

        # Get participant's id
        id = self.id.get()
        if id == "Participant's id":
            showwarning('Missing id', "Enter participant's id")
            return

        self.dir = os.path.join('.', 'data', id)
        if os.path.isdir(self.dir):
            ans = askyesno("Participant's id", '{} already exists. Continue experiment with this participant?'.format(id))
            if ans:
                logger.info('continuing with participant {}'.format(id))
                cols = os.path.join(self.dir, 'colours.json')
                try:
                    self.colours = json.load(open(cols, 'rb'))
                    logger.info('loaded colours from {}'.format(cols))
                except:
                    logger.exception('failed to load colours from {}'.format(cols))
            else:
                logger.info('do not continue with participant {}. returning'.format(id))
                return
        else:
            os.makedir(self.dir)
            logger.info('created new participant {}'.format(id))

        # Get experiment selections
        sel = {
            'contrast': self.contrast_var.get(),
            'isolum': self.isolum_var.get(),
            'free': self.free_var.get(),
            'divided': self.divided_var.get(),
            'selective': self.selective_var.get()
            }
        logger.info('selected experiments: {}'.format(sel))

        need_def, need_grey, need_col = self.need_definition(sel)
        if need_def:
            popup = PopupEntries(self, need_grey, need_col)
            self.root.wait_window(popup.top)
            if not popup.finished:
                return
            self.save_colours(self.colours)

        mon_name = self.params['monitor_name']
        calib_name = self.params['calibration_name']
        try:
            mon = self.get_monitor(mon_name, calib_name)
            logger.info('loaded monitor {} with calibration {}'.format(mon_name, calib_name))
        except Exception as e:
            logger.exception('monitor not found:')
            showwarning('Monitor', 'Monitor object not found')
            return

        self.win = visual.Window(
            size = [1920, 1080],
            monitor = mon,
            screen = 0,
            numSamples = 8,
            fullscr = True,
            allowGUI = False,
            colorSpace = 'rgb255',
            color = 128,
            units = 'deg')
        self.win.mouseVisible = False

        self.thank_you = visual.TextStim(
            win = self.win,
            colorSpace = 'rgb255',
            color = 200,
            text = '',
            pos = (0, 0))

        # The app is no longer needed
        self.root.quit()
        self.root.destroy()

        exps = [ ('contrast', 'ContrastDetection', ContrastDetection),
                ('isolum', 'IsoluminanceDetection', IsoluminanceDetection),
                ('free', 'FreeChoiceExperiment', FreeChoiceExperiment),
                ('divided', 'DividedAttentionExperiment', DividedAttentionExperiment) ,
                ('selective', 'SelectiveAttentionExperiment', SelectiveAttentionExperiment) ]

        for name, fullname, exp in exps:

            if name in ['contrast', 'isolum']:
                if sel[name]: # if this experiment is selected
                    try:
                        experiment = exp(self.win, id, self.params[fullname])
                        experiment.main_sequence()
                    except Exception as e:
                        self.win.close()
                        showwarning('Experiment error', str(e))
                        logger.exception('error in experiment:')
                        return
                    finally:
                        filename = os.path.join(self.dir, experiment.export_filename)
                        experiment.export_results(filename, ['Mean colour:', experiment.output_col])
                        self.add_colour(name, experiment.output_col)

            elif name in ['free', 'divided', 'selective']:
                if sel[name]:
                    try:
                        experiment = exp(self.win, id, self.colours, self.params[fullname])
                        experiment.main_sequence()
                    except Exception as e:
                        self.win.close()
                        showwarning('Experiment error', str(e))
                        logger.exception('error in experiment:')
                        return
                    finally:
                        filename = os.path.join(self.dir, experiment.export_filename)
                        experiment.export_results(filename)

        self.win.flip()
        self.thank_you.text = self.params['thank_you_text']
        self.thank_you.draw()
        self.win.flip()
        event.waitKeys()
        self.win.close()

        logger.info('finished experiment')


    def load_params(self, file):

        with open(file, 'rb') as f:
            params = json.load(f)
        return params


    def need_definition(self, sel):

        grey = sel['contrast'] or self.colours['fg_grey']
        col = sel['isolum'] or self.colours['bg_col']

        no_detects = not(grey and col)
        exps = sel['free'] or sel['divided'] or sel['selective']

        need_def = exps and no_detects
        return need_def, not grey, not col


    def get_monitor(self, name, calib):

        if mon not in monitors.getAllMonitors():
            raise Exception('monitor not found')

        mon = monitors.Monitor(name)
        mon.setCurrent(calib)
        return mon


    def add_colour(self, exp_name, value):

        if exp_name in ['contrast', 'ContrastDetection']:
            self.colours['fg_grey'] = value
        elif exp_name in ['isolum', 'IsoluminanceDetection']:
            self.colours['bg_col'] = value
        self.save_colours(self.colours)


    def save_colours(self, col_dict):
        for name, value in col_dict.items():
            if type(value) is np.ndarray:
                col_dict[name] = list(value)
        path = os.path.join(self.dir, 'colours.json')
        with open(path, 'wb') as f:
            json.dump(col_dict, f)


    def run_tests(self):

        logger.info('running tests')
        from test_experiment_part import TestExperimentPart
        from test_tools import TestTools

        to_run = [TestTools, TestExperimentPart]
        loader= unittest.TestLoader()
        suites = [loader.loadTestsFromTestCase(test) for test in to_run]

        suite = unittest.TestSuite(suites)
        runner = unittest.TextTestRunner()
        result = runner.run(suite)

        showinfo('Test results', '{} error(s) detected'.format(len(result.failures)))
        if not result.wasSuccessful():
            for i in result.failures:
                logger.error('test error:\n{}'.format(i[1]))
        else:
            logger.info('all tests are successful')





if __name__ == '__main__':
    app = Application(tk.Tk())
    app.root.mainloop()
