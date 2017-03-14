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
from MovieProject.preprocessing import concatData, Preprocessor
from MovieProject.learning import buildTestModel, LinearSVM, perceptron
from MovieProject.resources import RES_PATH
from flask import json
from os.path import isfile, join
import matplotlib.pyplot as plt
from string import maketrans

from MovieProject.resources import RES_PATH


path = join(RES_PATH, 'evaluations/')

preprocessingChanged = False #Set to true if the processing has changed

#Test function
def preprocessFileGeneric(filename, **kwargs):
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
    for key in kwargs:
        if kwargs[key]:
            files[key] = join(path, filename + "-%ssave.data" %(key) )

    if not files:
        #TODO : raise an error
        print "Nothing to preprocess here !"

    #mat_name = path + filename + '-' + names + '-save.data'
    labels_name = join(path, filename + '-LABELSsave.data')

    dontPreprocess = (not preprocessingChanged) and isfile(labels_name)
    
    for f in files:
        dontPreprocess = dontPreprocess and isfile(files[f])
        
    dicoMatrix = {}
    labels = np.array([])
    
    pProcessor = Preprocessor(**kwargs)
    
    if(preprocessingChanged):
        print "Preprocessing has changed !"

    #if data has not been preprocessed 
    if(not dontPreprocess):
        print "File %s in process ..." %(filename)
        #load data from json
        jname = join(path, filename + '.json')
        with open(jname) as data_file:    
            data = json.load(data_file)

        #Get ids and labels of data
        ids = [int(key) for key in data]
        labels = np.array([data[key] for key in data])

        #preprocess data
        dicoMatrix = pProcessor.preprocessMatrix(ids)

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

        with open(labels_name, 'r') as f:
            labels = pickle.load(f)
                 
    return dicoMatrix, labels

    
def combinaison(seq):
    """
        Return all differents part from a list 
    """
    p = []
    for i in range(1, 2**len(seq)):
        p.append([ seq[j] for j in range(len(seq)) if (i>>j)&1 ])
    return sorted(p, key=lambda l: len(l))
    

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
    result = {}
    params = {"titles" : True,
              "rating" : True,
              "overviews" : True,
              "keywords" : True,
              "genres" : True,
              "actors" : True,
              "directors" : True,
              "compagnies" : True,
              "language" : True,
              "belongs" : True,
              "runtime" : True,
              "date" : True }
    

    meanScoreKeras = 0.
    meanScorePerceptron = 0.
    meanScoreSVM = 0.
    totalScores = 0.


    #Get all files from PATH, and get the score of the classifier on these files        
    for file in os.listdir(path):
        if file.endswith(".json") and ("simple" not in file):
            dico, labels = preprocessFileGeneric(file.replace(".json", ""), **params)
                        
            for i, p in enumerate(combinaison(params.keys())):
                
                for key in params: params[key] = key in p
                
                data = Preprocessor(**params).prepareDico({ key: dico[key] for key in params if params[key]})                     
                
                print "#### {} ####".format(p)   
                name = str(p).translate(maketrans("[]\'","   "))
                scoreKeras = 0.0
                scorePerceptron = 0.0
                scoreSVM = 0.0
                result[name] = {}
                if(doKeras):
                    #Prepare the dico that the model takes as parameter
                    _, scoreKeras = buildTestModel(data, labels, folds=5)
                    result[name]["Keras"] = scoreKeras
                if(doPerceptron):
                    #data = concatData([ dico[key] for key in dico ])
                    scorePerceptron = perceptron.evaluatePerceptron(data, labels)
                    result[name]["Perceptron"] = scorePerceptron
                if(doSVM):
                    #data = concatData([ dico[key] for key in dico ])
                    trainInd = int(0.8*len(data) )                    
                    svm = LinearSVM()
                    svm.train( data[:trainInd], labels[:trainInd])
                    scoreSVM = svm.evaluate(data[trainInd:], labels[trainInd:])
                    result[name]["SVM"] = scoreSVM

                meanScoreKeras += scoreKeras
                meanScorePerceptron += scorePerceptron
                meanScoreSVM += scoreSVM
                totalScores += 1
    
    #Compute the mean score for the classifier
    meanScoreKeras /= totalScores
    meanScorePerceptron /= totalScores
    meanScoreSVM /= totalScores
                
    return meanScoreKeras, meanScorePerceptron, meanScoreSVM, result


def testClassifier2(doKeras=False, doPerceptron=False, doSVM=False):
    """
    Tests model accuracy.
        parameters : 
            -doKeras, doPerceptron, doSVM : booleans that tells the classifiers you want to test
        returns : 
            - the mean scores for the classifiers selected
    """

    if(not (doKeras or doPerceptron or doSVM)):
        raise ValueError('You must specify at least one classifier to test!!!')
        
    result = {}
    params = {"titles" : True,
              "rating" : True,
              "overviews" : True}
#              "keywords" : True,
#              "genres" : True,
#              "actors" : True,
#              "directors" : True,
#              "compagnies" : True,
#              "language" : True,
#              "belongs" : True,
#              "runtime" : True,
#              "date" : True }
    
    paramsIn = dict(params)
    paramsOut = {}

    while len(paramsIn.keys()) > 0:

        pData = { p:True for p in paramsOut.keys() }
        resDescriptor = {}
        
        for p in paramsIn.keys(): 
            pProcessor = dict(pData)
            pProcessor[p] = True
                 
            scoreKeras = 0.0
            scorePerceptron = 0.0
            scoreSVM = 0.0
            nbFile = 0.0
            
            resDescriptor[p] = {}
#            for file in os.listdir(path)  :
            for file in ['moviesEvaluated-test.json']: 
                if file.endswith(".json") and ("simple" not in file):
                    dico, labels = preprocessFileGeneric(file.replace(".json", ""), **params)
                    data = Preprocessor(**pProcessor).prepareDico(dico)  
                    
                    nbFile += 1
                    
                    if data.shape[1] == 1 : continue
                    
                    print "#### {} ####".format(pProcessor.keys())   

                    if(doKeras):
                        #Prepare the dico that the model takes as parameter
                        _, score = buildTestModel(data, labels, folds=5)
                        scoreKeras += score
                        
                    if(doPerceptron):
                        #data = concatData([ dico[key] for key in dico ])
                        scorePerceptron += perceptron.evaluatePerceptron(data, labels)
                        
                    if(doSVM):
                        #data = concatData([ dico[key] for key in dico ])
                        trainInd = int(0.8*len(data) )                    
                        svm = LinearSVM()
                        svm.train( data[:trainInd], labels[:trainInd])
                        scoreSVM += svm.evaluate(data[trainInd:], labels[trainInd:])
                        
            
            if doKeras: resDescriptor[p]["Keras"] = scoreKeras / nbFile
            if doPerceptron: resDescriptor[p]["Perceptron"] = scorePerceptron / nbFile
            if doSVM: resDescriptor[p]["SVM"] = scoreSVM / nbFile 

        maxIndex, valueModels = sorted(resDescriptor.iteritems(), key=lambda (k,v):(v["Keras"],k), reverse=True)[0]
        pData[maxIndex] = True
        
        name = str(pData.keys()).translate(maketrans("[]\'","   "))
        result[name] = resDescriptor[maxIndex]
         
        paramsIn.pop(maxIndex)
        paramsOut[maxIndex] = True
                  
    return result
                
                              
            

def graphique(result, sortBy, nbValue=None, minAverage=0):
    if type(result) != dict:        #on s'assure ici que la donnee est bien un dico pour le reste du programme
        return
    
    if nbValue >= len(result.keys()):
        return
    
    invalide = 0
    nbGraph = 0.5
    legende = 99.
    origine = 0.
    
    colors = {"Keras":"Red","SVM":"Blue","Perceptron":"Green"}
    
    for cat, value in sorted(result.iteritems(), key=lambda (k,v):(v[sortBy],k), reverse=True)[:nbValue]:
        origine = nbGraph-0.25        
        valide = 0        
        
        for test in value: #Pour chaque resultat on fait un graphique droit, de cette manière nous pourrons
            if result[cat][test]>minAverage:
                abscisse = [nbGraph, nbGraph]               #avoir plusieurs couleurs différentes. A noter quue plt.hist peut faire un histogramme beaucoup plus facilement.
                ordonne = [0, result[cat][test]]
                print(str(test))
                plt.plot(abscisse, ordonne, linewidth = 3, color=colors[test])
                plt.text(nbGraph, result[cat][test], str(test))
                nbGraph += 0.5
                valide = 1
            else: 
                invalide += 1
        
        if valide == 1:
            legende -= 1.5
            plt.text(origine, legende, str(cat))
            plt.plot([origine, origine], [50, 100], color="black")

        if nbGraph >= 5:
            plt.title("Resultats")
            plt.ylabel("Reussite")
            plt.axis([0, nbGraph, 50, 100])            
            plt.show()
            plt.figure()
            nbGraph = 0.5
            legende = 99.

    
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
#        scoreK, scoreP , scoreSVM, resultat = testClassifier(doKeras=False, doSVM=True, doPerceptron=True)
        resultat = testClassifier2(doKeras=True, doSVM=True, doPerceptron=False)
        
        print "The classifier keras has an average accuracy of ", scoreK 
        print "The classifier perceptron has an average accuracy of ", scoreP 
        print "The classifier SVM has an average accuracy of ", scoreSVM
        
        with open(join(RES_PATH, "evaluation.data"), 'w') as f:
            pickle.dump(resultat, f)
                    
        with open(join(RES_PATH, "evaluation.data")) as res:    
            resultat = pickle.load(res)
            graphique(resultat, "Keras", minAverage=60)
    