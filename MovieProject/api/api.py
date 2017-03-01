#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:16:32 2017

@author: Kaito
"""
from flask import Flask, jsonify, request, json, session, g
from flask_cors import CORS, cross_origin
from bcrypt import gensalt, hashpw

from datetime import datetime, timedelta
from functools import wraps
from jwt import encode, decode, DecodeError, ExpiredSignature

from MovieProject.preprocessing import Preprocessor
from MovieProject.learning import buildModel, suggestNMovies
from MovieProject.sql import DatabaseManager

import numpy as np


app = Flask(__name__)
app.config['TOKEN_SECRET'] = 'Secret_Token' #Change this
app.config['SECRET_KEY'] = 'Secret_Key' #Change this
app.config['CORS_HEADERS'] = ['Content-Type', 'Authorization']
app.config['CORS_AUTOMATIC_OPTIONS'] = True
CORS(app)



dbManager = DatabaseManager()


movieIds = {"415":1, "9320":0, "26914":1, "11059":1}




def createToken(user):
    """
        Create a token for a user with an expiration of ...
    """
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=1)
    }
    token = encode(payload, app.config['TOKEN_SECRET'])
    return token.decode('unicode_escape')


def parseToken(req):
    """
        Check if the token is correct
    """
    token = req.headers.get('Authorization').split()[1]
    return decode(token, app.config['TOKEN_SECRET'])


def loginRequired(f):
    """
        Decorator for use of token to have an access to a route 
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #Allow OPTIONS request
        if request.headers.get("Access-Control-Request-Headers") == "authorization":
            response = jsonify(message="ok")
            response.status_code = 200
            return response
        
        #Reject request with no header Authorization
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parseToken(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function



@app.route('/testId', methods=['GET'])
@loginRequired
@cross_origin()
def get_tasks():
    return jsonify(movieIds), 200


@app.route('/train', methods=['POST'])
@loginRequired
@cross_origin()
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



@app.route('/auth/signup', methods=['POST'])
@cross_origin()
def signup():
    data = json.loads(request.data)

    password = hashpw(data["password"].encode('utf-8'), gensalt())
    
    dbManager.insertUser(data["name"], email=data["email"], password=password)
    user = dbManager.getUser(data["name"])
    
    session['logged_in'] = True

    return jsonify(token=createToken(user)), 200


@app.route('/auth/login', methods=['POST'])
@cross_origin()
def login():
    data = json.loads(request.data)

    user = dbManager.getUser(data["name"])
    if not user:
        return jsonify(error="No such user"), 404
    
    password = data["password"].encode('utf-8')

    if user.password == hashpw(password, user.password):
        session['logged_in'] = True
        return jsonify(token=createToken(user)), 200
    else:
        return jsonify(error="Wrong name or password"), 400


@app.route('/auth/logout')
@cross_origin()
@loginRequired
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'}), 200



if __name__ == '__main__':
    app.run(debug=False, host= '0.0.0.0')

