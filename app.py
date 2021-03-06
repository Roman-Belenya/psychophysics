from psychopy import monitors
import Tkinter as tk
import logging
from experiment_part import *
import json
from tools import *
import tkFileDialog
from tkMessageBox import showwarning, showinfo, askyesno
import unittest

DIRS = ['./data', './logs']
for DIR in DIRS:
    if not os.path.isdir(DIR):
        os.mkdir(DIR)

time = datetime.datetime.strftime(datetime.datetime.now(), '%d-%b-%Y %H-%M-%S,%f')
logfile = os.path.join('./logs', time + '.log')
logging.basicConfig(filename = logfile,
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(funcName)s: %(message)s',
    filemode = 'a')
logger = logging.getLogger(__name__)


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

        if self.params['run_tests']:
            self.run_tests()

        self.colours = self.params['default_colours']

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
        self.colour_var = tk.IntVar()
        tk.Checkbutton(
            self.frame,
            text = 'Colour test',
            variable = self.colour_var).grid(row = 1, column = 0, sticky = 'W', pady = (0, 5))
        self.colour_var.set(1) # checked off by default

        self.contrast_var = tk.IntVar()
        tk.Checkbutton(
            self.frame,
            text = 'Contrast detection',
            variable = self.contrast_var).grid(row = 2, column = 0, sticky = 'W')
        self.contrast_var.set(1)

        self.isolum_var = tk.IntVar()
        tk.Checkbutton(
            self.frame,
            text = 'Isoluminance deteciton',
            variable = self.isolum_var).grid(row = 3, column = 0, sticky = 'W', pady = (0, 5))

        self.free_var = tk.IntVar()
        tk.Checkbutton(
            self.frame,
            text = 'Free choice',
            variable = self.free_var).grid(row = 4, column = 0, sticky = 'W')
        self.free_var.set(1)

        self.divided_var = tk.IntVar()
        tk.Checkbutton(
            self.frame,
            text = 'Divided attention',
            variable = self.divided_var).grid(row = 5, column = 0, sticky = 'W')
        self.divided_var.set(1)

        self.selective_var = tk.IntVar()
        tk.Checkbutton(
            self.frame,
            text = 'Selective attention',
            variable = self.selective_var).grid(row = 6, column = 0, sticky = 'W')
        self.selective_var.set(1)

        # Buttons
        self.tests_button = tk.Button(self.frame,
            text = 'Run tests',
            command = self.run_tests,
            height = 2,
            width = 10,
            relief = tk.GROOVE)
        self.tests_button.grid(row = 7, column = 0, columnspan = 2, sticky = 'EW', pady = (20, 0))

        self.start_button = tk.Button(self.frame,
            text = 'Start experiment',
            command = self.start_experiment,
            height = 2,
            width = 10,
            relief = tk.GROOVE)
        self.start_button.grid(row = 8, column = 0, columnspan = 2, sticky = 'EW', pady = (10, 0))

        logger.info('started app')




    def start_experiment(self):

        np.random.seed(1)

        # Get participant's id
        _id = self.id.get().rstrip()
        if has_illegal_chars(_id):
            showwarning('Illegal charater', 'Avoid /\\:*?"<>| in the name')
            return
        elif _id in ["Participant's id", '']:
            showwarning('Missing id', "Enter participant's id")
            return

        # Make directories
        self.dir = os.path.join('.', 'data', _id)
        if os.path.isdir(self.dir):
            ans = askyesno("Participant's id", '{} already exists. Continue experiment with this participant?'.format(_id))
            if ans:
                logger.info('continuing with participant {}'.format(_id))
                cols_file = os.path.join(self.dir, 'colours.json')
                try:
                    self.colours = json.load(open(cols_file, 'rb'))
                    showinfo('Loaded existing colours', self.colours)
                    logger.info('loaded colours from {}'.format(cols_file))
                except:
                    showwarning('Failed to load colours', 'Continuing with default')
                    logger.exception('failed to load colours from {}'.format(cols_file))
            else:
                logger.info('do not continue with participant {}. returning'.format(_id))
                return
        else:
            os.mkdir(self.dir)
            logger.info('created new participant {}'.format(_id))

        # Get experiment selections
        sel = {
            'colour': self.colour_var.get(),
            'contrast': self.contrast_var.get(),
            'isolum': self.isolum_var.get(),
            'free': self.free_var.get(),
            'divided': self.divided_var.get(),
            'selective': self.selective_var.get()
            }
        logger.info('selected experiments: {}'.format(sel))

        # need_def, need_grey, need_col = self.need_definition(sel)
        # if need_def:
        #     popup = PopupEntries(self, need_grey, need_col)
        #     self.root.wait_window(popup.top)
        #     if not popup.finished:
        #         return
        #     self.save_colours(self.colours)

        # Load the monitor
        mon = load_monitor(self.params['Monitors'][self.params['current_monitor']])
        logger.info('loaded monitor {}'.format(mon.currentCalib))

        self.win = visual.Window(
            size = mon.getSizePix(),
            monitor = mon,
            screen = 0,
            fullscr = True,
            allowGUI = False,
            colorSpace = 'rgb255',
            color = 128,
            units = 'deg')
        self.win.mouseVisible = False

        self.thank_you = visual.ImageStim(
            win = self.win,
            image = self.params['thank_you_img'])

        # The app is no longer needed
        self.root.quit()
        self.root.destroy()

        exps = [('colour', 'ColourTest', ColourTest),
                ('contrast', 'ContrastDetection', ContrastDetection),
                ('isolum', 'IsoluminanceDetection', IsoluminanceDetection),
                ('free', 'FreeChoiceExperiment', FreeChoiceExperiment),
                ('divided', 'DividedAttentionExperiment', DividedAttentionExperiment) ,
                ('selective', 'SelectiveAttentionExperiment', SelectiveAttentionExperiment) ]

        for name, fullname, exp in exps:

            if sel[name]: # if this experiment is selected
                try:
                    experiment = exp(self.win, _id, self.colours, self.params[fullname])
                    experiment.main()
                except Exception as e:
                    self.win.close()
                    showwarning('Experiment error', 'See {}'.format(logfile))
                    logger.exception('error in experiment:')
                    return
                finally:
                    if name in ['contrast', 'isolum']:
                        avg = ['Mean Colour:', experiment.get_mean_col()]
                        experiment.export_results(self.dir, avg)
                        self.colours = experiment.get_colours_dict()
                    else:
                        experiment.export_results(self.dir)


        self.save_colours()
        self.win.flip()
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


    def save_colours(self):

        for name, value in self.colours.items():
            if type(value) is np.ndarray:
                self.colours[name] = list(value)

        path = os.path.join(self.dir, 'colours.json')
        with open(path, 'wb') as f:
            json.dump(self.colours, f)


    def run_tests(self):

        logger.info('running tests')
        from test_experiment_part import TestExperimentPart
        from test_tools import TestTools

        to_run = [TestTools, TestExperimentPart]
        loader = unittest.TestLoader()
        loader.sortTestMethodsUsing = None
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


if __name__ == '__main__':
    app = Application(tk.Tk())
    app.root.mainloop()
