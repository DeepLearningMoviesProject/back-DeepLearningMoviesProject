# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 17:09:54 2017

@author: darke
"""


from MovieProject.preprocessing.tools import (getMovies, getKeywords, getDirectors, getActors, getCredits,
                                              loadGloveDicFromFile, getGenres, getTmdbGenres, loadD2VModel, SIZE_VECTOR)
from MovieProject.resources import GLOVE_DICT_FILE, D2V_FILE
from words import meanWords, wordsToGlove
from texts import textToVect

import numpy as np
from string import punctuation
from enum import Enum


class People(Enum):
    ACTOR = 1
    DIRECTOR = 2


def preprocess(idMovies, doTitles=False, doRating=False, doOverviews=False, doKeywords=False, doGenres=False, doActors=False, doDirectors=False):
    """
        Parameter : 
            idMovies : int array of ids of Movies you want to process datas
            do... : the movies' data you want to extract
        Return : the dictionnary ready for the classifier
    """

    mat = preprocessMatrix(idMovies, mTitles=doTitles, mKeywords=doKeywords, mOverviews=doOverviews, mRating=doRating, mGenres=doGenres, mActors=doActors, mDirectors=doDirectors)
    
    return prepareDico(mat, doTitles=doTitles, doRating=doRating, doOverviews=doOverviews, doKeywords=doKeywords, doGenres=doGenres, doActors=doActors, doDirectors=doDirectors)


def preprocessMatrix(idMovies, mTitles=False, mKeywords=False, mOverviews=False, mRating=False, mGenres=False, mActors=False, mDirectors=False):
    """
        
        Parameter:
            idMovies -> array of movie's id from tmdb
            mTitles, mKeywords, mOverviews, mRating, mGenres, mActors, mDirectors -> boolean (default: False) indicates which matrix to process
            
        return:
            dictionary of label:matrix, where label is name of matrix processed
    """


    matrix = {}
    
    if mKeywords or mActors or mDirectors or mTitles:
        dicoGlove = loadGloveDicFromFile(GLOVE_DICT_FILE)
    
    if mOverviews:
        modelD2V = loadD2VModel(D2V_FILE)
    
    movies = getMovies(idMovies)    
    
    infos = []
    keywords = []
    credits = []

    print "Loading data from TMDB"
    cpt = 0
    for i in range(len(movies)):
        movie = movies[i]
        
        try:
            # If those request failed, doesn't append results to arrays
            if mOverviews or mTitles or mRating or mGenres: info = movie.info()
            if mKeywords: keyword = movie.keywords()
            if mActors or mDirectors: credit = movie.credits()
            
            if mOverviews or mTitles or mRating or mGenres:infos.append(info)
            if mKeywords: keywords.append(keyword)
            if mActors or mDirectors: credits.append(credit)
        except:
            print "Error, movie " + str (movie) + " NOT FOUND"
            
        cpt += 1
        if(cpt > len(movies)/20.):
            print "%.0f%% requests loaded..." %(100*i/(1.0*len(movies)))
            cpt = 0

    if mKeywords:
        print "Processing Keywords"
        matrix["keywords"] = keywordsProcessing(keywords, dicoGlove)
    
    if mOverviews:
        print "Processing Overviews..."
        matrix["overviews"] = overviewProcessingD2V(infos, modelD2V)
    
    if mTitles:
        print "Processing titles..."
        matrix["titles"] = titlesProcessing(infos, dicoGlove)
    
    if mRating:
        print "Processing rating..."
        matrix["rating"] = ratingProcessing(infos)
        
    if mGenres:
        print "Processing genres..."
        matrix["genres"] = genresProcessing(infos)
    
    if mDirectors:
        print "Processing directors..."
        matrix["directors"] = peopleProcessing(credits, dicoGlove, People.DIRECTOR)
    
    if mActors:
        print "Processing actors..."
        matrix["actors"] = peopleProcessing(credits, dicoGlove, People.ACTOR)
    
    return matrix


def _concatData(listMatrix):
    '''
        Recursive function that concats a list of matrixes
        The matrix must have the same dimensions

        returns : a unique matrix that contains all the data that were on the list of matrix
    '''
    if(len(listMatrix)==0):
        return np.array([])
        
    if(len(listMatrix)==1):
        return listMatrix[0]
    
    return np.hstack((listMatrix[0], _concatData(listMatrix[1:])))

def prepareDico(matrix, doTitles=False, doRating=False, doOverviews=False, doKeywords=False, doGenres=False, doActors=False, doDirectors=False):
    '''
        Parameters : 
            matrixes : the matrixes that have been preprocessed
            do... : the boolean that tells which matrix has been preprocessed and can be set in the dictionnary
        return : the dictionnary ready for the classifier with the following matrix if required :
            data : the matrix with the data concatenate correctly (titles, rating, overviews)
            genres : matrix for the genres
            actors : matrix for the actors
            directors : matrix for the directors
    '''
    dico = {}
    toConcat = []
    

    if(doTitles):
        toConcat.append(matrix["titles"])

    if(doRating):
        toConcat.append(matrix["rating"])

    if(doOverviews):
        toConcat.append(matrix["overviews"])

    if(doKeywords):
        toConcat.append(matrix["keywords"])

    concatMatrix = _concatData(toConcat)
    
    if concatMatrix.size:
        dico["data"] = concatMatrix


    if(doGenres):
        dico["genres"] = matrix["genres"]

    if(doActors):
        dico["actors"] = matrix["actors"]

    if(doDirectors):
        dico["directors"] = matrix["directors"]
    
    return dico
    

def overviewProcessingD2V(infos, model):
    """
        Parameter : 
            infos array of movies you want to get overviews with
            the Doc2Vec model
        Return : 
            ndarray. Matrix of Overviews values calculated by Glove. One line by movie.
    """
    
    meanMatrixOverview = np.empty([len(infos), SIZE_VECTOR])  
    
    for i in range(len(infos)):
        info = infos[i]        
        
        overview = "".join(c for c in info["overview"] if c not in punctuation)       
        
        meanMatrixOverview[i] = textToVect(overview, model)

    return meanMatrixOverview
    
def overviewProcessing(infos, dicoGlove):
    """
        Parameter : 
            infos array of movies you want to get overviews with
            the Glove dictionnary (dicoGlove)
        Return : 
            ndarray. Matrix of Overviews values calculated by Glove. One line by movie.
    """
    
    sizeVector = dicoGlove[dicoGlove.keys()[0]].shape[0]
    meanMatrixOverview = np.empty([len(infos), sizeVector])  
    
    for i in range(len(infos)):
        info = infos[i]        
        
        overview = "".join(c for c in info["overview"] if c not in punctuation)       
        words = []
            
        for w in overview.split():
            words.append(w.lower().encode('UTF-8'))
     
        gArray, wSize = wordsToGlove(words, dicoGlove)
        
        meanMatrixOverview[i] = meanWords(gArray, wSize)

    return meanMatrixOverview
    
def keywordsProcessing(moviesKeywords, dicoGlove):
    """
        Parameter : keywords array of movies you want to process keywords with
                    the Glove dictionnary (dicoGlove)
        Return : Matrix of keywords values calculated by Glove. One line by movie.
    """
    
    sizeVector = dicoGlove[dicoGlove.keys()[0]].shape[0]
    meanMatrixKeywords = np.empty([len(moviesKeywords), sizeVector]) 
    
    for i in range(len(moviesKeywords)):
        keyword = moviesKeywords[i]

        keywords = getKeywords(keyword)
        gArray, wSize = wordsToGlove(keywords, dicoGlove)
        
        meanMatrixKeywords[i] = meanWords(gArray, wSize)
           
    return meanMatrixKeywords


def titlesProcessing(infos, dicoGlove):
    """
        Parameter : 
            infos array of movies you want to process titles with
            the Glove dictionnary (dicoGlove)
        Return : 
            ndarray. Matrix of titles values calculated by Glove. One line by movie.
    """
    
    sizeVector = dicoGlove[dicoGlove.keys()[0]].shape[0]
    meanMatrixTitles = np.empty([len(infos), sizeVector]) 
    
    for i in range(len(infos)):        
        info = infos[i]
        
        overview = "".join(c for c in info["title"] if c not in punctuation)
        overview = overview.split()
        words = []
            
        for w in overview:
            words += w.lower().encode('UTF-8')
            
        gArray, wSize = wordsToGlove(words, dicoGlove)
        
        meanMatrixTitles[i] = meanWords(gArray, wSize)

    return meanMatrixTitles

def ratingProcessing(infos):
    """
        Parameter : 
            infos array of movies you want to process rating with
            the Glove dictionnary (dicoGlove)
        Return : 
            ndarray. Matrix of rating values calculated by Glove. One line by movie.
    """
    
    meanMatrixRating = np.empty([len(infos), 1])
    for i in range(len(infos)):  
        meanMatrixRating[i] = infos[i]["vote_average"]/10.0

    return meanMatrixRating



def genresProcessing(infos):
    """
        Parameter:
            infos array of movies you want to process rating with
            the Glove dictionnary (dicoGlove)
        Return:
            ndarray. Matrix of genres where each value is 1 if genre is present, 0 otherwise
    
    """
    
    TMDB_GENRES = getTmdbGenres()
    
    genresArray = np.empty([len(infos), len(TMDB_GENRES.keys())])

    for i in range(len(infos)):
        info = infos[i]
  
        genresVect = np.zeros(len(TMDB_GENRES.keys()))

        for genre in getGenres(info["genres"]):
            try:
                genresVect[TMDB_GENRES[genre]] = 1
            except:
                print "Unknown genre for %s -> %s" %(info["title"], genre)

        genresArray[i] = genresVect        
            
    return genresArray


def peopleProcessing(moviesCredits, dicoGlove, kindOfPeople):
    """
        Parameter:
            moviesCredits -> array of movie's moviesCredits you want to process people with
                      the Glove dictionnary (dicoGlove)
            dicoGlove -> GloVe dictionary
            kindOfPeople -> People enum type, indicating is Directors or Actors 
        Return:
            ndarray. Matrix of people values calculated by Glove. One line by movie.
    """
    
    if not isinstance(kindOfPeople, People):
        raise ValueError("kindOfPeople must be an instance of People enum class")
        
    sizeVector = dicoGlove[dicoGlove.keys()[0]].shape[0]
    meanMatrixPeople = np.empty([len(moviesCredits), sizeVector]) 
    names = []
    
    for i in range(len(moviesCredits)):
        credit = moviesCredits[i]
        
        if kindOfPeople is People.DIRECTOR: names = getDirectors(credit)
        elif kindOfPeople is People.ACTOR: names = getActors(credit)
        
        words = []
        for name in names:
            words += name.lower().encode('UTF-8').split()
        
        gArray, wSize = wordsToGlove(words, dicoGlove)        
        meanMatrixPeople[i] = meanWords(gArray, wSize)
    
    return meanMatrixPeople
