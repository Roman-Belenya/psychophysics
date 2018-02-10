from psychopy import monitors
import numpy as np
import csv

files = ['./spectra_data/luminance.dat',
         './spectra_data/red.dat',
         './spectra_data/green.dat',
         './spectra_data/blue.dat']

lums = []
for file in files:
    vec = []
    with open(file, 'rb') as f:
        for i, line in enumerate(f):
            if i > 1:
                vec.append(float(line.split('\t')[1]))
    lums.append(vec)

levels = map(int, np.linspace(0, 255, len(lums[0])))


mon = monitors.Monitor('labDell')
# 'matlab', 'psychopy', 'no_gamma'

# Matlab method
mon.setCurrent('matlab')
gammaGrid = []
with open('./gammaGrid.txt', 'rb') as f:
    for line in f:
        gammaGrid.append(map(float, line.rstrip().split('\t')))

mon.setDistance(40)
mon.setWidth(52)
mon.setSizePix([1920, 1200])
mon.setLevelsPre(levels)
mon.setLumsPre(lums)
mon.setLineariseMethod(4)
mon.setGammaGrid(gammaGrid)
mon.setNotes('matlab')


# Psychopy's method
mon.setCurrent('psychopy')
gammaGrid = []
for chan in lums:
    model = monitors.GammaCalculator(inputs = levels, lums = chan, eq = 4)
    gammaGrid.append([model.min, model.max, model.gamma, model.a, model.b, model.k])

mon.setDistance(40)
mon.setWidth(52)
mon.setSizePix([1920, 1200])
mon.setLevelsPre(levels)
mon.setLumsPre(lums)
mon.setLineariseMethod(4)
mon.setGammaGrid(gammaGrid)
mon.setNotes('psychopy')



# Get the spectra data
datafile = './spectra_data/spectra.csv'

wavelengths = []
power = []

with open(datafile, 'rb') as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if i == 0:
            print line
            continue
        line = map(float, line)
        wavelengths.append(line[0])
        power.append(line[1:])

wavelengths = np.array(wavelengths) # 1xN
power = np.transpose(power) # should be a 3xN matrix

dkl2rgb = monitors.makeDKL2RGB(wavelengths, power)
lms2rgb = monitors.makeLMS2RGB(wavelengths, power)

mon.setDKL2RGB(dkl2rgb)
mon.setLMS2RGB(lms2rgb)

mon.saveMon()


