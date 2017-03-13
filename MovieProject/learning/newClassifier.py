#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    This module is dedicated to a different type of classifier :
        this classifier is binding users together to suggest movies.
    The model of the classifier is builded only once, and can be build again if new data are required
    The model is the same for every user, so the suggestion only need one model

    @author: elsa
"""
import math
import numpy as np
from keras.callbacks import Callback, EarlyStopping, ModelCheckpoint
from keras.layers import Embedding, Reshape, Merge, Dropout, Dense
from keras.models import Sequential
from MovieProject.sql import *

from MovieProject.preprocessing.tools import dbPreprocessingTools

K_FACTORS = 50
RNG_SEED = 1446557
#File where the model weighs are saved
MODEL_WEIGHTS_FILE = '../resources/persist/model/global/model_weights.h5'

#Copy from CFModel

def _predict_rating(userid, movieid, model):
    '''
        Predicts the rating a user will give to a movie
    '''
    return model.rate(userid - 1, movieid - 1)

class CFModel(Sequential):
    '''
        Classic model
    '''
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
    '''
        Model with more layers
    '''
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
    
def createModelUniq():
    '''
        Creates the global model and saves it into a file
        Returns : the keras model
    '''
    
    #Get data from DB
    t = dbPreprocessingTools()
    users, movies, ratings = t.preprocessingUserMovies()
    
    max_userid = np.amax(users)
    max_movieid = np.amax(movies)
    print len(ratings), 'ratings loaded.'
    print "max user id :", max_userid
    print "max movie id :", max_movieid
    
    print 'Users:', users, ', shape =', len(users)
    print 'Movies:', movies, ', shape =', len(movies)
    print 'Ratings:', ratings, ', shape =', len(ratings)
    
    	#Faire le modèle
    model = DeepModel(max_userid + 1, max_movieid + 1, K_FACTORS)
    model.compile(loss='mse', optimizer='adamax')
    
    callbacks = [EarlyStopping('val_loss', patience=5), 
    	             ModelCheckpoint(MODEL_WEIGHTS_FILE, save_best_only=True)]
    history = model.fit([users, movies], ratings, nb_epoch=50, validation_split=.1, verbose=2, callbacks=callbacks)
        
    min_val_loss, idx = min((val, idx) for (idx, val) in enumerate(history.history['val_loss']))
    print 'Minimum RMSE at epoch', '{:d}'.format(idx+1), '=', '{:.4f}'.format(math.sqrt(min_val_loss))
    
    return model

def suggestMoviesSaveNBest(model, user, n=0, **kwargs):
    '''
        Returns the suggestion for the user according to the global model (saved in a file)
        TODO : Save the n best movies suggested
        The suggestion is based on the movies that are in our database (already added by the other users).
        
        Parameters :
            user : (int) a user id
            n : (int) the amount of movies we want to save (0 by default)
            model : (keras model) the model used for the prediction, will be removed from the parameters in the future
        
        Returns : the list of all the movies in the database witht their rating prediciton
    '''
    #TODO Get model from file
    
    #Get movies the user didn't rate from DB
    manager = DatabaseManager()
    moviesList = manager.getNotRatedMoviesfromUser(user)
    
    print len(moviesList), "movies to predict"
    
    user_predictions = []
    
    for m in moviesList :
        p = _predict_rating(user, m, model)
        movie = {'movie' : m, 'accuracy' : p}
        user_predictions.append(movie)
    
#    user_predictions.sort_values(by='predictions', 
#                             ascending=False)
    # TODO : save n best ?
    return user_predictions

if __name__ == '__main__':
        
    params = { "titles":True,
               "rating":True,
               "overviews":True,
               "keywords":True,
               "genres":True,
               "actors":True,
               "directors":True,
              "compagnies" : True,
              "language" : True,
              "belongs" : True,
              "runtime" : True,
              "date" : True }
        
    
    model = createModelUniq()
    
    #Prédictions
    testUser = 2
    
    print testUser
    print type(testUser)
    
    predictions = suggestMoviesSaveNBest(model, testUser)
    
    print predictions