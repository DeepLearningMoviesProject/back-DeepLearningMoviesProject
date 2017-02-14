# -*- coding: utf-8 -*-
"""
Pre-processes the data we want to provide to the learning model.

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

import threading, time



class _RunRequest(threading.Thread):
    
    def __init__(self, result, target, *args):
        """
            Run request from TMDB into another thread and assure that less 40 requests
            are send in 10 seconds
       
            Parameters:
                result -> mutable who will contain the result of method target
                target -> method to run in another thread
                args -> param of the function target
        """
        self._target = target
        self._args = args
        self.res = result
        self.maxTime = 0.8
        threading.Thread.__init__(self)
 
    def run(self):
        start = time.time()
        self.res.append(self._target(*self._args))
        timeResquest = time.time() - start
        
        if self.maxTime - timeResquest > 0 : time.sleep(self.maxTime - timeResquest)
        

class People(Enum):
    ACTOR = 1
    DIRECTOR = 2
    
    
class Preprocessor():
    
    def __init__(self, **kwargs):
        """
        
        """
        
        self.toDo = { "titles" : False,
                      "rating" : False,
                      "overviews" : False,
                      "keywords" : False,
                      "genres" : False,
                      "actors" : False,
                      "directors" : False }
        
        for key, value in kwargs.items():
            if key in self.toDo:
                self.toDo[key] = value
        
                
        if self.toDo["keywords"] or self.toDo["actors"] or self.toDo["directors"] or self.toDo["titles"]:
            self.dicoGlove = loadGloveDicFromFile(GLOVE_DICT_FILE)
            self.sizeGloveVector = self.dicoGlove[self.dicoGlove.keys()[0]].shape[0]
        
        if self.toDo["overviews"]:
            self.modelD2V = loadD2VModel(D2V_FILE)
        

    def preprocess(self, idMovies):
        """
        Pre-processes the data of interest that we want to provide to the learning model.
            Parameters: 
                - idMovies: int array of ids of Movies you want to process datas
            Return: 
                - the dictionnary ready for the classifier
        """
    
        mat = self.preprocessMatrix(idMovies)
        
        return self.prepareDico(mat)


    def preprocessMatrix(self, idMovies):
        """
        Create the matrices from the interest data we want to provide to the learning model.
            Parameters:
                - idMovies: array of movie's id from tmdb
            return:
                - dictionary of label:matrix, where label is name of matrix processed (key = titles, keywords, overviews, rating, genres, directors, actors)
        """
    
        matrix = {}
        
        movies = getMovies(idMovies)    
        
        infos = []
        keywords = []
        credits = []
    
        print "Loading data from TMDB"
        cpt = 0
        for i in range(len(movies)):
            movie = movies[i]
            info, keyword, credit = [], [], []
            threads = []
            
            try:
                # If those request failed, doesn't append results to arrays
                if self.toDo["overviews"] or self.toDo["titles"] or self.toDo["rating"] or self.toDo["genres"]: 
                    threads.append(_RunRequest(info, movie.info))
                if self.toDo["keywords"]: 
                    threads.append(_RunRequest(keyword, movie.keywords))
                if self.toDo["actors"] or self.toDo["directors"]: 
                    threads.append(_RunRequest(credit, movie.credits))
                                        
                for t in threads: t.start()
                for t in threads: t.join()
                
                if self.toDo["overviews"] or self.toDo["titles"] or self.toDo["rating"] or self.toDo["genres"]:infos.append(info[0])
                if self.toDo["keywords"]: keywords.append(keyword[0])
                if self.toDo["actors"] or self.toDo["directors"]: credits.append(credit[0])
                
            except:
                print "Error, movie " + str (movie) + " NOT FOUND"
                
            cpt += 1
            if(cpt > len(movies)/20.):
                print "%.0f%% requests loaded..." %(100*i/(1.0*len(movies)))
                cpt = 0
    
        if self.toDo["keywords"]:
            print "Processing Keywords"
            matrix["keywords"] = self.keywordsProcessing(keywords)
        
        if self.toDo["overviews"]:
            print "Processing Overviews..."
            matrix["overviews"] = self.overviewProcessingD2V(infos)
        
        if self.toDo["titles"]:
            print "Processing titles..."
            matrix["titles"] = self.titlesProcessing(infos)
        
        if self.toDo["rating"]:
            print "Processing rating..."
            matrix["rating"] = self.ratingProcessing(infos)
            
        if self.toDo["rating"]:
            print "Processing genres..."
            matrix["genres"] = self.genresProcessing(infos)
        
        if self.toDo["directors"]:
            print "Processing directors..."
            matrix["directors"] = self.peopleProcessing(credits, People.DIRECTOR)
        
        if self.toDo["actors"]:
            print "Processing actors..."
            matrix["actors"] = self.peopleProcessing(credits, People.ACTOR)
        
        return matrix
    
    
    def prepareDico(self, matrix):
        '''
        Create dictionary for the classifier with the following matrix if required.
            parameters: 
                - matrix: matrices that have been preprocessed
                - doTitles, doKeywords, doOverviews, doRating, doGenres, doActors, doDirectors: boolean (default=False) that tells which matrix has been preprocessed and can be set in the dictionnary
            return: 
                - dictionary of label:matrix, where label is name of matrix (key = titles, keywords, overviews, rating, genres, directors, actors)
        '''
        
        return concatData([ matrix[key] for key in sorted(matrix) if self.toDo[key] ])
    

    def overviewProcessingD2V(self, infos):
        """
        Pre-process overviews thanks to Dov2Vec model.
            parameters: 
                - infos: array of movies you want to get overviews with
                - model: the Doc2Vec model
            return: 
                - a ndarray of overviews values calculated by Glove. One line by movie.
        """
        
        meanMatrixOverview = np.empty([len(infos), SIZE_VECTOR])  
        
        for i, info in enumerate(infos):            
            overview = "".join(c for c in info["overview"] if c not in punctuation)       
            
            meanMatrixOverview[i] = textToVect(overview, self.modelD2V)
    
        return meanMatrixOverview
        
        
    def overviewProcessing(self, infos):
        """
        Pre-process overviews thanks to Glove model.
            parameters: 
                - infos: array of movies you want to get overviews with
            return: 
                - a ndarray of overviews values calculated by Glove. One line by movie.
        """

        meanMatrixOverview = np.empty([len(infos), self.sizeGloveVector])  
        
        for i, info in enumerate(infos):            
            overview = "".join(c for c in info["overview"] if c not in punctuation)       
            words = []
                
            for w in overview.split():
                words.append(w.lower().encode('UTF-8'))
         
            gArray, wSize = wordsToGlove(words, self.dicoGlove)
            
            meanMatrixOverview[i] = meanWords(gArray, wSize)
    
        return meanMatrixOverview
        
    
    def keywordsProcessing(self, moviesKeywords):
        """
            Pre-process keywords thanks to Glove model.
            parameters: 
                - moviesKeywords: array of movies you want to process keywords with
            return:
                - a ndarray of keywords values calculated by Glove. One line by movie.
        """
        
        meanMatrixKeywords = np.empty([len(moviesKeywords), self.sizeGloveVector]) 
        
        for i, keyword in enumerate(moviesKeywords):    
            keywords = getKeywords(keyword)
            gArray, wSize = wordsToGlove(keywords, self.dicoGlove)
            
            meanMatrixKeywords[i] = meanWords(gArray, wSize)
               
        return meanMatrixKeywords
    
    
    def titlesProcessing(self, infos):
        """
            Pre-process titles thanks to Glove model.
            parameters : 
                - infos: array of movies you want to process titles with
            return : 
                - a ndarray of titles values calculated by Glove. One line by movie.
        """
        
        meanMatrixTitles = np.empty([len(infos), self.sizeGloveVector]) 
        
        for i, info in enumerate(infos):            
            overview = "".join(c for c in info["title"] if c not in punctuation)
            overview = overview.split()
            words = []
                
            for w in overview:
                words += w.lower().encode('UTF-8')
                
            gArray, wSize = wordsToGlove(words, self.dicoGlove)
            
            meanMatrixTitles[i] = meanWords(gArray, wSize)
    
        return meanMatrixTitles
    
    
    def ratingProcessing(self, infos):
        """
        Pre-process rating.
            parameters : 
                - infos:  array of movies you want to process rating with
            return : 
                - a ndarray of rating values. One line by movie.
        """
        
        meanMatrixRating = np.empty([len(infos), 1])
        for i, info in enumerate(infos):  
            meanMatrixRating[i] = info["vote_average"]/10.0
    
        return meanMatrixRating
    
    
    def genresProcessing(self, infos):
        """
        Pre-process genres.
            Parameter:
                - infos: array of movies you want to process rating with
            Return:
                - a ndarray. of genres where each value is 1 if genre is present, 0 otherwise
        
        """
        
        TMDB_GENRES = getTmdbGenres()
        
        genresArray = np.empty([len(infos), len(TMDB_GENRES.keys())])
    
        for i, info in enumerate(infos):      
            genresVect = np.zeros(len(TMDB_GENRES.keys()))
    
            for genre in getGenres(info["genres"]):
                try:
                    genresVect[TMDB_GENRES[genre]] = 1
                except:
                    print "Unknown genre for %s -> %s" %(info["title"], genre)
    
            genresArray[i] = genresVect        
                
        return genresArray
    
    
    def peopleProcessing(self, moviesCredits, kindOfPeople):
        """
        Pre-process actors and directors
            parameters:
                - moviesCredits -> array of movie's moviesCredits you want to process people
                - dicoGlove: GloVe dictionary (dicoGlove)
                - kindOfPeople: People enum type, indicating is Directors or Actors 
            return:
                - a ndarray of people values calculated by Glove. One line by movie.
        """
        
        if not isinstance(kindOfPeople, People):
            raise ValueError("kindOfPeople must be an instance of People enum class")
            
        meanMatrixPeople = np.empty([len(moviesCredits), self.sizeGloveVector]) 
        names = []
        
        for i, credit in enumerate(moviesCredits):
            if kindOfPeople is People.DIRECTOR: names = getDirectors(credit)
            elif kindOfPeople is People.ACTOR: names = getActors(credit)
            
            words = []
            for name in names:
                words += name.lower().encode('UTF-8').split()
            
            gArray, wSize = wordsToGlove(words, self.dicoGlove)        
            meanMatrixPeople[i] = meanWords(gArray, wSize)
        
        return meanMatrixPeople


def concatData(listMatrix):
    '''
    Recursive function that concats a list of matrices. The matrices must have the same dimensions.
        parameters : 
            - listMatrix : a list of numpy array
        returns : 
            - an numpy array containing all data in the list of matrices
    '''
    if(len(listMatrix)==0):
        return np.array([])
        
    if(len(listMatrix)==1):
        return listMatrix[0]
    
    return np.hstack((listMatrix[0], concatData(listMatrix[1:])))
