#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 11:24:39 2017

@author: Julian
"""

from liblinearutil import *
from numpy import nonzero


class LinearSVM():
    
    def __init__(self):
        """
            Constructor of the SVM model with paramters : -s 0 -c 4 -B 1
            See liblinear doc to get info for arguments
        """
        
        self._param = parameter('-s 0 -c 4 -B 1')
        self._model = None
        
        
    def train(self, data, labels):
        """
            Train the SVM model with labels associated to the data
        
            Parameters:
                data -> ndarray, the data to train the model
                labels -> ndarray, labels associted to the data. Must have the same dimenstion
            return:
                SVM model
        
        """
        
        prob  = problem(labels, self._formatData(data))
        self._model = train(prob, self._param)
        return self._model
    
    
    def evaluate(self, data, labels):
        """
            Predict labels from data and compare the result to orginals labels
        
            Parameters:
                data -> ndarray, the data to train the model
                labels -> ndarray, labels associted to the data. Must have the same dimenstion
            return:
                Float, the accuracy 
        """
        
        p_label = self.predict(self._formatData(data), labels)
        acc, mse, scc = evaluations(labels, p_label)
        return acc

    def predict(self, data, labels):
        """
            Predict labels from data
        
            Parameters:
                data -> ndarray, the data to train the model
                labels -> ndarray, labels associted to the data. Must have the same dimenstion
            return:
                ndarray, the predicted labels
        """
        
        p_label, p_acc, p_val = predict(labels, self._formatData(data),self._model, '-b 1')
        return p_label
        

    def _formatData(self, matrix):
        """
            Format matrix2D data into list of dictionary {index:value}
        
            Parameters:
                matrix -> ndarray of data
            return:
                list of dictionary  {indice:value}
        """
        
        if type(matrix) == type([]):
            return matrix
    
        l = []
        for i in range(len(matrix)):
            indVal = {}
            for k in nonzero(matrix[i])[0]:
                indVal[k+1] = matrix[i][k]
            l.append(indVal)
        
        return l