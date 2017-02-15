#!/usr/bin/env python2 
# -*- coding: utf-8 -*- 
""" 
Allows to preprocess tweets 
 
Created on Tue Feb  7 14:18:47 2017 
@author: coralie 
""" 
from __future__ import unicode_literals 

from MovieProject.preprocessing.texts import withoutAccents 
# Library to write utf-8 text file 
import codecs 
#import regex 
import re 
 
 
list_punctuation = [",",".","!","?","[","]","(",")","{","}","-",'"',"'",":","$","\\","/",";","+","=","$","&","<",">","@"] 
 
 
def preprocessTweet(tweet): 
    """ 
    Preprocess the tweets
        Parameters :  
            - tweet : a single tweet 
        Return : 
            - the tweet preprocessed 
    """ 
    #Convert to lower case 
    tweet = tweet.lower() 
    #Remove all punctuation of list_punctuation 
    tweet = "".join(c for c in tweet if c not in list_punctuation) 
    tweet = withoutAccents(tweet) 
    tweet = convertUselessWords(tweet)   
    tweet = removeRepetitions(tweet) 
    return tweet 
 
     
def removeRepetitions(s): 
    """ 
    Look for repetitions of character and replace with the character itself 
    Remove also additional white spaces 
        Parameters : 
            - s : string   
        Return :  
            - the string without any repetitions of caracters 
    """ 
    # Remove additional caracters 
    s = re.sub(r'(\w)\1+', r'\1', s) 
    # Remove additional white spaces 
    s = re.sub( '\s+', ' ', s ).strip() 
    return s 
     
     
def convertUselessWords(s): 
    """ 
    Convert useless expressions on tweets like urls to URL and "#word" to "word" 
    Remove all @username 
        Parameters : 
            - s : string 
        Return :  
            - the string without any useless words 
    """ 
    #Convert www.* or https?://* 
    s = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',s) 
    #Convert @username to AT_USER 
    s = re.sub('@[^\s]+','',s) 
    #Replace #word with word 
    s = re.sub(r'#([^\s]+)', r'\1', s) 
    return s 
     
     
def tweetToVect(tweet, model): 
    """ 
    Get descriptors of text thanks to the given model 
        Parameters: 
            - text -> String 
            - model -> the Doc2Vec model 
        Return: 
            - ndarray. Descriptors of the text passed in parameters 
    """ 
 
    return model.infer_vector(preprocessTweet(tweet))     
 
 
     
if __name__ == "__main__":    
     
    #print removeRepetitions("girlllll have fun!! it will be amazing!! i miss theeem!! ")    
    #print convertUselessWords("@Nemrodx3 Ce site est vraiment trop top ! www.deepLearning.com #DeepLearning #ProjetDeFou") 
    #print preprocessTweet("@Nemrodx3 Ce siiiiiiite est vraiment trop tooooooop !!!   !!!!!  www.deepLearning.com #DeepLearning #ProjetDeFou") 
    #print "".join(c for c in "!/\:?,!;.+=&<>)](['" if c not in list_punctuation) 
    #print "".join(c for c in '"' if c not in list_punctuation) 
     
    source = ['../resources/test_twitter_neg.txt','../resources/test_twitter_pos.txt','../resources/train_twitter_neg.txt','../resources/train_twitter_pos.txt'] 
    processed = ['../resources/test_twitter_neg_processed.txt','../resources/test_twitter_pos_processed.txt','../resources/train_twitter_neg_processed.txt','../resources/train_twitter_pos_processed.txt'] 
    nb=0 
    for s in source : 
        #Read the tweets one by one and process it 
        fSource = codecs.open(s, 'r', 'utf-8') 
        fProcessed = codecs.open(processed[nb], "w", 'utf-8') 
        line = fSource.readline() 
        nb+=1 
        print '%d/%d ...' % (nb,len(source)) 
         
        while line: 
            processedTweet = preprocessTweet(line) 
            #print processedTweet 
            fProcessed.write(processedTweet+'\n') 
            line = fSource.readline() 
     
        fSource.close() 
        fProcessed.close() 