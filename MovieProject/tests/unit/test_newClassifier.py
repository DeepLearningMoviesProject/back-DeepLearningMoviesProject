#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Test for MovieProject/learning/newClassifier.py

Created on Wed Mar 15 09:21:56 2017
@author: elsa
"""

from MovieProject.learning.newClassifier import *
from MovieProject.resources import GLOBAL_MODEL_FILE
import unittest

class NewClassifierTest(unittest.TestCase):
    """Test case used to test 'learning.newClassifier'."""

#    # This method will be called BEFORE every test
#    def setUp(self):
        
    def test_buildModelUniq(self):
        """Tests 'newClassifier.buildModelUniq'."""
        model = buildModelUniq()
        #Test that it returns a model
        self.assertNotEqual(model, None)
        #Test that it creates a file

    def test_suggestMoviesSaveNBest(self):
        """Tests 'newClassifier.suggestMoviesSaveNBest'."""
        #Test no user
        #Test n > amount of suggest movies for the user (> 45 for user 2)
        #Test if user doesn't exists
        
    def test_getNBestMovies(self):
        """Tests 'newClassifier.getNBestMovies'."""
        #Test if file doesn't exists for user
        #Test if file exists with less movies
        #Test if file exists with more movies
        
    def test_getModel(self):
        """Tests 'newClassifier.getModel'."""
        
        

if __name__ == '__main__':
    unittest.main()