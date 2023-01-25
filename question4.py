import math
import numpy as np
import numpy.random as sim
import matplotlib.pyplot as plt

T = 2
n = 10
N = 100

dates = np.linspace(0, T, n + 1)
pas = T/n
rate = np.zeros((n + 1, N)) + 0.04

B = [1]
interg = np.zeros((n + 1, N))
coeff = np.ones((n + 1, N))

a = 0.1
b = 0.02
gamma = 0.12


def vasicek(r, t1, t2, a, b, gamma):
    return r + a * (b - r) * (t2 - t1) + gamma * math.sqrt(pas) * sim.randn()


for j in range(N):
    for i in range(1, n + 1):
        rate[i, j] = vasicek(rate[i - 1, j], dates[i-1], dates[i], a, b, gamma)
        interg[i, j] = pas * np.sum(rate[: i - 1, j])
        coeff[i, j] = np.exp(- 1 * interg[i, j])


for i in range(1, n + 1):
    b = np.mean(coeff[i, :])
    B.append(b)

graph = plt.plot(dates, B)
plt.show()
