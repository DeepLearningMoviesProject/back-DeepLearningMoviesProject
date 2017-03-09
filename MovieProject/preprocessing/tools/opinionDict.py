#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Allows to create a dictionary of opinion words to preprocess tweets (filter words of interest).

Created on Thu Feb 16 14:50:35 2017
@author: coralie
"""

from __future__ import unicode_literals 
# Library to write utf-8 text file
import codecs

from MovieProject.resources import OPINION_FILE, OPINION_DICT_FILE
from os.path import isfile
import re
import numpy as np


list_punctuation = ["-","'"] 


def extractOpinionWords():
    """ 
    Creates the opinion dictionary from the opinion file as a map, where the words are the keys
        return:
            - dictionary Object, which key->word and value->word
    """
    opinionDict = {}

    with codecs.open(OPINION_FILE,'r','utf-8') as f:
        
        #Read the files line by line (word by word) and store each word in the dictionary
        for line in f:
            values = line.split()
            word = values[0]

            #For each composed word, store them as a composed word, a concatened word and as two differents word
            for c in word :
                if c in list_punctuation :
                    ww = "".join(cc for cc in word if cc not in list_punctuation)
                    opinionDict[ww] = ww
                    if c in list_punctuation[0]:
                        for w in re.sub("[^\w]", " ",  word).split() :
                            opinionDict[w] = w
            opinionDict[word] = word
    
    return opinionDict


def saveDicIntoFile(opinionDic):
    """
    Save the opinion dictionary memory Object into binary file    
        Parameters:
            - opinionDic -> <Dict Object> representing the opinion dictionary
    """
    
    np.save(OPINION_DICT_FILE, np.asarray([opinionDic]))
    
    
def loadDicFromFile():
    """
    Create an memory Object of opinion dictionary from binary file
        Parameters:
            - filename : the name of the binary file
    """
        
    #if the resource file is not present, creates the file containing all vectors and return vectors
    if not isfile(OPINION_DICT_FILE):
        dic = extractOpinionWords()
        saveDicIntoFile(dic)
        return dic
    
    return np.load(OPINION_DICT_FILE)[0]


if __name__ == "__main__":
    
    # if the script is run, create dictionary and save it into file
    print "Creating and saving the opinion dictionary"
    saveDicIntoFile(extractOpinionWords())