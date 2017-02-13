#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:47:11 2017
@author: coralie
"""

from MovieProject.preprocessing.tools import shuffle
from MovieProject.learning import perceptron
from MovieProject.tests.evaluation import evaluation
import numpy as np


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


def test():
    
    #filename = 'moviesEvaluatedCoralie'
    #filename = 'moviesEvaluated-16'
    filename = 'moviesEvaluatedJulian'
    
    result, labels = evaluation.preprocessFileGeneric(filename, doTitles=True, doRating=True, doOverviews=True, doKeywords=True, doGenres=True, doActors=True, doDirectors=True)
    T = result["titles"]
    K = result["keywords"]
    O = result["overviews"]
    R = result["rating"]
    G = result["genres"]
    A = result["actors"]
    D = result["directors"]

    print "TITLES : "
    perceptron.evaluatePerceptron(T, labels, verbose=True)  
    print "KEYWORDS : "
    perceptron.evaluatePerceptron(K, labels, verbose=True) 
    print "OVERVIEWS : "
    perceptron.evaluatePerceptron(O, labels, verbose=True) 
    print "RATES : "
    perceptron.evaluatePerceptron(R, labels, verbose=True)     
    print "GENRES : "
    perceptron.evaluatePerceptron(G, labels, verbose=True)    
    print "ARTISTS : "
    perceptron.evaluatePerceptron(A, labels, verbose=True)  
    print "DIRECTORS : "
    perceptron.evaluatePerceptron(D, labels, verbose=True) 
    
    RG = np.hstack((G,R))
    print "\n"
    print "RATES / TITLE"
    perceptron.evaluatePerceptron(np.hstack((R,T)), labels, verbose=True) 
    print "RATES / KEYWORDS"
    perceptron.evaluatePerceptron(np.hstack((R,K)), labels, verbose=True) 
    print "RATES / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((R,O)), labels, verbose=True) 
    print "RATES / GENRES"
    perceptron.evaluatePerceptron(np.hstack((R,G)), labels, verbose=True) 
    print "RATES / ARTISTS"
    perceptron.evaluatePerceptron(np.hstack((R,A)), labels, verbose=True) 
    print "RATES / DIRECTORS"
    perceptron.evaluatePerceptron(np.hstack((R,D)), labels, verbose=True) 

    RGK = np.hstack((RG,K))
    print "\n"
    print "RATES / GENRES / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RG,T)), labels, verbose=True) 
    print "RATES / GENRES / KEYWORDS"
    perceptron.evaluatePerceptron(np.hstack((RG,K)), labels, verbose=True) 
    print "RATES / GENRES / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((RG,O)), labels, verbose=True) 
    print "RATES / GENRES / ARTISTS"
    perceptron.evaluatePerceptron(np.hstack((RG,A)), labels, verbose=True) 
    print "RATES / GENRES / DIRECTORS"
    perceptron.evaluatePerceptron(np.hstack((RG,D)), labels, verbose=True) 
    
    RGKA = np.hstack((RGK,A))
    print "\n"
    print "RATES / GENRES / KEYWORDS / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RGK,T)), labels, verbose=True) 
    print "RATES / GENRES / KEYWORDS / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((RGK,T)), labels, verbose=True) 
    print "RATES / GENRES / KEYWORDS / ARTISTES"
    perceptron.evaluatePerceptron(np.hstack((RGK,T)), labels, verbose=True) 
    print "RATES / GENRES / KEYWORDS / DIRECTORS"
    perceptron.evaluatePerceptron(np.hstack((RGK,T)), labels, verbose=True) 
    
    RGKAD = np.hstack((RGKA,D))
    print "\n"
    print "RATES / GENRES / KEYWORDS / ARTISTES / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RGKA,T)), labels, verbose=True) 
    print "RATES / GENRES / KEYWORDS / ARTISTES / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((RGKA,O)), labels, verbose=True) 
    print "RATES / GENRES / KEYWORDS / ARTISTES / DIRECTORS"
    perceptron.evaluatePerceptron(np.hstack((RGKA,D)), labels, verbose=True) 
    
    RGTADO = np.hstack((RGKAD,O))
    print "\n"
    print "RATES / GENRES / KEYWORDS / ARTISTES / DIRECTORS / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RGKAD,T)), labels, verbose=True) 
    print "RATES / GENRES / KEYWORDS / ARTISTES / DIRECTORS / OVERVIEWS"
    perceptron.evaluatePerceptron(np.hstack((RGKAD,O)), labels, verbose=True) 
    
    print "\n"
    print "RATES / GENRES / KEYWORDS / ARTISTES / DIRECTORS / OVERVIEWS / TITLES"
    perceptron.evaluatePerceptron(np.hstack((RGTADO,T)), labels, verbose=True) 
    
            
    
if __name__ == "__main__": 
    
    #testShuffle()
    #testCrossValidationSplit()
    #testevaluatePerceptron()
    test()