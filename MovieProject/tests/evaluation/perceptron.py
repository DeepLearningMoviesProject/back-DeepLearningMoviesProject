#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:47:11 2017
@author: coralie
"""

from MovieProject.preprocessing.tools import shuffle
from MovieProject.preprocessing import preprocessing
from MovieProject.learning import perceptron
from os.path import isfile
import numpy as np
from flask import json
import pickle


def testShuffle():
    #x = np.array([[0., 0.], [1., 1.], [2., 2.], [3., 3.]])
    x = np.array([0, 1, 2, 3])
    y = np.array([0, 1, 2, 3])
    print "Data : \n" + str(x)
    print "Labels : \n" + str(y) + "\n"
    x,y = shuffle.shuffleDataLabeled(x,y)
    print "Data shuffled: \n" + str(x)
    print "Labels shuffled: \n" + str(y) + "\n"


def testCrossValidationSplit():
    data = np.array([[1,2,2],[2,1,1],[5,8,9],[10,9,8],[9,8,7],[1,3,2]])
    label = np.array([0,0,1,1,1,0])
    print "Data : \n" + str(data)
    print "Label associated : \n" + str(label) + "\n"
    result = perceptron.crossValidationSplit(data, label)
    xTrain, yTrain = result["train"]
    xTest, yTest = result["test"]
    print "Training data (70%) : \n " + str(xTrain)
    print "Label associated : \n" + str(yTrain) + "\n"
    print "Testing data (30%) : \n " + str(xTest)
    print "Label associated : \n"  + str(yTest) + "\n"
    
    
def testevaluatePerceptron():
    # Data
    data = np.array([[1,2,2],[2,1,2],[5,8,9],[10,9,8],[9,8,7],[1,3,2],[5,4,9],[2,2,2],[1,4,1],[1,1,1],[2,1,3],[5,10,9],[11,9,8],[9,10,7],[1,3,1],[5,6,9],[2,3,2],[1,4,3]])
    # Labels
    label = np.array([0,0,1,1,1,0,1,0,0,0,0,1,1,1,0,1,0,0])
    # Perceptron model
    perceptron.evaluatePerceptron(data,label,verbose=True)  

    
def findIds(filename):
    """
    Allows to find datas thanks to movies ids, preprocesses theses datas and stores them in differents files.
    If the files already exist, we just loads them.
    
    Parameters :
        filename : name of the file contained all ids and label associated of a user preferences
    
    Return :
        a liste of all matrix of parameters > titles, keywords, overviews, rates, genres, artistes, directors, labels
    """
    path = '../../resources/evaluations/'
    
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


def test():
    
    #filename = 'moviesEvaluatedCoralie'
    #filename = 'moviesEvaluated-16'
    filename = 'moviesEvaluatedJulian'
    
    result = findIds(filename)
    T = result["T"]
    K = result["K"]
    O = result["O"]
    R = result["R"]
    G = result["G"]
    A = result["A"]
    D = result["D"]

    print "TITLES : "
    perceptron.evaluatePerceptron(result["T"], result["Label"], verbose=True)  
    print "KEYWORDS : "
    perceptron.evaluatePerceptron(result["K"], result["Label"], verbose=True) 
    print "OVERVIEWS : "
    perceptron.evaluatePerceptron(result["O"], result["Label"], verbose=True) 
    print "RATES : "
    perceptron.evaluatePerceptron(result["R"], result["Label"], verbose=True)     
    print "GENRES : "
    perceptron.evaluatePerceptron(result["G"], result["Label"], verbose=True)    
    print "ARTISTS : "
    perceptron.evaluatePerceptron(result["A"], result["Label"], verbose=True)  
    print "DIRECTORS : "
    perceptron.evaluatePerceptron(result["D"], result["Label"], verbose=True) 
    
    RG = np.hstack((G,R))
    print "\n"
    print "RATES / TITLE"
    perceptron.evaluatePerceptron(np.hstack((R,T)), result["Label"], verbose=True) 
    print "RATES / KEYWORDS"
    perceptron.evaluatePerceptron(np.hstack((R,K)), result["Label"], verbose=True) 
    print "RATES / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((R,O)), result["Label"], verbose=True) 
    print "RATES / GENRES"
    perceptron.evaluatePerceptron(np.hstack((R,G)), result["Label"], verbose=True) 
    print "RATES / ARTISTS"
    perceptron.evaluatePerceptron(np.hstack((R,A)), result["Label"], verbose=True) 
    print "RATES / DIRECTORS"
    perceptron.evaluatePerceptron(np.hstack((R,D)), result["Label"], verbose=True) 

    RGK = np.hstack((RG,K))
    print "\n"
    print "RATES / GENRES / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RG,T)), result["Label"], verbose=True) 
    print "RATES / GENRES / KEYWORDS"
    perceptron.evaluatePerceptron(np.hstack((RG,K)), result["Label"], verbose=True) 
    print "RATES / GENRES / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((RG,O)), result["Label"], verbose=True) 
    print "RATES / GENRES / ARTISTS"
    perceptron.evaluatePerceptron(np.hstack((RG,A)), result["Label"], verbose=True) 
    print "RATES / GENRES / DIRECTORS"
    perceptron.evaluatePerceptron(np.hstack((RG,D)), result["Label"], verbose=True) 
    
    RGKA = np.hstack((RGK,A))
    print "\n"
    print "RATES / GENRES / KEYWORDS / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RGK,T)), result["Label"], verbose=True) 
    print "RATES / GENRES / KEYWORDS / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((RGK,T)), result["Label"], verbose=True) 
    print "RATES / GENRES / KEYWORDS / ARTISTES"
    perceptron.evaluatePerceptron(np.hstack((RGK,T)), result["Label"], verbose=True) 
    print "RATES / GENRES / KEYWORDS / DIRECTORS"
    perceptron.evaluatePerceptron(np.hstack((RGK,T)), result["Label"], verbose=True) 
    
    RGKAD = np.hstack((RGKA,D))
    print "\n"
    print "RATES / GENRES / KEYWORDS / ARTISTES / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RGKA,T)), result["Label"], verbose=True) 
    print "RATES / GENRES / KEYWORDS / ARTISTES / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((RGKA,O)), result["Label"], verbose=True) 
    print "RATES / GENRES / KEYWORDS / ARTISTES / DIRECTORS"
    perceptron.evaluatePerceptron(np.hstack((RGKA,D)), result["Label"], verbose=True) 
    
    RGTADO = np.hstack((RGKAD,O))
    print "\n"
    print "RATES / GENRES / KEYWORDS / ARTISTES / DIRECTORS / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RGKAD,T)), result["Label"], verbose=True) 
    print "RATES / GENRES / KEYWORDS / ARTISTES / DIRECTORS / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((RGKAD,O)), result["Label"], verbose=True) 
    
    print "\n"
    print "RATES / GENRES / KEYWORDS / ARTISTES / DIRECTORS / OVERVIEWS / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RGTADO,T)), result["Label"], verbose=True) 
    
            
    
if __name__ == "__main__": 
    
    #testShuffle()
    #testCrossValidationSplit()
    #testevaluatePerceptron()
    test()