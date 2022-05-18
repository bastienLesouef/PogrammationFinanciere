# cours 3: 18/05/2022
# Option pricing with vasicek rate model OptionPricingRateModel
# Option pricing without rate model OptionPricing

import math
import numpy as np
import numpy.random as sim


class OptionPricing:

    def __init__(self, initial_price, riskless, maturity, nb_traj, nb_sub):
        self.r = riskless
        self.p0 = initial_price
        self.T = maturity
        self.N = nb_traj
        self.n = nb_sub
        self.dates = np.linspace(0, self.T, self.n + 1)
        self.prices = np.zeros((self.n + 1, self.N)) + initial_price

    def g(self, t, x):
        # modele de vol et modele de moyenne
        return 5 / 100 * (1 + t / self.T + 1 / (1 + x ** 2))

    def call(self, final_price, strike):
        return max(final_price - strike, 0)

    def prices_cal(self):
        for j in range(self.N):
            st_act_price = self.p0
            for i in range(1, self.n + 1):
                # first we calculate the actual price called st_act_price
                st_act_price = \
                    st_act_price + self.g(self.dates[i], st_act_price) * \
                    st_act_price * math.sqrt(self.T/self.n) * sim.randn()

                self.prices[i, j] = st_act_price * math.exp(self.r * self.dates[i])

    def european_call(self, strike):
        """ return the price of an european call"""
        payoff = []
        for j in range(self.N):
            payoff.append(self.call(self.prices[self.n, j], strike) * math.exp(- self.r * self.T))

        return np.mean(payoff)

    def call_average(self, strike):
        """ return the price of a call on average"""
        payoff = []
        for j in range(self.N):
            # the path average
            avg = np.mean(self.prices[:, j])
            payoff.append(self.call(avg, strike) * math.exp(- self.r * self.T))

        return np.mean(payoff)


class OptionPricingRateModel(OptionPricing):
    #
    #   Use Varcisek rate model for pricing
    #
    def __init__(self, initial_price, riskless, maturity, nb_traj, nb_sub):
        super().__init__(initial_price, riskless, maturity, nb_traj, nb_sub)
        self.rate = np.zeros((self.n + 1, self.N)) + 1

    def vasicek(self, r, t1, t2, a, b, gamma):
        return r + a * (b - r)*(t2 - t1) + gamma * math.sqrt(self.T/self.n) * sim.randn()

    def compute_rate(self, a, b, gamma):
        """
        function that compute the 'rate' vector
        based on vasicek rate model
        :param a: parameter
        :param b: parameter
        :param gamma: parameter
        :return: return nothing.
        """
        for j in range(self.N):
            # initial value
            rt = 0.01
            for i in range(1, self.n + 1):
                r0 = self.vasicek(rt, self.dates[i], self.dates[i - 1], a, b, gamma)
                self.rate[i, j] = self.rate[i - 1, j] + rt * self.rate[i - 1, j] * (self.dates[i] - self.dates[i - 1])

    def prices_cal(self):
        """
        redef of monte carlo path generator
        :return: nothing
        """
        for j in range(self.N):
            st_act_price = self.p0
            for i in range(1, self.n + 1):
                # first we calculate the actual price called st_act_price
                st_act_price = \
                    st_act_price + self.g(self.dates[i], st_act_price) * \
                    st_act_price * math.sqrt(self.T/self.n) * sim.randn()

                # we use the Vasicek rate model
                self.prices[i, j] = st_act_price * self.rate[i, j]

    def european_call(self, strike):
        """ return the price of an european call"""
        payoff = []
        for j in range(self.N):
            payoff.append(self.call(self.prices[self.n, j], strike) * self.rate[self.n, j])

        return np.mean(payoff)

    def call_average(self, strike):
        """ return the price of a call on average"""
        payoff = []
        for j in range(self.N):
            # the path average
            avg = np.mean(self.prices[:, j])
            payoff.append(self.call(avg, strike) * self.rate[self.n, j])

        return np.mean(payoff)