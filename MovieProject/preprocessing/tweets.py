#!/usr/bin/env python2 
# -*- coding: utf-8 -*- 
""" 
Allows to preprocess tweets 
 
Created on Tue Feb  7 14:18:47 2017 
@author: coralie 
""" 
from __future__ import unicode_literals 

from MovieProject.preprocessing.texts import withoutAccents 
from MovieProject.preprocessing.tools import opinionDict as od
#import regex 
import re 
 
 
list_punctuation = [",",".","!","?","[","]","(",")","{","}","-",'"',"'",":","$","\\","/",";","+","=","&","<",">","@","*","_"] 
 
 
def preprocessTweet(tweet, dico): 
    """ 
    Preprocess the tweets
        Parameters :  
            - tweet : a single tweet 
            - dico : dictionnary of opinion words
        Return : 
            - the tweet preprocessed 
    """ 
    # Convert to lower case 
    tweet = tweet.lower()
    # Remove accentued caracters
    tweet = withoutAccents(tweet) 
    # Remove all useless words (hashtag, user, url)
    tweet = convertUselessWords(tweet)
    # Remove all punctuation of list_punctuation 
    tweet = "".join(c for c in tweet if c not in list_punctuation)
    # Remove caractere repetition (more than 3 repetition only)
    tweet = removeRepetitions(tweet)
    # Check if words are present in the dictionnary
    listWords=[]
    words = tweet.split()
    for word in words :
        if word in dico.keys() :
            listWords.append(word)
    
    return ' '.join(listWords)
 
     
def removeRepetitions(s): 
    """ 
    Look for 3 or more repetitions of character and replace with the character itself.
    Remove also additional white spaces and replace by only one white space.
        Parameters : 
            - s : string   
        Return :  
            - the string without any 3 or more caracters repetitions and without additional white spaces
    """ 
    # Remove additional caracters 
    s = re.sub(r'(\w)\1{2,100}', r'\1', s) 
    # Remove additional white spaces 
    s = re.sub( '\s+', ' ', s ).strip() 
    return s 
     
     
def convertUselessWords(s): 
    """ 
    Remove useless expressions on tweets like urls and @username.
    Convert #word to word
        Parameters : 
            - s : string 
        Return :  
            - the string without any useless words 
    """ 
    #Remove www.* or https?://* 
    s = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',s) 
    #Remove @username
    s = re.sub('@[^\s]+','',s) 
    #Replace #word with word 
    s = re.sub(r'#([^\s]+)', r'\1', s) 
    return s 
     
     
def tweetToVect(tweet, model): 
    """ 
    Get descriptors of text thanks to the given model 
        Parameters: 
            - tweet -> string
            - model -> the Doc2Vec model 
        Return: 
            - ndarray. Descriptors of the text passed in parameters 
    """ 
 
    return model.infer_vector(preprocessTweet(tweet))     
 
 
     
if __name__ == "__main__":    
     
    dico = od.extractOpinionWords()
    
    #print removeRepetitions("girlllll have fun!! it will be amazing!! i miss theeem!! loop ")    
    #print convertUselessWords("@Nemrodx3 Ce site est vraiment trop top ! www.deepLearning.com #DeepLearning #ProjetDeFou") 
    print preprocessTweet("@Nemrodx3 Great ! Wonderfuuuul ! Ce siiiiiiite est vraiment trop tooooooop !!!   !!!!!  www.deepLearning.com #DeepLearning #ProjetDeFou #Good",dico) 
    #print "".join(c for c in "!/\:?,!;.+=&<>)](['" if c not in list_punctuation) 
    #print "".join(c for c in '"' if c not in list_punctuation) 
     
    """
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
    """