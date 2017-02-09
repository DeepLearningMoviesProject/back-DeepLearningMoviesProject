#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Perceptron Algorithm

Perceptron is a classification algorithm for problems with two classes (0 and 1) where a linear equation (like or hyperplane) can be used to separate the two classes.

It receives input signals from examples of training data that we weight and combined in a linear equation called the activation.
The activation is then transformed into an output value or prediction using a transfer function, such as the step transfer function.

It is closely related to linear regression and logistic regression that make predictions in a similar way (e.g. a weighted sum of inputs).

The weights of the Perceptron algorithm must be estimated from your training data using stochastic gradient descent.


Created on Wed Feb  8 10:37:35 2017
@author: coralie
"""

import numpy as np
from sklearn.linear_model import perceptron
from MovieProject.learning import crossValidationSplit
from MovieProject.preprocessing.tools import shuffle

def evaluatePerceptron(datas, labels, nb=50) : 
    """
    Evaluates training with perceptron. This perceptron is initialize thank's to a random state,
    so the result changes at each iteration with a different random state. Because of that, 
    we need to take the mean of all results to evaluate the accuracy.
    
    Parameters : 
        nb : the number of train (random state changes at each iteration)
        datas : numpy array of datas to train the model
        labels : numpy array of labels associated
    
    Return :
        A dictionary of keys associated with values :
            "accuracyTrain" : the mean accuracy on training,
            "accuracyTest" : the mean accuracy on testing,
            "minAccuracyTrain" : the minimum accuracy on training,
            "maxAccuracyTrain" : the maximum accuracy on training,
            "minAccuracyTest" : the minimum accuracy on testing,
            "maxAccuracyTest" : the maximum accuracy on testing
    """
    
    accuracyTrain = 0.
    minAccuracyTrain = 100
    maxAccuracyTrain = 0.
    accuracyTest = 0.
    minAccuracyTest = 100.
    maxAccuracyTest = 0.
        
    for i in range(nb) :
    
        # shuffle
        datas,labels = shuffle.shuffleIdLabeled(datas,labels)
        # split
        result = crossValidationSplit.crossValidationSplit(datas,labels)
        xTrain, yTrain = result["train"]
        xTest, yTest = result["test"]
        # train & evaluate
        model = perceptron.Perceptron(n_iter=100, verbose=0, random_state=i, fit_intercept=True, eta0=0.002)
        model.fit(xTrain,yTrain)
        accTrain = model.score(xTrain, yTrain)
        accuracyTrain += (accTrain*100)
        minAccuracyTrain = accTrain < minAccuracyTrain and accTrain or minAccuracyTrain
        maxAccuracyTrain = accTrain > maxAccuracyTrain and accTrain or maxAccuracyTrain
        accTest = model.score(xTest, yTest)
        accuracyTest += (accTest*100)
        minAccuracyTest = accTest < minAccuracyTest and accTest or minAccuracyTest
        maxAccuracyTest = accTest > maxAccuracyTest and accTest or maxAccuracyTest
        
        #print "Prediction : " + str(model.predict(xTest))
        
    meanAccuracyTrain = accuracyTrain/nb
    meanAccuracyTest = accuracyTest/nb
    print "Accuracy on data trained: " + str(meanAccuracyTrain) + "%   [min:" + str(minAccuracyTrain) + " - max:" + str(maxAccuracyTrain) + "]"
    print "Accuracy on data tested: " + str(meanAccuracyTest) + "%   [min:" + str(minAccuracyTest) + " - max:" + str(maxAccuracyTest) + "]"
    
    
    return {"accuracyTrain":meanAccuracyTrain, "accuracyTest":meanAccuracyTest, "minAccuracyTrain":minAccuracyTrain, "maxAccuracyTrain":maxAccuracyTrain, "minAccuracyTest":minAccuracyTest, "maxAccuracyTest":maxAccuracyTest}

    
    
    
if __name__ == "__main__": 
    
    # Data
    data = np.array([[1,2,2],[2,1,2],[5,8,9],[10,9,8],[9,8,7],[1,3,2],[5,4,9],[2,2,2],[1,4,1],[1,1,1],[2,1,3],[5,10,9],[11,9,8],[9,10,7],[1,3,1],[5,6,9],[2,3,2],[1,4,3]])
    
    # Labels
    label = np.array([0,0,1,1,1,0,1,0,0,0,0,1,1,1,0,1,0,0])
    
    # Perceptron model
    evaluatePerceptron(data,label)
    