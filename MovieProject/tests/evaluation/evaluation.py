#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Evaluate multi couches neuronal network compared to perceptron and SVM

Created on Thu Feb  9 14:50 2017
@author: elsa
"""
import numpy as np
import pickle
import os
from MovieProject.preprocessing import preprocessMatrix, prepareDico, concatData
from MovieProject.learning import buildTestModel, LinearSVM, perceptron
from flask import json
from os.path import isfile


path = '../../resources/evaluations/'

preprocessingChanged = False #Set to true if the processing has changed

#Test function
def preprocessFileGeneric(filename, doTitles=False, doRating=False, doOverviews=False, doKeywords=False, doGenres=False, doActors=False, doDirectors=False):
    '''
    Allows to save the preprocessing in files, save some time for the tests
        parameters : 
            - do... : the data you want to preprocess are set to True
            - filename : from where the data come (json file name without its extension .json)
        return : 
            - a dico of the matrix with the data preprocessed, we can build the model with it
    '''

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

    if not files:
        #TODO : raise an error
        print "Nothing to preprocess here !"

    #mat_name = path + filename + '-' + names + '-save.data'
    labels_name = path + filename + '-LABELSsave.data'

    dontPreprocess = (not preprocessingChanged) and isfile(labels_name)
    
    for f in files:
        dontPreprocess = dontPreprocess and isfile(files[f])
        
    
#    T = np.array([])
#    G = np.array([])
    dicoMatrix = {}
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
        dicoMatrix = preprocessMatrix(ids, mTitles=doTitles, mKeywords=doKeywords, mOverviews=doOverviews, mRating=doRating, mGenres=doGenres, mActors=doActors, mDirectors=doDirectors)

        #save preprocessed data - all matrix
        for key in files:
            #Recompute only if the preprocess has changed or if the file doesn't exists
            if(preprocessingChanged or (not isfile(key))):
                with open(files[key], 'w') as f:
                    pickle.dump(dicoMatrix[key], f)
        #Save labels
        with open(labels_name, 'w') as f:
            pickle.dump(labels, f)
    else:
        print "File %s load process ..." %(filename)
        #load preprocessed data - all matrix
        for key in files:
            with open(files[key], 'r') as f:
                dicoMatrix[key] = pickle.load(f)
#        with open(mat_name, 'r') as f:
#            dico = pickle.load(f)
        #Load labels
        with open(labels_name, 'r') as f:
            labels = pickle.load(f)
        
    'Process OK, model ready to be built !'
    return dicoMatrix, labels

    
    
def testClassifier(doKeras=False, doPerceptron=False, doSVM=False):
    '''
    Tests model accuracy.
        parameters : 
            -doKeras, doPerceptron, doSVM : booleans that tells the classifiers you want to test
        returns : 
            - the mean scores for the classifiers selected
    '''

    if(not (doKeras or doPerceptron or doSVM)):
        raise ValueError('You must specify at least one classifier to test!!!')
    
    meanScoreKeras = 0
    meanScorePerceptron = 0
    meanScoreSVM = 0
    totalScores = 0
    
    doTitles=True
    doRating=True
    doOverviews=True
    doKeywords=True
    doGenres=True
    doActors=True
    doDirectors=True

    #Get all files from PATH, and get the score of the classifier on these files
    for file in os.listdir(path):
        if file.endswith(".json") and ("simple" not in file):
            dico, labels = preprocessFileGeneric(file.replace(".json", ""), doTitles=True, doRating=True, doOverviews=True, doKeywords=True, doGenres=True, doActors=True, doDirectors=True)
            data = prepareDico(dico, doTitles, doRating, doOverviews, doKeywords, doGenres, doActors, doDirectors)
            
            scoreKeras = 0
            scorePerceptron = 0
            scoreSVM = 0
            
            if(doKeras):
                #Prepare the dico that the model takes as parameter
                _, scoreKeras = buildTestModel(data, labels, folds=5)
            if(doPerceptron):
                #data = concatData([ dico[key] for key in dico ])
                scorePerceptron = perceptron.evaluatePerceptron(data, labels)
            if(doSVM):
                #data = concatData([ dico[key] for key in dico ])
                trainInd = int(0.8*len(data) )
                
                svm = LinearSVM()
                svm.train( data[:trainInd], labels[:trainInd])
                scoreSVM = svm.evaluate(data[trainInd:], labels[trainInd:])

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
    
    doOne = False    #If we want to learn a specific movie
    
    scoreP = 0
    scoreSVM = 0
    scoreK = 0
    
    if(doOne):
        #One movie : the one we want to learn
        filename = 'moviesEvaluatedCoralie'
        d, labels = preprocessFileGeneric(filename, doTitles=True, doRating=True, doOverviews=True, doKeywords=True, doGenres=True, doActors=True, doDirectors=True) 
        mat = prepareDico(d, doTitles = True, doRating = True, doOverviews = True, doKeywords=True, doGenres=True, doActors=True, doDirectors=True) 
        _, scoreK = buildTestModel(mat, labels, folds=2)
    else:
        #All movies
        scoreK, scoreP , scoreSVM = testClassifier(doKeras=True, doSVM=True, doPerceptron=True)
    
    print "The classifier keras has an average accuracy of ", scoreK
    print "The classifier perceptron has an average accuracy of ", scoreP
    print "The classifier SVM has an average accuracy of ", scoreSVM