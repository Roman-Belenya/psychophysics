from psychopy import visual, event, monitors, tools
import numpy as np

mon = monitors.Monitor('LabDell')
mon.setCurrent('experiment')
d = 1

def cart2sph(dklCart):

    z,y,x = dklCart

    radius = np.sqrt(x**2 + y**2 + z**2)
    azimuth = np.arctan2(x, y)
    if azimuth < 0:
        azimuth += 2 * np.pi
    elevation = np.arctan(float(z)/np.sqrt(x**2 + y**2))

    azimuth = azimuth * (180 / np.pi)
    elevation *= (180 / np.pi)

    sphere = np.array([elevation, azimuth, radius])

    return sphere




win = visual.Window(
    size = [1024, 1024],
    monitor = mon,
    screen = 0,
    fullscr = False,
    allowGUI = False,
    color = [0, 0, 0],
    units = 'pix',
    useRetina = True)

stim1 = visual.GratingStim(
    win = win,
    tex = None,
    size = 255,
    pos = [-200, 0],
    colorSpace = 'dkl')
stim1.color = [90, 0, 1]

col1 = visual.TextStim(
    win = win,
    text = str(stim1.color),
    pos = [-200, -200],
    color = 1)

space1 = visual.TextStim(
    win = win,
    text = str(stim1.colorSpace),
    pos = [-200, 200],
    color = 1)

stim2 = visual.GratingStim(
    win = win,
    tex = None,
    size = 255,
    pos = [200, 0],
    colorSpace = 'dkl')
stim2.color = [90, 0, 1]

col2 = visual.TextStim(
    win = win,
    text = str(stim2.color),
    pos = [200, -200],
    color = 0.2)

space2 = visual.TextStim(
    win = win,
    text = str(stim2.colorSpace),
    pos = [200, 200],
    color = 1)


stim3 = visual.GratingStim(
    win = win,
    tex = None,
    mask = 'circle',
    size = 128,
    pos = [0, 0],
    colorSpace = 'dkl')

current_stim = stim1

stim1.draw()
col1.draw()
space1.draw()
stim2.draw()
col2.draw()
space2.draw()
win.flip()


while True:

    key = event.waitKeys()

    if key[0] == 'left':
        current_stim = stim1
        col1.color = 1
        col2.color = 0.2
    elif key[0] == 'right':
        current_stim = stim2
        col2.color = 1
        col1.color = 0.2

    elif key[0] == 'up':
        if current_stim.colorSpace == 'rgb255':
            rgb = current_stim.color / 127.5 - 1
            conversionMatrix =  np.linalg.inv(mon.getDKL_RGB())
            dkl = np.dot(conversionMatrix, rgb)
            dkl = cart2sph(dkl)
            current_stim.colorSpace = 'dkl'
            current_stim.color = dkl
    elif key[0] == 'down':
        if current_stim.colorSpace == 'dkl':
            rgb = tools.colorspacetools.dkl2rgb(current_stim.color, mon.getDKL_RGB())
            rgb = (rgb + 1) * 127.5
            current_stim.colorSpace = 'rgb255'
            current_stim.color = rgb

    elif key[0] == 'q':
        current_stim.color += [d, 0, 0]
    elif key[0] == 'a':
        current_stim.color -= [d, 0, 0]

    elif key[0] == 'w':
        current_stim.color += [0, d, 0]
    elif key[0] == 's':
        current_stim.color -= [0, d, 0]

    elif key[0] == 'e':
        dd = d
        if current_stim.colorSpace == 'dkl':
            dd = d * 0.1
        current_stim.color += [0, 0, dd]
    elif key[0] == 'd':
        dd = d
        if current_stim.colorSpace == 'dkl':
            dd = d * 0.1
        current_stim.color -= [0, 0, dd]

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
        current_stim.color = [0,0,0]


    elif key[0] in ['return', 'escape']:
        break


    if current_stim == stim1:
        stim1 = current_stim
    else:
        stim2 = current_stim

    col1.text = str(np.around(stim1.color, 2))
    space1.text = str(stim1.colorSpace)
    col2.text = str(np.around(stim2.color, 2))
    space2.text = str(stim2.colorSpace)

    stim1.draw()
    col1.draw()
    space1.draw()
    stim2.draw()
    col2.draw()
    space2.draw()
    win.flip()


win.close()
