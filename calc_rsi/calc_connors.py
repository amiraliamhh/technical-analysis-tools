from .calc_rsi import calcChanges, calcDownwardMovements, calcUpwardMovements, calcAvgUpwardOrDownward, calcRelativeStrength, calcRSI, calculateRSI

def calcStreak(close_prices=[]):
    changes = calcChanges(close_prices)
    streaks = []
    for i in range(len(changes)):
        if changes[i] == 0:
            streaks.append(0)
        elif changes[i] > 0:
            if len(streaks) > 0 and streaks[i - 1] > 0:
                streaks.append(streaks[i - 1] + 1)
            else:
                streaks.append(1)
        else:
            if len(streaks) > 1 and streaks[i - 1] < 0:
                streaks.append(streaks[i - 1] - 1)
            else:
                streaks.append(-1)

    return streaks

def calculateStreakRSI(close_prices, period=14):
    streaks = calcStreak(close_prices)

    streakChanges = [streaks[0]] + calcChanges(streaks)

    upwards = calcUpwardMovements(streakChanges)
    downwards = calcDownwardMovements(streakChanges)

    avgUp = calcAvgUpwardOrDownward(upwards, period)
    avgDown = calcAvgUpwardOrDownward(downwards, period)

    relativeStrength = calcRelativeStrength(avgUp, avgDown)
    rsi = calcRSI(relativeStrength)

    return rsi

def calculateDailyReturn(close_prices):
    dailyReturn = []
    for i in range(1, len(close_prices)):
        dailyReturn.append((close_prices[i] - close_prices[i - 1]) / close_prices[i - 1])

    return dailyReturn

def calculateRelativeMagnitude(dailyReturns=[], lookbackPeriod=100):
    if len(dailyReturns) <= lookbackPeriod:
        return []

    relativeMagnitude = []
    for i in range(lookbackPeriod, len(dailyReturns)):
        count = 0
        for j in range(i - lookbackPeriod, i):
            if dailyReturns[j] > dailyReturns[i]:
                count += 1
        relativeMagnitude.append(((lookbackPeriod - count) / lookbackPeriod) * 100)

    return relativeMagnitude

def calculateConnorsRSI(close_prices=[], lookbackPeriod=100, period=3):
    dailyReturn = calculateDailyReturn(close_prices)
    
    relativeMagnitude = calculateRelativeMagnitude(dailyReturn, lookbackPeriod)
    calculatedRSI = calculateRSI(close_prices, period)
    rsi = calculatedRSI[lookbackPeriod - (period - 1):]
    calculatedStreakRSI = calculateStreakRSI(close_prices, period)
    streakRSI = calculatedStreakRSI[lookbackPeriod - (period - 1):]

    connors = []

    for i in range(len(close_prices) - (lookbackPeriod + 1)):
        connors.append((relativeMagnitude[i] + rsi[i] + streakRSI[i]) / 3)

    return connors
