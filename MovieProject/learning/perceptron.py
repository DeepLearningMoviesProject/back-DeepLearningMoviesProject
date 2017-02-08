#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Perceptron Algorithm

Perceptron is a classification algorithm for problems with two classes (0 and 1) where a linear equation (like or hyperplane) can be used to separate the two classes.

It receives input signals from examples of training data that we weight and combined in a linear equation called the activation.
-> activation = sum(weight_i * x_i) + bias 
The activation is then transformed into an output value or prediction using a transfer function, such as the step transfer function.
-> prediction = 1.0 if activation >= 0.0 else 0.0 

It is closely related to linear regression and logistic regression that make predictions in a similar way (e.g. a weighted sum of inputs).

The weights of the Perceptron algorithm must be estimated from your training data using stochastic gradient descent.


Created on Wed Feb  8 10:37:35 2017
@author: coralie
"""

import numpy as np
from sklearn.linear_model import perceptron
from MovieProject.learning import crossValidationSplit

    
def trainingPerceptron(datas, labels) : 
    """
    Training perceptron
    
    Parameters : 
        datas : 
        labels :      
    """
    result = crossValidationSplit.crossValidationSplit(datas,labels)
    xTrain, yTrain = result["train"]
    xTest, yTest = result["test"]
    
    model = perceptron.Perceptron(n_iter=100, verbose=0, random_state=None, fit_intercept=True, eta0=0.002)
    model.fit(xTrain,yTrain)
    
    print "Accuracy   " + str(model.score(xTrain, yTrain)*100) + "%"
    print "Prediction " + str(model.predict(xTest))

    
    
    
if __name__ == "__main__": 
    
    # Data
    data = np.array([[1,2,2],[2,1,1],[5,8,9],[10,9,8],[9,8,7],[1,3,2],[5,4,9],[2,2,2],[1,4,1]])
    
    # Labels
    label = np.array([0,0,1,1,1,0,1,0,0])
    
    # Perceptron model
    trainingPerceptron(data,label)
    