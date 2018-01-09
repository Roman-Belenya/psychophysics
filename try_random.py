import numpy as np

np.random.seed(1)
for i in range(10):
    a = np.random.choice([0, 1], size = 2000, p = [0.2, 0.8])
    print (a == 1).sum() / float(len(a))