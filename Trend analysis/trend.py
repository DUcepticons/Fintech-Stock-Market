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
corrmat = data.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corrmat, vmax=.8, square=True)
'''


X_train = (data.iloc[:-80,1:-1].values).astype('float32')
scaler = scale.fit(X_train)
X_train=scaler.transform(X_train)
Y_train = (data.iloc[:-80,-1].values).astype('float32')

#X_test = (data.iloc[-1180:-15,1:-1].values).astype('float32')
#scaler.transform(X_test)
#Y_test = (data.iloc[-1180:-15,-1].values).astype('float32')

X_check = (data.iloc[-80:,1:-1].values).astype('float32')
X_check=scaler.transform(X_check)


model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(100, input_dim=X_train.shape[1], activation=tf.nn.sigmoid))
model.add(tf.keras.layers.Dense(100, activation=tf.nn.sigmoid))
model.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid))

model.compile(optimizer="nadam", loss="binary_crossentropy", metrics = ['accuracy'])
model.fit(X_train, Y_train, epochs=500, batch_size=35, validation_split = 0.33)
prediction = model.predict(X_check)
