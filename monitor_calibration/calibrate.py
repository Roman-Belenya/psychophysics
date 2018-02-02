from psychopy import visual, event, monitors
import numpy as np
np.random.seed(1)

mon = monitors.Monitor('labDell')
mon.setCurrent('psychopy')
print mon.currentCalib['notes']

win = visual.Window(
    size = [1920, 1200],
    monitor = mon,
    screen = 0,
    fullscr = True,
    colorSpace = 'rgb255',
    color = 128,
    units = 'pix')

noise_tex = np.random.rand(1920, 1200) * 2 - 1
noise_tex = np.random.binomial(2, 0.5, (1920, 1200)) - 1
noise = visual.GratingStim(
    win = win,
    tex = noise_tex,
    interpolate = False,
    size = [1920, 1200])

reference = visual.GratingStim(
    win = win,
    tex = None,
    colorSpace = 'rgb255',
    color = [1,1,1],
    size = [512, 256])

target = visual.GratingStim(
    win = win,
    tex = None,
    colorSpace = 'rgb255',
    color = [0,0,0],
    size = 256)

curr_colour = visual.TextStim(
    win = win,
    pos = (0, -500),
    colorSpace = 'rgb255',
    color = [0, 255, 255])

curr_calib = visual.TextStim(
    win = win,
    colorSpace = 'rgb255',
    color = 0)



def calibrate(chan, n = 32):

    curr_calib.text = chan
    curr_calib.draw()
    win.flip()
    event.waitKeys()

    steps = np.linspace(0, 255, n)
    i = 0

    while True:

        tc = int(steps[i])

        if chan == 'red':
            target_col = [tc, 0, 0]
        elif chan == 'green':
            target_col = [0, tc, 0]
        elif chan == 'blue':
            target_col = [0, 0, tc]
        elif chan == 'luminance':
            target_col = [tc] * 3
        else:
            return

        target.color = target_col
        # reference.color = [255 - k for k in target_col]
        curr_colour.text = '{}/{}: {}'.format(i+1, n, str(target_col))

        # noise.draw()
        # reference.draw()
        target.draw()
        curr_colour.draw()
        win.flip()

        key = event.waitKeys(keyList = ['left', 'right', 'return'])
        if key[0] == 'left' and i > 0:
            i -= 1
        elif key[0] == 'right' and i < len(steps) - 1:
            i += 1
        elif key[0] == 'return':
            return


if __name__ == '__main__':

    # Measure levels
    calibs = ['luminance', 'red', 'green', 'blue']
    for calib in calibs:
        calibrate(calib, n = 32)

    # Measure pure colours
    # cols = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
    # for col in cols:
    #     target.color = col
    #     target.draw()
    #     win.flip()
    #     event.waitKeys()


    # Determine maxLum/5
    # while True:
    #     key = event.waitKeys()
    #     if key[0] == 'up':
    #         target.color += 1
    #     elif key[0] == 'down':
    #         target.color -= 1
    #     elif key[0] == 'escape':
    #         break
    #     target.draw()
    #     win.flip()
    #     print target.color

    # Test calibration

    # cols = [0, 128, 255]
    # for col in cols:
    #     target.color = col
    #     target.draw()
    #     win.flip()
    #     event.waitKeys()

    win.close()
