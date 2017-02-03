# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 16:57:58 2017

@author: elsa
"""

import numpy as np
import pickle
from MovieProject.learning import buildModel, buildTestModel
from MovieProject.preprocessing import preprocess
from flask import json
import os.path

#Test function
def test():
    path = '../resources/evaluations/'
    filename = 'moviesEvaluated-16'
    tname = path + filename + '-Tsave.data'
    gname = path + filename + '-Gsave.data'
    lname = path + filename + '-LABELSsave.data'

    preprocessingChanged = False
    dontPreprocess = (not preprocessingChanged) and os.path.isfile(tname) and os.path.isfile(gname) and os.path.isfile(lname)
    T = np.array([])
    G = np.array([])
    labels = np.array([])
    

    
    #if data has not been preprocessed 
    if(not dontPreprocess):
        print 'In process ...'
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
        print 'Load process ...'
        #load preprocessed data (T & G)
        with open(tname, 'r') as f:
            T = pickle.load(f)
        with open(gname, 'r') as f:
            G = pickle.load(f)
        with open(lname, 'r') as f:
            labels = pickle.load(f)
    
    'Process OK, model ready to be built !'
    model = buildTestModel(T, G, labels)
    #model = buildModel(T, G, labels)


if __name__ == '__main__':
    test()