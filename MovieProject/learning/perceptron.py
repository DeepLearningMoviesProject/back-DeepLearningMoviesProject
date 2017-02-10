#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Evaluation of the perceptron algorithm

Perceptron is a classification algorithm for problems with two classes (0 and 1) where a linear equation (like or hyperplane) can be used to separate the two classes.
It receives input signals from examples of training data that we weight and combined in a linear equation called the activation.
The activation is then transformed into an output value or prediction using a transfer function, such as the step transfer function.

Created on Wed Feb  8 10:37:35 2017
@author: coralie
"""

import numpy as np
from sklearn.linear_model import perceptron
from MovieProject.preprocessing.tools import shuffle


def crossValidationSplit(dataset, labelset):
    """
    Split a dataset into two folds in order to obtain 70% of training data and 30% of testing data.
        Parameters :
            - dataset : ndarray of movie data to split
            - labelset : ndarray  of label associated, to split in the same ways
        Return : 
            - a dictionary ok key:(tuple), containing for the key "train" the tuple of 
            (training datas,training labels) and for the key "test", the tuple (testing datas, testing labels)
    """
    if len(dataset) != len(labelset) :
        raise ValueError
        
    nbData = len(dataset)
    foldSize = int(nbData*0.7)
    
    xTrain = dataset[0:foldSize,:]
    xTest = dataset[foldSize:,:]

    yTrain = labelset[0:foldSize]
    yTest = labelset[foldSize:]

    return {'train':(xTrain,yTrain),'test':(xTest,yTest)}


            
def evaluatePerceptron(datas, labels, nb=50, verbose=False) : 
    """
    Evaluates training with perceptron. This perceptron is initialize thank's to a random state,
    so the result changes at each iteration with a different random state. Because of that, 
    we need to take the mean of all results to evaluate the accuracy.
    
    Parameters : 
        - datas : ndarray of datas to train the model
        - labels : ndarray of labels associated
        - nb : the number of train (random state changes at each iteration)
        - verbose : boolean (default=False) allows to show or not more informations on accuracy.
    
    Return :
        - the mean accuracy on testing
    """
    accuracyTest = 0.
        
    if verbose :
        accuracyTrain = 0.
        minAccuracyTrain = 100
        maxAccuracyTrain = 0.
        minAccuracyTest = 100.
        maxAccuracyTest = 0.
        
    for i in range(nb) :
        # shuffle
        datas,labels = shuffle.shuffleDataLabeled(datas,labels)
        # split
        result = crossValidationSplit(datas,labels)
        xTrain, yTrain = result["train"]
        xTest, yTest = result["test"]
        # train & evaluate
        model = perceptron.Perceptron(n_iter=100, verbose=0, random_state=i, fit_intercept=True, eta0=0.002)
        model.fit(xTrain,yTrain)
        accTest = model.score(xTest, yTest)
        accuracyTest += (accTest*100)
        
        if verbose :
            accTrain = model.score(xTrain, yTrain)
            accuracyTrain += (accTrain*100)
            minAccuracyTrain = accTrain < minAccuracyTrain and accTrain or minAccuracyTrain
            maxAccuracyTrain = accTrain > maxAccuracyTrain and accTrain or maxAccuracyTrain
            minAccuracyTest = accTest < minAccuracyTest and accTest or minAccuracyTest
            maxAccuracyTest = accTest > maxAccuracyTest and accTest or maxAccuracyTest
            #print "Prediction : " + str(model.predict(xTest))
        
    meanAccuracyTest = accuracyTest/nb
    
    if verbose :
        meanAccuracyTrain = accuracyTrain/nb
        print "Accuracy on data trained: " + str(meanAccuracyTrain) + "%   [min:" + str(minAccuracyTrain) + " - max:" + str(maxAccuracyTrain) + "]"
        print "Accuracy on data tested: " + str(meanAccuracyTest) + "%   [min:" + str(minAccuracyTest) + " - max:" + str(maxAccuracyTest) + "]"
    
    
    return meanAccuracyTest
    