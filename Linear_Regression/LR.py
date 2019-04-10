import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

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
        self.profits = round(self.profits,2)
        self.profits = str(self.profits)
        self.profits += "\n"

def chooseAction(yPoly, y): #Returns true if predicted value n is an increase over y @ n-1, else returns false
    return yPoly > y

def fileWrite100(predictedPrices, profits): #Write the data for the smaller data set to a file
    file = open("100predictions.txt", "a")
    
    for i in predictedPrices:
        file.write(str(i)+"\n")
    
    file.close()

    file = open("100profits", "a")

    for j in profits:
        file.write(str(j))

    file.close()

def fileWriteFullDataSet(predictedPrices, profits): #Write the data for the full data set to a file
    file = open("predictions.txt", "a")
    
    for i in predictedPrices:
        file.write(str(i)+"\n")

    file.close()

    file = open("profits.txt", "a")

    for j in profits:
        file.write(str(j))
    
    file.close()

def DataSetRegression(X, y, dataSize): #Preform a linear regression on the data
    profList = []
    pfolio = portfolio()
    predictedPrices = []
    
    X = sm.add_constant(X) # adding a constant
    for n in range (5, dataSize, 1):
        model = sm.OLS(y[n-5:n], X[n-5:n]).fit()
        prediction = model.predict(X[n+1: n+2]).values
        action = chooseAction(prediction, y[n])
        pfolio.executeAction(action, y[n])
        predictedPrices.append(prediction)
        pfolio.calcProfits()
        profList.append(pfolio.profits)
        print(y[n], y[n+1],predictedPrices[n-5], prediction, action, pfolio.assets, pfolio.profits)

    fileWrite100(predictedPrices, profList) if dataSize == 103 else fileWriteFullDataSet(predictedPrices,profList)
    print (pfolio.assets, pfolio.profits)
    #plotData(predictedPrices, y)



def loadData(fileName):
    col_names = ['y', 'x1','x2','x3','x4','x5']
    df = pd.read_csv(fileName, header=None, names=col_names)
    y = df['y']
    X=df[['x1','x2','x3','x4','x5']]
    return X,y

def plotData(predictedPrices, y):
    print (predictedPrices)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(predictedPrices, label ='Predicted Prices')
    #ax.plot(y, label = 'Actual Prices')
    plt.legend(loc=2)
    plt.show()

X,y = loadData("DJI.csv")
DataSetRegression(X,y,103)
X2,y2 = loadData("DJI2.csv")
DataSetRegression(X2,y2,27808)







