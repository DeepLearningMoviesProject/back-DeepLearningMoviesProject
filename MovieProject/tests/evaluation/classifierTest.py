# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 16:57:58 2017

@author: Elsa Navarro
"""

import numpy as np
import pickle
import os
from MovieProject.learning import buildTestModel
from MovieProject.preprocessing import preprocess, preprocessMatrix
from flask import json
from os.path import isfile

path = '../../resources/evaluations/'

doTitles=False
doKeywords=False
doOverviews=True
doRating=False

doGenres=True
doActors=True
doDirectors=True

preprocessingChanged = False #Set to true if the processing has changed

#Test function
def preprocessMovie(filename):
    #filename = 'moviesEvaluated-16'
    tname = path + filename + '-Tsave.data'
    gname = path + filename + '-Gsave.data'
    lname = path + filename + '-LABELSsave.data'

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

        # datas = preprocessMatrix(ids, mTitles = true)
       # T = datas['titles']

        #save preprocessed data (T & G)
        with open(tname, 'w') as f:
            pickle.dump(T, f)
        # with open(gname, 'w') as f:
        #     pickle.dump(G, f)
        with open(lname, 'w') as f:
            pickle.dump(labels, f)
    else:
        print "File %s load process ..." %(filename)
        #load preprocessed data (T & G)
        with open(tname, 'r') as f:
            T = pickle.load(f)
        with open(gname, 'r') as f:
            G = pickle.load(f)
        with open(lname, 'r') as f:
            labels = pickle.load(f)
        
    'Process OK, model ready to be built !'
    return T, G, labels
    
    
def concatData(listMatrix):
    if(len(listMatrix)==0):
        return np.array([])
        
    if(len(listMatrix)==1):
        return listMatrix[0]
    
    return np.hstack((listMatrix[0], concatData(listMatrix[1:])))

def prepareDico(matrix):
    dico = {}
    toConcat = []
    
    if(doTitles):
        toConcat.append(matrix["titles"])

    if(doRating):
        toConcat.append(matrix["rating"])

    if(doOverviews):
        toConcat.append(matrix["overviews"])

    if(doKeywords):
        toConcat.append(matrix["keywords"])

    concatMatrix = concatData(toConcat)
    
    if concatMatrix.size:
        dico["data"] = concatMatrix


    if(doGenres):
        dico["genres"] = matrix["genres"]

    if(doActors):
        dico["actors"] = matrix["actors"]

    if(doDirectors):
        dico["directors"] = matrix["directors"]
    
    return dico
    
#Test function
def preprocessMovieGeneric(filename):
    #filename = 'moviesEvaluated-16'
    names = []
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
        dontPreprocess = dontPreprocess and isfile(f)
    
#    T = np.array([])
#    G = np.array([])
    martix = {}
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
        #dico = prepareDico(matrix)

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
        for key, value in files:
            with open(value, 'w') as f:
                pickle.dump(matrix[key], f)
                matrix[key] = pickle.load(f)
#        with open(mat_name, 'r') as f:
#            dico = pickle.load(f)
        #Load labels
        with open(labels_name, 'r') as f:
            labels = pickle.load(f)
        
    'Process OK, model ready to be built !'
    return prepareDico(matrix), labels


def testClassifier():

    meanScore = 0
    totalScores = 0

    #Get all files from PATH, and get the score of the classifier on these files
    for file in os.listdir(path):
        if file.endswith(".json"):
            dico, labels = preprocessMovieGeneric(file.replace(".json", ""))
            # dico = {
            #     "data" : T,
            #     "genres" : G,
            # }
            model, score = buildTestModel(dico, labels, folds=5)
            meanScore += score
            totalScores += 1
    #Compute the mean score for the classifier
    meanScore /= totalScores
    return meanScore


if __name__ == '__main__':
    #All movies
    score = testClassifier()
    #One movie
#    filename = 'moviesEvaluated-simple'
#    dico, labels = preprocessMovieGeneric(filename)
#    model, score = buildTestModel(dico, labels, folds=2)
    
    print "The classifier has an average accuracy of ", score