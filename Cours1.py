# -*- coding: utf-8 -*-

# Packages
import numpy as np
import numpy.random as sim
import matplotlib.pyplot as plt

# Parameters
N = 100000


def InvFx(u):
    if u < 0:
        y = None
    elif u <= 1 / 4:
        y = 1
    elif u <= 5 / 8:
        y = 2
    elif u <= 6 / 8:
        y = 3
    elif u > 6 / 8:
        y = 4

    return y


# Simulate some u values
U = [sim.uniform(0, 1) for i in range(N)]
X = [InvFx(x) for x in U]

# Frequencies
freq = np.arange(0, 4, dtype=float)
for i in range(1, 5):
    l = [x for x in X if x == i]
    freq[i - 1] = len(l) / N

# Histogram
ax = np.arange(1, 5)
plt.bar(ax, freq, color='lightcoral')
plt.title('Empirical Distribution')
plt.show()

# Exponential inverse
lambd = 2


def InvFy(u):
    if u <= 0:
        u = 1 / 2
    return -1 / lambd * np.log(u)


V = [sim.uniform(0, 1) for i in range(N)]
Y = [InvFy(y) for y in V]
Z = [y ** x for x, y in zip(X, Y)]
E = np.mean(Z)
