# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 22:19:45 2017

@author: darke
"""

import numpy as np
#import nltk
from nltk.corpus import stopwords

from apiTMDB import *

#nltk.download()

cachedStopWords = stopwords.words("english")

GLOVE_FILE = 'GLOVE/glove.6B.50d.txt'
DICO_FILE = "GLOVE/glove_dico.npy"


def extractGloveVects(filename):
    """ 
        Creates the glove dictionnary from the glove file as a map, where the words are the key
        Forgets the stopwords
        
        Parameters:
            filename -> The name of GloVefile
        
        return:
            Dictionary Object, which key->word and value->descriptors
            
    """
    
    embeddings_index = {}

    with open(GLOVE_FILE) as f:
        for line in f:
            values = line.split()
            word = values[0]
            if word not in cachedStopWords:
                coefs = np.asarray(values[1:], dtype='float32')
                embeddings_index[word] = coefs

    return embeddings_index


def wordsToGlove(words, gloveDic):
    """
        Turn the words in the array words into their glove descriptors
        Returns the descriptors matching with the array of words. 
        Forgets words that are not in the dico (including stopwords)
        Words must be in an array, and be all strings, with one word by string
        
        Parameters:
            words -> ndarray of String
            gloveDic -> GloVe dictionary (Dict Object)
            
        return:
            ndarray of GloVe descriptors of each word
    """
    gloveWords = []
    for w in words:
        wg = gloveDic.get(w.lower()) # return None if key is not present
        if wg is not None:
            gloveWords.append(wg)
            
    return np.asarray(gloveWords)


def meanWords(gWords):
    """
        Calculates the mean vector for the glove words gWords
        
        Parameters:
            gWords -> ndarray of GloVe descriptors
            
        return:
            ndarray of dimensions (nb descriptors, 1)
    """
    
    return sum(gWords) / gWords.shape[0]



def saveGloveDicIntoFile(filename, gloveDic):
    """
        Save the GloVe dictionary memory Object into binary file    
    
        Parameters:
            filename -> Name of the new file containing the GloVe dictionary
            gloveDic -> <Dict Object> representing the GloVe dictionary
    """
    
    np.save(filename, np.asarray([gloveDic]))
    
    
def loadGloveDicFromFile(filename):
    """
        Create an memory Object of GloVe dictionary from binary file
        
        Parameters:
            filename -> Name of the binary file
    """
    
    return np.load(filename)[0]