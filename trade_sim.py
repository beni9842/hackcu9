import pandas as pd
import numpy as np

# Define the asset and time period to retrieve data for
symbol = 'AAPL'
start = '2020-01-01'
end = '2020-12-31'

# Retrieve historic data for the asset
prices = pd.read_csv('data/train/ATVI-1D-2016-02-14T00:00:00Z.csv')['close'].values[800:]

# Define the initial portfolio balance and trade size
portfolio_balance = 1000000
n_shares = 0

def dca(n_buys=25, n_shares=0, portfolio_balance=100000):
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

def predict_buy(predictions, n_shares=0, portfolio_balance=100000, risk=10):
    critical_days = get_critical_numbers(predictions)
    for i in range(len(prices)):
        if i in critical_days:
            today = prices[i]
            next_critical_day = int(np.where(critical_days==i)[0]) + 1
            next_critical_price = predictions[next_critical_day]
            if next_critical_price > today:
                buy_amount = (next_critical_price - today)**risk
                if (portfolio_balance > buy_amount):
                    portfolio_balance -= buy_amount
                    n_shares += buy_amount / today
    final_price = prices[-1]
    portfolio_balance += n_shares * final_price
    return portfolio_balance

print(dca())
predictions = pd.read_csv("data/pred.csv")['0'].values
print(predict_buy(predictions=predictions))

# Plot the results
import matplotlib.pyplot as plt
plt.plot(prices)
plt.plot(predictions)
plt.legend(['Actual', 'Predicted'])
plt.show()