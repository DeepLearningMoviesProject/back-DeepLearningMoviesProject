#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Allows to preprocess tweet files in order to create a better corpus of tweets.

Created on Thu Feb 16 15:43:57 2017
@author: coralie
"""

from __future__ import unicode_literals 
# Library to write utf-8 text file
import codecs

from MovieProject.resources import TRAIN_TWITTER_NEG_FILE, TRAIN_TWITTER_POS_FILE, TEST_TWITTER_NEG_FILE, TEST_TWITTER_POS_FILE, TRAIN_TWITTER_NEG_TR_FILE, TRAIN_TWITTER_POS_TR_FILE, TEST_TWITTER_NEG_TR_FILE, TEST_TWITTER_POS_TR_FILE
from MovieProject.preprocessing.tools import opinionDict as od
from MovieProject.preprocessing import tweets as tw


def _processTweetsFile():
    """ 
    Preprocesses all tweets in tweet files and write them in the corresponding files only if the preprocessing results is a non-nul string)
    """
    filesSource = [TRAIN_TWITTER_NEG_FILE,TRAIN_TWITTER_POS_FILE,TEST_TWITTER_NEG_FILE,TEST_TWITTER_POS_FILE]
    filesProcessed = [TRAIN_TWITTER_NEG_TR_FILE,TRAIN_TWITTER_POS_TR_FILE,TEST_TWITTER_NEG_TR_FILE,TEST_TWITTER_POS_TR_FILE]
    dico = od.extractOpinionWords()
    i=0
    
    for filename in filesSource :
        #Read the files one by one and process them
        fSource = codecs.open(filename, 'r', 'utf-8') 
        fProcessed = codecs.open(filesProcessed[i], "w", 'utf-8')
        i+=1
        j=0
        lines = fSource.readlines()
        
        for line in lines:
            #Print advancement
            j+=1
            if j%1000 == 0 :
                print '%d / %d : %d / %d' %(i, len(filesSource), j, len(lines))
            #Read the tweets one by one and process it
            processedTweet = tw.preprocessTweet(line,dico) 
            if processedTweet :
                fProcessed.write(processedTweet+'\n')
     
        fSource.close() 
        fProcessed.close() 
        
    
if __name__ == "__main__":
    _processTweetsFile()
    