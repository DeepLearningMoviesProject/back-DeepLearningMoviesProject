# -*- coding: utf-8 -*-
"""
Created on Thu Feb 07 15:08 2017

@author: elsa
"""
from __future__ import unicode_literals

import numpy as np
from random import randint
from MovieProject.preprocessing import preprocess
from keras.models import Sequential
#from MovieProject.preprocessing.tools import getMovie
import tmdbsimple as tmdb

batch = 500

def predict(movie, model):
    '''
        Predicts the class of the movie according to the model
        
        Parameters : 
            movie : the id of the movie we want to know the class of, the id must exist
            model : the model that matches the taste of the user

        returns : a boolean to tell if the movie is liked or not
    '''

    arrayMovie = np.array([movie])
    
    print "movies prediction : ", arrayMovie

    T, G = preprocess(arrayMovie)
    
    print "preprocessing done for the movie, start the prediction"

    #TODO : The prediction must be done with the model
    pred = 1 #model.predict([T, G], batch_size=batch, verbose=0)

    return pred
    
def pickNMovie(n):
    '''
        Get n movies from tmdb, max 20

        return : a random list of movies
    '''
    #Pick a random page from Discover
    pages_max = 1000
    p = randint(0,pages_max)
    response = tmdb.Discover().movie(page=p)
    pageRes = response['results']
    
    nbMovies = len(pageRes)
    print 'nb movies : ', nbMovies

    if(n==1):
        mIndex = randint(0,nbMovies)
        movie = pageRes[mIndex]['id']
        return np.array(movie)
    else:
        n = np.minimum(n, nbMovies)
        movies = np.zeros(n)
        for i in range(0,n):
            movies[i] = pageRes[i]['id']
        return movies

def suggestNMovies(model, n):
    """
        Suggests n movies for the person that has this model
        
        Parameters :
            model : the model that the suggestion fits
            n : the amount of suggestions to return
        
        return : a list of n suggestions that are liked according to the model
    """
    suggestion = np.array([])
    pickSize = 20
    print "n : ", n, " sugg.len : ", len(suggestion)
    
    while(len(suggestion) < n):
        remains_size = n - len(suggestion)
        movies = pickNMovie(np.minimum(pickSize, remains_size))
        
        #checks if movies are not already in suggestion and remove them if so
        inter = np.intersect1d(suggestion, movies)
        if( inter.size != 0):
            suggestion = np.setdiff1d(movies, inter)
            
        #Keep in suggestion the movies that matches the model
        for m in movies:
            if(predict(m, model)):
                suggestion = np.append(suggestion, m)

    return suggestion
    