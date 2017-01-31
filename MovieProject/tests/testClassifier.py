# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 16:57:58 2017

@author: elsa
"""

import numpy as np
from MovieProject.learning import classifier

#Test function
def test():
        
    #X1: simulation realisateurs
    X1_train = np.empty((2,2))
    #X2: simulation acteurs
    X2_train = np.empty((2,3))
    #X3: simulation quelquonque
    X3_train = np.empty((2,4))
    #X: simulation vecteur glove
    X_train = np.empty((2,5))
    #Y : Labels
    nbY = 1
    Y_train = np.empty((2,nbY ))
    
    i = 0
    y = 0
    while (i<2):
        y = 0
        while (y<nbY):
            Y_train[i][y] = 0
            y += 1
        i += 1
    
    X1_train[0][0] = 3
    X1_train[0][1] = 4
    X1_train[1][0] = 7 
    X1_train[1][1] = 8
    
    X2_train[0][0] = 322
    X2_train[0][1] = 46
    X2_train[0][2] = 72
    X2_train[1][1] = 889
    X2_train[1][2] = 45
    X2_train[1][0] = 72
    
    X3_train[0][0] = 322
    X3_train[0][1] = 46
    X3_train[0][2] = 72
    X3_train[1][1] = 889
    X3_train[1][2] = 45
    X3_train[1][0] = 72
    X3_train[0][3] = 322
    X3_train[1][3] = 46
    
    X_train[0][0] = 322
    X_train[0][1] = 46
    X_train[0][2] = 72
    X_train[1][1] = 889
    X_train[1][2] = 45
    X_train[1][0] = 72
    X_train[0][3] = 322
    X_train[1][3] = 46
    X_train[0][4] = 322
    X_train[1][4] = 46
    
    model = classifier.createModel(X_train, X1_train, Y_train)
    
test()