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

from MovieProject.learning import sentimentPrediction as pred
from MovieProject.preprocessing import Preprocessor
from MovieProject.sql import User, DatabaseManager
from MovieProject.preprocessing.tools import createCorpusOfAbtracts, gloveDict, D2VOnCorpus
from MovieProject.learning import buildModel, suggestNMovies, sentimentAnalysis
from MovieProject.resources import GLOVE_DICT_FILE, OVERVIEWS_TR_FILE, OVERVIEW_MODEL, SENTIMENT_ANALYSIS_MODEL

import numpy as np
from os.path import isfile

from exceptions import Exception



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
        'sub': user.name,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=14)
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

        g.user_name = payload['sub']

        return f(*args, **kwargs)

    return decorated_function


def getIdFromLikedMovies(username, isLiked):
    """
    
    """
    
    movies = dbManager.getMoviesLikedByUser(username,isLiked)
    return { str(movie.idMovie) : int(movie.liked) for movie in movies}


@app.route('/testId', methods=['GET'])
@loginRequired
@cross_origin()
def get_tasks():
    return jsonify(movieIds), 200


@app.route('/api/train', methods=['POST'])
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
@cross_origin()
@loginRequired
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



@app.route('/api/updateMovies', methods=["POST"])
@cross_origin()
@loginRequired
def updateMovies():
    data = json.loads(request.data)
    
    try:
        dbManager.updateLikedMoviesForUser(g.user_name, data)
    except Exception as e:
        return jsonify(error=str(e), movies=getIdFromLikedMovies(g.user_name, None)), 500
    else:
        return jsonify(movies=getIdFromLikedMovies(g.user_name, None)), 200
    

@app.route('/api/likedMovies/<string:opinion>', methods=["GET"])
@cross_origin()
@loginRequired
def likedMovies(opinion):
    if opinion == "liked": isLiked = True
    elif opinion == "disliked" : isLiked = False
    elif opinion == "all" : isLiked = None 
    else : return jsonify(error="Argument \"%s\" not authorized" %(opinion)), 400
    
    return jsonify(movies=getIdFromLikedMovies(g.user_name, isLiked)), 200


@app.route('/auth/signup', methods=['POST'])
@cross_origin()
def signup():
    data = json.loads(request.data)

    password = hashpw(data["password"].encode('utf-8'), gensalt())
    occupation = dbManager.getOccupation(data["occupation"])
    country = dbManager.getRegion(data["country"])
    
    if data["sex"] == "H": sex = True
    elif data["sex"] == "F": sex = False
    else: sex = None
    
    user = User(data["name"], password, data["email"],
                birthday=data["birthday"], 
                sexe=sex, 
                idOccupation=occupation.id,
                idCountry=country.id)
    
    dbManager.insertUser(user)
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
               
               
        return jsonify(movies={umovie.idMovie:int(umovie.liked) for umovie in user.movies},
                       token=createToken(user)), 200
    else:
        return jsonify(error="Wrong name or password"), 400


@app.route('/auth/logout')
@cross_origin()
@loginRequired
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'}), 200


    
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

