# -*- coding: utf-8 -*-
"""
Allows to predict if a movie will be enjoyed by a user, thanks to his own training model

Created on Thu Feb 07 15:08 2017
@author: elsa
"""
from __future__ import unicode_literals

import numpy as np
from random import randint
from MovieProject.preprocessing import Preprocessor
from flask import json, jsonify
#from MovieProject.preprocessing.tools import getMovie
import tmdbsimple as tmdb

batch = 500

def predictMovies(movies, model, **kwargs):
    '''
    Predicts the classes of the movies according to the model
        parameters : 
            - movies : an array of the movie's id we want to know the class of, the id must exist
            - model : the model that matches the taste of the user, it must not be None
        returns : 
            - a np.array of values between 0 and 1, that show how much a movie is likely to be loved
    '''
    if model is None:
        raise ValueError('The model ', model, ' is not defined!')

    pProcessor = Preprocessor(**kwargs)
    
    data = pProcessor.preprocess(movies)
    
    print "preprocessing done for the movie, start the prediction"
    
    pred = model.predict(data, batch_size=batch, verbose=0)
    
    return pred

def suggestNMovies(model, n, **kwargs):
    """
    Suggests n movies for the person that has this model
        parameters :
            - model : the model that the suggestion fits, must not be None
            - n : the amount of suggestions to return
            - kwargs : the arguments necessary to preprocess the data
        return : 
            - a list of n suggestions that are liked according to the model
    """
    suggestion = []
    checkedIds = []
    toFind = n
    nTry = 0
    tryMax = 5
    
    #While we haven't found all of the movies
    while(toFind > 0 and nTry < tryMax):
        
        #Get the amount of pages from tmdb that suits our criteria
        pages = tmdb.Discover().movie(vote_count_gte=20)
        totalPages = pages['total_pages'] 
        
        #Init an array of the movies to Find and then fill it
        movies = []
        moviesIds = np.zeros(toFind)
        i = 0
        while(len(movies) < toFind):
            #We pick a random page and a random movie in this page
            iPage =  randint(1,totalPages)
            page = tmdb.Discover().movie(page=iPage, vote_count_gte=20)
            result = page["results"]
            iMovie = randint(0,len(result)-1)
            resMovie = result[iMovie]
            idMovie = resMovie['id']
            #We check that we didn't already checked the movie
            if(idMovie not in checkedIds):
                #We save the movie, and remember its id
                movies.append(resMovie)
                checkedIds.append(idMovie)
                moviesIds[i] = int(idMovie)
                i += 1
                
        #Now we have a movies list of the movies we need to find
        #We compute the predictions matching the model to know which movies to keep
        predictions = predictMovies(moviesIds, model, **kwargs)

        print "predictions done, we sort the results to keep"
        print predictions 
        print moviesIds 
        
        i = 0
        added = 0
        #For each prediction keep in the suggestion the ones that are > 0.5
        for p in predictions:
            if(moviesIds[i] != movies[i]['id']):
                raise ValueError("The movies ids doesn't match for movies ", moviesIds[i], " and ", movies[i]['id'])
            pred = p.item()
            if(pred > 0.5):
                #Add the accuracy of the movie according to the model
                movie = movies[i]
                movie[u'accuracy'] = pred
                print moviesIds[i], " is selected with accuracy ", pred, "!!!!!!!!!!!!!!"
                suggestion.append(movie)
                added += 1
            i += 1
        toFind -= added
        nTry += 1

    return suggestion    


#def saveModel(username, model):
#    """
#        Save model on resource/persist/model/username_model.json
#
#        username : unique key for a user, and a model is unique for a user
#        model : the keras model for the user
#    """
#    # serialize model to JSON
#    model_json = model.to_json()
#    model_filepath = RES_MODEL_PATH + '/' + username + '_model'
#    
#    #If the model directory doesn't exists, we create it
#    if not exists(RES_MODEL_PATH):
#        makedirs(RES_MODEL_PATH)
#
#    with open(model_filepath + '.json', "w") as json_file:
#        json_file.write(model_json)
#
#    # serialize weights to HDF5
#    model.save_weights(model_filepath + '.h5')
#
#    print("Saved model to disk")
#
#def loadModel(username):
#    """
#        Save model on resource/persist/model/username_model.json
#
#        username : unique key for a user, and a model is unique for a user
#        model : the keras model for the user
#    """
#    # serialize model to JSON
#   # model_json = model.to_json()
#    model_filepath = RES_MODEL_PATH + '/' + username + '_model'
#    
#    #If file doesn't exists, we return None
#    if(isfile(model_filepath + '.json') and isfile(model_filepath + '.h5')):
#        # load json and create model
#        json_file = open(model_filepath + '.json', 'r')
#        loaded_model_json = json_file.read()
#        json_file.close()
#        loaded_model = model_from_json(loaded_model_json)
#        # load weights into new model
#        loaded_model.load_weights(model_filepath + '.h5')
#        print("Loaded model from disk")
#        
#        return loaded_model
#    # evaluate loaded model on test data
#    # loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
#    # score = loaded_model.evaluate(X, Y, verbose=0)
#    else :
#        print "The model doesn't exists"
#        return None
#
#
#def getIdFromLikedMovies(username, isLiked):
#    """
#    
#    """
#    
#    movies = dbManager.getMoviesLikedByUser(username,isLiked)
#    return { str(movie.idMovie) : int(movie.liked) for movie in movies}

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

        #Retrieve the user movies
#    username = g.user_name
    username = 'User1'
    userMovies = getIdFromLikedMovies(username, None)

    #extract the ids and the labels of each movie
    ids = [int(key) for key in userMovies]
    labels = np.array([userMovies[key] for key in userMovies])
    
    print "Movies extracted"
    
    pProcessor = Preprocessor(**params)

    #preprocess data
    data = pProcessor.preprocess(ids)
    
    print "Movies loaded, building model"
    
    model = buildModel(data, labels)

    print "Saving model to file ..."
    
    saveModel(username, model)