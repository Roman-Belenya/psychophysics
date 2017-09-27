from psychopy import visual, core, event
import numpy as np
from PIL import Image

pic = np.zeros([8, 8, 3], dtype = np.float32)

win = visual.Window(monitor = 'testMonitor', fullscr = True, units = 'pix', colorSpace = 'rgb', color = 0, size = [1920, 1080])
stim = visual.GratingStim(win, tex = pic, size = [1920, 1080], colorSpace = 'rgb')
lum = visual.TextStim(win, text = '0', pos = (0, 0), colorSpace = 'rgb', color = -1)

delta = 0.001

stim.draw()
win.flip()

finished = False

while not finished:
    key = event.waitKeys()
    if key[0] == 'up':
        pic[:, 0:4, :] += delta
    elif key[0] == 'down':
        pic[:, 0:4, :] -= delta
    elif key[0] == 'escape':
        finished = True

    lum.text = str(pic[0,0,0])
    stim.tex = pic

    stim.draw()
    lum.draw()
    win.flip()

win.close()


pic = np.zeros([1080, 1920, 3], dtype = np.uint8) + 128
pic[:, 0:540, :] += 100
Image.fromarray(pic).save('compare.png', 'PNG')


