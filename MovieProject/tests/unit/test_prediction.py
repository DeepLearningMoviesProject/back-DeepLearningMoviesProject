#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Test for MovieProject/learning/classifier

Created on Fri Feb 17 13:26:55 2017
@author: elsa
"""

import unittest
from MovieProject.preprocessing import Preprocessor
from MovieProject.learning import buildModel, predict, suggestNMovies
import numpy as np

#movies = {"11":1,"18":1,"22":1}
#ids = [int(key) for key in movies]
#labels = np.array([movies[key] for key in movies])
#params = { "titles":False,
#           "rating":True,
#           "overviews":True,
#           "keywords":True,
#           "genres":True,
#           "actors":False,
#           "directors":True,
#          "compagnies" : False,
#          "language" : True,
#          "belongs" : True,
#          "runtime" : False,
#          "date" : True }


class PredictionTest(unittest.TestCase):
    """Test case used to test the module 'learning.prediction'."""

    def test_predict(self):
        """Tests 'prediction.predict'."""
        movies = {"11":1,"18":1,"22":1}
        ids = [int(key) for key in movies]
        labels = np.array([movies[key] for key in movies])    
        params = { "titles":True,
                   "rating":True,
                   "overviews":True,
                   "keywords":True,
                   "genres":True,
                   "actors":True,
                   "directors":True,
                  "compagnies" : True,
                  "language" : True,
                  "belongs" : True,
                  "runtime" : True,
                  "date" : True }
        pProcessor = Preprocessor(**params)
        data = pProcessor.preprocess(ids)
        
        model = buildModel(data, labels)
        
        print "start predict"
        toPredict = []
        #Non existant id
        #No id
        #Movie with specials characters, empty strings
#        predictions = suggestNMovies(toPredict, model, **params)
        
#        self.assertEqual(predictions, toPredict)
#        self.assertEqual(toPredict, [])

    def test_suggestNMovies(self):
    	"""Tests 'prediction.pickNMovies'."""
     
