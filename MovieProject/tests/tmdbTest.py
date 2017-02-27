#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:16:32 2017

@author: Kaito
"""
import numpy as np
import tmdbsimple as tmdb
from keras.models import Sequential
from keras.layers import Dense
from datetime import datetime

tmdb.API_KEY = 'ff3f07bf3577a496a2f813488eb29980'

model = Sequential()


def searchData2(ids=[], threshold=0.5): 
    """ Parameters:
            ids: array of movie's id
        return:
            tuple of 2 matrix of n*1 dimension
            -> X_train and Y_train
    """
    
    print "searching data"
    # matrice de n lignes avec 1 classe (note)
    X_train = np.empty((len(ids),1))
    Y_train = np.empty((len(ids),1))   
    
    for i in range(len(ids)):
        movie = tmdb.Movies(ids[i])
        response = movie.info()
        
        X_train[i][0] = response['vote_average']/10.0
        Y_train[i][0] = 1 if (X_train[i][0] >= threshold) else 0
               
    return X_train, Y_train

def searchData(ids=[]): 
    """ Parameters:
            ids: array of movie's id
        return:
            matrix of data
    """
    
    print "searching data"
    print ids
    # matrice de n lignes avec 1 classe (note)
    X_train = np.empty((len(ids),1))
    
    for i in range(len(ids)):
        movie = tmdb.Movies(ids[i])
        response = movie.info()
        
        X_train[i][0] = response['vote_average']/10.0
               
    return X_train
        

def trainData(X_train, Y_train):
    """ 
        Train the model
    
        Parameters:
            X_train: train matrix
            Y_train: class matrix
    """
    print "training"
    model.add(Dense(output_dim=60, input_dim=1, init='normal', activation='relu'))
    model.add(Dense(output_dim=30, init='normal', activation='relu'))
    model.add(Dense(output_dim=15, init='normal', activation='relu'))
    model.add(Dense(output_dim=1, init='normal', activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, Y_train, batch_size=500, nb_epoch=2000)

def predictData(tests):
    """
        Predict classes
        
        Parameters:
            tests: matrix containing data to predict
        return:
            tuple of proba and classes predicted
    """
    
    prob = model.predict_proba(tests)
    classe = model.predict_classes(tests)
    classe = model.predict_classes(tests)

    return prob, classe
    

if __name__ == "__main__":
    #Batman & Robin, Chapeau melon et bottes de cuir, Troll2, House of the dead, Battlefield heart, Alone in the dark, King rising.
    #Le dernier samouraï, Le seigneur des anneaux, Le parrain, Le voyage de Chihiro, Figth club, La vita bella, Princesse mononoke, Intouchable, Les 7 samourai,
    #Forest Gump, Pulpe fiction, Interstellar, Comme des bêtes, 
    
    X_train, Y_train = searchData2([415, 9320, 26914, 11059, 5491, 12142, 2312, 616, 121 , 238, 129, 550, 637, 128, 77338, 346 ,13 , 680, 157336, 328111, 297761, 127380, 121856, 313369, 259316, 207932, 346672, 302946, 333484, 346685, 343611, 47971], 0.8);
    
    trainData(X_train, Y_train)
    
    tests = np.empty((10,1))
    tests[0][0] = 0/10.0
    tests[1][0] = 1/10.0
    tests[2][0] = 3/10.0
    tests[3][0] = 6/10.0
    tests[4][0] = 7/10.0
    tests[5][0] = 9/10.0
    tests[6][0] = 5/10.0
    tests[7][0] = 6/10.0
    tests[8][0] = 7/10.0
    tests[9][0] = 8/10.0
    
    proba, classes = predictData(tests)
    
    print proba
    print classes