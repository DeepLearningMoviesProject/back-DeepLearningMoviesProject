#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Allows to predict opinion about a tweet thank's to a pre-trained model.

Created on Wed Feb 15 17:09:59 2017
@author: coralie
"""

from MovieProject.resources import GLOVE_DICT_FILE
from MovieProject.resources import SENTIMENT_ANALYSIS_MODEL

from MovieProject.preprocessing.tools import opinionDict as od
from MovieProject.preprocessing.tools import gloveDict
from MovieProject.preprocessing.tools import apiTMDB as tmdb
from MovieProject.preprocessing.tools import SearchTweets as ts
from MovieProject.preprocessing import tweets as tw
from keras.models import load_model


modelPath = SENTIMENT_ANALYSIS_MODEL

batch = 500

dicoGlove = gloveDict.loadGloveDicFromFile(GLOVE_DICT_FILE)
    
def predict(tweet, model, dico): 
    '''
    Predicts the sentiment class of the tweet according to the model
        parameters : 
            - tweet : string of the unpreprocess tweet
            - model : the model used by the prediction
            - dico : dictionnary of opinion words
        returns : 
            - a boolean to tell if the movie is liked or not (1: like, -1: dislike, 0: neutre)
    '''    
    
    # Tweet preprocessing thank's to glove dictionnary
    tweet = tw.preprocessTweet(tweet,dico)
    
    # Predict classe and return it when probability is hight
    if tweet :
        
        # Infer tweet vector
        tweet = tw.tweetToVect(tweet, dicoGlove)
        # Reshape
        tweet = tweet.reshape(1, tweet.shape[0])
        tweet = tweet.astype('float32')    
        # Reshape if the model is LSTM or Convolutional    
        tweet = tweet.reshape(tweet.shape[0], 1, tweet.shape[1])
        # Predict the tweet classe
        result = model.predict_proba(tweet, batch_size=batch, verbose=0)
        # Return classe only for hight probabilities
        if result <=0.10 :
            #print "Predicted classe -1 with probability %f " %(result)
            return -1
        if result >=0.90 :
            #print "Predicted classe 1 with probability %f " %(result)
            return 1
    # Return neutral classe in others cases  
    #print "Predicted classe 0 "
    return 0 
    

    
def classificationMovies(idMovies):
    """
    Ranks movies based on their popularity on twitter and reviews on twitter.
        Parameters:
            - titles : list of the movies titles
        Return: a tuple of ordonned dictionnary
            - first value : dictionnary ordered by popularity {movie title : popularity value}
            - second value : dictionnary ordered by reviews {movie title : reviews value}
    """
    model = load_model(modelPath)
    dico = od.extractOpinionWords()
    popularity = {}
    sentiments = {} 
    maxPopularity = 0
    
    movies = tmdb.getMovies(idMovies)
    
    for m,movie in enumerate(movies) :
        title = movie.info()['title']
        #title = _preprocessTitle(title)
        print "> Processing for movie title : %s" %(title)
        tweets = ts.SearchOnTwitter([title, 'movie'],'en')
        popularity[idMovies[m]] = float(len(tweets))
        sentiments[idMovies[m]] = 0.0

        maxPopularity = popularity[idMovies[m]] if popularity[idMovies[m]] > maxPopularity else maxPopularity

        for i,tweet in enumerate(tweets) :
            #print "%d / %d" %(i,len(tweets))
            #print "> Original tweet : %s" %(tweet)
            tweet = tw.removeMovie(tweet, title)
            p = predict(tweet, model, dico)
            sentiments[idMovies[m]] = sentiments[idMovies[m]] - 1 if p==-1 else sentiments[idMovies[m]] + p

        sentiments[idMovies[m]] = sentiments[idMovies[m]] / len(tweets) if len(tweets)>0 else 0
    
    if maxPopularity > 0 :
        for key,val in popularity.items():
            popularity[key] = val / maxPopularity
    
    popularity = sorted(popularity.items(), key=lambda t: t[1], reverse=True)
    sentiments = sorted(sentiments.items(), key=lambda t: t[1], reverse=True)

    return (popularity, sentiments) 
    
    
    
def _preprocessTitle(title):
    """
    Preprocess of title, in order to improve the tweet research
        Parameters:
            - title : string of the movie title
        Return:
            - string of the movie title preprocessed
    """
    title = title.split(":")
    last = title.pop()
    return last    
    
    
    