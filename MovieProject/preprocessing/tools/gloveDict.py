#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:14:35 2017
@author: Julian
"""

from MovieProject.resources import GLOVE_CORPUS_FILE, GLOVE_DICT_FILE
from os.path import isfile, isdir

import numpy as np

from nltk.corpus import stopwords
from nltk.data import path


# Download stopwords if not present
if not isdir(path[0]):
    from nltk import download
    download("stopwords")

_cachedStopWords = stopwords.words("english")


def _extractGloveVects():
    """ 
        Creates the glove dictionnary from the glove file as a map, where the words are the key
        Forgets the stopwords
        
        return:
            Dictionary Object, which key->word and value->descriptors
            
    """
    
    embeddings_index = {}

    with open(GLOVE_CORPUS_FILE) as f:
        for line in f:
            values = line.split()
            word = values[0].lower()
            if word not in _cachedStopWords:
                coefs = np.asarray(values[1:], dtype='float32')
                embeddings_index[word] = coefs

    return embeddings_index


def saveGloveDicIntoFile(gloveDic):
    """
        Save the GloVe dictionary memory Object into binary file    
    
        Parameters:
            gloveDic -> <Dict Object> representing the GloVe dictionary
    """
    
    np.save(GLOVE_DICT_FILE, np.asarray([gloveDic]))
    
    
def loadGloveDicFromFile():
    """
        Create an memory Object of GloVe dictionary from binary file
        
        Parameters:
            filename -> Name of the binary file
    """
        
    #if the resource file is not present, creates the file containing all vectors
    #and return vectors
    if not isfile(GLOVE_DICT_FILE):
        vects = _extractGloveVects()
        saveGloveDicIntoFile(vects)
        return vects
    
    return np.load(GLOVE_DICT_FILE)[0]


if __name__ == "__main__":
    
    # if the script is run, create dictionary of vectors and save it into file
    print "Creating and saving the GloVe dictionary"
    saveGloveDicIntoFile(_extractGloveVects())