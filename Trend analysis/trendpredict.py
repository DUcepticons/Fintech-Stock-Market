# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:47:20 2019

@author: niloy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import seaborn as sns
from sklearn.preprocessing import StandardScaler

scale = StandardScaler()
np.random.seed(7)
data = pd.read_csv("gptrend.csv")
data2 = pd.read_csv("sqtrend.csv")
data = data.append(data2, ignore_index = True)

'''
corrdata = data.iloc[:,1:]
corrmat = corrdata.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corrmat, vmax=.8, square=True)
trend = 500 * data.iloc[:,-1]
plt.plot(trend)
plt.plot(data.iloc[:,0])
'''


X_train = (data.iloc[:-80,1:-1].values).astype('float32')
scaler = scale.fit(X_train)
X_train=scaler.transform(X_train)
Y_train = (data.iloc[:-80,-1].values).astype('float32')


X_check = (data.iloc[-80:,1:-1].values).astype('float32')
X_check=scaler.transform(X_check)
Y_check = (data.iloc[-80:,-1].values).astype('float32')

model = tf.keras.models.load_model("Trendanalysis.h5")
prediction = model.predict(X_check)
