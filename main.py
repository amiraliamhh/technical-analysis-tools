from calc_rsi import calculateRSI, calculateConnorsRSI
from starlette.middleware.cors import CORSMiddleware
from rest import requests
from fastapi import FastAPI
import simulation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/sanity')
def sanity():
    return { 'msg': 'success' }

@app.post('/calculate-rsi')
def calculate_rsi(body: requests.CalculateRSIParams):
    rsi = calculateRSI(body.close_prices, body.period)
    return { "data": rsi }

@app.post('/calculate-connors')
def calcStreaks(body: requests.CalculateConnorsRSIParams):
    return { "data": calculateConnorsRSI(body.close_prices, period=body.period, lookbackPeriod=body.lookback_period) }

@app.post('/simulate-rsi')
def simulateTrade(body: requests.CalculateRSIParams):
    s = simulation.Simulate(body.close_prices, 14, 70, 30)
    charge = s.simulateBasedOnRSI()
    return { "charge": charge }

@app.post('/simulate-connors')
def simulateTradeConnors(body: requests.CalculateConnorsRSIParams):
    s = simulation.Simulate(body.close_prices, 3, 70, 30)
    charge = s.simulateBasedOnConnors()
    return { "charge": charge }
