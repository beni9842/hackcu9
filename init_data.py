import services.stock_data
import pandas as pd
import os

os.makedirs("data/train", exist_ok=True)
os.makedirs("data/test", exist_ok=True)

symbol = 'TSLA'
timeframe = '1min'
start = '2020-01-01T00:00:00Z'
end = '2022-03-01T00:00:00Z'

TSLA_data = pd.DataFrame(services.stock_data.get_historical_data(symbol, timeframe, start, end))
TSLA_data.to_csv("data/train/{symbol}-{timeframe}-{start}-{end}.csv".format(symbol=symbol, timeframe=timeframe, start=start, end=end))
