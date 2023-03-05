import alpaca_trade_api as tradeapi
import time
import pandas as pd
import numpy as np
from services.stock_data import get_historical_data
import services

predicted_price = ()
symbol = get_historical_data[0]
timeframe = get_historical_data[1]
start = get_historical_data[2]
end = get_historical_data[3]

## alpaca account and buying power
account = tradeapi.get_account()

## current market price
barset = get_historical_data(symbol, 'day', limit=1)
stock_bars = barset[symbol]
current_price = stock_bars[0].c

## check funds
buying_power = float(account.buying_power)
total_stock = int(buying_power/current_price)

if total_stock > 0: 

    ## buy
    if predicted_price >= current_price:
        tradeapi.submit_order(
            symbol = symbol,
            qty = 1,
            side ='buy',
            type ='market',
            time_in_force ='gtc'
        )

    ## sell
    elif predicted_price < current_price:
        tradeapi.submit_order(
            symbol = symbol,
            qty = 1,
            side ='sell',
            type ='market',
            time_in_force ='gtc'
        )

    ## hold
    elif predicted_price == current_price:
        print("hold")

else:
    print("Insufficient Funds")