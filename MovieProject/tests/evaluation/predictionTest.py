# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 17:20:44 2017

@author: elsa
"""
from MovieProject.learning import buildModel, suggestNMovies
from MovieProject.tests import preprocessMovie


if __name__ == "__main__":
    '''
        Builds the model fitting the movies in filename and then suggests a list of 10 movies
    '''

    filename = 'moviesEvaluated-16'

    T, G, labels = preprocessMovie(filename)

    model = buildModel(T, G, labels)    

    print suggestNMovies(model, 10)