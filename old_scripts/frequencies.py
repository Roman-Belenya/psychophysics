import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

x = np.linspace(0, 60, 120)

hz60 = [0, 1] * 60
hz30 = [2,2,3,3] * 30
hz20 = [4,4,4,5,5,5] * 20
hz15 = [6,6,6,6,7,7,7,7] * 15
hz10 = [8,8,8,8,8,8,9,9,9,9,9,9] * 10

plt.plot(x, hz60, '.-', label = '60 Hz')
plt.plot(x, hz30, '.-', label = '30 Hz')
plt.plot(x, hz20, '.-', label = '20 Hz')
plt.plot(x, hz15, '.-', label = '15 Hz')
plt.plot(x, hz10, '.-', label = '10 Hz')

plt.grid(True, which='both')
plt.minorticks_on()
plt.legend()
plt.yticklabels = []

plt.show()