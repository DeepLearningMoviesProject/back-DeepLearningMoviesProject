#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 14:27:16 2017

@author: coralie
"""

#gensim
from gensim.models import Doc2Vec

modelPath = '../resources/abstracts20EpochSize100.d2v'

# Infer vector of unknow abstracts thanks to Doc2Vec Model    
def inferVector(abstract, modelPath) :
    model_loaded = Doc2Vec.load(modelPath)
    return model_loaded.infer_vector(abstract)
    
    
if __name__ == "__main__":  
        
    # 1) Load model pre-trained
    model_loaded = Doc2Vec.load(modelPath)
    
    
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

    # 2) Infer vector from abstract
    #print inferVector('the girl is little and pretty', modelPath)