# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 16:57:58 2017

@author: Elsa Navarro
"""

import numpy as np
import pickle
from MovieProject.preprocessing import Preprocessor
from flask import json
from os.path import isfile

path = '../../resources/evaluations/'

doTitles=True
doKeywords=True
doOverviews=True
doRating=True

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