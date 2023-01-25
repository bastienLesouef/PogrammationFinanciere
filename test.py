import numpy as np
import numpy.random as sim
import matplotlib.pyplot as plt

T = 3
n = 1000
N = 10  # nombre de trajectoirs
pas = T / n  # detla ti

r0 = 0.04
a = 0.1
b = 0.02
lmbda = 0.12
B = [1]  # approximtion du ZC , on suppose que B0=1
interg = np.zeros((n + 1, N))
coeff = np.ones((n + 1, N))

r = np.ones((n + 1, N)) * r0

for j in range(N):
    for i in range(1, n + 1):
        r[i, j] = r[i - 1, j] + a * (b - r[i - 1, j]) * pas + lmbda * np.sqrt(pas) * sim.randn()
        interg[i, j] = pas * np.sum(r[:i - 1, j])
        coeff[i, j] = np.exp(-1 * interg[i, j])

for i in range(1, n + 1):
    b = np.mean(coeff[i, :])
    B.append(b)

dates = np.linspace(0, T, n + 1)  # n+1 dates
graph = plt.plot(dates, B)
plt.show()