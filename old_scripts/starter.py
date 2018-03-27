from experiment_part import *
import json
from psychopy import visual, core
from tools import *
import sys

id = 'test'
params = json.load(open('./parameters.json'))

if os.path.isdir('./test/'):
    raise Exception('delete test folder')

os.makedirs('./test/stimuli')


colours = {"fg_col": [225, 0, 0],
           "bg_grey": 128,
           "bg_col": [0, 116, 0],
           "fg_grey": 130}

win = visual.Window(
    size = [1920, 1080],
    monitor = 'labBENQ',
    fullscr = True,
    colorSpace = 'rgb255',
    color = 128,
    units = 'deg')


con = ContrastDetection(win, id, params['ContrastDetection'])

iso = IsoluminanceDetection(win, id, params['IsoluminanceDetection'])

choice = FreeChoiceExperiment(win, id, colours, params['FreeChoiceExperiment'])

divided = DividedAttentionExperiment(win, id, colours, params['DividedAttentionExperiment'])


if __name__ == '__main__':
    arg = sys.argv[1]
    if 'c' in arg:
        con.main_sequence()
    if 'i' in arg:
        iso.main_sequence()
    if 'f' in arg:
        choice.main_sequence()
    if 'd' in arg:
        divided.main_sequence()

    if 'u' in arg:
        divided.make_images_sequence()


