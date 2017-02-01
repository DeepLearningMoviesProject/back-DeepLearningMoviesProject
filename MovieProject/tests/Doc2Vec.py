#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Test trained Doc2Vec model

Created on Tue Jan 31 14:27:16 2017
@author: coralie
"""

#gensim
from gensim.models import Doc2Vec
# To pre-process abtract
from MovieProject.preprocessing import texts

modelPath = '../resources/abstracts20EpochSize100.d2v'

# Infer vector of unknow abstracts thanks to Doc2Vec Model    
def inferVector(abstract, modelPath) :
    model_loaded = Doc2Vec.load(modelPath)
    return model_loaded.infer_vector(abstract)
    
    
if __name__ == "__main__":  
        
    # Just some tests
    print model_loaded.most_similar("vampire")
    print "\n"
    print model_loaded.most_similar("zombie")
    print "\n"
    print model_loaded.most_similar("gang")
    print "\n"
    print model_loaded.most_similar("police")
    print "\n"
    print model_loaded.most_similar("girl")
    print "\n"
    print model_loaded.most_similar("peoples")
    #print model_loaded['girl']

    # How use the Doc2Vec model ?
    
    # 1) Load model pre-trained
    #model_loaded = Doc2Vec.load(modelPath)
    
    # 2) Pre-process texte
    #abstract = "The Vampire gïrl is little and pretty !!!! ..."
    #abstract = texts.preProcessingAbstracts(abstract)
    #print abstract
    
    # 3) Infer vector from abstract
    #vector = inferVector(abstract, modelPath)
    #print vector
    
