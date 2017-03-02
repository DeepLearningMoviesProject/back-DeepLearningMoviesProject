#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:16:32 2017

@author: Kaito
"""
from flask import Flask, jsonify, request, abort, json
#from testTMDB import searchData, trainData
from MovieProject.learning import sentimentPrediction as pred
from MovieProject.preprocessing import Preprocessor
from MovieProject.preprocessing.tools import createCorpusOfAbtracts, gloveDict, D2VOnCorpus
from MovieProject.learning import buildModel, suggestNMovies, sentimentAnalysis
import numpy as np

from os.path import isfile
from MovieProject.resources import GLOVE_DICT_FILE, OVERVIEWS_TR_FILE, OVERVIEW_MODEL, SENTIMENT_ANALYSIS_MODEL



app = Flask(__name__)


movieIds = {"415":1, "9320":0, "26914":1, "11059":1}

@app.route('/testId', methods=['GET'])
def get_tasks():
    return jsonify(movieIds)


@app.route('/train', methods=['POST'])
def trainModel():    
    
    dico = json.loads(request.data)
    ids = [int(key) for key in dico]
    
    #X_train = searchData(ids)
    labels = np.array([dico[key] for key in dico])
    
    print "Movies received"

    params = { "titles":True,
               "rating":True,
               "overviews":True,
               "keywords":True,
               "genres":True,
               "actors":True,
               "directors":True,
              "compagnies" : True,
              "language" : True,
              "belongs" : True,
              "runtime" : True,
              "date" : True }
    
    pProcessor = Preprocessor(**params)

    #preprocess data
    data = pProcessor.preprocess(ids)
    
    print "Movies loaded, building model"
    
    model = buildModel(data, labels)
    
    return jsonify({'result': "ok"})
    
#    print "Model built, start prediction"
#    
#    sugg = suggestNMovies(model, 10, **params)
#    
#    print "Movies predicted !"
#    
#    return jsonify(sugg)


@app.route('/prediction', methods=['GET'])
def predictMovies():
    
    #Here we create a model but in the end we will load it from the DB
    movies = {"11":1,"18":1,"22":1}
     
    ids = [int(key) for key in movies]
    
    labels = np.array([movies[key] for key in movies])
    
    print "Movies received"

    params = { "titles":True,
               "rating":True,
               "overviews":True,
               "keywords":True,
               "genres":True,
               "actors":True,
               "directors":True,
              "compagnies" : True,
              "language" : True,
              "belongs" : True,
              "runtime" : True,
              "date" : True }
    
    pProcessor = Preprocessor(**params)

        #preprocess data
    data = pProcessor.preprocess(ids)
    
    print "Movies loaded, building model"
    
    model = buildModel(data, labels)
    
    print "Model built, start prediction"
    
    #This is what we will do after we get the model from DB
    
    sugg = suggestNMovies(model, 10, **params)
    
    print "Movies predicted !"
    return jsonify(sugg)


    
@app.route('/popularity', methods=['POST'])
def checkPopularity():   
   
    dico = json.loads(request.data)
    ids = [int(key) for key in dico]
    popularity, sentiments = pred.classificationMovies(ids) 
    return jsonify({"popularity" : popularity, "sentiments" : sentiments})

    
def _initAPI():
    """
        Create all resources needed if they don't already exist
    """
    #If the file is not present in the resource, creates it 
    if not isfile(GLOVE_DICT_FILE):
        print 'Creation of the glove dictionnary file...'
        gloveDict.createGloveDic()
    if not isfile(OVERVIEWS_TR_FILE):
        print 'Create the corpus of overviews :'
        createCorpusOfAbtracts.createCorpus(OVERVIEWS_TR_FILE)
    if not isfile(OVERVIEW_MODEL):
        print 'Create the D2V model on the overwiews corpus :'
        D2VOnCorpus.createD2VModel()
    if not isfile(SENTIMENT_ANALYSIS_MODEL):   
        print 'Create the sentiment analysis model on tweets corpus :'
        sentimentAnalysis.createModel()

    
if __name__ == '__main__':
    
    _initAPI()
    
    app.run(debug=False, host= '0.0.0.0')

