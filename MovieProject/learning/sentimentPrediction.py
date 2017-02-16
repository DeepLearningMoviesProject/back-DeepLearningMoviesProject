#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Allows to predict opinion about a tweet thank's to a pre-trained model.

Created on Wed Feb 15 17:09:59 2017
@author: coralie
"""

from MovieProject.resources import SENTIMENT_TWITTER_MODEL, SENTIMENT_ANALYSIS_MODEL
from MovieProject.tests import twitterSearch as ts
from MovieProject.preprocessing.tools import D2VOnCorpus as d2v
from MovieProject.preprocessing import tweets as tw
from keras.models import load_model

batch = 500

modelD2VPath = SENTIMENT_TWITTER_MODEL
modelPath = SENTIMENT_ANALYSIS_MODEL
#modelPath = '../resources/sentimentAnalysisModelIMDB.h5'


def predict(tweet, modelD2V, model):
    '''
    Predicts the sentiment class of the tweet according to the model
        parameters : 
            - tweet : string of the unpreprocess tweet
            - model : the model used by the prediction
        returns : 
            - a boolean to tell if the movie is liked or not
    '''
    
    #arrayMovie = np.array([movie])
    
    # Tweet preprocessing
    tweet = tw.preprocessTweet(tweet)
    
    # Infer tweet vector
    tweet = tw.tweetToVect(tweet, modelD2V)

    # Reshape
    tweet = tweet.reshape(1, tweet.shape[0])
    tweet = tweet.astype('float32')    
    # Reshape if the model is LSTM or Convolutional    
    tweet = tweet.reshape(tweet.shape[0], 1, tweet.shape[1])
    
    print tweet .shape
    
    #
    print model.predict_classes(tweet, batch_size=batch, verbose=0)
    pred = model.predict_proba(tweet, batch_size=batch, verbose=0)
    
    return pred
    
    
if __name__ == "__main__": 
    
    modelD2V = d2v.loadD2VModel(modelD2VPath)
    model = load_model(modelPath)
    
    tweets = ts.testTwitterSearch(['Inception','movie'],'en')
    #testTweepy(['python', 'javascript', 'ruby'])
    print len(tweets)
    tweet = tweets[70]
    print tw.preprocessTweet(tweet)
    print predict('I like this movie !',modelD2V, model)