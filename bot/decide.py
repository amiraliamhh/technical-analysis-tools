from calc_rsi import MeanBIndex

class Decider(MeanBIndex):
    def __init__(self, candles, buy_price, lookback_period=100, period=3, take_profit_period=13, isTuple=False):
        MeanBIndex.__init__(self, candles, lookback_period, period, isTuple)
        self.buy_price = buy_price
        self.take_profit_period = take_profit_period

    # -1 -> buy
    def decision(self):
        if self.connors[-1] < 30:
            return -1
        
        return self.takeProfit(self.buy_price, n=self.take_profit_period)
