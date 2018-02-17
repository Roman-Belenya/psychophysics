from psychopy import visual, event, monitors
import numpy as np

mon = monitors.Monitor('LabDell')
mon.setCurrent('experiment')
space = 'dkl'
d = 1


win = visual.Window(
    size = [1024, 1024],
    monitor = mon,
    screen = 0,
    fullscr = False,
    allowGUI = False,
    color = [0, 0, 0],
    units = 'pix')

stim1 = visual.GratingStim(
    win = win,
    tex = None,
    size = 255,
    pos = [-200, 0],
    colorSpace = space)
stim1.color = [0, 174, 0]

col1 = visual.TextStim(
    win = win,
    text = str(stim1.color),
    pos = [-200, -200])

stim2 = visual.GratingStim(
    win = win,
    tex = None,
    size = 255,
    pos = [200, 0],
    colorSpace = space)
stim2.color = [225, 0, 0]

col2 = visual.TextStim(
    win = win,
    text = str(stim2.color),
    pos = [200, -200])


stim3 = visual.GratingStim(
    win = win,
    tex = None,
    mask = 'circle',
    size = 128,
    pos = [0, 0],
    colorSpace = space)

current_stim = stim1

stim1.draw()
col1.draw()
stim2.draw()
col2.draw()
win.flip()


while True:

    key = event.waitKeys()

    if key[0] == '1':
        current_stim = stim1
    elif key[0] == '2':
        current_stim = stim2

    elif key[0] == 'q':
        current_stim.color += [d, 0, 0]
    elif key[0] == 'a':
        current_stim.color -= [d, 0, 0]

    elif key[0] == 'w':
        current_stim.color += [0, d, 0]
    elif key[0] == 's':
        current_stim.color -= [0, d, 0]

    elif key[0] == 'e':
        current_stim.color += [0, 0, d]
    elif key[0] == 'd':
        current_stim.color -= [0, 0, d]

    elif key[0] == 'f':

        win.flip()
        frame = 0
        key = None

        while not key:
            if frame % 1 == 0:
                if np.all(stim3.color == stim1.color):
                    stim3.color = stim2.color
                else:
                    stim3.color = stim1.color
            stim3.draw()
            win.flip()
            frame += 1
            key = event.getKeys()

    elif key[0].startswith('num_'):
        d = int(key[0].split('_')[1])

    elif key[0] == 'r':
        stim1.color = [0,0,0]
        stim2.color = [0,0,0]


    elif key[0] in ['return', 'escape']:
        break


    if current_stim == stim1:
        stim1 = current_stim
    else:
        stim2 = current_stim

    col1.text = str(np.around(stim1.color, 2))
    col2.text = str(np.around(stim2.color, 2))

    stim1.draw()
    col1.draw()
    stim2.draw()
    col2.draw()
    win.flip()


win.close()
