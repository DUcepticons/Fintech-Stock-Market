# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:47:20 2019

@author: niloy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf


data = pd.read_csv("gptrend.csv")
data2 = pd.read_csv("sqtrend.csv")

data = data.append(data2, ignore_index = True)

X_train = (data.iloc[:-1180,1:-1].values).astype('float32')
Y_train = (data.iloc[:-1180,-1].values).astype('float32')

X_test = (data.iloc[-1180:-15,1:-1].values).astype('float32')
Y_test = (data.iloc[-1180:-15,-1].values).astype('float32')
X_check = (data.iloc[-15:,1:-1].values).astype('float32')


model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid))

model.compile(optimizer="Adam", loss="mean_squared_error")
model.fit(X_train, Y_train, epochs=100)
model.evaluate(X_test,Y_test)

prediction = model.predict(X_check)
