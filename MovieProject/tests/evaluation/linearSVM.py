#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 15:00:40 2017

@author: Julian
"""

from evaluation import *
from liblinearutil import *


def processSVM(matrix):
    """
    
        Parameters:
            matrix -> ndarray of data
        return:
            list of dictionary  {indice:value}
    """
    
    l = []
    for i in range(len(matrix)):
        indVal = {}
        for k in np.nonzero(matrix[i])[0]:
            indVal[k+1] = matrix[i][k]
        l.append(indVal)
    
    return l

def concatMatrix(*matrixes):
    
    if(len(matrixes) == 0):
        raise ValueError
        
    elif(len(matrixes) == 1):
        return matrixes[0]
        
    elif(len(matrixes) == 2):
        return np.hstack((matrixes[0], matrixes[1]))
    else:
        return concatMatrix(np.hstack((matrixes[0], matrixes[1])), *matrixes[2:])

dicoMatrix, labels = preprocessMovieGeneric("moviesEvaluatedJulian", 
                                            doTitles=True, doRating=True, 
                                            doOverviews=True, doKeywords=True, 
                                            doGenres=True, doActors=True, doDirectors=True)

# "dicoMatrix keys(): actors, genres, data, directors"

                  

newDico = {}

for key in dicoMatrix:
    newDico[key] = processSVM(dicoMatrix[key])


mat = processSVM(concatMatrix(*[ dicoMatrix[key] for key in dicoMatrix ]))

trainInd = int(0.8*len(mat) )

y, x = labels[:trainInd], mat[:trainInd]
prob  = problem(y, x)
param = parameter('-s 0 -c 4 -B 1')
m = train(prob, param)

p_label, p_acc, p_val = predict(labels[trainInd:], mat[trainInd:], m, '-b 1')
ACC, MSE, SCC = evaluations(labels[trainInd:], p_label)


