# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 16:57:58 2017

@author: Elsa Navarro
"""

import numpy as np
import pickle
import os
from MovieProject.learning import buildModel, buildTestModel
from MovieProject.preprocessing import preprocess
from flask import json
from os.path import isfile

path = '../resources/evaluations/'

#Test function
def testMovies(filename):
    #filename = 'moviesEvaluated-16'
    tname = path + filename + '-Tsave.data'
    gname = path + filename + '-Gsave.data'
    lname = path + filename + '-LABELSsave.data'

    preprocessingChanged = True #Set to true if the processing has changed
    dontPreprocess = (not preprocessingChanged) and isfile(tname) and isfile(gname) and isfile(lname)
    
    T = np.array([])
    G = np.array([])
    labels = np.array([])
    
    #if data has not been preprocessed 
    if(not dontPreprocess):
        print "File % in process ...", filename
        #load data from json
        jname = path + filename + '.json'
        with open(jname) as data_file:    
            data = json.load(data_file)

        #Get ids and labels of data
        ids = [int(key) for key in data]
        labels = np.array([data[key] for key in data])

        #preprocess data
        T, G = preprocess(ids)

        #save preprocessed data (T & G)
        with open(tname, 'w') as f:
            pickle.dump(T, f)
        with open(gname, 'w') as f:
            pickle.dump(G, f)
        with open(lname, 'w') as f:
            pickle.dump(labels, f)
    else:
        print "File % load process ...", filename
        #load preprocessed data (T & G)
        with open(tname, 'r') as f:
            T = pickle.load(f)
        with open(gname, 'r') as f:
            G = pickle.load(f)
        with open(lname, 'r') as f:
            labels = pickle.load(f)
        print 'T done : ', T
        print 'G done : ', G
        print 'labels done : ', labels
            
    
    'Process OK, model ready to be built !'
    model, score = buildTestModel(T, G, labels, folds=3)
    return score


def testClassifier():

    meanScore = 0
    totalScores = 0

    #Get all files from PATH, and get the score of the classifier on these files
    for file in os.listdir(path):
        if file.endswith(".json"):
            meanScore += testMovies(file.replace(".json", ""))
            totalScores += 1
    #Compute the mean score for the classifier
    meanScore /= totalScores
    return meanScore


if __name__ == '__main__':
   # testMovies('moviesEvaluated-16')
   score = testClassifier()
   print "The classifier has an average accuracy of %.", score