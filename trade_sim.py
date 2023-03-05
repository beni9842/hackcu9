import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the asset and time period to retrieve data for

# Retrieve historic data for the asset

# Define the initial portfolio balance and trade size

def dca(prices, n_buys=25, n_shares=0, portfolio_balance=100000):
    trade_interval = len(prices) / n_buys
    for i in range(len(prices)):
        if i % trade_interval == 0:
            today = prices[i]
            if (portfolio_balance > today):
                portfolio_balance -= today
                n_shares += 1
    final_price = prices[-1]
    portfolio_balance += n_shares * final_price
    return portfolio_balance

def get_critical_numbers(arr):
    
    ##Returns a NumPy array containing the critical numbers of the input array.
    critical_numbers = np.array([], dtype=int)
    
    for i in range(1, len(arr)-1):
        if (arr[i] < arr[i-1]) and (arr[i] < arr[i+1]):
            critical_numbers = np.append(critical_numbers, i)
        elif (arr[i] > arr[i-1]) and (arr[i] > arr[i+1]):
            critical_numbers = np.append(critical_numbers, i)

    return critical_numbers

def predict_buy(prices, predictions, n_shares=0, portfolio_balance=100000, risk=2):
    critical_days = get_critical_numbers(predictions)
    for i in range(len(prices)):
        if i in critical_days:
            today = prices[i]
            next_critical_day = int(np.where(critical_days==i)[0]) + 1
            next_critical_price = predictions[next_critical_day]
            if next_critical_price > today:
                buy_amount = min(portfolio_balance, (next_critical_price - today)**risk)
                if (portfolio_balance >= buy_amount):
                    portfolio_balance -= buy_amount
                    n_shares += buy_amount / today
            elif next_critical_price < today:
                sell_amount = min(n_shares*today, (today - next_critical_price)*risk)
                portfolio_balance += sell_amount
                n_shares -= sell_amount / today
    final_price = prices[-1]
    portfolio_balance += n_shares * final_price
    return portfolio_balance

tsla = pd.read_csv('data/prices/tsla.csv')['close'].values[800:]
atvi = pd.read_csv('data/prices/atvi.csv')['close'].values[800:]

datasets = [('tsla', tsla), ('atvi', atvi)]
for symbol, prices in datasets:
    prices = pd.read_csv('data/prices/{symbol}.csv'.format(symbol=symbol))['close'].values[800:]

    pred = pd.read_csv("data/pred/{symbol}.csv".format(symbol=symbol))['0'].values
    real = prices

    bal = 100000
    n_shares = 0
    print(dca(prices=prices, portfolio_balance=bal, n_shares=n_shares, n_buys=25))
    print(predict_buy(prices=prices, predictions=pred, portfolio_balance=bal, n_shares=n_shares, risk=2))

# plt.plot(real)
# plt.plot(pred)
# plt.legend(['Actual', 'Predicted'])
# plt.show()