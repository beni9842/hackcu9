import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

# Load data
df = pd.read_csv('data/train/AAPL-1D-2016-02-14T00:00:00Z.csv').loc[:,['close']]

# Preprocess data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df.values.reshape(-1, 1))

# Split data into training and testing sets
training_data_len = int(np.ceil(len(scaled_data) * 0.8))
train_data = scaled_data[0:training_data_len, :]
x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# Build model
model = Sequential()
model.add(LSTM(units=50, activation='relu', return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, activation='relu', return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))

# Compile model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train model
model.fit(x_train, y_train, epochs=100, batch_size=32)

# Test model
test_data = scaled_data[training_data_len - 60:, :]
x_test = []
y_test = df['close'][training_data_len:].values

for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# Evaluate model
rmse = np.sqrt(np.mean((predictions - y_test)**2))
print(rmse)


# Plot the results
import matplotlib.pyplot as plt
plt.plot(y_test)
plt.plot(predictions[:,0])
plt.legend(['Actual', 'Predicted'])
plt.show()