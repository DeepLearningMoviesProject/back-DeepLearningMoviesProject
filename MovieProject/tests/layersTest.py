# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from __future__ import print_function

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Merge, BatchNormalization, Embedding, Flatten
from keras.optimizers import SGD

#X1: simulation realisateurs
X1_train = np.empty((2,2))
#X2: simulation acteurs
X2_train = np.empty((2,3))
#X3: simulation quelquonque
X3_train = np.empty((2,4))
#X: simulation vecteur glove
X_train = np.empty((2,5))
#Y : Labels
nbY = 1
Y_train = np.empty((2,nbY ))

i = 0
y = 0
while (i<2):
    y = 0
    while (y<nbY):
        Y_train[i][y] = 0
        y += 1
    i += 1

X1_train[0][0] = 3
X1_train[0][1] = 4
X1_train[1][0] = 7 
X1_train[1][1] = 8

X2_train[0][0] = 322
X2_train[0][1] = 46
X2_train[0][2] = 72
X2_train[1][1] = 889
X2_train[1][2] = 45
X2_train[1][0] = 72

X3_train[0][0] = 322
X3_train[0][1] = 46
X3_train[0][2] = 72
X3_train[1][1] = 889
X3_train[1][2] = 45
X3_train[1][0] = 72
X3_train[0][3] = 322
X3_train[1][3] = 46


X_train[0][0] = 322
X_train[0][1] = 46
X_train[0][2] = 72
X_train[1][1] = 889
X_train[1][2] = 45
X_train[1][0] = 72
X_train[0][3] = 322
X_train[1][3] = 46
X_train[0][4] = 322
X_train[1][4] = 46


X_branch = Sequential()
X_branch.add(Embedding(1000, 1, input_length=5))
X_branch.add(Flatten())


X1_branch = Sequential()
X1_branch.add(Dense(5, input_shape = (2,), init='normal', activation='relu'))
X1_branch.add(BatchNormalization())

X2_branch = Sequential()
X2_branch.add(Dense(10, input_shape =  (3,) , activation = 'relu'))
X2_branch.add(BatchNormalization())

X3_branch = Sequential()
X3_branch.add(Dense(10, input_shape =  (4,) , activation = 'relu'))
X3_branch.add(BatchNormalization())

#On merge en cascade

X1X2_branch = Sequential()
X1X2_branch.add(Merge([X1_branch, X2_branch], mode = 'concat'))
X1X2_branch.add(Dense(1,  activation = 'sigmoid'))


X1X2X3_branch = Sequential()
X1X2X3_branch.add(Merge([X3_branch, X1X2_branch], mode = 'concat'))
X1X2X3_branch.add(Dense(1,  activation = 'sigmoid'))

final_branch = Sequential()
final_branch.add(Merge([X_branch, X1X2X3_branch], mode = 'concat'))

final_branch.add(Dense(30,  activation = 'relu'))
final_branch.add(Dense(1,  activation = 'sigmoid'))

sgd = SGD(lr = 0.1, momentum = 0.9, decay = 0, nesterov = False)
final_branch.compile(loss = 'binary_crossentropy', optimizer = sgd, metrics = ['accuracy'])

final_branch.fit([X_train, X3_train,X1_train, X2_train], Y_train, batch_size = 2000, nb_epoch = 100, verbose = 1)
print("done")	
