from calc_rsi import calculateRSI

# TODO: make it a class
def simulate(close_prices, period=14):
    rsi = calculateRSI(close_prices)
    chargeInStable = 1000
    charge = chargeInStable / close_prices[0]
    chargeInStable = 0 
    
    def sell(index, cs, c):
        indexOfClosePrice = index + period
        cs = c * close_prices[indexOfClosePrice]
        return cs

    def buy(index, cs, c):
        indexOfClosePrice = index + period
        c = cs / close_prices[indexOfClosePrice]
        return c

    for i in range(len(rsi)):
        if rsi[i] > 70 and charge > 0:
            chargeInStable = sell(i, chargeInStable, charge)
            charge = 0

        elif rsi[i] < 30 and chargeInStable > 0:
            charge = buy(i, chargeInStable, charge)
            chargeInStable = 0

    if chargeInStable == 0:
        chargeInStable = charge * close_prices[-1]

    return chargeInStable
