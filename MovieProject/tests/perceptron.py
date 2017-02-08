#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:47:11 2017

@author: coralie
"""

from MovieProject.preprocessing import preprocessing
from MovieProject.learning import perceptron
from os.path import isfile
import numpy as np
from flask import json
import pickle

path = '../resources/evaluations/'

filename = 'moviesEvaluated-16'

    
#Test function
def findIds(filename):

    tname = path + filename + '-Tsave.data'
    kname = path + filename + '-Ksave.data'
    oname = path + filename + '-Osave.data'
    rname = path + filename + '-Rsave.data'
    gname = path + filename + '-Gsave.data'
    aname = path + filename + '-Asave.data'
    dname = path + filename + '-Dsave.data'
    lname = path + filename + '-LABELSsave.data'

    preprocessingChanged = False #Set to true if the processing has changed
    dontPreprocess = (not preprocessingChanged) and isfile(tname) and isfile(kname) and isfile(oname) and isfile(rname) and isfile(gname) and isfile(aname) and isfile(dname) and isfile(lname)
    
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

        result = preprocessing.preprocessMatrix(ids, mTitles=True, mKeywords=True, mOverviews=True, mRating=True, mGenres=True, mActors=True, mDirectors=True)
        
        #save labels
        with open(lname, 'w') as f:
            pickle.dump(labels, f)
        with open(tname, 'w') as f:
            pickle.dump(result['titles'], f)
            T = result['titles']
        with open(kname, 'w') as f:
            pickle.dump(result['keywords'], f) 
            K = result['keywords']
        with open(oname, 'w') as f:
            pickle.dump(result['overview'], f)
            O = result['overview']
        with open(rname, 'w') as f:
            pickle.dump(result['rating'], f)
            R = result['rating']
        with open(gname, 'w') as f:
            pickle.dump(result['genres'], f)
            G = result['genres']
        with open(aname, 'w') as f:
            pickle.dump(result['actors'], f)
            A = result['actors']
        with open(dname, 'w') as f:
           pickle.dump(result['directors'], f)
           D = result['directors']
            
    else:
        print "File % load process ...", filename
        #load preprocessed data (T & G)
        with open(tname, 'r') as f:
            T = pickle.load(f)
        with open(kname, 'r') as f:
            K = pickle.load(f)      
        with open(oname, 'r') as f:
            O = pickle.load(f)
        with open(rname, 'r') as f:
            R = pickle.load(f)
        with open(gname, 'r') as f:
            G = pickle.load(f)
        with open(aname, 'r') as f:
            A = pickle.load(f)
        with open(dname, 'r') as f:
            D = pickle.load(f)            
        with open(lname, 'r') as f:
            labels = pickle.load(f)
            
    return (T,K,O,R,G,A,D,labels)

            
    
if __name__ == "__main__": 

    filename = 'moviesEvaluated-16'
    T, labels = findIds(filename)
    print "training perceptron on title"
    trainingPerceptron(T, labels)