from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn import metrics
from scipy.interpolate import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import multiprocessing

#BASH SCRIPT TO RUN ON ALL SYS ARG OPTIONS: for i in {1..10000}; do python3 lr.py $i; done

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

col_names = ['count','prices']
# load dataset
df = pd.read_csv("DJI2.csv", header=None, names=col_names)
X = df['count']
X = X.values
y = df['prices']
y = y.values

for i in range (1, 10000):
    pfolio = portfolio()
    
    for n in range (1,27809, i):
        #polyfit output: [m, b], y = mx + b
        MBvalues = np.polyfit(X[0:n],y[0:n],1)
        m,b = MBvalues
        yPoly = (m*(n+1)) + b #Predict a value 1 timestep ahead
        action = chooseAction(yPoly, y[n]) #True = buy, False = sell
        pfolio.executeAction(action, y[n])

    pfolio.calcProfits()
    f = open("profits.txt", "a+")
    f.write(pfolio.profits)
    f.close()
    print(pfolio.profits)
    del pfolio



#plt.plot(X,y, 'o')
#plt.plot(X,np.polyval(p1,X),'r-')
#plt.plot(X,np.polyval(p2,X),'b--')
#plt.plot(X,np.polyval(p3,X),'m:')
#plt.show()




