from calc_rsi import calculateRSI
from simulation import simulate
from rest import requests
from fastapi import FastAPI

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
    charge = simulate(body.close_prices)
    return { "charge": charge }

