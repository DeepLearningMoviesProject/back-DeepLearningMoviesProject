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
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Embedding, Reshape, Merge, Dropout, Dense
from keras.models import Sequential
from MovieProject.sql import *
from os.path import exists, join
from os import makedirs
import pickle

from MovieProject.preprocessing.tools import dbPreprocessingTools
from MovieProject.resources import GLOBAL_MODEL_FILE, RES_PREDICTIONS_PATH, RES_GLOBAL_PATH


K_FACTORS = 50
RNG_SEED = 1446557

path = RES_GLOBAL_PATH
filename = GLOBAL_MODEL_FILE.replace(path, '')
filename = filename.replace('.h5', '')


#Copy from CFModel

def _predictRating(userid, movieid, model):
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
    
def buildModelUniq():
    '''
        Creates the global model and saves it into a file
        Returns : the keras model
    '''
    
    #Get data from DB
    t = dbPreprocessingTools()
    users, movies, ratings = t.preprocessingUserMovies()
    
    maxUserid = np.amax(users)
    maxMovieid = np.amax(movies)
    print len(ratings), ' ratings loaded.'
    print "max user id :", maxUserid
    print "max movie id :", maxMovieid
    
    print 'Users:', users, ', shape =', len(users)
    print 'Movies:', movies, ', shape =', len(movies)
    print 'Ratings:', ratings, ', shape =', len(ratings)
    
    	#Create the model
    model = DeepModel(maxUserid + 1, maxMovieid + 1, K_FACTORS)
    model.compile(loss='mse', optimizer='adamax')
    
    #Save max_userid and max_movieid
#    maxids_filepath = RES_GLOBAL_PATH + '/max_ids.json'
#    with open(movies_filepath, 'w') as f:
#        json.dump(nBest, f, ensure_ascii=False)
    
    callbacks = [EarlyStopping('val_loss', patience=5), 
    	             ModelCheckpoint(GLOBAL_MODEL_FILE, save_best_only=True)]
    history = model.fit([users, movies], ratings, nb_epoch=50, validation_split=.1, verbose=2, callbacks=callbacks)
        
    min_val_loss, idx = min((val, idx) for (idx, val) in enumerate(history.history['val_loss']))
    print 'Minimum RMSE at epoch', '{:d}'.format(idx+1), '=', '{:.4f}'.format(math.sqrt(min_val_loss))
    
    return model

def suggestMoviesSaveNBest(user, n=0):
    '''
        Returns the suggestion for the user according to the global model (saved in a file)
        The suggestion is based on the movies that are in our database (already added by the other users).
        
        Parameters :
            user : (int) a user id
            n : (int) the amount of movies we want to save (0 by default)
            
        Returns : the list of all the movies in the database witht their rating prediciton
    '''
    #Get the model from file
    model = getModel()
    
    if model is None :
        print "the model doesn't exists !"
        raise
        #TODO : raise an error
    
    #Get movies the user didn't rate from DB
    manager = DatabaseManager()
    moviesList = manager.getNotRatedMoviesfromUser(user)
    
    print len(moviesList), "movies to predict"
    
    userPredictions = {}
    
    for m in moviesList :
        userPredictions[str(m)] = _predictRating(user, m, model).item()
    
    saved = 0
    nBest = {}
    #Iterate over dict in order 
    for key, value in sorted(userPredictions.iteritems(), key=lambda (k,v): (v,k),reverse=True):  
        if(saved > n):
            break
        nBest[key] = value
        saved += 1
    
    #Save nBest to file
    moviesFilepath = join(RES_PREDICTIONS_PATH, str(user) + '_predictions.json')
    
    #If the predictions directory doesn't exists, we create it
    if not exists(RES_PREDICTIONS_PATH):
        makedirs(RES_PREDICTIONS_PATH)
        
    with open(moviesFilepath, 'w') as f:
        pickle.dump(nBest, f)
    
    return userPredictions, nBest

def getNBestMovies(user, n=0):
    '''
        Retrieves the best movies for a user that has been saved in a file
        If the file doesn't exists, we do the suggestion
        
        Params :
            user : (int) user id
            
        Returns : a dict of movies (key) and their prediction (value)
    '''
    # load json
    moviesFilepath = join(RES_PREDICTIONS_PATH, str(user) + '_predictions.json')
    nBest = {}
    
#    with open(movies_filepath) as json_predictions:
#        predictions = json.load(json_predictions)

    if not exists(moviesFilepath):
        allPred, nBest = suggestMoviesSaveNBest(user, n)
    else:
        with open(moviesFilepath, 'r') as f:
            n_best = pickle.load(f)
    
    if(len(n_best) < n):
        allPred, nBest = suggestMoviesSaveNBest(user, n)
        
    return nBest

def getModel(redoModel = False):
    '''
        Retrieves the model in the file system or builds it if necessary.       
        
        Params :
            redoModel : boolean to tell if the model MUST be done again
            
        Returns :
            the model of the the new classifier
    '''
    model = None
    
    if (not exists(GLOBAL_MODEL_FILE)) or redoModel:
        model = buildModelUniq()
    else:
        t = dbPreprocessingTools()
        users, movies, ratings = t.preprocessingUserMovies()
        #TODO : Warning, max_userid and max_movie_id might have to be retrieve differently
        
        max_userid = np.amax(users) + 1
        max_movieid = np.amax(movies) + 1

        model = DeepModel(max_userid, max_movieid, K_FACTORS)
        model.load_weights(GLOBAL_MODEL_FILE)
        
    return model

if __name__ == '__main__':
    # Creates and save the model if doesn't exists
    model = getModel(redoModel = True)
