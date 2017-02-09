#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 14:50 2017

@author: elsa
"""
import numpy as np
import pickle
import os
from MovieProject.preprocessing import preprocessMatrix, prepareDico
from MovieProject.learning import buildTestModel
from flask import json
from os.path import isfile


path = '../../resources/evaluations/'

preprocessingChanged = False #Set to true if the processing has changed

#Test function
def preprocessMovieGeneric(filename, doTitles=False, doRating=False, doOverviews=False, doKeywords=False, doGenres=False, doActors=False, doDirectors=False):
    #filename = 'moviesEvaluated-16'
    files = {}
    if(doTitles):
        files['titles'] = path + filename + '-Tsave.data'

    if(doRating):
        files['rating'] = path + filename + '-Rsave.data'

    if(doOverviews):
        files['overviews'] = path + filename + '-Osave.data'

    if(doKeywords):
        files['keywords'] = path + filename + '-Ksave.data'

    if(doGenres):
        files['genres'] = path + filename + '-Gsave.data'

    if(doActors):
        files['actors'] = path + filename + '-Asave.data'

    if(doDirectors):
        files['directors'] = path + filename + '-Dsave.data'

    #mat_name = path + filename + '-' + names + '-save.data'
    labels_name = path + filename + '-LABELSsave.data'

    dontPreprocess = (not preprocessingChanged) and isfile(labels_name)
    
    for f in files:
        dontPreprocess = dontPreprocess and isfile(files[f])
        
    
    
#    T = np.array([])
#    G = np.array([])
    matrix = {}
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
        matrix = preprocessMatrix(ids, mTitles=doTitles, mKeywords=doKeywords, mOverviews=doOverviews, mRating=doRating, mGenres=doGenres, mActors=doActors, mDirectors=doDirectors)

        #save preprocessed data - all matrix
        for key in files:
            #Recompute only if the preprocess has changed or if the file doesn't exists
            if(preprocessingChanged or (not isfile(key))):
                with open(files[key], 'w') as f:
                    pickle.dump(matrix[key], f)
        #Save labels
        with open(labels_name, 'w') as f:
            pickle.dump(labels, f)
    else:
        print "File %s load process ..." %(filename)
        #load preprocessed data - all matrix
        for key in files:
            with open(files[key], 'r') as f:
                matrix[key] = pickle.load(f)
#        with open(mat_name, 'r') as f:
#            dico = pickle.load(f)
        #Load labels
        with open(labels_name, 'r') as f:
            labels = pickle.load(f)
        
    'Process OK, model ready to be built !'
    return prepareDico(matrix, doTitles, doRating, doOverviews, doKeywords, doGenres, doActors, doDirectors), labels

def testClassifier(doKeras=False, doPerceptron=False, doSVM=False):
    '''
        Tests the classifiers specified
        
        Parameters : booleans that tells the classifiers you want to test
        
        returns : the mean scores for the classifiers
    '''

    if(not (doKeras or doPerceptron or doSVM)):
        raise ValueError('You must specify at least one classifier to test!!!')
    
    meanScoreKeras = 0
    meanScorePerceptron = 0
    meanScoreSVM = 0
    totalScores = 0

    #Get all files from PATH, and get the score of the classifier on these files
    for file in os.listdir(path):
        if file.endswith(".json") and ("simple" not in file):
            dico, labels = preprocessMovieGeneric(file.replace(".json", ""), doTitles=True, doRating=True, doOverviews=True, doKeywords=True, doGenres=True, doActors=True, doDirectors=True)
            scoreKeras = 0
            scorePerceptron = 0
            scoreSVM = 0
            if(doKeras):
                _, scoreKeras = buildTestModel(dico, labels, folds=5)
            if(doPerceptron):
                pass
                #TODO : call perceptron function TMTC
            if(doSVM):
                pass
                #TODO : call SVM function TMTC
            meanScoreKeras += scoreKeras
            meanScorePerceptron += scorePerceptron
            meanScoreSVM += scoreSVM
            totalScores += 1
    #Compute the mean score for the classifier
    meanScoreKeras /= totalScores
    meanScorePerceptron /= totalScores
    meanScoreSVM /= totalScores
    return meanScoreKeras, meanScorePerceptron, meanScoreSVM


if __name__ == '__main__':
    
    doOne = False
    score = 0
    
    if(doOne):
        #One movie
        filename = 'moviesEvaluated-simple'
        dico, labels = preprocessMovieGeneric(filename, doTitles=True, doOverviews=True, doActors=True)
        _, score = buildTestModel(dico, labels, folds=2)
    else:
        #All movies
        score, _ , _ = testClassifier(doKeras=True) #Test for keras
    
    
    print "The classifier keras has an average accuracy of ", score