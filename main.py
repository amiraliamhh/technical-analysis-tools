import calc_rsi

CLOSE_PRICES = [
    16.66,
    16.85,
    16.93,
    16.98,
    17.08,
    17.030001,
    17.09,
    16.76,
    16.67,
    16.719999,
    16.860001,
    16.85,
    16.870001,
    16.9,
    16.92,
    16.860001,
    16.74,
    16.73,
    16.82,
]

changes = calc_rsi.calcChanges(CLOSE_PRICES)

upwards = calc_rsi.calcUpwardMovements(changes)
downwards = calc_rsi.calcDownwardMovements(changes)

avgUp = calc_rsi.calcAvgUpwardOrDownward(upwards)
avgDown = calc_rsi.calcAvgUpwardOrDownward(downwards)

avgUp2 = calc_rsi.calcAvgUpwardOrDownward2(upwards)
avgDown2 = calc_rsi.calcAvgUpwardOrDownward2(downwards)

relativeStrength = calc_rsi.calcRelativeStrength(avgUp, avgDown)
relativeStrength2 = calc_rsi.calcRelativeStrength(avgUp2, avgDown2)

rsis1 = calc_rsi.calcRSI(relativeStrength)
rsis2 = calc_rsi.calcRSI(relativeStrength2)

print(rsis1)
print(rsis2)
