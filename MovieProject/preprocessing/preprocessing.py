# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 17:09:54 2017

@author: darke
"""


from MovieProject.preprocessing.tools import getMovies, getKeywords, loadGloveDicFromFile, getGenres, getTmdbGenres
from MovieProject.resources import GLOVE_DICT_FILE
from words import meanWords, wordsToGlove

import numpy as np
from string import punctuation





def preprocess(idMovies):
    """
        Parameter : 
            int array of ids of Movies you want to process datas
        Return : 
            ndarray. Matrix of KeyWords,Titles,Overview and rating values calculated 
            by Glove. One line by movie.
    """
    
    print "Loading GloVe dico"
    dicoGlove = loadGloveDicFromFile(GLOVE_DICT_FILE)
    movies = getMovies(idMovies)
    responses = []
    infoUsers = len(movies)/100.0*10
    i = 0
    cpt = 5
    
    for movie in movies:
        try:
            r = movie.info()
            responses.append(r)
        except:
            print "Error, movie " + str (movie) + " NOT FOUND"
        i += 1
        if(i > infoUsers):
            print str(cpt)+"% requests loaded..."
            cpt += 5
            i = 0
    print "50% requests loaded..."
    meanKeywords = keywordsProcessing(movies, dicoGlove)
    print "100% requests loaded and keywords preprocessed ! "
    print "Processing Overview..."
    meanOverviews = overviewProcessing(responses, dicoGlove)
    print "Processing titles..."
    meanTitles = titlesProcessing(responses, dicoGlove)
    print "Processing rating..."
    meanRating = ratingProcessing(responses, dicoGlove)
    
    finalMatrix = np.hstack((np.hstack((np.hstack((meanKeywords,meanOverviews)),meanTitles)),meanRating))
    
    print "Processing genres..."
    genres = genresProcessing(responses)
    return finalMatrix, genres
    
def overviewProcessing(responses, dicoGlove):
    """
        Parameter : 
            Responses array of movies you want to get overviews with
            the Glove dictionnary (dicoGlove)
        Return : 
            ndarray. Matrix of Overviews values calculated by Glove. One line by movie.
    """
    
    meanMatrixOverview = []    
    i = 0
    for response in responses:        
        
        overview = "".join(c for c in response["overview"] if c not in punctuation)       
        overview = overview.split()
        words = []
            
        for w in overview:
            words += w.lower().encode('UTF-8')
     
        gArray = wordsToGlove(words, dicoGlove)
        
        if i == 0:
            i = 1
            meanMatrixOverview = meanWords(gArray)
        else:
            meanMatrixOverview = np.vstack([meanMatrixOverview,meanWords(gArray)])

    return meanMatrixOverview
    
def keywordsProcessing(movies, dicoGlove):
    """
        Parameter : movies array of movies you want to process keywords with
                    the Glove dictionnary (dicoGlove)
        Return : Matrix of keywords values calculated by Glove. One line by movie.
    """
    
    meanMatrixKeywords = []    
    i = 0 
    infoUsers = len(movies)/100.0*10
    p = 0
    cpt = 55
    for movie in movies:        
        try:
            response = movie.keywords()
            keywords = getKeywords(response)
            gArray = wordsToGlove(keywords, dicoGlove)
            
            if i == 0:
                i = 1
                meanMatrixKeywords = meanWords(gArray)
            else:
                meanMatrixKeywords = np.vstack([meanMatrixKeywords,meanWords(gArray)])
        except:
             pass   
        p += 1
        if(p > infoUsers):
           print str(cpt)+"% requests loaded..."
           cpt += 5
           p = 0
    return meanMatrixKeywords

def titlesProcessing(responses, dicoGlove):
    """
        Parameter : 
            Responses array of movies you want to process titles with
            the Glove dictionnary (dicoGlove)
        Return : 
            ndarray. Matrix of titles values calculated by Glove. One line by movie.
    """
    
    meanMatrixTitles = []  
    i = 0
    for response in responses:        

        overview = "".join(c for c in response["title"] if c not in punctuation)
        overview = overview.split()
        words = []
            
        for w in overview:
            words += w.lower().encode('UTF-8')
            
        gArray = wordsToGlove(words, dicoGlove)
        if i == 0:
            i = 1
            meanMatrixTitles = meanWords(gArray)
        else:
            meanMatrixTitles = np.vstack([meanMatrixTitles,meanWords(gArray)])

    return meanMatrixTitles

def ratingProcessing(responses, dicoGlove):
    """
        Parameter : 
            Responses array of movies you want to process rating with
            the Glove dictionnary (dicoGlove)
        Return : 
            ndarray. Matrix of rating values calculated by Glove. One line by movie.
    """
    
    meanMatrixRating = []
    i = 0
    for response in responses:  
        if i == 0:
            i = 1
            meanMatrixRating = response["vote_average"]/10.0
        else:
            meanMatrixRating = np.vstack([meanMatrixRating,response["vote_average"]/10.0])

    return meanMatrixRating



def genresProcessing(responses):
    """
        Parameter:
            Responses array of movies you want to process rating with
            the Glove dictionnary (dicoGlove)
        Return:
            ndarray. Matrix of genres where each value is 1 if genre is present, 0 otherwise
    
    """
    
    TMDB_GENRES = getTmdbGenres()
    
    genresArray = np.empty([len(responses), len(TMDB_GENRES.keys())])

    for i in range(len(responses)):
        response = responses[i]
  
        genresVect = np.zeros(len(TMDB_GENRES.keys()))

        for genre in getGenres(response["genres"]):
            try:
                genresVect[TMDB_GENRES[genre]] = 1
            except:
                print "Unknown genre for %s -> %s" %(response["title"], genre)

        genresArray[i] = genresVect        
            
    return genresArray

