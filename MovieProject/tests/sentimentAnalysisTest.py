#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 11:32:22 2017

@author: coralie
"""
from MovieProject.learning import sentimentAnalysis as sa
from MovieProject.resources import SENTIMENT_ANALYSIS_MODEL


if __name__ == "__main__":   
   
    modelPath = SENTIMENT_ANALYSIS_MODEL
    
    data = sa.preprocessDatasModel()
    trainX = data["trainX"]
    trainY = data["trainY"]
    testX = data["testX"]
    testY = data["testY"]
 
    """
    # Simple RN fully connected
    print "Test a simple 3 layer fully connected network : \n"
    model = fullyConnectedRN(trainX,trainY)
    evaluate(model, testX, testY)
    """
    
    # LSTM RN
    print "Test LSTM : \n"
    model = sa.LSTMModelRN(trainX ,trainY, testX, testY)
    print(model.summary())
    sa.evaluateLSTM(model, testX, testY)
    
    model.save(modelPath)  