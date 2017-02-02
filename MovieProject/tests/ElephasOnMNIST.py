#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
MNIST model to test Elephas

Created on Thu Feb  2 14:20:07 2017
@author: coralie
"""

import numpy as np

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.utils import np_utils


"""
Load training data :
    the data, shuffled and split between tran and test sets
"""

(X_train, y_train), (X_test, y_test) = mnist.load_data()
#print("X_train original shape", X_train.shape)
#print("y_train original shape", y_train.shape)


"""
Format the data for training : 
    the neural-network is going to take a single vector for each training example, 
    so we need to reshape the input so that each 28x28 image becomes a single 
    784 dimensional vector. We'll also scale the inputs to be in the 
    range [0-1] rather than [0-255]
"""

nb_classes = 10

X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
#print("Training matrix shape", X_train.shape)
#print("Testing matrix shape", X_test.shape)

Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)


"""
Build the neural network :
    a simple 3 layer fully connected network
"""

model = Sequential()
model.add(Dense(512, input_shape=(784,)))

# An "activation" is just a non-linear function applied to the output of the layer above. 
# Here, with a "rectified linear unit", we clamp all values below 0 to 0.
model.add(Activation('relu')) 
# Dropout helps protect the model from memorizing or "overfitting" the training data                           
model.add(Dropout(0.2))   
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(10))
# This special "softmax" activation among other things, ensures the output is 
# a valid probaility distribution, that its values are all non-negative and sum to 1.
model.add(Activation('softmax')) 


"""
Compile the model
"""

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=["accuracy"])


"""
Train the model
"""

model.fit(X_train, Y_train, batch_size=128, nb_epoch=4, show_accuracy=True, verbose=1, validation_data=(X_test, Y_test))


"""
Evaluate its performance
"""

score = model.evaluate(X_test, Y_test, verbose=0)
print('Loss on tests:', score[0])
print('Accuracy on test:', score[1])



