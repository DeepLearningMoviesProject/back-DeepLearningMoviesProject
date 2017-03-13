# -*- coding: utf-8 -*-
""" 
Module to handle GloVe representation of words.

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
            (ndarray, int). Tuple of GloVe descriptors of each word and size of descriptors
    """
    
    SIZE_VECTOR = gloveDic[gloveDic.keys()[0]].shape[0]
    
    gloveWords = []
    for w in words:
        wg = gloveDic.get(w.lower()) # return None if key is not present
        if wg is not None:
            gloveWords.append(wg)
    
    if len(gloveWords) == 0:
        return np.zeros((1, SIZE_VECTOR)), SIZE_VECTOR

    return np.asarray(gloveWords), SIZE_VECTOR


def meanWords(gWords, size):
    """
        Calculates the mean vector for the glove words gWords
        
        Parameters:
            gWords -> ndarray of GloVe descriptors
            size -> size of word descriptors
            
        return:
            ndarray of dimensions (nb descriptors, 1)
    """
    if gWords.shape[0] == 0:
        return np.zeros(size)
    if gWords.shape[0] == 1:
        return gWords[0]
    else:
        return sum(gWords) / gWords.shape[0]


if __name__ == '__main__':
    from MovieProject.preprocessing.tools import gloveDict
    gloveDic = gloveDict.loadGloveDicFromFile()
    resultArray,size = wordsToGlove(["dad","sgergergrezgerzgre","cat"], gloveDic)
    print resultArray
    
    