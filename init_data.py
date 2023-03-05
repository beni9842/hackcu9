import services.stock_data
import pandas as pd
import os


os.makedirs("data/prices", exist_ok=True)
#os.makedirs("data/test", exist_ok=True)

time = "1D"
start = '2017-10-17T00:00:00Z'
end = '2023-03-04T00:00:00Z'





tsla = pd.DataFrame(services.stock_data.get_prices('TSLA', time, start, end))
tsla.to_csv('data/prices/tsla.csv')
atvi = pd.DataFrame(services.stock_data.get_prices('ATVI', time, start, end))
atvi.to_csv('data/prices/atvi.csv')
f =  pd.DataFrame(services.stock_data.get_prices('F', time, start, end))
f.to_csv('data/prices/f.csv')
