from experiment_part import *
import json
from psychopy import visual, core
from tools import *
import Tkinter as tk
import tkFileDialog
import ast
from tkMessageBox import showwarning, showinfo, askyesno
import subprocess

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

        self.grey_var = tk.StringVar(); self.grey_var.set('[0, 0, 0]')
        self.col_var = tk.StringVar(); self.col_var.set('[0, 0, 0]')

        if def_grey:
            tk.Label(self.top, text = 'Contrast (FG):').grid(row = 0, column = 0, sticky = 'E', pady = 5)
            self.grey_entry = tk.Entry(self.top,
                textvariable = self.grey_var,
                width = 15,
                justify = tk.CENTER,
                relief = tk.FLAT)
            self.grey_entry.grid(row = 0, column = 1, padx = (10, 0), pady = 5)

        if def_col:
            tk.Label(self.top, text = 'Isoluminance (BG):').grid(row = 1, column = 0, sticky = 'E', pady = 5)
            self.col_entry = tk.Entry(self.top,
                textvariable = self.col_var,
                width = 15,
                justify = tk.CENTER,
                relief = tk.FLAT)
            self.col_entry.grid(row = 1, column = 1, padx = (10, 0), pady = 5)

        tk.Button(self.top,
            text = 'OK',
            command = self.ok,
            width = 5,
            relief = tk.GROOVE).grid(row = 2, column = 1, pady = (10, 0))
            
        tk.Button(self.top,
            text = 'Load colours',
            command = self.load_colours,
            width = 10,
            relief = tk.GROOVE).grid(row = 2, column = 0, pady = (10,0))


    def ok(self):

        try:
            grey = ast.literal_eval(self.grey_var.get())
            col = ast.literal_eval(self.col_var.get())
            for arr in [grey, col]:
                assert len(arr) == 3
                assert all(0 <= i <= 255 for i in arr)
        except:
            showwarning('Entry', 'Incorrect value')
            return

        if self.def_grey:
            self.master.colours['fg_grey'] = grey

        if self.def_col:
            self.master.colours['bg_col'] = col

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
            self.grey_var.set(str(d['fg_grey']))
            self.col_var.set(str(d['bg_col']))
        except:
            showwarning('File error', 'Bad colours file')
            return


class Application(object):

    def __init__(self, root):

        self.root = root
        self.root.resizable(width = False, height = False)
        self.root.title('Psychophysics')
        self.program_path = os.getcwd()
        self.frame = tk.Frame(root)
        self.frame.grid(row = 0, column = 0, sticky = 'wns', padx=  30, pady = 30)

        if not os.path.isfile('./parameters.json'):
            showwarning('Parameters', 'Missing parameters file')
            return
        self.params = self.load_params('./parameters.json')
        
        self.colours = {
            'bg_grey': self.params['ContrastDetection']['bg_grey'],
            'fg_grey': None,
            'bg_col': None,
            'fg_col': self.params['IsoluminanceDetection']['fix_col']
            }

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




    def start_experiment(self):

        np.random.seed(1)
        id = self.id.get()
        if id == "Participant's id":
            showwarning('Missing id', "Enter participant's id")
            return

        self.dir = os.path.join('.', id)
        if os.path.isdir(self.dir):
            ans = askyesno('Participant id', 'This participant exists. Overwrite?')
            if ans == 0:
                return
            else:
                shutil.rmtree(self.dir)
        os.makedirs(os.path.join(self.dir, 'stimuli'))

        free = self.free_var.get()
        contrast = self.contrast_var.get()
        isolum = self.isolum_var.get()

        if free and not (contrast and isolum):
            popup = PopupEntries(self, not contrast, not isolum)
            # self.root.wait_window(popup.top)
            if not popup.finished:
                return
            self.save_colours(self.colours)

        self.win = visual.Window(
            size = [1920, 1080],
            monitor = 'labBENQ',
            fullscr = True,
            colorSpace = 'rgb255',
            color = 128,
            units = 'deg')
        self.win.mouseVisible = False


        # Contrast detection
        if contrast:
            self.contrast = ContrastDetection(self.win, id, self.params['ContrastDetection'])
            try:
                self.contrast.main_sequence()
            except Exception as e:
                self.win.close()
                showwarning('Experiment error', str(e))
            finally:
                filename = os.path.join(self.dir, 'contrast.exp')
                col = [round(i, 2) for i in self.contrast.output_col]
                self.contrast.export_results(filename, ['Mean colour:', col])

                self.colours['fg_grey'] = self.contrast.output_col
                self.save_colours(self.colours)


        # Isoluminance detection
        if isolum:
            self.isolum = IsoluminanceDetection(self.win, id, self.params['IsoluminanceDetection'])
            try:
                self.isolum.main_sequence()
            except Exception as e:
                self.win.close()
                showwarning('Experiment error', str(e))
            finally:
                filename = os.path.join(self.dir, 'isoluminance.exp')
                col = [round(i, 2) for i in self.isolum.output_col]
                self.isolum.export_results(filename, ['Mean colour:', col])

                self.colours['bg_col'] = self.isolum.output_col
                self.save_colours(self.colours)
         

        # Free choice experiment
        if free:

            correct = self.check_colours_dict(self.colours)
            if not correct:
                self.win.close()
                showwarning('Colours', 'Error with colours')
                return

            self.free_choice = FreeChoiceExperiment(self.win, id, self.params['FreeChoiceExperiment'])
            try:
                self.free_choice.define_colours(self.colours)
                self.free_choice.main_sequence()
            except Exception as e:
                self.win.close()
                showwarning('Experiment error', str(e))
            finally:
                filename = os.path.join(self.dir, 'free_choice.exp')
                self.free_choice.export_results(filename)


        self.win.close()
        showinfo('Experiment', 'Finished!')


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
        except:
            return False

        return True


    def run_tests(self):
        subprocess.call(['python', 'test_tools.py'])
        subprocess.call(['python', 'test_experiment_part.py'])





if __name__ == '__main__':
    app = Application(tk.Tk())
    app.root.mainloop()
