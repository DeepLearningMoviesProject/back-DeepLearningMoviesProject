# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 16:33:30 2017

@author: elsa
"""

#from __future__ import print_function

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Merge, BatchNormalization, Embedding, Flatten, Dropout
from keras.optimizers import SGD, Adam
from keras.constraints import maxnorm
from sklearn.cross_validation import StratifiedKFold

epoch = 800
batch = 64

def createModel(dataLen = 0):
    '''
        Creates the model

        Parameters : the length of the matrix we want to fit our model on, must be > 0

        return : The model, ready to be fit
    '''
    
    dataOutputDim = dataLen

    if(dataLen==0):
        raise ValueError('The model can\'t be created if there is no matrix !')
    
    finalBranch = Sequential()
    #finalBranch.add(Dropout(0.2, input_shape=(dataLen,)))
    finalBranch.add(Dense(dataOutputDim, input_dim=dataLen, activation = 'relu'))
    finalBranch.add(BatchNormalization())
    
    #TODO : maybe change this dropout
    finalBranch.add(Dropout(0.2))
    finalBranch.add(Dense((dataOutputDim/2),  activation = 'relu', W_constraint = maxnorm(3)))
    # finalBranch.add(Dropout(0.2))
    # finalBranch.add(Dense((dataOutputDim/2),  activation = 'relu', W_constraint = maxnorm(3)))
    finalBranch.add(Dropout(0.2))
    finalBranch.add(Dense(1,  activation = 'sigmoid', W_constraint = maxnorm(3)))
    
    #TODO : Change optimizer
#    sgd = SGD(lr = 0.1, momentum = 0.9, decay = 0, nesterov = False)
    adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    finalBranch.compile(loss = 'binary_crossentropy', optimizer = adam, metrics = ['accuracy'])

    return finalBranch

def createTrainModelDico(mat, labels, iTest = [], iTrain = [], doTest=False):
    """
        Creates, fits and returns the specific model fitting the entries
        
        Parameters : 
            mat : a matrix of the data to train on - np.array
            labels : the labels of the data to train (binary) - np.array
            iTrain : an array of indexes for the training
            iTest : an array of indexes for the tests
            doTest : set to true if you want to test the model
            
        return :
            the model that is trained with the parameters
            
    """
    matTrain = []
    matTest = []

    labelsTrain = []
    labelsTest = []
    
    if mat is None :
        #TODO : raise an exception
        print "there is no data to build the model on !"

    dataLen = len(mat[0])
    
    if (dataLen==0):
        #TODO : raise an exception
        print "the matrix is empty, the model can't be done"

    if(doTest):
        labelsTrain = labels[iTrain]
        labelsTest = labels[iTest]
        matTrain = mat[iTrain]
        matTest = mat[iTest]
    else:
        labelsTrain = labels
        matTrain = mat

    #Create the model
    model = createModel(dataLen = dataLen)
    
    #Train model
    model.fit(matTrain, labelsTrain, batch_size = batch, nb_epoch = epoch, verbose = 1)

    # evaluate the model
    scores = None
    if(doTest):
        scores = model.evaluate(matTest,labelsTest, verbose=0)
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    return model, scores

def buildModel(mat, labels):
    '''
        Builds the model that matches the movies represented in mat and the labels (like/dislike)
        
        Parameters : 
            mat : contains the characteristics of the movies we want to build the model on
            labels : tells whether the movie is liked or not (binary)           
            
        return :
            the model trained on the movies
    '''

    model, _ = createTrainModelDico(mat, labels)
    return model
    
def buildTestModel(mat, labels, folds):
    '''
        Builds the model that matches the data of movies contained in mat and the like/dislike (labels)
        Tests it with k-cross validation
        mat must have been preprocessed correctly
        
        Parameters : 
            mat : contains the characteristics of the movies we want to build the model on
            labels : tells whether the movie is liked or not (binary)       
            folds : the number of k-cross validation we want to do (no more than the no of labels, 5 to 9 is fine)
            
        return :
            the model trained on the movies, the medium score of the k-cross validation
    '''
    
    cvscores = []
    model = None # Clearing the NN.

    n_folds = folds
    skf = StratifiedKFold(labels, n_folds=n_folds, shuffle=True)

    for i, (train, test) in enumerate(skf):
        print "Running Fold", i+1, "/", n_folds
        # print " train, test : ", train, " ", test
        iTrain = np.array(train)
        iTest = np.array(test)
        model = None # Clearing the NN.
        model, scores = createTrainModelDico(mat, labels, iTest, iTrain, doTest=True)
        cvscores.append(scores[1] * 100)

    mean_score = np.mean(cvscores)
    print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
    return model, mean_score