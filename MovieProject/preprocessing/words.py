# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 22:19:45 2017

@author: darke
"""

import numpy as np


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
