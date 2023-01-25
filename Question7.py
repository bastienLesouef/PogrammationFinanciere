import math
import numpy as np
import numpy.random as sim
import matplotlib.pyplot as plt


class ComputePrice():
    #
    #   Use Varcisek rate model for pricing
    #
    def __init__(self, initial_price, maturity, nb_traj, nb_sub):
        self.p0 = initial_price
        self.T = maturity
        self.N = nb_traj
        self.n = nb_sub
        self.dates = np.linspace(0, self.T, self.n + 1)
        self.prices = np.zeros((self.n + 1, self.N)) + initial_price
        self.drift = math.sqrt(self.T/self.n)
        self.rate = np.zeros((self.n + 1, self.N)) + 1

    def vasicek(self, r, t1, t2, a, b, gamma):
        return r + a * (b - r)*(t2 - t1) + gamma * self.drift * sim.randn()

    def g(self, t, x):
        # modele de vol et modele de moyenne
        return 15 / 100 * (1 + math.sqrt(t) + (x + 1) / (1 + x ** 2))

    def prices_cal(self, a, b, gamma):
        """
        redef of monte carlo path generator
        :return: nothing
        """
        for j in range(self.N):
            st_act_price = self.p0
            rt = 0.04
            for i in range(1, self.n + 1):
                # we compute a variable for Wt that we will use for the next brownian
                wt = self.drift * sim.randn()
                # first we calculate the rt rate based on Vasicek rate model
                self.rate[i, j] = self.rate[i - 1, j] + rt * self.rate[i - 1, j] * (self.dates[i] - self.dates[i - 1])
                rt = rt + a * (b - rt)*(self.dates[i] - self.dates[i-1]) + gamma * wt

                # Now we calculate the actual price called st_act_price
                # it correspond to S tilde
                # we use g() that is the dynamic of sigma
                st_act_price = \
                    st_act_price + self.g(self.dates[i], st_act_price) * \
                    st_act_price * (1/3 * wt + 2/3 * self.drift * sim.randn())

                # we use the Vasicek rate model
                self.prices[i, j] = st_act_price * self.rate[i, j]

    def graph(self):
        plt.title('Simulation de Monte Carlo des prix St')
        plt.plot(self.dates, self.prices)
        plt.show()


class OptionPricing(ComputePrice):

    def __init__(self,initial_price, maturity, nb_traj, nb_sub):
        super().__init__(initial_price, maturity, nb_traj, nb_sub)

    def europ_payoff(self, final_price, middle_price):
        return max(middle_price - final_price, 0)

    def call(self, final_price, strike):
        return max(final_price - strike, 0)

    def european_price(self):
        """
        return the price of an european call
        :param strike: the strike
        :return: European call price
        """
        payoff = []
        for j in range(self.N):
            middle_price = self.prices[int(self.n/2), j]
            payoff.append(self.europ_payoff(self.prices[self.n, j], middle_price) / self.rate[self.n, j])

        return np.mean(payoff)

    def asian_call(self, strike):
        """ return the price of a call on average"""
        payoff = []
        for j in range(self.N):
            # the path average
            avg = np.mean(self.prices[:, j])
            payoff.append(self.call(avg, strike) / self.rate[self.n, j])

        return np.mean(payoff)



option = OptionPricing(30, 2, 1000, 100)
option.prices_cal(0.1, 0.02, 0.12)
european = option.european_price()

save = []
for i in range(5,60,5):
    asian = option.asian_call(i)
    save.append(asian)

print("european")
print(european)
print("asian")
print(save)
