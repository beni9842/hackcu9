import alpaca_trade_api as tradeapi
import numpy as np
import os

# authentication and connection details
api_key = 'PKNEGEAAV0HAW889927M'
api_secret = 'xJlJJ8j8Sqo7WttLoz8YNV5qOjUt5zixKdtYrdva'
base_url = 'https://paper-api.alpaca.markets'

# instantiate REST API
v2 = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# obtain account information
account = v2.get_account()
print(account)

def get_historical_data(symbol, timeframe, start, end, limit=1000):
    bars = v2.get_bars(symbol, timeframe, start=start, end=end, limit=limit)
    data = []
    for bar in bars:
        data.append({
            'timestamp': bar.t,
            'open': bar.o,
            'high': bar.h,
            'low': bar.l,
            'close': bar.c,
            'volume': bar.v
        })
    return data

