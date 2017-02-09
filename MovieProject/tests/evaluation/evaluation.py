#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 14:50 2017

@author: elsa
"""
import numpy as np
import pickle
from MovieProject.preprocessing import preprocess, preprocessMatrix, prepareDico
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
def preprocessMovieGeneric(filename):
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
        dontPreprocess = dontPreprocess and isfile(f)
    
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