# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:47:20 2019

@author: niloy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from statistics import mean


data = pd.read_csv("sqdata.csv")
cp = (data.iloc[:,1].values).astype('float32')
high = (data.iloc[:,3].values).astype('float32')
low = (data.iloc[:,4].values).astype('float32')
trend = (data.iloc[:,-1].values).astype('float32')
MA=[]
MACD=[]
K=[]
D=[]
RSI=[]
R=[]
EMA12 = [0]
EMA26 = [0]

for i in range(15,len(data)):

        sum_of_cp=0
        sum_of_ht=0
        sum_of_lt=0
        for j in range(i-15,i):
            sum_of_cp+=cp[j]
            #sum_of_ht+=high[j]
            #sum_of_lt+=low[j]
    
        MA.append(sum_of_cp/15)
        #RS=(sum_of_ht/15)/(sum_of_lt/15)
        
        
    
        K.append(((cp[i]-min(low[i-15:i]))*100)/(max(high[i-15:i])-min(low[i-15:i])))
        R.append(((max(high[i-15:i])-cp[i])*100)/(max(high[i-15:i])-min(low[i-15:i])))
        
        if i>=17:
            D.append((K[i-15-2]+K[i-15-1]+K[i-15])/3)
            
        if i>=26:
            
            EMA12.append(((cp[i]-EMA12[i-25-1])*(2/(12+1))) + EMA12[i-25-1])
            EMA26.append(((cp[i]-EMA26[i-25-1])*(2/(26+1))) + EMA26[i-25-1])
            
            MACD.append(EMA12[i-25]-EMA26[i-25])
        
'''
maxMA = max(MA)
minMA = min(MA)
maxMACD = max(MACD)
minMACD = min(MACD)
maxK = max(K)
minK = min(K)
maxD = max(D)
minD = min(D)
maxR = max(R)
minR = min(R)
for i in range(0,len(MA)):
    MA[i] = (MA[i] - mean(MA))/(maxMA-minMA)
    K[i] = (K[i] - mean(K))/(maxK-minK)
    R[i] = (R[i] - mean(R))/(maxR-minR)
for i in range(0,len(MACD)):
    MACD[i] = (MACD[i] - mean(MACD))/(maxMACD-minMACD)
for i in range(0,len(D)):
    D[i] = (D[i] - mean(D))/(maxD-minD)    
'''
    
t_data = [cp[26:],MA[11:],MACD,K[11:],D[9:],R[11:],trend[26:]]
df = pd.DataFrame(t_data)
df = df.T
df.columns = ['CP','MA','MACD','K','D','R','Trend']
export_csv = df.to_csv (r'sqtrend.csv', index = None, header=True)


#plt.plot(cp[15:])

'''
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(1, activation=tf.nn.relu))

model.compile(optimizer="adam", loss="mean_squared_error")
model.fit(X_train, Y_train, epochs=500)
model.evaluate(X_test,Y_test)

prediction = model.predict(X_check)
'''