from calc_rsi import calculateRSI
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
