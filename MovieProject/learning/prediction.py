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
#from flask import json, jsonify
#from MovieProject.preprocessing.tools import getMovie
import tmdbsimple as tmdb

batch = 500

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
    

def predictMovies(movies, model, **kwargs):
    '''
    Predicts the class of the movie according to the model
        parameters : 
            - movies : an array of the id of the movie we want to know the class of, the id must exist
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
            - model : the model that the suggestion fits
            - n : the amount of suggestions to return
            - kwargs : the arguments necessary to preprocess the data
        return : 
            - a list of n suggestions that are liked according to the model
    """
    suggestion = []
    checkedIds = []
    toFind = n
    
    #While we haven't found all of the movies
    while(toFind > 0):
        
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
#                print movie, " is selected with accuracy ", pred, "!!!!!!!!!!!!!!"
                suggestion.append(movie)
                added += 1
            i += 1
        toFind -= added

    return suggestion