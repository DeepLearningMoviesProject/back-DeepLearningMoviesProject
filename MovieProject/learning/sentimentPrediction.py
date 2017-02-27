#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Allows to predict opinion about a tweet thank's to a pre-trained model.

Created on Wed Feb 15 17:09:59 2017
@author: coralie
"""

from MovieProject.resources import GLOVE_DICT_FILE
from MovieProject.resources import SENTIMENT_ANALYSIS_MODEL

from MovieProject.preprocessing.tools import gloveDict
from MovieProject.preprocessing.tools import opinionDict as od
from MovieProject.tests import twitterSearch as ts
from MovieProject.preprocessing import tweets as tw
from keras.models import load_model


modelPath = SENTIMENT_ANALYSIS_MODEL

batch = 500


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
    dicoGlove = gloveDict.loadGloveDicFromFile(GLOVE_DICT_FILE)
    tweet = tw.preprocessTweet(tweet,dico)
    #print tweet
    
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
        pred = model.predict_classes(tweet, batch_size=batch, verbose=0)
        pred = -1 if pred == 0 else 1
        result = model.predict_proba(tweet, batch_size=batch, verbose=0)
        print "Predicted classe %d with probability %f " %(pred,result)
        # Return classe only for hight probabilities
        if result <=0.10 or result >= 0.90 :
            return pred

    # Return neutral classe in others cases    
    return 0 
    

    
def classificationMovies(titles):
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
    
    for title in titles :
        title = _preprocessTitle(title)
        print "> Movie title : %s" %(title)
        tweets = ts.testTwitterSearch([title, 'movie'],'en')
        popularity[title] = len(tweets)
        sentiments[title] = 0.0

        for i,tweet in enumerate(tweets) :
            print "%d / %d" %(i,len(tweets))
            print "> Original tweet : %s" %(tweet)
            tweet = tw.removeMovie(tweet, title)
            p = predict(tweet, model, dico)
            sentiments[title] = sentiments[title] - 1 if p==-1 else sentiments[title] + p

        sentiments[title] = sentiments[title] / len(tweets) if len(tweets)>0 else 0

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
    
    
    