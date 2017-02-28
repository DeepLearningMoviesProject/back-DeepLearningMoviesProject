#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:16:32 2017

@author: Kaito
"""
from flask import Flask, jsonify, request, abort, json, session
from bcrypt import gensalt, hashpw
#from testTMDB import searchData, trainData
from MovieProject.preprocessing import Preprocessor
from MovieProject.learning import buildModel, suggestNMovies
from MovieProject.sql import DatabaseManager
import numpy as np

app = Flask(__name__)
app.config['TOKEN_SECRET'] = 'Secret_Token' #Change this
app.config['SECRET_KEY'] = 'Secret_Key' #Change this

dbManager = DatabaseManager()


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
    
    print "Model built, start prediction"
    
    movies = suggestNMovies(model, 10, **params)
    
    print "Movies predicted !"
    
#    return jsonify({'result': "ok"})
    
    dico = {"prediction" : movies.tolist()}
    return jsonify(dico)


@app.route('/auth/signup', methods=['POST'])
def signup():
    data = json.loads(request.data)

    password = hashpw(data["password"].encode('utf-8'), gensalt())
    
    dbManager.insertUser(data["name"], email=data["email"], password=password)
    user = dbManager.getUser(data["name"])
    
    session['logged_in'] = True

    return jsonify(token=user.token(app.config['TOKEN_SECRET']))


@app.route('/auth/login', methods=['POST'])
def login():
    data = json.loads(request.data)

    user = dbManager.getUser(data["name"])
    if not user:
        return jsonify(error="No such user"), 404
    
    password = data["password"].encode('utf-8')

    if user.password == hashpw(password, user.password):
        session['logged_in'] = True
        return jsonify(token=user.token(app.config['TOKEN_SECRET'])), 200
    else:
        return jsonify(error="Wrong name or password"), 400


@app.route('/auth/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})



if __name__ == '__main__':
    app.run(debug=False, host= '0.0.0.0')


