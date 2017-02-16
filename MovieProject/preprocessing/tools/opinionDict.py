#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 14:50:35 2017

@author: coralie
"""
# Library to write utf-8 text file
import codecs

from MovieProject.resources import OPINION_FILE, OPINION_DICT_FILE
from os.path import isfile
import re
import numpy as np


list_punctuation = ["-","'"] 

def extractOpinionWords():
    """ 
    Creates the opinions dictionnary from the opinion file as a map, where the words are the key
        return:
            - dictionary Object, which key->word and value->word
    """
    opinionDict = {}

    with codecs.open(OPINION_FILE,'r','utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            for c in word :
                if c in list_punctuation :
                    ww = "".join(cc for cc in word if cc not in list_punctuation)
                    opinionDict[ww] = ww
                    if c in list_punctuation[0]:
                        for w in re.sub("[^\w]", " ",  word).split() :
                            opinionDict[w] = w
            opinionDict[word] = word
    
    return opinionDict


def saveGloveDicIntoFile(opinionDic):
    """
    Save the opinion dictionary memory Object into binary file    
        Parameters:
            - opinionDic -> <Dict Object> representing the opinion dictionary
    """
    
    np.save(OPINION_DICT_FILE, np.asarray([opinionDic]))
    
    
def loadGloveDicFromFile(filename):
    """
    Create an memory Object of opinion dictionary from binary file
        Parameters:
            - filename : the name of the binary file
    """
        
    #if the resource file is not present, creates the file containing all vectors
    #and return vectors
    if not isfile(OPINION_DICT_FILE):
        dic = _extractOpinionWords()
        saveGloveDicIntoFile(dic)
        return dic
    
    return np.load(filename)[0]


if __name__ == "__main__":
    
    # if the script is run, create dictionary of vectors and save it into file
    #print "Creating and saving the GloVe dictionary"
    saveGloveDicIntoFile(extractOpinionWords())