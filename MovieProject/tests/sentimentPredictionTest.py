#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 11:25:31 2017

@author: coralie
"""
from MovieProject.learning import sentimentPrediction as pred

    
    
if __name__ == "__main__": 
    
    #titles = ["harry potter and the deathly hallows"," Star Wars : The Clone Wars", "Black Swan", "Les temps modernes", "Fight club"]
    ids = [12444,140607,44214,3082,550]
    popularity, sentiments = pred.classificationMovies(ids)
    
    print popularity
    print sentiments
    