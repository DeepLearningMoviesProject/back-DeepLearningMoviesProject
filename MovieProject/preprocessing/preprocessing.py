# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 17:09:54 2017

@author: darke
"""
from MovieProject.preprocessing.words import *
from MovieProject.tests.apiTMDB import *
import numpy as np
GLOVE_FILE = 'GLOVE/glove.6B.50d.txt'
DICO_FILE = "GLOVE/glove_dico.npy"



def preprocess(idMovies):
    """
        Parameter : int array of ids of Movies you want to process datas
        Return : Matrix of KeyWords,Titles,Overview and rating values calculated 
        by Glove. One line by movie.
    """
    
    print "Loading GloVe dico"
    dicoGlove = loadGloveDicFromFile(DICO_FILE)
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
        Parameter : responses array of movies you want to get overviews with
                    the Glove dictionnary (dicoGlove)
        Return : Matrix of Overviews values calculated by Glove. One line by movie.
    """
    
    meanArray = []    
    
    for response in responses:        
        
        overview = "".join(c for c in response["overview"] if c not in string.punctuation)       
        overview = overview.split()
        words = []
            
        for w in overview:
            words += w.lower().encode('UTF-8')
     
        gArray = wordsToGlove(words, dicoGlove)
        print meanWords(gArray)
        meanArray.append(meanWords(gArray))

    t = np.array(meanArray)
    return t
    
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
        Parameter : responses array of movies you want to process titles with
                    the Glove dictionnary (dicoGlove)
        Return : Matrix of titles values calculated by Glove. One line by movie.
    """
    
    meanArray = []  
    
    for response in responses:        

        overview = "".join(c for c in response["title"] if c not in string.punctuation)
        overview = overview.split()
        words = []
            
        for w in overview:
            words += w.lower().encode('UTF-8')
     
        gArray = wordsToGlove(words, dicoGlove)
        meanArray.append(meanWords(gArray))

    return meanArray

def ratingProcessing(responses, dicoGlove):
    """
        Parameter : responses array of movies you want to process rating with
                    the Glove dictionnary (dicoGlove)
        Return : Matrix of rating values calculated by Glove. One line by movie.
    """
    meanArray = []
    
    for response in responses:        
        meanArray.append(response["vote_average"]/10.0)

    return meanArray
