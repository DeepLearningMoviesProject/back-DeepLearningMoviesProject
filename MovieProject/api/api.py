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
from MovieProject.sql import User, DatabaseManager
from MovieProject.preprocessing.tools import createCorpusOfAbtracts, gloveDict, D2VOnCorpus
from MovieProject.learning import getNBestMovies, saveModel, loadModel, preprocessDataTrainModel, suggestNMovies, sentimentAnalysis
from MovieProject.resources import GLOVE_DICT_FILE, OVERVIEWS_TR_FILE, OVERVIEW_MODEL, SENTIMENT_ANALYSIS_MODEL

#import numpy as np
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

params = {"titles" : False,
          "rating" : True,
          "overviews" : True,
          "keywords" : False,
          "genres" : True,
          "actors" : False,
          "directors" : True,
          "compagnies" : True,
          "language" : False,
          "belongs" : True,
          "runtime" : True,
          "date" : False }

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


@app.route('/testId', methods=['GET'])
@cross_origin()
@loginRequired
def get_tasks():
    return jsonify(movieIds), 200


@app.route('/api/train', methods=['POST'])
@cross_origin()
@loginRequired
def trainModel():

    #Retrieve the user movies
    username = g.user_name
#    username = 'User1'
    userMovies = dbManager.getIdFromLikedMovies(username, None)
    model = preprocessDataTrainModel(userMovies, **params)

    print "Saving model to file ..."
    
    saveModel(username, model)

    #Tell to the front that the model is ready
    return jsonify({'result': "ok"})


@app.route('/api/prediction', methods=['GET'])
@cross_origin()
@loginRequired
def predictMovies():
    
    #Here we load the model for the user
    username = g.user_name
#    username = 'User1'
    
    model = loadModel(username)
    
    print "Model retrieved !"
    
    if model is None :
        userMovies = dbManager.getIdFromLikedMovies(username, None)
        model = preprocessDataTrainModel(userMovies, **params)
    
    if model is not None :
        #Here we suggest 10 movies
        sugg = suggestNMovies(model, 10, **params)
    
        print "Movies predicted !"
        return jsonify(sugg)
    else:
        return jsonify({'error': "Failed to create model for this user."})
    

@app.route('/api/predictionFM', methods=['GET'])
@cross_origin()
@loginRequired
def predictMoviesFM():
    
    #Here we load the model for the user
    username = g.user_name
    userID = dbManager.getUser(username).id
    
    movies = getNBestMovies(userID, n=10)
    
    return jsonify(movies)
    
@app.route('/api/updateMovies', methods=["POST"])
@cross_origin()
@loginRequired
def updateMovies():
    data = json.loads(request.data)
    
    try:
        dbManager.updateLikedMoviesForUser(g.user_name, data)
    except Exception as e:
        return jsonify(error=str(e), movies=dbManager.getIdFromLikedMovies(g.user_name, None)), 500
    else:
        return jsonify(movies=dbManager.getIdFromLikedMovies(g.user_name, None)), 200
    

@app.route('/api/likedMovies/<string:opinion>', methods=["GET"])
@cross_origin()
@loginRequired
def likedMovies(opinion):
    if opinion == "liked": isLiked = True
    elif opinion == "disliked" : isLiked = False
    elif opinion == "all" : isLiked = None 
    else : return jsonify(error="Argument \"%s\" not authorized" %(opinion)), 400
    
    return jsonify(movies=dbManager.getIdFromLikedMovies(g.user_name, isLiked)), 200


@app.route('/api/likedMovie/<int:idMovie>/<int:isLiked>', methods=["POST", "PUT"])
@cross_origin()
@loginRequired
def likedMovie(idMovie, isLiked):
    if request.method == "POST":
        dbManager.insertUserMovie(g.user_name, idMovie, bool(isLiked))
        return "", 201
        
    elif request.method == "PUT":
        dbManager.updateLikedMovieForUser(g.user_name, idMovie, bool(isLiked))
        return "", 204


    
@app.route('/api/popularity', methods=['POST'])
@cross_origin()
@loginRequired
def checkPopularity():   
   
    data = json.loads(request.data)
    popularity = pred.classificationMovies(data['movies']) 
    return jsonify(popularity)

    
@app.route('/api/likedMovie/<int:idMovie>', methods=["DELETE"])
@cross_origin()
@loginRequired
def removeLikedMovie(idMovie):
    dbManager.removeUserMovieFromUser(g.user_name, idMovie)
    return jsonify({"id":idMovie}), 200


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

    return jsonify(name=user.name, email=user.email,
                   token=createToken(user)), 200


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
               
               
        return jsonify(name=user.name, email=user.email,
                       movies={umovie.idMovie:int(umovie.liked) for umovie in user.movies},
                       token=createToken(user)), 200
    else:
        return jsonify(error="Wrong name or password"), 400


@app.route('/auth/logout')
@cross_origin()
@loginRequired
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'}), 200    


@app.route('/api/user',methods=['GET'])
@cross_origin()
@loginRequired
def get_user_info():
    user = dbManager.getUser(g.user_name)
    dico = {"name": g.user_name, "email": user.email}
    return jsonify(dico), 200
    
    
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
