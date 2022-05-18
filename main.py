from Cours2 import BM
from Cours3 import OptionPricing, OptionPricingRateModel

if __name__ == '__main__':
    opt = OptionPricingRateModel(25, 0.02, 5, 5000, 1000)
    opt.compute_rate(0.3, 0.02, 0.04)
    opt.prices_cal()
    price0 = opt.european_call(10)
    print(price0)
    price1 = opt.call_average(10)
    print(price1)