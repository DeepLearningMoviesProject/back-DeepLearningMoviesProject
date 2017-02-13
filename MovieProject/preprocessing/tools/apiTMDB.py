#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 14:32:28 2017

@author: Kaito
"""

import numpy as np
import tmdbsimple as tmdb

from os.path import isfile
from MovieProject.resources import GENRES_FILE


tmdb.API_KEY = 'ff3f07bf3577a496a2f813488eb29980'

    
def getMovies(idMovies):
    """
        Retrieve list of TMDB Movie object from a list of ids
        
        Parameters:
            idMovies -> array of int 
        return:
           Array of TMDB Movie object 
    """

    return [ getMovie(idMovie) for idMovie in idMovies ]


def getCredits(movies):
    """
        Retrieve credits from a list of movies
        
        Parameter:
            movies -> list of TMDB Movie object
        return:
            array containing movie's credits
        
    """
    
    return [ movie.credits() for movie in movies ]


def getKeywords(tmdbKeywords={}):
    """
        Extract keywords from tmdb keyword's dictionary 
        
        return:
            array of string containing each keyword
    """
    
    words = []    
    for keyword in tmdbKeywords["keywords"]:
        words += keyword["name"].lower().encode('UTF-8').split()

    return words


def getGenres(tmdbGenres=[]):
    """
        Extract keywords from tmdb keyword's dictionary 
        
        return:
            array of string containing each keyword
    """
        
    return [ genre["name"].lower().encode('UTF-8') for genre in tmdbGenres ]
    

def getMovie(id): 
    """ Parameters:
            ids: movie's id
        return:
            movie object
    """
    
    return tmdb.Movies(id)

def saveTmdbGenres():
    """
        Download genres from TMDB and save it into binary file
    """
        
    listGenres = tmdb.Genres().list()["genres"]
    
    genres = { g["name"].lower().encode('UTF-8'):i for i, g in enumerate(listGenres) }

    np.save(GENRES_FILE, np.asarray([genres]))
    
    
def getTmdbGenres():
    """
        Get dictionary of genres from TMDB associated with an index
        
        return:
            dict object {"String":int,...}
    """

    #If the file is not present in the resource, creates it 
    if not isfile(GENRES_FILE):
        saveTmdbGenres()

    return np.load(GENRES_FILE)[0]

    
def getDirectors(movieCredit):
    """
        Retrieve the movie's Director
        
        Parameter:
            list of credits from TMDB movie object
            
        return:
            String  array representing the movie's directors
    """

    
    return [ people["name"] for people in movieCredit["crew"] if people["job"].lower() == "director" ] 
    
def getActors(movieCredit):
    """
        Retrieve the movie's Actors
        
        Parameter:
            list of credits from TMDB movie object
            
        return:
            String array representing the 4 first movie's actors
    """

    actors = movieCredit["cast"]
    nbActors = 4 if len(actors) >= 4 else len(actors)
    
    return [actor["name"] for actor in actors [:nbActors]]


#if __name__ == "__main__":
#    
#    movie = getMovie(415)
#    response = movie.info()
#    
#    #for people in movie.credits()["crew"]:
#    #   print "Name: %s - %s" %(people["name"], people["job"]) # important: Director
#    
#    print "############################"
#    
#    
#    #for people in movie.credits()["cast"]: print "%s" %(people["name"])
#    
#    print "############################"
#    
#    print "Title: %s" %(response["title"])
#    print "Keywords: %s" %(" ".join(getKeywords(movie.keywords())))
#    print "Genres: %s" %(" ".join(getGenres(response["genres"])))
#    print "Overview: %s" %(response["overview"])
#    print "Vote: %s" %(response["vote_average"])
#    print "Budget: %s" %(response["budget"])
#    
#    print "------------------------------"
#    
#    #for key in response.keys(): print "%s: %s" %(key, response[key])
#        
#    print "------------------------------"
    
    #for key in response.keys(): print key,
