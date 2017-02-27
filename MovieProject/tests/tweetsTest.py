#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 15:47:10 2017

@author: coralie
"""

from MovieProject.preprocessing import tweets as tw
from MovieProject.preprocessing.tools import gloveDict
from MovieProject.resources import GLOVE_DICT_FILE


     
if __name__ == "__main__":    
     
    #dico = od.extractOpinionWords()
    
    #print removeRepetitions("girlllll have fun!! it will be amazing!! i miss theeem!! loop ")    
    #print convertUselessWords("@Nemrodx3 Ce site est vraiment trop top ! www.deepLearning.com #DeepLearning #ProjetDeFou") 
    #print preprocessTweet("@Nemrodx3 Great ! Wonderfuuuul ! Ce siiiiiiite est vraiment trop tooooooop !!!   !!!!!  www.deepLearning.com #DeepLearning #ProjetDeFou #Good",dico) 
    #print "".join(c for c in "!/\:?,!;.+=&<>)](['" if c not in list_punctuation) 
    #print "".join(c for c in '"' if c not in list_punctuation) 
     
    dicoGlove = gloveDict.loadGloveDicFromFile(GLOVE_DICT_FILE)

    print tw.tweetToVect("Hello beautiful man", dicoGlove)
    
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