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


def test1():
    
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
    
    
    
def predictionAPI(titles):

    model = load_model(modelPath)
    dico = od.extractOpinionWords()
    popularity = {}
    sentiments = {} 
    
    for title in titles :
        title = preprocessTitle(title)
        print "> Movie title : %s" %(title)
        tweets = ts.testTwitterSearch([title, 'movie'],'en')
        popularity[title] = len(tweets)
        sentiments[title] = 0.0

        for i,tweet in enumerate(tweets) :
            print "%d / %d" %(i,len(tweets))
            print "> Original tweet : %s" %(tweet)
            tweet = tw.removeMovie(tweet, title)
            p = pred.predict(tweet, model, dico)
            sentiments[title] = sentiments[title] - 1 if p==-1 else sentiments[title] + p

        sentiments[title] = sentiments[title] / len(tweets) if len(tweets)>0 else 0

    popularity = sorted(popularity.items(), key=lambda t: t[1], reverse=True)
    sentiments = sorted(sentiments.items(), key=lambda t: t[1], reverse=True)
    
    return (popularity, sentiments)

    
    
def preprocessTitle(title):
    
    title = title.split(":")
    last = title.pop()
    return last
    
    
    
if __name__ == "__main__": 
    
    titles = ["harry potter and the deathly hallows"," Star Wars : The Clone Wars", "Black Swan", "Les temps modernes", "Fight club"]
    popularity, sentiments = predictionAPI(titles)
    
    print popularity
    print sentiments
    