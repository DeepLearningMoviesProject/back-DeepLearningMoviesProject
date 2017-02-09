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



dicoMatrix, labels = preprocessMovieGeneric("moviesEvaluatedJulian", True, True, True, True, True, True, True)

# "dicoMatrix keys(): actors, genres, data, directors"

                  

newDico = {}

for key in dicoMatrix:
    newDico[key] = processSVM(dicoMatrix[key])
    




### Train model

trainInd = int(0.7*len(newDico["data"]) )
testInd = int( 0.3*len(newDico["data"]) )

y, x = labels[:trainInd], newDico["data"][:trainInd]
prob  = problem(y, x)
param = parameter('-s 0 -c 4 -B 1')
m = train(prob, param)

p_label, p_acc, p_val = predict(labels[testInd:], newDico["data"][testInd:], m, '-b 1')
ACC, MSE, SCC = evaluations(labels[testInd:], p_label)

