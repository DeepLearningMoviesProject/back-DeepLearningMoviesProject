#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 14:32:28 2017

@author: Kaito
"""

import numpy as np
import tmdbsimple as tmdb
from string import punctuation
from datetime import datetime

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
            array containing movies' credits
    """
    
    return [ movie.credits() for movie in movies ]


def getKeywords(tmdbKeywords):
    """
        Extract keywords from tmdb keyword's dictionary 
        
        return:
            array of string containing each keyword
    """
    
    words = []
    if "keywords" in tmdbKeywords:
        for keyword in tmdbKeywords["keywords"]:
            words += _format(keyword["name"]).split()
    else:
        raise AttributeError("%s instance has no attribute keywords" % tmdbKeywords)        
    return words


def getGenres(movieInfo):
    """
        Extract genres from tmdb keyword's dictionary 
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            array of string containing each genre
    """
    if "genres" in movieInfo:
        return [ _format(genre["name"]) for genre in movieInfo["genres"] ]
    else:
        raise AttributeError("%s instance has no attribute genre" % movieInfo)    

def getRating(movieInfo):
    """
        Retrieve the movie's Rating
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            int
    """
    if "vote_average" in movieInfo:
        return movieInfo["vote_average"]        
    else:
        raise AttributeError("%s instance has no attribute vote_average (rating)" % movieInfo)    

def getTitle(movieInfo):
    """
        Retrieve the movie's Title
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            string
    """
    if "title" in movieInfo:
        #We remove the punctuation
        title = "".join(c for c in movieInfo["title"] if c not in punctuation)
        #We return the title as a list of words in the right format
        return [ _format(w) for w in title.split() ]
    else:
        raise AttributeError("%s instance has no attribute title" % movieInfo)    


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
    if "crew" in movieCredit:
        return [ _format(people["name"]) for people in movieCredit["crew"] if people["job"].lower() == "director" ]
    else:
        raise AttributeError("%s instance has no attribute crew" % movieCredit)    
    
def getOverview(movieInfo):
    """
        Retrieve the movie's Overview
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            string (empty if overview doesn't exist)
    """
    
    if "overview" in movieInfo:
        overview = "" if movieInfo["overview"] is None else movieInfo["overview"]
        return _format("".join(c for c in overview if c not in punctuation))
    else: 
        raise AttributeError("The parameter has no attribute 'overview'")
    
    
    
def getActors(movieCredit):
    """
        Retrieve the movie's Actors
        
        Parameter:
            list of credits from TMDB movie object
            
        return:
            String array representing the 4 first movie's actors
    """
    if "cast" in movieCredit:
        actors = movieCredit["cast"]
        nbActors = 4 if len(actors) >= 4 else len(actors)
        
        return [ _format(actor["name"]) for actor in actors [:nbActors]]
    else:
        raise AttributeError("%s instance has no attribute crew" % movieCredit)    


def getRuntime(movieInfo):
    """
        Retrieve the movie's runtime
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            int
    """
    if "runtime" in movieInfo:
        return 0 if movieInfo["runtime"] is None else movieInfo["runtime"]
    else:
        raise AttributeError("%s instance has no attribute runtime" % movieInfo)    


def getYear(movieInfo):
    """
        Retrieve the release Year of the movie
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            int 
    """
    if "release_date" in movieInfo:
        date = movieInfo["release_date"]
        if (date != '') :
            return datetime.strptime(date, "%Y-%m-%d").year
        else:
            return 0
    else:
        raise AttributeError("%s instance has no attribute release_date" % movieInfo)    

def getBudget(movieInfo):
    """
        Retrieve the Budget of the movie
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            int 
    """
    if "budget" in movieInfo:
        return int(movieInfo["budget"])
    else:
        raise AttributeError("%s instance has no attribute budget" % movieInfo)  


def getProdCompagnies(movieInfo):
    """
        Retrieve production companies of the movie
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            array of String of companies
    """
    if "production_companies" in movieInfo:
        return [ _format(info["name"]) for info in movieInfo["production_companies"] ]
    else:
        raise AttributeError("%s instance has no attribute production_companies" % movieInfo)    


def getLanguage(movieInfo):
    """
        Retrieve the movie's spoken language
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            array of String
    """
    if "spoken_languages" in movieInfo:
        return [ _format(language["name"]) for language in movieInfo["spoken_languages"] ]
    else:
        raise AttributeError("%s instance has no attribute spoken_languages" % movieInfo)  
    
    
def getBelongsTo(movieInfo):
    """
        Retrieve the fact that a movie belongs to a collection
        
        Parameter:
            movieInfo -> dictionary of Movie.info()
        return:
            Boolean that tells whether the movie belongs to a collection
    """
    if "belongs_to_collection" in movieInfo:
        belongsTo = movieInfo["belongs_to_collection"]
        return belongsTo is not None and belongsTo["name"] or belongsTo
    else:
        raise AttributeError("%s instance has no attribute belongs_to_collection" % movieInfo)  

def _format(text):
    """
        Convert the given text in UTF-8 lowercase 
        
        Parameters:
            text -> String
        return:
            text formated
    """
    
    if isinstance(text, unicode):
        return text.lower().encode("UTF-8")
    elif isinstance(text, str):
        return text.lower() 
