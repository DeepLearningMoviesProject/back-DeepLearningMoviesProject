#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Allows to preprocess texts

Created on Wed Feb  1 13:32:46 2017
@author: coralie
"""

list_punctuation = [",",".","!","?","[","]","(",")","{","}"]


def withoutAccents(ch, encod='utf-8'):
    """
        Remove specific accents on string
        
        Parameters : 
            ch : the string to change
            encod : the encod of this chain (utf-8 by default)
        
        returns : 
            the chain in the correct format, with all the accents removed
    """    
    alpha1 = u"àâäåçéèêëîïôöùûüÿğñ"
    alpha2 = u"aaaaceeeeiioouuuygn"
    conv = False
    if not isinstance(ch, unicode):
        ch = unicode(ch, encod,'replace')
        conv = True
    tableconv = {ord(a):b for a, b in zip(alpha1, alpha2)}
    x = ch.translate(tableconv)
    if conv:
        x = x.encode(encod)
    return x
  
    
def preProcessingAbstracts(abstract):
    """
        Pre-processing of abstracts
        
        Parameters : The abstract with no modifications

        returns : 
            the abstract ready to be preprocessed, with the punctuation removed (except for ' and -), in lower case and without accents
    """    
    #Convert to lower case
    abstract = abstract.lower()
    # Remove specific accents
    abstract = withoutAccents(abstract)
    #Remove all punctuation of list_punctuation
    abstract = "".join(c for c in abstract if c not in list_punctuation)
    return abstract


    
def textToVect(text, model):
    """
        Get descriptors of text thanks to the given model
        
        Parameters:
            text -> String
            model -> the Doc2Vec model
            
        return:
            ndarray. Descriptors of the text passed in parameters
    """

    return model.infer_vector(preProcessingAbstracts(text))