#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 11:25:31 2017

@author: coralie
"""
from MovieProject.learning import sentimentPrediction as pred
from MovieProject.preprocessing.tools import opinionDict as od
from MovieProject.resources import SENTIMENT_ANALYSIS_MODEL
from MovieProject.tests import twitterSearch as ts
from MovieProject.preprocessing import tweets as tw
from keras.models import load_model


modelPath = SENTIMENT_ANALYSIS_MODEL

    
if __name__ == "__main__": 
    
    model = load_model(modelPath)
    dico = od.extractOpinionWords()
    
    title = 'Inception'
    
    tweets = ts.testTwitterSearch([title,'movie'],'en')
    #testTweepy(['python', 'javascript', 'ruby'])
    print len(tweets)
    tweet = tweets[4] 
    #tweet = 'The movie Inception for example...there are only a handful of people on this planet that can make something better than that' 
    #tweet = 'INCEPTION is the best movie of all time'
    #tweet = 'Inception was a good movie'
    #tweet = 'Or maybe Inception or The Revenant'
    #tweet = 'Many people are familiar to The Dark Knight and Inception, but not with Seven. It's an old thriller-mystery-suspense movie'
    print "> Original tweet : " + tweet
    tweet = tw.removeMovie(tweet, title)
    print "> Original tweet (removed title) : " + tweet
    print "> Preprocessed tweet : " + tw.preprocessTweet(tweet,dico)
    print pred.predict(tweet, model, dico)