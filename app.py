from experiment_part import *
import json
from psychopy import visual, core
from tools import *
import Tkinter as tk
import ast
from tkMessageBox import showwarning, showinfo, askyesno

class PopupEntries(object):
    def __init__(self, master, grey = True, col = True):
    
        self.master = master
        self.top = tk.Toplevel(master.root, padx = 20, pady = 20)
        self.top.title('Define colours')
        self.grey = grey
        self.col = col
        self.finished = False
        
        self.grey_var = tk.StringVar(); self.grey_var.set('0')
        self.col_var = tk.StringVar(); self.col_var.set('[0, 0, 0]')
        
        if grey:
            tk.Label(self.top, text = 'FG grey:').grid(row = 0, column = 0, sticky = 'E', pady = 5)
            self.grey_entry = tk.Entry(self.top,
                textvariable = self.grey_var,
                width = 10,
                justify = tk.CENTER, 
                relief = tk.FLAT)
            self.grey_entry.grid(row = 0, column = 1, padx = (10, 0), pady = 5)
            
        if col:
            tk.Label(self.top, text = 'BG [r, g, b]:').grid(row = 1, column = 0, sticky = 'E', pady = 5)
            self.col_entry = tk.Entry(self.top,
                textvariable = self.col_var, 
                width = 10,
                justify = tk.CENTER, 
                relief = tk.FLAT)
            self.col_entry.grid(row = 1, column = 1, padx = (10, 0), pady = 5)
        
        tk.Button(self.top,
            text = 'OK', 
            command = self.ok,
            width = 5,
            relief = tk.GROOVE).grid(row = 2, column = 0, columnspan = 2, pady = (10, 0))
        
        
    def ok(self):
    
        try:
            grey = ast.literal_eval(self.grey_var.get())
            assert type(grey) is int
            assert 0 <= grey <= 255
            col = ast.literal_eval(self.col_var.get())
            assert type(col) is list
            assert len(col) == 3
            for i in col:
                assert 0 <= i <= 255
        except:
            showwarning('Entry', 'Incorrect value')
            return
    
        if self.grey:
            self.master.colours['fg_grey'] = grey
            
        if self.col:
            self.master.colours['bg_col'] = col
            
        self.finished = True    
        self.top.destroy()
        
        
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

        self.id = tk.StringVar()
        self.id.set("Participant's id")
        self.id_entry = tk.Entry(self.frame, 
            textvariable = self.id, 
            justify = tk.CENTER, 
            relief = tk.FLAT, 
            width = 15)
        self.id_entry.grid(row = 0, column = 0, padx = 10, pady = (0, 20))
        
        self.colours = {'bg_grey': self.params['ContrastDetection']['bg_grey'],
            'fg_col': self.params['IsoluminanceDetection']['fix_col']}
        
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
        
        # Start button
        self.start_button = tk.Button(self.frame,
            text = 'Start experiment',
            command = self.start_experiment,
            height = 2,
            width = 10,
            relief = tk.GROOVE)
        self.start_button.grid(row = 6, column = 0, columnspan = 2, sticky = 'EW', pady = (20, 0))
        

    def start_experiment(self):
    
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
            self.root.wait_window(popup.top)
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
        

        # Contrast detection
        if contrast:
            self.contrast = ContrastDetection(self.win, id, self.params['ContrastDetection'])
            self.contrast.main_sequence()
            filename = os.path.join(self.dir, 'contrast.exp')
            self.contrast.export_results(filename, ['Mean colour:', self.contrast.output_col])
            
            self.colours['fg_grey'] = self.contrast.output_col
            self.save_colours(self.colours)
        
        # Isoluminance detection
        if isolum:
            self.isolum = IsoluminanceDetection(self.win, id, self.params['IsoluminanceDetection'])
            self.isolum.main_sequence()
            filename = os.path.join(self.dir, 'isoluminance.exp')
            self.isolum.export_results(filename, ['Mean colour:', self.isolum.output_col])
            
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
            self.free_choice.define_colours(self.colours)
            self.free_choice.main_sequence()
            
            filename = os.path.join(self.dir, 'free_choice.exp')
            self.free_choice.export_results(filename)
        
        
        self.win.close()
        showinfo('Experiment', 'Finished!')
            
            
    def load_params(self, file):
        
        with open(file, 'rb') as f:
            params = json.load(f)
        return params
        
    def save_colours(self, col_dict):
    
        path = os.path.join(self.dir, 'colours.json')
        with open(path, 'wb') as f:
            json.dump(col_dict, f)
            
    def check_colours_dict(self, col_dict):
        try:
            for name, value in col_dict.items():
                assert name in ['bg_grey', 'fg_grey', 'bg_col', 'fg_col']
                assert type(value) in [int, list]
                if type(value) is int:
                    assert 0 <= value <= 255
                elif type(value) is list:
                    for v in list:
                        assert 0 <= v <= 255
        except:
            return False
        
        return True
        

        
if __name__ == '__main__':
    app = Application(tk.Tk())
    app.root.mainloop()