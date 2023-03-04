import numpy as np
from random import randint
from sklearn.preprocessing import MinMaxScaler
from services.stock_data import get_historical_data
import alpaca_trade_api as tradeapi
import pandas as pd


def scale_data(symbol, timeframe, start, end):

    ## reading the historical data into a pandas frame
    start_date = pd.Timestamp(start)
    end_date = pd.Timestamp(end)
    bars = get_historical_data(symbol, timeframe, start=start_date, end=end_date)
    df = pd.DataFrame(bars)
    data = df['close'].values

    ## robust scaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.reshape(-1, 1))

    return scaled_data.flatten()

symbol = 'TSLA'
timeframe = '1min'
start = '2020-01-01T00:00:00Z'
end = '2022-03-01T00:00:00Z'
scaled_data = scale_data(symbol, timeframe, start, end)

print(scaled_data)
