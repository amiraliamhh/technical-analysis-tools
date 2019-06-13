from calc_rsi import calculateRSI

class Simulate:
    def __init__(self, close_prices, period=14, overbought=70, oversell=30):
        self.close_prices = close_prices
        self.period = period
        self.overbought = overbought
        self.oversell = oversell
        self.charge = 1000 / close_prices[0]
        self.chargeInStable = 0
        self.rsi = calculateRSI(close_prices)

    def sell(self, index):
        indexOfClosePrice = index + self.period
        self.chargeInStable = self.charge * self.close_prices[indexOfClosePrice]
        self.charge = 0

    def buy(self, index):
        indexOfClosePrice = index + self.period
        self.charge = self.chargeInStable / self.close_prices[indexOfClosePrice]
        self.chargeInStable = 0

    def simulate(self):
        for i in range(len(self.rsi)):
            if self.rsi[i] > 70 and self.charge > 0:
                self.sell(i)

            elif self.rsi[i] < 30 and self.chargeInStable > 0:
                self.buy(i)

        chargeInStable = self.chargeInStable
        if chargeInStable == 0:
            chargeInStable = self.charge * self.close_prices[-1]
        
        return chargeInStable
