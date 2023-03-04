import services.stock_data
import pandas as pd
import os

os.makedirs("data/train", exist_ok=True)
os.makedirs("data/test", exist_ok=True)

# 01/01/20, 1/12/15-1/15/15, 3/1/21-3/3/21, 2/14/23,  12/25/17
# 2020-01-01T00:00:00Z, 2015-12-15T00:00:00Z, 2021-03-01T00:00:00Z , 2023-02-14T00:00:00Z, 2017-12-25T00:00:00Z
symbol = 'TSLA'
timeframe = '1min'
start = '2020-01-01T00:00:00Z'
end = '2022-03-01T00:00:00Z'

TSLA_data = pd.DataFrame(services.stock_data.get_historical_data(symbol, timeframe, start, end))
TSLA_data.to_csv("data/train/{symbol}-{timeframe}-{start}-{end}.csv".format(symbol=symbol, timeframe=timeframe, start=start, end=end))

symbols= ['TSLA', 'AMZN','APPL','GOOG','ATVI','F','BRK-B']
start_times = ['2020-12-01T00:00:00Z','2015-12-15T00:00:00Z', '2021-03-01T00:00:00Z', '2023-02-14T00:00:00Z', '2017-12-25T00:00:00Z']
end = '2022-03-01T00:00:00Z'

dfs = []
for symbols in stickers:
    df = pd.DataFrame(services.stock_data.get_historical_data(symbol, timeframe, start, end))
    dfs.append(df)

result = pd.concat(dfs)
result.to_csv('historical_stock_data.csv', index=False)

