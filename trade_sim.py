import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Define the asset and time period to retrieve data for

# Retrieve historic data for the asset

# Define the initial portfolio balance and trade size

def dca(prices, n_buys=25, n_shares=0, portfolio_balance=100000):
    trade_interval = len(prices) / n_buys
    assets = np.array([])
    equidy = np.array([])
    for i in range(len(prices)):
        if i % trade_interval == 0:
            today = prices[i]
            if (portfolio_balance > today):
                portfolio_balance -= today
                n_shares += 1
        assets= np.append(assets, n_shares * today)
        equidy = np.append(equidy, portfolio_balance)
    return pd.DataFrame({'assets':assets, 'equidy':equidy, 'value':np.array(assets + equidy)})

def get_critical_numbers(arr):
    
    ##Returns a NumPy array containing the critical numbers of the input array.
    critical_numbers = np.array([], dtype=int)
    
    for i in range(1, len(arr)-1):
        if (arr[i] < arr[i-1]) and (arr[i] < arr[i+1]):
            critical_numbers = np.append(critical_numbers, i)
        elif (arr[i] > arr[i-1]) and (arr[i] > arr[i+1]):
            critical_numbers = np.append(critical_numbers, i)

    return critical_numbers

from sklearn.preprocessing import MinMaxScaler



def predict_buy(prices, predictions, n_shares=0, portfolio_balance=100000):
    scaler = MinMaxScaler()
    scaled_predictions = scaler.fit_transform(predictions.reshape(-1, 1))

    critical_days = get_critical_numbers(scaled_predictions)
    assets = np.array([])
    equidy = np.array([])
    for i in range(len(prices)):
        today = prices[i]
        if i in critical_days:
            critical_day = np.where(critical_days==i)[0]
            critical_price = scaled_predictions[i]
            if (critical_day != len(prices)-1):
                next_critical_day = critical_day + 1
                next_critical_price = scaled_predictions[next_critical_day]
                if next_critical_price > critical_price:
                    buy_amount = min(portfolio_balance * .9, portfolio_balance * ((next_critical_price - critical_price) * today))
                    portfolio_balance -= buy_amount
                    n_shares += buy_amount / today
                elif next_critical_price < critical_price:
                    sell_amount = min(n_shares * today, n_shares * ((critical_price - next_critical_price) * today))
                    portfolio_balance += sell_amount
                    n_shares -= sell_amount / today
        assets = np.append(assets, n_shares * today)
        equidy = np.append(equidy, portfolio_balance)

    return pd.DataFrame({'assets':assets, 'equidy':equidy, 'value':np.array(assets + equidy)})

tsla = pd.read_csv('data/prices/tsla.csv')['close'].values[800:]
atvi = pd.read_csv('data/prices/atvi.csv')['close'].values[800:]
f = pd.read_csv('data/prices/f.csv')['close'].values[800:]

datasets = [('tsla', tsla), ('atvi', atvi), ('f', f)]
for symbol, prices in datasets:

    pred = pd.read_csv("data/pred/{symbol}.csv".format(symbol=symbol))['0'].values
    real = prices

    bal = 10000
    n_shares = 0
    
    dca_financials = dca(prices=prices, portfolio_balance=bal, n_shares=n_shares, n_buys=25)
    pca_financials = predict_buy(prices=prices, predictions=pred, portfolio_balance=bal, n_shares=n_shares)

    print("dca {symbol} -> ${val}".format(symbol=symbol, val=dca_financials['value'].values[-1]))
    print("pca {symbol} -> ${val}".format(symbol=symbol, val=pca_financials['value'].values[-1]))

    plt.plot(dca_financials['value'])
    # plt.plot(dca_financials['equidy'])
    # plt.plot(dca_financials['assets'])

    plt.plot(pca_financials['value'])
    # plt.plot(pca_financials['equidy'])
    # plt.plot(pca_financials['assets'])
    # 

    plt.legend(['dca value', 'pca value'])
    os.makedirs("data/img/", exist_ok=True)
    plt.savefig("data/img/{symbol}-fin.png".format(symbol=symbol))
    plt.close()

# plt.plot(real)
# plt.plot(pred)
# plt.legend(['Actual', 'Predicted'])
# plt.show()