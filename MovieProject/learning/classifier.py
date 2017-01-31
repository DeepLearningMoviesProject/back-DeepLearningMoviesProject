# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 16:33:30 2017

@author: elsa
"""


from __future__ import print_function

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Merge, BatchNormalization, Embedding, Flatten
from keras.optimizers import SGD


def createModel(textEntries, genresEntries, classEntries):
#def trainModel(textEntries, genresEntries, actorsEntries, realEntries, classEntries):
    """
        Creates, fits and returns the specific model fitting the entries
        
        Parameters : 
            textEntries : a matrix with all the float values preprocessed (keywords, overview, title, note, etc.)
            genresEntries : a matrix of binary values that tells the movie's genres
            classEntries : a matrix of binary values that tells the class of the movie (like/dislike)            
            
        return :
            the model is trained with the parameters
            
    """
    
    genres_dim = len(genresEntries[0])
    text_dim = len(textEntries[0])
    
    text_input_dim = 1000
    text_output_dim = 2
    genres_output_dim = 5
    
    text_branch = Sequential()
    text_branch.add(Embedding(text_input_dim, text_output_dim, input_length=text_dim))
    text_branch.add(Flatten())
    
    genres_branch = Sequential()
    genres_branch.add(Dense(genres_output_dim, input_shape = (genres_dim,), init='normal', activation='relu'))
    genres_branch.add(BatchNormalization())
    
#    actors_branch = Sequential()
#    actors_branch.add(Dense(10, input_shape =  (3,) , activation = 'relu'))
#    actors_branch.add(BatchNormalization())
    
#    real_branch = Sequential()
#    real_branch.add(Dense(10, input_shape =  (4,) , activation = 'relu'))
#    real_branch.add(BatchNormalization())
    
    #We merge in cascade
    
#    merge1_branch = Sequential()
#    merge1_branch.add(Merge([genres_branch, actors_branch], mode = 'concat'))
#    merge1_branch.add(Dense(1,  activation = 'sigmoid'))
    
#    merge2_branch = Sequential()
#    merge2_branch.add(Merge([real_branch, merge1_branch], mode = 'concat'))
#    merge2_branch.add(Dense(1,  activation = 'sigmoid'))  

    final_branch = Sequential()
    final_branch.add(Merge([text_branch, genres_branch], mode = 'concat'))
    
    #Here are all of our layers, the preprocessing is over
    final_branch.add(Dense(30,  activation = 'relu'))
    final_branch.add(Dense(1,  activation = 'sigmoid'))
    
    sgd = SGD(lr = 0.1, momentum = 0.9, decay = 0, nesterov = False)
    final_branch.compile(loss = 'binary_crossentropy', optimizer = sgd, metrics = ['accuracy'])
    np.random.seed(2017)
    
    final_branch.fit([textEntries, genresEntries], classEntries, batch_size = 2000, nb_epoch = 100, verbose = 1)
#    final_branch.fit([textEntries, genresEntries, actorsEntries, realEntries], classEntries, batch_size = 2000, nb_epoch = 100, verbose = 1)
    return final_branch


