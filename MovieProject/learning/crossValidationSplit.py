#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Allows to create a training set and a testing set from all datas and labels

Created on Wed Feb  8 13:30:53 2017
@author: coralie
"""

import numpy as np


def crossValidationSplit(dataset, labelset):
    """
    Split a dataset into 2 folds in order to obtain 70% of training data and 30 testing data
    
    Parameters :
        dataset : numpy array to split
    
    Return : 
        a dictionary containing for the key "train" a tuple of training datas and training labels
        and for the key "test", a tuple of testing datas and testing labels
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
 
    
if __name__ == "__main__": 
    
    data = np.array([[1,2,2],[2,1,1],[5,8,9],[10,9,8],[9,8,7],[1,3,2]])
    label = np.array([0,0,1,1,1,0])
    result = crossValidationSplit(data, label)
    xTrain, yTrain = result["train"]
    xTest, yTest = result["test"]
    print "Training data (70%) : "
    print xTrain
    print "Label associated : "
    print yTrain
    print "Testing data (30%) : "
    print xTest
    print "Label associated : " 
    print yTest