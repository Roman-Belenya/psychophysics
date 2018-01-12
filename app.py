import psychopy
from psychopy import monitors
import logging
from experiment_part import *
import json
from tools import *
import Tkinter as tk
import tkFileDialog
import ast
from tkMessageBox import showwarning, showinfo, askyesno
import subprocess
import unittest

logdir = './logs'
if not os.path.isdir(logdir):
    os.mkdir(logdir)
time = datetime.datetime.strftime(datetime.datetime.now(), '%d-%b-%Y %H-%M-%S,%f')
logging.basicConfig(filename = os.path.join(logdir, time + '.log'),
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s: %(message)s',
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

        # Get participant's id and make directories
        id = self.id.get()
        if id == "Participant's id":
            showwarning('Missing id', "Enter participant's id")
            return
        logger.info('creating new participant {}'.format(id))

        self.dir = os.path.join('.', id)
        if os.path.isdir(self.dir):
            ans = askyesno('Participant id', 'This participant exists. Overwrite?')
            if ans == 0:
                return
            else:
                shutil.rmtree(self.dir)
                logger.info('overwriting {}'.format(self.dir))
        os.makedirs(os.path.join(self.dir, 'stimuli'))

        # Get experiment selections
        selections = {
            'free': self.free_var.get(),
            'contrast': self.contrast_var.get(),
            'isolum': self.isolum_var.get(),
            }
        logger.info('selected experiments: {}, {}, {}'.format(*selections.items()))

        # Need to define colours if free choice is selected, but one of isolum or contrast is not
        need_def = selections['free'] and not (selections['contrast'] and selections['isolum'])
        if need_def:
            popup = PopupEntries(self, not selections['contrast'], not selections['isolum'])
            self.root.wait_window(popup.top)
            if not popup.finished:
                return
            self.save_colours(self.colours)

        self.win = visual.Window(
            size = [1920, 1080],
            monitor = self.params['monitor_name'],
            screen = 0,
            fullscr = True,
            colorSpace = 'rgb255',
            color = 128,
            units = 'deg')
        self.win.mouseVisible = True


        # Contrast detection
        if selections['contrast']:
            self.contrast = ContrastDetection(self.win, id, self.params['ContrastDetection'])
            try:
                self.contrast.main_sequence()
            except Exception as e:
                self.win.close()
                showwarning('Experiment error', str(e))
                logging.exception('error in contrast main sequence:')
            finally:
                filename = os.path.join(self.dir, 'contrast.exp')
                self.contrast.export_results(filename, ['Mean colour:', self.contrast.output_col])

                self.colours['fg_grey'] = self.contrast.output_col
                self.save_colours(self.colours)

        # Isoluminance detection
        if selections['isolum']:
            self.isolum = IsoluminanceDetection(self.win, id, self.params['IsoluminanceDetection'])
            try:
                self.isolum.main_sequence()
            except Exception as e:
                self.win.close()
                showwarning('Experiment error', str(e))
                logging.exception('error in contrast main sequence:')
            finally:
                filename = os.path.join(self.dir, 'isoluminance.exp')
                self.isolum.export_results(filename, ['Mean colour:', self.isolum.output_col])

                self.colours['bg_col'] = self.isolum.output_col
                self.save_colours(self.colours)


        # Free choice experiment
        if selections['free']:
            self.free_choice = FreeChoiceExperiment(self.win, id, self.params['FreeChoiceExperiment'])

            correct = self.check_colours_dict(self.colours)
            if not correct:
                self.win.close()
                showwarning('Colours', 'Error with colours')
                logger.warning('bad colours dict: {}. terminating experiment'.format(self.colours))
                return

            try:
                self.free_choice.define_colours(self.colours)
                self.free_choice.main_sequence()
            except Exception as e:
                self.win.close()
                showwarning('Experiment error', str(e))
                logging.exception('error in contrast main sequence:')
            finally:
                filename = os.path.join(self.dir, 'free_choice.exp')
                self.free_choice.export_results(filename)


        self.win.close()
        showinfo('Experiment', 'Finished!')
        logging.info('finished experiment')
        self.root.quit()
        self.root.destroy()


    def load_params(self, file):

        with open(file, 'rb') as f:
            params = json.load(f)
        return params


    def save_colours(self, col_dict):
        for name, value in col_dict.items():
            if type(value) is np.ndarray:
                col_dict[name] = list(value)
        path = os.path.join(self.dir, 'colours.json')
        with open(path, 'wb') as f:
            json.dump(col_dict, f)

    def check_colours_dict(self, col_dict):
        try:
            for name, value in col_dict.items():
                assert name in ['bg_grey', 'fg_grey', 'bg_col', 'fg_col']
                assert type(value) is list
                for v in value:
                    assert 0 <= v <= 255
        except Exception:
            logger.exception('bad colours dict')
            return False

        return True


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

        if not result.wasSuccessful():
            showwarning('Test results', 'Some tests were not successful')
            for i in result.failures:
                logging.error('test error:\n'.format(i[1]))





if __name__ == '__main__':
    app = Application(tk.Tk())
    app.root.mainloop()
