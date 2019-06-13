from pydantic import BaseModel
from typing import List

ClosePrices = List[float]

class CalculateRSIParams(BaseModel):
    close_prices: ClosePrices
    period: int

class CalculateConnorsRSIParams(CalculateRSIParams):
    lookback_period: int
