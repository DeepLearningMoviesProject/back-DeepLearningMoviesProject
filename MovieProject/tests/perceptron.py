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

    

def findIds(filename):
    """
    Allows to find datas thanks to movies ids, preprocesses theses datas and stores them in differents files.
    If the files already exist, we just loads them.
    
    Parameters :
        filename : name of the file contained all ids and label associated of a user preferences
    
    Return :
        a liste of all matrix of parameters > titles, keywords, overviews, rates, genres, artistes, directors, labels
    """
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
        #load preprocessed data
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
            
    return {"T":T, "K":K, "O":O, "R":R, "G":G, "A":A, "D":D, "Label":labels}

            
    
if __name__ == "__main__": 

    #filename = 'moviesEvaluatedCoralie'
    filename = 'moviesEvaluated-16'
    #filename = 'moviesEvaluatedJulian'
    result = findIds(filename)
    T = result["T"]
    K = result["K"]
    O = result["O"]
    R = result["R"]
    G = result["G"]
    A = result["A"]
    D = result["D"]

    print "TITLES : "
    perceptron.evaluatePerceptron(result["T"], result["Label"])
    print "KEYWORDS : "
    perceptron.evaluatePerceptron(result["K"], result["Label"])
    print "OVERVIEWS : "
    perceptron.evaluatePerceptron(result["O"], result["Label"])
    print "RATES : "
    perceptron.evaluatePerceptron(result["R"], result["Label"])    
    print "GENRES : "
    perceptron.evaluatePerceptron(result["G"], result["Label"])   
    print "ARTISTS : "
    perceptron.evaluatePerceptron(result["A"], result["Label"]) 
    print "DIRECTORS : "
    perceptron.evaluatePerceptron(result["D"], result["Label"])
    
    RG = np.hstack((G,R))
    print "\n"
    print "RATES / TITLE"
    perceptron.evaluatePerceptron(np.hstack((R,T)), result["Label"])
    print "RATES / KEYWORDS"
    perceptron.evaluatePerceptron(np.hstack((R,K)), result["Label"])
    print "RATES / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((R,O)), result["Label"])
    print "RATES / GENRES"
    perceptron.evaluatePerceptron(np.hstack((R,G)), result["Label"])
    print "RATES / ARTISTS"
    perceptron.evaluatePerceptron(np.hstack((R,A)), result["Label"])
    print "RATES / DIRECTORS"
    perceptron.evaluatePerceptron(np.hstack((R,D)), result["Label"])

    RGK = np.hstack((RG,K))
    print "\n"
    print "RATES / GENRES / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RG,T)), result["Label"])
    print "RATES / GENRES / KEYWORDS"
    perceptron.evaluatePerceptron(np.hstack((RG,K)), result["Label"])
    print "RATES / GENRES / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((RG,O)), result["Label"])
    print "RATES / GENRES / ARTISTS"
    perceptron.evaluatePerceptron(np.hstack((RG,A)), result["Label"])
    print "RATES / GENRES / DIRECTORS"
    perceptron.evaluatePerceptron(np.hstack((RG,D)), result["Label"])
    
    RGKA = np.hstack((RGK,A))
    print "\n"
    print "RATES / GENRES / KEYWORDS / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RGK,T)), result["Label"])
    print "RATES / GENRES / KEYWORDS / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((RGK,T)), result["Label"])
    print "RATES / GENRES / KEYWORDS / ARTISTES"
    perceptron.evaluatePerceptron(np.hstack((RGK,T)), result["Label"])
    print "RATES / GENRES / KEYWORDS / DIRECTORS"
    perceptron.evaluatePerceptron(np.hstack((RGK,T)), result["Label"])
    
    RGKAD = np.hstack((RGKA,D))
    print "\n"
    print "RATES / GENRES / KEYWORDS / ARTISTES / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RGKA,T)), result["Label"])
    print "RATES / GENRES / KEYWORDS / ARTISTES / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((RGKA,O)), result["Label"])
    print "RATES / GENRES / KEYWORDS / ARTISTES / DIRECTORS"
    perceptron.evaluatePerceptron(np.hstack((RGKA,D)), result["Label"])
    
    RGTADO = np.hstack((RGKAD,O))
    print "\n"
    print "RATES / GENRES / KEYWORDS / ARTISTES / DIRECTORS / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RGKAD,T)), result["Label"])
    print "RATES / GENRES / KEYWORDS / ARTISTES / DIRECTORS / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((RGKAD,O)), result["Label"])
    
    print "\n"
    print "RATES / GENRES / KEYWORDS / ARTISTES / DIRECTORS / OVERVIEWS / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RGTADO,T)), result["Label"])
    