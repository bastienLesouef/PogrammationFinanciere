# cours 2: 11/05/2022
# simulation de mouvements browniens


import math
import numpy as np
import numpy.random as sim
import matplotlib.pyplot as plt

class BM:

    def __init__(self, T, nb_traj, nb_sub, sigma, mu):
        self.T = T
        self.N = nb_traj
        self.n = nb_sub
        self.sigma = sigma
        self.mu = mu
        self.B = np.zeros((self.n + 1, self.N))
        self.dates = np.linspace(0, self.T, self.n + 1)
        self.prices = np.zeros((self.n + 1, self.N)) + 100

        self.cal()
        self.graph()

    def cal(self):

        for j in range(self.N):
            for i in range(1, self.n + 1):
                self.B[i, j] = self.B[i-1, j] + np.sqrt(self.T/self.n) * sim.randn()
                self.prices[i, j] = \
                    self.prices[0, j] * math.exp(self.sigma * self.B[i, j] +
                                                 (self.mu - (self.sigma**2)/2)*(self.T/self.n)*i)

    def graph(self):

        plt.plot(self.dates, self.prices)
        plt.show()

    def hist_per(self, period):

        if 0 <= period <= self.T:
            plt.hist(self.prices[period, :])
            plt.show()

    def euler_schem(self):
        # modele de vol et modele de moyenne
        def g(t, x): return 10 / 100 * (1 + t / self.T + 1 / (1 + x ** 2))
        def m(t, x): return 3 / 100 * (2 + t / self.T + math.cos(2 * math.pi * t / self.T))
        # def
        st_mod = np.zeros((self.n + 1, self.N)) + 100
        for j in range(self.N):
            for i in range(1, self.n + 1):
                st_mod[i, j] = \
                    st_mod[i - 1, j] + \
                    g((self.T/self.n)*(i-1), st_mod[i - 1, j]) * st_mod[i - 1, j] * math.sqrt(self.T/self.n) * sim.randn() + \
                    m((self.T/self.n)*(i-1), st_mod[i - 1, j]) * st_mod[i - 1, j] * self.T/self.n

        plt.plot(self.dates, st_mod)
        plt.show()

        return st_mod





