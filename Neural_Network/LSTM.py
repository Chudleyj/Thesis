import numpy as np
import pandas as pd
import talib
import random
import matplotlib.pyplot as plt
import math
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation

def create_dataset(dataset, look_back):
    dataX, dataY = [], []
    for i in range(look_back, len(dataset)):
        dataX.append(dataset[i-look_back:i,0])
        dataY.append(dataset[i,0])
    return np.array(dataX), np.array(dataY)

random.seed(17)
dataframe = pd.read_csv('DJI.csv', usecols=[0])
dataset = dataframe.values
dataset = dataset.astype('float32')

sc = MinMaxScaler(feature_range = (0,1))
dataset_scaled = sc.fit_transform(dataset)

# split into train and test sets
train_size = int(len(dataset_scaled) * 0.5)
test_size = len(dataset_scaled) - train_size
train, test = dataset_scaled[0:train_size,:], dataset_scaled[train_size:len(dataset),:]

look_back = 5
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))

model = Sequential()
model.add(LSTM(
               units = 50,
               return_sequences = True,
               input_shape = (trainX.shape[1], 1)))

model.add(Dropout(0.2))

model.add(LSTM(
               units = 100))

model.add(Dropout(0.2))

model.add(Dense(units = 1))
model.add(Activation('linear'))

model.compile(loss = 'mean_squared_error', optimizer = 'rmsprop')
model.fit(
          trainX,
          trainY,
          epochs = 100,
          batch_size = 1,
          verbose = 1,
          validation_split = 0.05)

trainScore = model.evaluate(trainX, trainY, verbose = 0)
print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore, math.sqrt(trainScore)))
testScore = model.evaluate(testX, testY, verbose=0)
print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore, math.sqrt(testScore)))

trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

trainPredict = sc.inverse_transform(trainPredict)
testPredict = sc.inverse_transform(testPredict)

# shift train predictions for plotting
trainPredictPlot = np.empty_like(dataset)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

# shift test predictions for plotting
testPredictPlot = np.empty_like(dataset)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(look_back*2):len(dataset)+1, :] = testPredict

# plot baseline and predictions
plt.plot(dataset, color = 'r', label = 'Actual Prices')
plt.plot(trainPredictPlot, 'b', label = 'Training Data Predictions')
plt.plot(testPredictPlot, 'g', label = 'Test Data Predictions')
plt.title('Dow Jones Neural Network Predictions')
plt.xlabel('Year')
plt.ylabel('Price ($USD)')
plt.legend()
plt.show()


