# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 17:09:54 2017

@author: darke
"""


from apiTMDB import getGenres, getMovies, getKeywords
from MovieProject.resources import GLOVE_DICT_FILE
from words import meanWords, wordsToGlove
from .tools import loadGloveDicFromFile

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
    
    for movie in movies:
        try:
            r = movie.info()
            responses.append(r)
        except:
            print "Error, movie " + str (movie) + " NOT FOUND"

    print "Processing Overview..."
    meanOverview = overviewProcessing(responses, dicoGlove)
    print "Processing keywords..."
    meanKeywords = keywordsProcessing(movies, dicoGlove)
    print "Processing titles..."
    meanTitles = titlesProcessing(responses, dicoGlove)
    print "Processing rating..."
    meanRating = ratingProcessing(responses, dicoGlove)
    
    finalMatrix = np.concatenate(np.concatenate(np.concatenate(meanOverview, meanKeywords), meanTitles), meanRating)
    return finalMatrix
    
def overviewProcessing(responses, dicoGlove):
    """
        Parameter : 
            Responses array of movies you want to get overviews with
            the Glove dictionnary (dicoGlove)
        Return : 
            ndarray. Matrix of Overviews values calculated by Glove. One line by movie.
    """
    
    meanArray = []    
    
    for response in responses:        
        
        overview = "".join(c for c in response["overview"] if c not in punctuation)       
        overview = overview.split()
        words = []
            
        for w in overview:
            words += w.lower().encode('UTF-8')
     
        gArray = wordsToGlove(words, dicoGlove)
        print meanWords(gArray)
        meanArray.append(meanWords(gArray))

    return np.array(meanArray)
    
def keywordsProcessing(movies, dicoGlove):
    """
        Parameter : movies array of movies you want to process keywords with
                    the Glove dictionnary (dicoGlove)
        Return : Matrix of keywords values calculated by Glove. One line by movie.
    """
    
    meanArray = []    
    for movie in movies:        
        try:
            response = movie.keywords()
            keywords = getKeywords(response)
            gArray = wordsToGlove(keywords, dicoGlove)
            meanArray.append(meanWords(gArray))
        except:
             pass   
    return meanArray

def titlesProcessing(responses, dicoGlove):
    """
        Parameter : 
            Responses array of movies you want to process titles with
            the Glove dictionnary (dicoGlove)
        Return : 
            ndarray. Matrix of titles values calculated by Glove. One line by movie.
    """
    
    meanArray = []  
    
    for response in responses:        

        overview = "".join(c for c in response["title"] if c not in punctuation)
        overview = overview.split()
        words = []
            
        for w in overview:
            words += w.lower().encode('UTF-8')
     
        gArray = wordsToGlove(words, dicoGlove)
        meanArray.append(meanWords(gArray))

    return meanArray

def ratingProcessing(responses, dicoGlove):
    """
        Parameter : 
            Responses array of movies you want to process rating with
            the Glove dictionnary (dicoGlove)
        Return : 
            ndarray. Matrix of rating values calculated by Glove. One line by movie.
    """
    
    meanArray = []
    
    for response in responses:        
        meanArray.append(response["vote_average"]/10.0)

    return meanArray
