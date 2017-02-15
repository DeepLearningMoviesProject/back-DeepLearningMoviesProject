#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 14:32:28 2017

@author: Kaito
"""

import numpy as np
import tmdbsimple as tmdb
from string import punctuation

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
        words += _format(keyword["name"]).split()

    return words


def getGenres(movieInfo):
    """
        Extract keywords from tmdb keyword's dictionary 
        
        return:
            array of string containing each keyword
    """
    
    return [ _format(genre["name"]) for genre in movieInfo["genres"] ]

def getRating(movieInfo):
    """
        Retrieve the movie's Rating
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            int
    """
    
    return movieInfo["vote_average"]

def getTitle(movieInfo):
    """
        Retrieve the movie's Title
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            string
    """
    
    overview = "".join(c for c in movieInfo["title"] if c not in punctuation)
    overview = overview.split()
    return overview

def getMovie(id): 
    """
        Parameters:
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
    
    genres = { _format(g["name"]):i for i, g in enumerate(listGenres) }

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
    
def getOverview(movieInfo):
    """
        Retrieve the movie's Overview
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            string or None if overview doesn't exist
    """
    
    if movieInfo["overview"] is not None:
        return _format("".join(c for c in movieInfo["overview"] if c not in punctuation))
    else: 
        return None
    
    
    
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


def getRuntime(movieInfo):
    """
        Retrieve the movie's runtime
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            int
    """
    
    return 0 if movieInfo["runtime"] is None else movieInfo["runtime"]


def getYear(movieInfo):
    """
        Retrieve the release Year of the movie
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            int 
    """
    return int(movieInfo["release_date"][:4])

def getBudget(movieInfo):
    """
        Retrieve the Budget of the movie
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            int 
    """
    return int(movieInfo["budget"])


def getProdCompagnies(movieInfo):
    """
        Retrieve production compagnies of the movie
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            array of String of compagnies
    """
    return [ info["name"] for info in movieInfo["production_companies"] ]


def getLanguage(movieInfo):
    """
        Retrieve the movie's spoken language
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            array of String
    """
    return [ _format(language["name"]) for language in movieInfo["spoken_languages"] ]
    
    
def getBelongsTo(movieInfo):
    """
        Retrieve the movie's collection
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            String
    """
    
    belongsTo = movieInfo["belongs_to_collection"]
    
    return belongsTo is not None and belongsTo["name"] or belongsTo

def _format(text):
    """
        Convert the given text in UTF-8 lowercase 
        
        Parameters:
            text -> String
        return:
            text formated
    """
    return text.lower().encode("UTF-8")

if __name__ == "__main__":
    
    movie = getMovie(205056)
    response = movie.info()
    
    print movie.reviews()
    
    #for people in movie.credits()["crew"]:
    #   print "Name: %s - %s" %(people["name"], people["job"]) # important: Director
    
    print "############################"
    
    
    #for people in movie.credits()["cast"]: print "%s" %(people["name"])
    
    print "############################"
    
    print "Title: %s" %(response["title"])
    print "Keywords: %s" %(" ".join(getKeywords(movie.keywords())))
    print "Genres: %s" %(" ".join(getGenres(response)))
    print "Overview: %s" %(response["overview"])
    print "Vote: %s" %(response["vote_average"])
    print "Budget: %s" %(response["budget"])
    
    print "runtime: {}".format(getRuntime(response))
    
    print "------------------------------"
    
    #for key in response.keys(): print "%s: %s" %(key, response[key])
        
    print "------------------------------"
    
    #for key in response.keys(): print key,
