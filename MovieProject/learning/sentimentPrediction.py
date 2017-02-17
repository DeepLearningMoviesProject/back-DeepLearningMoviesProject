#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Allows to predict opinion about a tweet thank's to a pre-trained model.

Created on Wed Feb 15 17:09:59 2017
@author: coralie
"""
from MovieProject.resources import GLOVE_DICT_FILE
from MovieProject.preprocessing.tools import gloveDict

from MovieProject.preprocessing.tools import opinionDict as od
from MovieProject.resources import SENTIMENT_TWITTER_MODEL, SENTIMENT_ANALYSIS_MODEL
from MovieProject.tests import twitterSearch as ts
from MovieProject.preprocessing.tools import D2VOnCorpus as d2v
from MovieProject.preprocessing import tweets as tw
from keras.models import load_model

batch = 500

modelD2VPath = SENTIMENT_TWITTER_MODEL
modelPath = SENTIMENT_ANALYSIS_MODEL


def predict(tweet, modelD2V, model, dico):
    '''
    Predicts the sentiment class of the tweet according to the model
        parameters : 
            - tweet : string of the unpreprocess tweet
            - modelD2V :
            - model : the model used by the prediction
            - dico :
        returns : 
            - a boolean to tell if the movie is liked or not (1: like, 0: dislike, -1: neutre)
    '''    
    dicoGlove = gloveDict.loadGloveDicFromFile(GLOVE_DICT_FILE)
    
    # Tweet preprocessing
    tweet = tw.preprocessTweet(tweet,dico)
    
    #
    if tweet :
        
        # Infer tweet vector
        #tweet = tw.tweetToVect(tweet, modelD2V)
        tweet = tw.tweetToVect(tweet, dicoGlove)
        # Reshape
        tweet = tweet.reshape(1, tweet.shape[0])
        tweet = tweet.astype('float32')    
        # Reshape if the model is LSTM or Convolutional    
        tweet = tweet.reshape(tweet.shape[0], 1, tweet.shape[1])
        # Predict the tweet classe
        pred = model.predict_classes(tweet, batch_size=batch, verbose=0)
        print model.predict_proba(tweet, batch_size=batch, verbose=0)
        
        return pred
        
    #    
    else :
        return -1
    
    
if __name__ == "__main__": 
    
    modelD2V = d2v.loadD2VModel(modelD2VPath)
    model = load_model(modelPath)
    dico = od.extractOpinionWords()
    
    tweets = ts.testTwitterSearch(['Inception','movie'],'en')
    #testTweepy(['python', 'javascript', 'ruby'])
    print len(tweets)
    tweet = "it's bad"#tweets[1]
    print "original tweet : " + tweet
    print "preprocessed tweet : " + tw.preprocessTweet(tweet,dico)
    print predict(tweet,modelD2V, model, dico)