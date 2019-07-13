from .calc_connors import calculateConnorsRSI
import numpy

# candles: {
#   close
#   open
#   low
#   high
#   bindex
#   sindex
#   green
# }

# if candles are tuple (reading from database)
Close = 0
Open = 1
Low = 2
High = 3
Bindex = 4
Sindex = 5
Green = 6

class MeanBIndex:
    def __init__(self, candles, lookback_period=100, period=3, isTuple=False):
        self.candles = candles
        
        afterBearsBIndex = []
        afterBearsGreenBIndex = []
        afterBearsRedBIndex = []

        if isTuple:
            self.closes = list(map(lambda candle: candle[Close], candles))
            self.connors = calculateConnorsRSI(self.closes, lookback_period, period)
            
            for i in range(1, len(self.connors)):
                candleIndex = i + (lookback_period - 1)
    
                if self.connors[i - 1] < 30:
                    bindex = self.candles[candleIndex][Bindex]
                    afterBearsBIndex.append(bindex)
                    if self.candles[candleIndex][Green]:
                        afterBearsGreenBIndex.append(bindex)
                    else:
                        afterBearsRedBIndex.append(bindex)
    
            self.afterBearsBIndex = afterBearsBIndex
            self.afterBearsGreenBIndex = afterBearsGreenBIndex
            self.afterBearsRedBIndex = afterBearsRedBIndex

        else:
            self.closes = map(lambda candle: candle.close, candles)
            self.connors = calculateConnorsRSI(self.closes, lookback_period, period)

            for i in range(1, len(self.connors)):
                candleIndex = i + (lookback_period - 1)

                if self.connors[i - 1] < 30:
                    bindex = self.candles[candleIndex].bindex
                    afterBearsBIndex.append(bindex)
                    if self.candles[candleIndex].green:
                        afterBearsGreenBIndex.append(bindex)
                    else:
                        afterBearsRedBIndex.append(bindex)

            self.afterBearsBIndex = afterBearsBIndex
            self.afterBearsGreenBIndex = afterBearsGreenBIndex
            self.afterBearsRedBIndex = afterBearsRedBIndex

    def calcMeanBIndex(self, n=13):
        return numpy.mean(self.afterBearsBIndex[-1 * n:])

    def calcMeanBIndexGreen(self, n=13):
        return numpy.mean(self.afterBearsGreenBIndex[-1 * n:])

    def calcMeanBIndexRed(self, n=13):
        return numpy.mean(self.afterBearsRedBIndex[-1 * n:])

    def takeProfit(self, buyPrice, n=13):
        return buyPrice * (1 + self.calcMeanBIndex(n))

    def takeProfitGreen(self, buyPrice, n=13):
        return buyPrice * (1 + self.calcMeanBIndexGreen(n))

    def takeProfitRed(self, buyPrice, n=13):
        return buyPrice * (1 + self.calcMeanBIndexRed(n))
