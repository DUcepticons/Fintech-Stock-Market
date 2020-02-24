# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:47:20 2019

@author: raiyaan
training code from https://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/
"""

import pandas as pd
import tensorflow as tf

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder, MinMaxScaler


raw_data = pd.read_csv("appledata-output-categorical.csv")

#We take features of 4 days as input and action of the 4th day as output and construct a dataframe from this

list_data={}
list_data['Number-in-hand-1'] = raw_data.iloc[:-3,0].values.tolist() 
list_data['Price-1']= raw_data.iloc[:-3,1].values.tolist() 
list_data['Cash-1']= raw_data.iloc[:-3,2].values.tolist() 
list_data['Return-1']= raw_data.iloc[:-3,3].values.tolist() 

list_data['Number-in-hand-2']= raw_data.iloc[1:-2,0].values.tolist() 
list_data['Price-2']= raw_data.iloc[1:-2,1].values.tolist() 
list_data['Cash-2']= raw_data.iloc[1:-2,2].values.tolist() 
list_data['Return-2']= raw_data.iloc[1:-2,3].values.tolist() 

list_data['Number-in-hand-3']= raw_data.iloc[2:-1,0].values.tolist() 
list_data['Price-3']= raw_data.iloc[2:-1,1].values.tolist() 
list_data['Cash-3']= raw_data.iloc[2:-1,2].values.tolist() 
list_data['Return-3']= raw_data.iloc[2:-1,3].values.tolist() 

list_data['Number-in-hand-4']= raw_data.iloc[3:,0].values.tolist() 
list_data['Price-4']= raw_data.iloc[3:,1].values.tolist() 
list_data['Cash-4']= raw_data.iloc[3:,2].values.tolist() 
list_data['Return-4']= raw_data.iloc[3:,3].values.tolist() 

list_data['Action']= raw_data.iloc[3:,4].values.tolist() 


data = pd.DataFrame(list_data, columns = ['Number-in-hand-1','Price-1','Cash-1', 'Return-1','Number-in-hand-2','Price-2','Cash-2','Return-2', 'Number-in-hand-3','Price-3','Cash-3','Return-3', 'Number-in-hand-4','Price-4','Cash-4','Return-4','Action'])

X = (data.iloc[:,0:-1].values).astype('float32')
#min_max_scaler = MinMaxScaler()
#X = min_max_scaler.fit_transform(X)
Y = (data.iloc[:,-1].values)


# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = tf.keras.utils.to_categorical(encoded_Y)


# define baseline model
def baseline_model():
	# create model
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.LSTM(32, return_sequences=True, input_shape=(16, 16)))  # returns a sequence of vectors of dimension 32
    model.add(tf.keras.layers.LSTM(32, return_sequences=True))  # returns a sequence of vectors of dimension 32
    model.add(tf.keras.layers.LSTM(32))  # return a single vector of dimension 32
    model.add(tf.keras.layers.Dense(3, activation='softmax'))
    
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    return model

estimator = tf.keras.wrappers.scikit_learn.KerasClassifier(build_fn=baseline_model, epochs=50, batch_size=50, verbose=1)
kfold = KFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, X, dummy_y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
