from calc_rsi import calculateRSI, calculateConnorsRSI
from rest import requests
from fastapi import FastAPI
import simulation

app = FastAPI()

@app.get('/sanity')
def sanity():
    return { 'msg': 'success' }

@app.post('/calculate-rsi')
def calculate_rsi(body: requests.CalculateRSIParams):
    rsi = calculateRSI(body.close_prices)
    return { "data": rsi }

@app.post('/simulate')
def simulateTrade(body: requests.CalculateRSIParams):
    s = simulation.Simulate(body.close_prices, 14, 70, 30)
    charge = s.simulate()
    return { "charge": charge }

@app.post('/calculate-connors')
def calcStreaks(body: requests.CalculateConnorsRSIParams):
    return { "data": calculateConnorsRSI(body.close_prices, period=body.period, lookbackPeriod=body.lookback_period) }
