#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Test for MovieProject/learning/classifier

Created on Fri Feb 17 13:26:55 2017
@author: elsa
"""

from MovieProject.learning.prediction import *
import unittest

class PredictionTest(unittest.TestCase):

    """Test case used to test the module 'learning.prediction'."""

    def test_predict(self):
        """Tests 'prediction.predict'."""
            '''
            Predicts the class of the movie according to the model
                parameters : 
                    - movies : an array of the id of the movie we want to know the class of, the id must exist
                    - model : the model that matches the taste of the user
                returns : 
                    - a boolean to tell if the movie is liked or not
            '''
        predict(movies, model, **kwargs)

    def test_pickNMovies(self):
    	"""Tests 'prediction.pickNMovies'."""
     

    def test_suggestNMovies(self):
    	"""Tests 'prediction.pickNMovies'."""
     
