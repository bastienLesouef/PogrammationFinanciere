import math
import numpy as np
import numpy.random as sim

T = 2
n = 10
N = 100

dates = np.linspace(0, T, n + 1)
pas = math.sqrt(T/n)
rate = np.zeros((n + 1, N)) + 0.04


def vasicek(r, t1, t2, a, b, gamma):
    return r + a * (b - r) * (t2 - t1) + gamma * pas * sim.randn()


def compute_rate(a, b, gamma):
    """
    function that compute the 'rate' vector
    based on vasicek rate model
    :param a: parameter
    :param b: parameter
    :param gamma: parameter
    :return: return nothing.
    """
    for j in range(N):
        for i in range(1, n + 1):
            rate[i, j] = vasicek(rate[i - 1, j], dates[i-1], dates[i], a, b, gamma)

    return rate


