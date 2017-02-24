# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 17:20:44 2017

@author: elsa
"""

#from MovieProject.preprocessing import prepareDico
from MovieProject.learning import buildModel, suggestNMovies
from evaluation import preprocessFileGeneric

if __name__ == "__main__":
    '''
        Builds the model fitting the movies in filename and then suggests a list of 10 movies
    '''

    filename = 'moviesEvaluated-18'
    
    params = { "titles":True,
               "rating":True,
               "overviews":True,
               "keywords":True,
               "genres":True,
               "actors":True,
               "directors":True }

    data, labels = preprocessFileGeneric(filename.replace(".json", ""), **params)
#    d, labels = preprocessFileGeneric(filename, doTitles=True, doRating=True, doOverviews=True, doKeywords=True, doGenres=True, doActors=True, doDirectors=True) 
#    mat = prepareDico(d, doTitles = True, doRating = True, doOverviews = True, doKeywords=True, doGenres=True, doActors=True, doDirectors=True) 
    model= buildModel(data, labels)    
    

    print suggestNMovies(model, 10, **params)