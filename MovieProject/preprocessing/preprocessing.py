# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 17:09:54 2017

@author: darke
"""


from MovieProject.preprocessing.tools import getMovies, getKeywords, loadGloveDicFromFile
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
    
    for movie in movies:
        try:
            r = movie.info()
            responses.append(r)
        except:
            print "Error, movie " + str (movie) + " NOT FOUND"
    print "Processing keywords..."
    meanKeywords = keywordsProcessing(movies, dicoGlove)
    print "Processing Overview..."
    meanOverviews = overviewProcessing(responses, dicoGlove)
    print "Processing titles..."
    meanTitles = titlesProcessing(responses, dicoGlove)
    print "Processing rating..."
    meanRating = ratingProcessing(responses, dicoGlove)
    
    finalMatrix = np.hstack((np.hstack((np.hstack((meanKeywords,meanOverviews)),meanTitles)),meanRating))
    return finalMatrix
    
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
