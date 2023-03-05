import services.stock_data
import pandas as pd
import os

os.makedirs("data/train", exist_ok=True)
os.makedirs("data/test", exist_ok=True)

timeframe = "1D"
symbols= ['TSLA', 'AMZN','AAPL','GOOG','ATVI','F']
start_times = ['2020-01-01T00:00:00Z','2015-12-15T00:00:00Z', '2016-02-14T00:00:00Z', '2017-12-25T00:00:00Z']
end = '2023-03-04T00:00:00Z'

train = True
for symbol in symbols:
    for start_time in start_times:
        df = pd.DataFrame(services.stock_data.get_historical_data(symbol, timeframe, start_time, end))
        if (train):
            df.to_csv("data/train/{symbol}-{timeframe}-{start}-{end}.csv".format(symbol=symbol, timeframe=timeframe, start=start_time, end=end))
        else:
            df.to_csv("data/test/{symbol}-{timeframe}-{start}-{end}.csv".format(symbol=symbol, timeframe=timeframe, start=start_time, end=end))
        train = not train

