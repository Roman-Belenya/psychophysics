import numpy as np
import csv
from psychopy import monitors

datafile = 'C:\Users\marotta_admin\Desktop\spectra.csv'

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

wavelengths = np.array(wavelengths)
print wavelengths.shape
# power = np.transpose(power)
power = np.transpose(power)
print power.shape

m = monitors.makeLMS2RGB(wavelengths, power)
print m
