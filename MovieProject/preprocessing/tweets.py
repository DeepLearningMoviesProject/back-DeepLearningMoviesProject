#!/usr/bin/env python2 
# -*- coding: utf-8 -*- 
""" 
Allows to preprocess tweets 
 
Created on Tue Feb  7 14:18:47 2017 
@author: coralie 
""" 
from __future__ import unicode_literals 

from MovieProject.preprocessing.texts import withoutAccents 
from MovieProject.preprocessing import words as w

#import regex 
import re 
 
 
list_punctuation = [",",".","!","?","[","]","(",")","{","}","-",'"',"'",":","$","\\","/",";","+","=","&","<",">","@","*","_"] 
                     
 
def preprocessTweet(tweet, dico, encod='utf-8'): 
    """ 
    Preprocess the tweets
        Parameters :  
            - tweet : a single tweet 
            - dico : dictionnary of opinion words
        Return : 
            - the tweet preprocessed 
    """ 
    
    if not isinstance(tweet, unicode):
        tweet = unicode(tweet, encod,'replace')
        
    # Convert to lower case 
    tweet = tweet.lower()
    # Remove accentued caracters
    tweet = withoutAccents(tweet) 
    # Remove all useless words (hashtag, user, url)
    tweet = _convertUselessWords(tweet)
    # Remove all punctuation of list_punctuation 
    tweet = "".join(c for c in tweet if c not in list_punctuation)
    # Remove caractere repetition (more than 3 repetition only)
    tweet = _removeRepetitions(tweet)
    # Check if words are present in the dictionnary
    listWords=[]
    words = tweet.split()
    for word in words :
        if word in dico.keys() :
            listWords.append(word)
    
    return ' '.join(listWords)
 
     
def _removeRepetitions(s, encod='utf-8'): 
    """ 
    Look for 3 or more repetitions of character and replace with the character itself.
    Remove also additional white spaces and replace by only one white space.
        Parameters : 
            - s : string   
        Return :  
            - the string without any 3 or more caracters repetitions and without additional white spaces
    """ 
    if not isinstance(s, unicode):
        s = unicode(s, encod,'replace')
        
    # Remove additional caracters 
    s = re.sub(r'(\w)\1{2,100}', r'\1', s) 
    # Remove additional white spaces 
    s = re.sub( '\s+', ' ', s ).strip() 
    
    return s 
     
     
def _convertUselessWords(s, encod='utf-8'): 
    """ 
    Remove useless expressions on tweets like urls and @username.
    Convert #word to word
        Parameters : 
            - s : string 
        Return :  
            - the string without any useless words 
    """ 
    if not isinstance(s, unicode):
        s = unicode(s, encod,'replace')
    
    #Remove www.* or https?://* 
    s = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',s) 
    #Remove @username
    s = re.sub('@[^\s]+','',s) 
    #Replace #word with word 
    s = re.sub(r'#([^\s]+)', r'\1', s) 
    
    return s 

    
def removeMovie(tweet, title, encod='utf-8'): 
    """
    Remove movie title in the tweet, so as not to distort the results
        Parameters :
            - tweet : string of the tweet
            - title : title of the movie
    """
    if not isinstance(tweet, unicode):
        tweet = unicode(tweet, encod,'replace')
    if not isinstance(title, unicode):
        title = unicode(title, encod,'replace')
    # Convert to lower case 
    tweet = withoutAccents(tweet.lower())
    title = withoutAccents(title.lower())
    # Remove movie title
    tweet = re.sub(title,'',tweet) 
    
    return tweet
    
    
def tweetToVect(tweet, dicoGlove): 
    """ 
    Get descriptors of text thank's to glove model
        Parameters: 
            - tweet : string of the preprocessed tweet
            - dicoGlove : 
        Return: 
            - ndarray. vector of the text passed in parameters 
    """ 
    #return model.infer_vector(tweet)     
    
    gArray, wSize = w.wordsToGlove(tweet.split(), dicoGlove)             
    meanMatrixOverview = w.meanWords(gArray, wSize)
    
    return meanMatrixOverview       
 
     
    
    

    
    
    
    