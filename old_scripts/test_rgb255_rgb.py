from experiment_part import *
import tools
from psychopy import visual, event, core

imgfile = './images/letters/Hr.png'
imgfile1 = './images/letters/stimuli/Hr_parvo.png'
fg = tools.get_fg_mask(imgfile)
bg = fg * -1

win = visual.Window(
            size = [1920, 1080],
            monitor = 'labBENQ',
            fullscr = False,
            colorSpace = 'rgb255',
            color = 128,
            units = 'deg')
            
stim1 = visual.ImageStim(
            win = win,
            pos = (0, 0),
            image = imgfile,
            mask = bg,
            color = [0, 119, 0],
            units = 'deg',
            size = [7.84, 9.26],
            colorSpace = 'rgb255')
            
stim2 = visual.ImageStim(
            win = win,
            pos = (0, 0),
            image = imgfile,
            mask = fg,
            units = 'deg',
            size = [7.84, 9.26],
            colorSpace = 'rgb255')
stim2.color = tools.invert([225, 0, 0])
            
stim3 = visual.ImageStim(
            win = win,
            pos = (0, 0),
            image = imgfile1,
            units = 'deg',
            size = [7.84, 9.26],
            colorSpace = 'rgb')
    

key = None
while not key:
    stim1.draw()
    stim2.draw()
    win.flip()
    core.wait(0.2)
    stim3.draw()
    win.flip()
    core.wait(0.2)
    key = event.getKeys()
    
# stim1.draw()
# win.flip()
# event.waitKeys()

# stim2.draw()
# win.flip()
# event.waitKeys()

# stim3.draw()
# win.flip()
# event.waitKeys()

win.close()