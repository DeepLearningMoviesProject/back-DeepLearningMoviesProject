#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: elsa
"""
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from keras.callbacks import Callback, EarlyStopping, ModelCheckpoint
from keras.layers import Embedding, Reshape, Merge, Dropout, Dense
from keras.models import Sequential
from MovieProject.sql import *
# from CFModel import CFModel, DeepModel

from MovieProject.preprocessing.tools import dbPreprocessingTools

K_FACTORS = 50
RNG_SEED = 1446557
MODEL_WEIGHTS_FILE = 'ml1m_weights.h5'

#Copy from CFModel

def predict_rating(userid, movieid, model):
    return model.rate(userid - 1, movieid - 1)

class CFModel(Sequential):

    def __init__(self, n_users, m_items, k_factors, **kwargs):
        P = Sequential()
        P.add(Embedding(n_users, k_factors, input_length=1))
        P.add(Reshape((k_factors,)))
        Q = Sequential()
        Q.add(Embedding(m_items, k_factors, input_length=1))
        Q.add(Reshape((k_factors,)))
        super(CFModel, self).__init__(**kwargs)
        self.add(Merge([P, Q], mode='dot', dot_axes=1))

    def rate(self, user_id, item_id):
        return self.predict([np.array([user_id]), np.array([item_id])])[0][0]

class DeepModel(Sequential):

    def __init__(self, n_users, m_items, k_factors, p_dropout=0.2, **kwargs):
        P = Sequential()
        P.add(Embedding(n_users, k_factors, input_length=1))
        P.add(Reshape((k_factors,)))
        Q = Sequential()
        Q.add(Embedding(m_items, k_factors, input_length=1))
        Q.add(Reshape((k_factors,)))
        super(DeepModel, self).__init__(**kwargs)
        self.add(Merge([P, Q], mode='concat'))
        self.add(Dropout(p_dropout))
        self.add(Dense(k_factors, activation='relu'))
        self.add(Dropout(p_dropout))
        self.add(Dense(k_factors/2, activation='relu'))
        self.add(Dropout(p_dropout))
        self.add(Dense(1, activation='sigmoid'))

    def rate(self, user_id, item_id):
        return self.predict([np.array([user_id]), np.array([item_id])])[0][0]
    

if __name__ == '__main__':
    #Récupérer les données depuis la BD
    
    t = dbPreprocessingTools()
    users, movies, ratings = t.preprocessingUserMovies()
    
    	# Créer 3 arrays user, movies, ratings
    
    #	users = np.array([1,1,1,2,2,3,15,15])
    #	movies = np.array([5,6,7,5,8,6,6,7])
    #	ratings = np.array([0,1,1,0,0,1,0,1])
    
    
    max_userid = np.amax(users)
    max_movieid = np.amax(movies)
    print len(ratings), 'ratings loaded.'
    print max_userid
    print max_movieid
    
    print 'Users:', users, ', shape =', len(users)
    print 'Movies:', movies, ', shape =', len(movies)
    print 'Ratings:', ratings, ', shape =', len(ratings)
    
    	#Faire le modèle
    model = DeepModel(max_userid + 1, max_movieid + 1, K_FACTORS)
    model.compile(loss='mse', optimizer='adamax')
    
    callbacks = [EarlyStopping('val_loss', patience=5), 
    	             ModelCheckpoint(MODEL_WEIGHTS_FILE, save_best_only=True)]
    history = model.fit([users, movies], ratings, nb_epoch=10, validation_split=.1, verbose=2, callbacks=callbacks)
        
    min_val_loss, idx = min((val, idx) for (idx, val) in enumerate(history.history['val_loss']))
    print 'Minimum RMSE at epoch', '{:d}'.format(idx+1), '=', '{:.4f}'.format(math.sqrt(min_val_loss))
    
    #Prédictions
    
    manager = DatabaseManager()
    
    usersDb = manager.getAllUsers()
    testUser = users[0].item()
#    testUser = 2
    
    print testUser, " is user ", usersDb[0]
    print type(testUser)
    
    moviesList = manager.getNotRatedMoviesfromUser(testUser)
    
    print len(moviesList), "movies to predict"
    
    user_predictions = []  #{'movies' : [], 'predictions' : []}
    
    for m in moviesList :
        p = predict_rating(testUser, m, model)
        movie = {'movie' : m, 'accuracy' : p}
        user_predictions.append(movie)
    
#    user_predictions.sort_values(by='predictions', 
#                             ascending=False)
    
    print user_predictions