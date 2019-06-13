import functools

# (i + 1) - i
def calcChanges(closePrices):
    changes = []
    for i in range(1, len(closePrices)):
        changes.append(closePrices[i] - closePrices[i - 1])
    return changes

def calcUpwardMovements(changes):
    movements = []
    for i in range(len(changes)):
        if changes[i] >= 0:
            movements.append(changes[i])
        else:
            movements.append(0)
    return movements

def calcDownwardMovements(changes):
    movements = []
    for i in range(len(changes)):
        if changes[i] <= 0:
            movements.append(abs(changes[i]))
        else:
            movements.append(0)
    return movements

def calcAvgUpwardOrDownward(changes, period=14):
    if period <= 0:
        raise Exception('period can\'t be equal to or lower than 0')

    avg = []
    if len(changes) < period:
        return None

    def sum(x, y):
        return x + y

    for i in range(period - 1, len(changes)):
        if len(avg) >= i - period and len(avg) >= 1:
            avg.append((avg[i - period] * 13 + changes[i]) / 14)
        else:
            sumOfChanges = functools.reduce(sum, changes[i - (period - 1):(i + 1)])
            avg.append(sumOfChanges / period)

    return avg

def calcRelativeStrength(avgUp, avgDown):
    if len(avgUp) != len(avgDown):
        raise Exception('length of average up and average down must be equal')

    relativeStrength = []

    for i in range(len(avgUp)):
        relativeStrength.append(avgUp[i] / avgDown[i])

    return relativeStrength

def calcRSI(relativeStrengths):
    rsis = []
    for i in range(len(relativeStrengths)):
        rsis.append(100 - (100 / (relativeStrengths[i] + 1)))

    return rsis

def calculateRSI(close_prices, period=14):
    changes = calcChanges(close_prices)

    upwards = calcUpwardMovements(changes)
    downwards = calcDownwardMovements(changes)

    avgUp = calcAvgUpwardOrDownward(upwards, period)
    avgDown = calcAvgUpwardOrDownward(downwards, period)

    relativeStrength = calcRelativeStrength(avgUp, avgDown)
    rsi = calcRSI(relativeStrength)

    return rsi
