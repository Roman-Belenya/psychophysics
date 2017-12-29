from experiment_part import *
import json
from psychopy import visual, core
from tools import *
import Tkinter as tk
from tkMessageBox import showwarning, showinfo, askyesno


class Application(object):

    def __init__(self, root):

        self.root = root
        self.root.resizable(width = False, height = False)
        self.program_path = os.getcwd()
        self.frame = tk.Frame(root)
        self.frame.grid(row = 0, column = 0, sticky = 'wns', padx=  30, pady = 30)

        self.id = tk.StringVar()
        self.id.set('Participant id')
        self.id_entry = tk.Entry(self.frame, 
            textvariable = self.id, 
            justify = tk.CENTER, 
            relief = tk.FLAT, 
            width = 15)
        self.id_entry.grid(row = 0, column = 0, padx = 10)
        
        self.start_button = tk.Button(self.frame,
            text = 'Start experiment',
            command = self.start_experiment,
            height = 2,
            width = 10,
            relief = tk.GROOVE)
        self.start_button.grid(row = 1, column = 0, columnspan = 2, sticky = 'EW', pady = (20, 0))
        
        self.win = None
        self.params = None
        self.contrast = None
        self.isolum = None
        self.free_choice = None

    def start_experiment(self):
    
        id = self.id.get()
        if id == 'Participant id':
            showwarning('Missing id', "Enter participant's id")
            return
        
        dir = os.path.join('.', id)
        if os.path.isdir(dir):
            ans = askyesno('Participant id', 'This participant exists. Overwrite?')
            if ans == 0:
                return
            else:
                shutil.rmtree(dir)
        os.mkdir(dir)
            
        if not os.path.isfile('./parameters.json'):
            showwarning('Parameters', 'Missing parameters file')
            return
            
        self.params = self.load_params('./parameters.json')
            
        self.win = visual.Window(
            size = [1920, 1080],
            monitor = 'labBENQ',
            fullscr = True,
            colorSpace = 'rgb255',
            color = 128,
            units = 'deg')
        
        colours = {}

        # Contrast detection
        self.contrast = ContrastDetection(self.win, id, **self.params['ContrastDetection'])
        self.contrast.main_sequence()
        filename = os.path.join(dir, 'contrast.exp')
        self.contrast.export_results(filename, ['Mean colour:', self.contrast.output_col])
        
        colours['bg_grey'] = self.params['ContrastDetection']['bg_grey']
        colours['fg_grey'] = self.contrast.output_col
        
        self.save_colours(colours)
        
        # Isoluminance detection
        self.isolum = IsoluminanceDetection(self.win, id, **self.params['IsoluminanceDetection'])
        self.isolum.main_sequence()
        filename = os.path.join(dir, 'isoluminance.exp')
        self.isolum.export_results(filename, ['Mean colour:', self.isolum.output_col])
        
        colours['bg_col'] = self.isolum.output_col
        colours['fg_col'] = self.params['IsoluminanceDetection']['fix_col']
        
        # Free choice experiment
        self.free_choice = FreeChoiceExperiment(self.win, id, **self.params['FreeChoiceExperiment'])
        
        self.free_choice.define_colours(colours)
        self.free_choice.main_sequence()
        
        filename = os.path.join(dir, 'free_choice.exp')
        self.free_choice.export_results(filename)
        
        self.win.close()
        showinfo('Experiment', 'Finished!')
            
            
    def load_params(self, file):
        
        with open(file, 'rb') as f:
            params = json.load(f)
        return params
        
    def save_colours(self, col_dict):
    
        path = os.path.join(dir, 'colours.json')
        with open(path, 'wb') as f:
            json.dump(col_dict, f)
        

        
if __name__ == '__main__':
    app = Application(tk.Tk())
    app.root.mainloop()