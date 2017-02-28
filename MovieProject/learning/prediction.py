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
#from MovieProject.preprocessing.tools import getMovie
import tmdbsimple as tmdb

batch = 500

def predict(movies, model, **kwargs):
    '''
    Predicts the class of the movie according to the model
        parameters : 
            - movies : an array of the id of the movie we want to know the class of, the id must exist
            - model : the model that matches the taste of the user
        returns : 
            - a boolean to tell if the movie is liked or not
    '''
    
    #arrayMovie = np.array([movie])
    
#    print "movies prediction : ", movies
    
    pProcessor = Preprocessor(**kwargs)
    
    data = pProcessor.preprocess(movies)
    
#    data = preprocess(arrayMovie,  doTitles=True, doRating=True, doOverviews=True, doKeywords=True, doGenres=True, doActors=True, doDirectors=True)
    
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
    suggestion = np.array([])
    checkedIds = []
    toFind = n
    
    #While we haven't found all of the movies
    while(toFind > 0):
        
        #Get the amount of pages from tmdb that suits our criteria
        pages = tmdb.Discover().movie(vote_count_gte=20)
        totalPages = pages['total_pages'] 
        
        print totalPages, " pages to exploit"
        
        #Init an array of the movies to Find and then fill it
        movies = []
        moviesIds = np.zeros(toFind)
        i = 0
        while(len(movies) < toFind):
            #We pick a random page and a random movie in this page
            iPage =  randint(1,totalPages)
            page = tmdb.Discover().movie(page=iPage, vote_count_gte=20)
            iMovie = randint(0,len(page))
            resMovie = page["results"][iMovie]
            idMovie = resMovie['id']
            #We check that we didn't already checked the movie
            if(idMovie not in checkedIds):
                #We save the movie, and remember its id
                movies.append(resMovie)
                checkedIds.append(idMovie)
                moviesIds[i] = int(idMovie)
#                np.append(moviesIds, int(idMovie))
#                print movies[i]['id'], " added in movies !"
                i += 1
        #Now we have a movies list of the movies we need to find
        #We compute the predictions matching the model to know which movies to keep
        predictions = predict(moviesIds, model, **kwargs)
        
        
        i = 0
        added = 0
        #For each prediction keep in the suggestion the ones that are > 0.5
        for p in predictions:
#            print moviesIds[i], " has prediction ", p[0]
            if(moviesIds[i] != movies[i]['id']):
                #TODO : raise an exception
                print "Error : the movies ids are not correct !"
            if(p[0] > 0.5):
                #Add the accuracy of the movie according to the model
                movie = movies[i]
                movie['accuracy'] = p[0]
                suggestion = np.append(suggestion, movie)
                print movie['id'], " added with prediction ", movie['accuracy']
                added += 1
            i += 1
        toFind -= added
    
    return suggestion
    
          
    