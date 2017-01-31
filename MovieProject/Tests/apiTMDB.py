#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 14:32:28 2017

@author: Kaito
"""

import numpy as np
import tmdbsimple as tmdb

tmdb.API_KEY = 'ff3f07bf3577a496a2f813488eb29980'

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
    
    genres = []
    for genre in tmdbGenres:
        genres += genre["name"].lower().encode('UTF-8').split()
        
    return genres
    

def getMovie(id): 
    """ Parameters:
            ids: movie's id
        return:
            movie object
    """
    
    return tmdb.Movies(id)

    


if __name__ == "__main__":
    
    movie = getMovie(415)
    response = movie.info()
    
    #for people in movie.credits()["crew"]:
    #   print "Name: %s - %s" %(people["name"], people["job"]) # important: Director
    
    print "############################"
    
    
    #for people in movie.credits()["cast"]: print "%s" %(people["name"])
    
    print "############################"
    
    print "Title: %s" %(response["title"])
    print "Keywords: %s" %(" ".join(getKeywords(movie.keywords())))
    print "Genres: %s" %(" ".join(getGenres(response["genres"])))
    print "Overview: %s" %(response["overview"])
    print "Vote: %s" %(response["vote_average"])
    print "Budget: %s" %(response["budget"])
    
    print "------------------------------"
    
    #for key in response.keys(): print "%s: %s" %(key, response[key])
        
    print "------------------------------"
    
    #for key in response.keys(): print key,
