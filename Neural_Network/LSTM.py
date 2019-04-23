import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation

class portfolio:
    def __init__(self, bank = 10000, stocksOwned = 0, profits = 0):
        self.bank = bank
        self.stocksOwned = stocksOwned
        self.assets = bank
        self.profits = 0
    
    def executeAction(self, action, price):
        if action: #Buy
            self.stocksOwned += 1
            self.bank -= price
            self.assets = self.bank + (price * self.stocksOwned)
        
        else: #Sell
            self.stocksOwned -= 1
            self.bank  += price
            self.assets = self.bank + (price * self.stocksOwned)

    def calcProfits(self):
        self.profits = self.assets-10000
        self.profits = np.round(self.profits,2)
        self.profits = str(self.profits)
        self.profits += "\n"

    def chooseAction(self, predicted, y): #Returns true if predicted value n is an increase over y @ n-1, else returns false
        return predicted > y

def generateDataSet():
    df = pd.read_csv('DJI2.csv', usecols=[0])
    df = df.values
    return (df.astype('float32'))

def generateTrainTestData(df, splitSize): # split into train and test sets
    train_size = int(len(df) * splitSize)
    test_size = len(df) - train_size
    return (dataset_scaled[0:train_size,:], dataset_scaled[train_size:len(dataset),:])

def create_dataset(dataset, look_back):
    dataX, dataY = [], []
    for i in range(look_back, len(dataset)):
        dataX.append(dataset[i-look_back:i,0])
        dataY.append(dataset[i,0])
    return np.array(dataX), np.array(dataY)

def configureLSTMnetwork(numLayers, numUnits, dropoutVal=None,activationType=None):
                         
     model = Sequential()
     for i in range(0, numLayers-1):
         model.add(LSTM(
                        units = numUnits[i],
                        return_sequences = True,
                        input_shape = (trainX.shape[1], 1)))
         if dropoutVal is not None:
             model.add(Dropout(dropoutVal))
                         
     model.add(LSTM(
                    units = numUnits[-1]))
                         
     if dropoutVal is not None:
         model.add(Dropout(dropoutVal))
     
     model.add(Dense(units = 1))
     
     if activationType is not None:
         model.add(Activation(activationType))
     else:
         model.add(Activation('linear'))
     
     return model

def runLSTMnetwork(model, trainX, trainY, numEpochs, numBatch,lossType = None, optimizerType = None, validationSize = None):
    if lossType is not None:
        if optimizerType is not None:
            model.compile(loss = lossType, optimizer = optimizerType)
        else:
            model.compile(loss = lossType, optimizer = 'rmsprop')

    else:
        if optimizerType is not None:
            model.compile(loss = 'mean_squared_error', optimizer = optimizerType)
        else:
            model.compile(loss = 'mean_squared_error', optimizer = 'rmsprop')
                    
        if validationSize is not None:
            model.fit(
                      trainX,
                      trainY,
                      epochs = numEpochs,
                      batch_size = numBatch,
                      verbose = 1,
                      validation_split = validationSize)
        else:
            model.fit(
                      trainX,
                      trainY,
                      epochs = numEpochs,
                      batch_size = numBatch,
                      verbose = 1)

        return model

def writeProfitsToFile(profitsList):
    file = open("LSTMprofits3.txt", "w")
    for i in profitsList:
        file.write(str(i)+"\n")
    file.close()

def tradingSimulation(trainingPredictions, testPredictictions, actualPrices):
    pfolio = portfolio()
    proflist = []
    for i in range(len(trainingPredictions)):
        action = pfolio.chooseAction(trainingPredictions[i], actualPrices[i+4])
        pfolio.executeAction(action, actualPrices[i+4])
        pfolio.calcProfits()
        proflist.append(pfolio.profits)
    
    for i in range(len(testPredictictions)):
        action = pfolio.chooseAction(testPredictictions[i], actualPrices[50+i+look_back-1])
        pfolio.executeAction(action, actualPrices[55+i-1])
        pfolio.calcProfits()
        proflist.append(pfolio.profits)
    
    writeProfitsToFile(proflist)

def graphPredictions(dataset, trainPredict, testPredict):
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

if __name__ == "__main__":
    random.seed(17)

    dataset = generateDataSet()

    sc = MinMaxScaler(feature_range = (0,1))
    dataset_scaled = sc.fit_transform(dataset)

    train, test = generateTrainTestData(dataset_scaled, 0.5) #2nd parameter = % of data in training set

    look_back = 5

    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)

    trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
    testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))

    units = [100,50]
    model = configureLSTMnetwork(2,units,0.2) #'X' layers, list of units in each layer, 'X' % dropout

    model = runLSTMnetwork(model, trainX, trainY, 100, 1) #'X' epochs, 'X' batch size

    trainScore = model.evaluate(trainX, trainY, verbose = 0)
    print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore, math.sqrt(trainScore)))
    testScore = model.evaluate(testX, testY, verbose=0)
    print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore, math.sqrt(testScore)))

    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)

    trainPredict = sc.inverse_transform(trainPredict)
    testPredict = sc.inverse_transform(testPredict)

    tradingSimulation(trainPredict,testPredict,dataset)

    graphPredictions(dataset, trainPredict, testPredict)


