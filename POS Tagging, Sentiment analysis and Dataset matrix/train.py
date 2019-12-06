# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:47:20 2019

@author: niloy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf


data = pd.read_csv("Dataset Matrix.csv")
X_train = (data.iloc[:450,:-1].values).astype('float32')
Y_train = (data.iloc[:450,-1].values).astype('float32')

X_test = (data.iloc[450:-6,:-1].values).astype('float32')
Y_test = (data.iloc[450:-6,-1].values).astype('float32')
X_check = (data.iloc[-6:,:-1].values).astype('float32')

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(1894, activation=tf.nn.sigmoid))
model.add(tf.keras.layers.Dense(1894, activation=tf.nn.sigmoid))
model.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid))


model.compile(optimizer="adam", loss="binary_crossentropy")
model.fit(X_train, Y_train, epochs=40)
model.evaluate(X_test,Y_test)

prediction = model.predict(X_check)
print(prediction)