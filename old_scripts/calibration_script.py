import numpy as np
from psychopy import monitors
import matplotlib.pyplot as plt

data = {'k': './luminance.dat',
        'r': './red.dat',
        'g': './green.dat',
        'b': './blue.dat'}
lums = {}

for key, value in data.items():
    with open(value, 'rb') as f:
        vec = []
        for i, line in enumerate(f):
            if i >= 2:
                x = float(line.split('\t')[1])
                vec.append(x)
    lums[key] = vec


# for key in lums.keys():
#     lums[key][0] = lums['k'][0]

lums_m = np.array([lums['k'], lums['r'], lums['g'], lums['b']])


mon = monitors.Monitor('labDELL')
mon.setCurrent('calib')

mon.setDistance(40)
mon.setWidth(52)
mon.setSizePix([1920, 1200])

levels = np.linspace(0, 255, 32).tolist()
levels = [int(x) for x in levels]


mon.setLevelsPre(levels)
mon.setLumsPre(lums_m)

gammaGrid = []
for chan in ['k', 'r', 'g', 'b']:

    gamma = monitors.GammaCalculator(inputs = levels, lums = lums[chan], eq = 4)
    print gamma.a, gamma.b, gamma.k
    row = [gamma.min, gamma.max, gamma.gamma, gamma.a, gamma.b, gamma.k]
    gammaGrid.append(row)

gammaGrid = np.array(gammaGrid)
mon.setGammaGrid(gammaGrid)

print mon.currentCalib
mon.saveMon()
