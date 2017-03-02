#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:16:32 2017

@author: Kaito
"""
from flask import Flask, jsonify, request, abort, json
#from testTMDB import searchData, trainData
from MovieProject.preprocessing import Preprocessor
from MovieProject.learning import buildModel, suggestNMovies
import numpy as np

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


if __name__ == '__main__':
    app.run(debug=False, host= '0.0.0.0')

