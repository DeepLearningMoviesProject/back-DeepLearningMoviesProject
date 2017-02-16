#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:43:57 2017

@author: coralie
"""
from __future__ import unicode_literals 

# Library to write utf-8 text file
import codecs

from MovieProject.resources import TRAIN_TWITTER_NEG_FILE, TRAIN_TWITTER_POS_FILE, TEST_TWITTER_NEG_FILE, TEST_TWITTER_POS_FILE 
from MovieProject.preprocessing.tools import opinionDict as od
from MovieProject.preprocessing import tweets as tw
import re


def _processTweetsFile():
    """ 
    """
    files = [TRAIN_TWITTER_NEG_FILE,TRAIN_TWITTER_POS_FILE,TEST_TWITTER_NEG_FILE,TEST_TWITTER_POS_FILE]
    dico = od.extractOpinionWords()

    i=0
    for filename in files :
        
        print '%d / %d' %(i, len(files))
        i+=1
        
        #Read the tweets one by one and process it 
        fSource = codecs.open(filename, 'r', 'utf-8') 
        fProcessed = codecs.open(re.sub( '.txt', '_tr.txt', filename ), "w", 'utf-8')
        
        j=0
        
        lines = fSource.readlines()
        for line in lines: 
            j+=1
            if j%500 == 0 :
                print '%d / %d' %(j, len(lines))
            processedTweet = tw.preprocessTweet(line,dico) 
            if processedTweet :
                #print processedTweet
                fProcessed.write(processedTweet+'\n')
     
        fSource.close() 
        fProcessed.close() 
        
    
if __name__ == "__main__":
    _processTweetsFile()
    