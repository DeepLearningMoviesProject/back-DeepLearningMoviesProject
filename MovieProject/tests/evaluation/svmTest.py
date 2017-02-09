#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:03:58 2017

@author: edwin
"""
import numpy as np
import pickle
import os
from MovieProject.preprocessing import preprocess
from flask import json
from os.path import isfile
from sklearn import svm
from sklearn.cross_validation import train_test_split

path = '../resources/evaluations/'

#Test function
def preprocessMovie(filename):
    #filename = 'moviesEvaluated-16'
    tname = path + filename + '-Tsave.data'
    gname = path + filename + '-Gsave.data'
    lname = path + filename + '-LABELSsave.data'

    preprocessingChanged = False #Set to true if the processing has changed
    dontPreprocess = (not preprocessingChanged) and isfile(tname) and isfile(gname) and isfile(lname)
    
    T = np.array([])
    G = np.array([])
    labels = np.array([])
    
    if(preprocessingChanged):
        print "Preprocessing has changed !"

    #if data has not been preprocessed 
    if(not dontPreprocess):
        print "File %s in process ..." %(filename)
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
        
    'Process OK, model ready to be built !'
    return T, G, labels
    
def testMovie(filename):
    T, G, labels = preprocessMovie(filename)
    X_train, X_test, y_train, y_test = train_test_split(T, labels, test_size=0.2, random_state=0)
    clf = svm.SVC()
    clf.fit(X_train, y_train)  
    score = clf.score(X_test, y_test) 
    return score


def testClassifier():

    meanScore = 0
    totalScores = 0

    #Get all files from PATH, and get the score of the classifier on these files
    for file in os.listdir(path):
        if file.endswith(".json"):
            score = testMovie(file.replace(".json", ""))
            meanScore += score
            totalScores += 1
    #Compute the mean score for the classifier
    meanScore /= totalScores
    return meanScore


if __name__ == '__main__':
   # testMovies('moviesEvaluated-16')
   score = testClassifier()
   print "The classifier has an average accuracy of ", score