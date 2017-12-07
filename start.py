from experiment_part import *
import json
from psychopy import visual, core
from tools import *
import Tkinter as tk

with open('parameters.json', 'rb') as f:
    params = json.load(f)
    for i, j in params.items():
        for name, value in j.items():
            if type(value) is list:
                
                params[i][name] = np.array(value)
    

win = visual.Window(
    size = [1920, 1080],
    monitor = 'labBENQ',
    fullscr = True,
    colorSpace = 'rgb255',
    color = 128,
    units = 'deg')

contrast = ContrastDetection(win, **params['ContrastDetection'])
isolum = IsoluminanceDetection(win, **params['IsoluminanceDetection'])
free_choice = FreeChoiceExperiment(win, **params['FreeChoiceExperiment'])

contrast.main_sequence()
isolum.main_sequence()

fg_col = params['IsoluminanceDetection']['fix_col']
# bg_col = [0, 100, 0]
bg_col = isolum.output_col
fg_grey = 130
fg_grey = contrast.output_col
bg_grey = params['ContrastDetection']['grey']


free_choice.define_colours(fg_col, bg_col, fg_grey, bg_grey)
free_choice.main_sequence()

# exp = ExperimentPart(win, **params['Global'])
# exp.fixation_cross.draw()
# exp.win.flip()
# core.wait(2)
# exp.win.close()




class Applicaiton(object):
    
    def __init__(self, root):
    
        self.root = root
        self.program_path = os.getcwd()
        self.frame = tk.Frame(root)
        self.frame.grid(row = 0, column = 0, sticky = 'wns', padx=  30, pady = 30)
        
        tk.Label(self.frame, text = 'Participant id', row = 1, column = 0)
        self.subject_id = tk.Entry(self.frame)
        self.subject_id.grid(row = 1, column = 1)
        
    def start_experiment(self):
        pass