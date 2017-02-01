#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Pre-processing of texts

Created on Wed Feb  1 13:32:46 2017
@author: coralie
"""

list_punctuation = [",",".","!","?","[","]","(",")","{","}"]

"""
Remove specific accents on string
"""
def withoutAccents(ch, encod='utf-8'):
    alpha1 = u"àâäåçéèêëîïôöùûüÿğ"
    alpha2 = u"aaaaceeeeiioouuuyg"
    conv = False
    if not isinstance(ch, unicode):
        ch = unicode(ch, encod,'replace')
        conv = True
    tableconv = {ord(a):b for a, b in zip(alpha1, alpha2)}
    x = ch.translate(tableconv)
    if conv:
        x = x.encode(encod)
    return x
  
"""
Pre-processing of abstracts
"""    
def preProcessingAbstracts(abstract):
    #Convert to lower case
    abstract = abstract.lower()
    # Remove specific accents
    abstract = withoutAccents(abstract)
    #Remove all punctuation
    abstract = "".join(c for c in abstract if c not in list_punctuation)
    return abstract
