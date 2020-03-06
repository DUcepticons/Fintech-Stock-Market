# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:47:20 2019

@author: raiyaan
"""

import numpy as np
import pandas as pd
import tensorflow as tf

import matplotlib.pyplot as plt

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline

# multi-class classification with Keras
import pandas
import tensorflow as tf

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
# load dataset
dataframe = pandas.read_csv("iris.data", header=None)
dataset = dataframe.values
X = dataset[:,0:4].astype(float)



model = tf.keras.models.load_model("irisdata.h5")
prediction = model.predict(X)

