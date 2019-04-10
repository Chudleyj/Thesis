import numpy as np
import pandas as pd
import talib
import random
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

random.seed(17)

col_names = ['dates','prices']
# load dataset
dataset = pd.read_csv("DJI2.csv", header=None, names=col_names)
dataset.drop('dates', axis=1, inplace=True)
dataset['3day MA'] = dataset['prices'].shift(1).rolling(window = 3).mean()
dataset['10day MA'] = dataset['prices'].shift(1).rolling(window = 10).mean()
dataset['30day MA'] = dataset['prices'].shift(1).rolling(window = 30).mean()
dataset['Std_dev']= dataset['prices'].rolling(5).std()
dataset['RSI'] = talib.RSI(dataset['prices'].values, timeperiod = 9)
dataset['Price_Rise'] = np.where(dataset['prices'].shift(-1) > dataset['prices'], 1, 0)
dataset = dataset.dropna()

X = dataset.iloc[:,4:-1]
y = dataset.iloc[:,-1]

split = int(len(dataset)*0.9) #train on x % of data
X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

output_data = MinMaxScaler(feature_range=(0,1))
y_train = output_data.fit_transform(y_train.values.reshape(-1,1))
y_test = output_data.fit_transform(y_test.values.reshape(-1,1))

classifier = Sequential()

classifier.add(Dense(units = 128, kernel_initializer = 'uniform', activation = 'relu', input_dim = X.shape[1]))
classifier.add(Dropout(0.2))
classifier.add(Dense(units = 128, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dropout(0.2))
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))

classifier.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ['accuracy'])

classifier.fit(X_train, y_train, batch_size = 10, epochs = 100)

y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)
n_pred = output_data.inverse_transform(y_pred)

dataset['n_pred'] = np.NaN
dataset.iloc[(len(dataset) - len(n_pred)):,-1:] = n_pred
trade_dataset = dataset.dropna()

trade_dataset['Tomorrows Returns'] = 0.
trade_dataset['Tomorrows Returns'] = np.log(trade_dataset['prices']/trade_dataset['prices'].shift(1))
trade_dataset['Tomorrows Returns'] = trade_dataset['Tomorrows Returns'].shift(-1)

trade_dataset['Strategy Returns'] = 0.
trade_dataset['Strategy Returns'] = np.where(trade_dataset['n_pred'] == True, trade_dataset['Tomorrows Returns'], - trade_dataset['Tomorrows Returns'])

trade_dataset['Cumulative Market Returns'] = np.cumsum(trade_dataset['Tomorrows Returns'])
trade_dataset['Cumulative Strategy Returns'] = np.cumsum(trade_dataset['Strategy Returns'])


plt.figure(figsize=(10,5))
plt.plot(trade_dataset['Cumulative Market Returns'], color='r', label='Market Returns')
plt.plot(trade_dataset['Cumulative Strategy Returns'], color='g', label='Strategy Returns')
plt.legend()
plt.show()

