#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Test some ways to recover tweets from the api twitter

Created on Wed Feb 15 10:58:37 2017
@author: coralie
"""

# Import Twitter library for python
from TwitterSearch import TwitterSearchOrder, TwitterSearchException, TwitterSearch
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import pandas as pd

# User credentials to access Twitter API 
access_token = "1319988194-ZtgKLCSfbRNqBCgTplSmbnUv8T0G3PIPD4Iz5kR" #ACCESS TOKEN
access_token_secret = "AEVKTIetHGoejovVbzXB3vTGJiECc0gBSTqW6BBz1ArkU" #ACCESS TOKEN SECRET
consumer_key = "HR1S4juinegecRkr9Oc8LeBhr" #API KEY
consumer_secret = "YPIhNTZNYAOkYgMFaf4j5d9upu8PCWQZu87e0GA4eG2NHivW9u" #API SECRET


"""
TWEEPY LIBRARY
"""

# To store tweets loaded
tweets_data = []
tweets = pd.DataFrame()

class StdOutListener(StreamListener):
    """
    Basic listener that just store received tweets to tweets_data.
    """
    def on_status(self, data):
        tweets_data.append(data)
        print data
        return True

    def on_error(self, status):
        print status

def testTweepy(keywords):
    """
    Allows to test tweepy library thank's to StdOutListener class -> Print tweets of interest.
        Parameters:
            keywords : string array that tweets must contain
    """
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # Filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=keywords)
    
    
"""
TWITTER SEARCH LIBRARY
"""    

def testTwitterSearch(keywords, language):
    """
    Allows to test twitter search library -> Print tweets of interest.
        Parameters:
            keywords : string array that tweets must contain
            language : string indicating the language of the interest tweets
    """
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords(keywords) # let's define all words we would like to have a look for
        tso.set_language(language) # we want to see German tweets only
        tso.set_include_entities(False) # and don't give us all those entity information
    
        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key = consumer_key,
            consumer_secret = consumer_secret,
            access_token = access_token,
            access_token_secret = access_token_secret
         )
    
         # this is where the fun actually starts :)
        for tweet in ts.search_tweets_iterable(tso):
            print(tweet['text'])
            
    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)
    
    
        
if __name__ == "__main__":    
        
    testTwitterSearch(['Star wars','movie'],'en')
    #testTweepy(['python', 'javascript', 'ruby'])