#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Test for MovieProject/learning/classifier

Created on Fri Feb 17 13:26:55 2017
@author: elsa
"""

import unittest
from MovieProject.preprocessing import Preprocessor
from MovieProject.learning import buildModel, predictMovies, suggestNMovies
import numpy as np
import tmdbsimple as tmdb
from random import randint

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


class PredictionTest(unittest.TestCase):
    """Test case used to test the module 'learning.prediction'."""

    model = None
    idMovie1 = 0
    idMovie2 = 0

    # This method will be called BEFORE every test
    def setUp(self):

        #Pick 2 random movies
        pages = tmdb.Discover().movie(vote_count_gte=20)
        totalPages = pages['total_pages'] 
        iPage1 =  randint(1,totalPages)
        iPage2 =  randint(1,totalPages)
        page1 = tmdb.Discover().movie(page=iPage1, vote_count_gte=20)
        page2 = tmdb.Discover().movie(page=iPage2, vote_count_gte=20)
        result1 = page1["results"]
        result2 = page2["results"]
        iMovie1 = randint(0,len(result1)-1)
        iMovie2 = randint(0,len(result2)-1)
        self.idMovie1 = result1[iMovie1]['id']
        self.idMovie2 = result2[iMovie2]['id']

        #We build the model only once
        if self.model is None:
            #Movies to build the model
            movies = {"11":1,"18":1,"22":1}
            ids = [int(key) for key in movies]
            labels = np.array([movies[key] for key in movies])

            #We will build the model
            pProcessor = Preprocessor(**params)
            data = pProcessor.preprocess(ids)
            self.model = buildModel(data, labels)
 
    def test_predictMovies(self):
        """Tests 'prediction.predictMovies'."""
        
        #Regular movies - they exist in tmdb
        toPredict = [self.idMovie1, self.idMovie2]
        predictionsValid = predictMovies(toPredict, self.model, **params)
        pValidValue1 = predictionsValid[0].item()
        pValidValue2 = predictionsValid[1].item()
        print predictionsValid
        print pValidValue1
        print pValidValue2
        #No movie
        toPredict = []
        predictionsEmpty = predictMovies(toPredict, self.model, **params)
        #Movie with incorrect ID
        toPredict = [1]
        predictionsInvalid = predictMovies(toPredict, self.model, **params)
        #Try to predict movies with an invalid model (None)
        with self.assertRaises(ValueError):
            predictionsValidModelInvalid = predictMovies(toPredict, None, **params)
        
        self.assertEqual(predictionsEmpty, [])
        self.assertEqual(predictionsInvalid, [])
        self.assertTrue(pValidValue1 <= 1.0 and pValidValue1 >= 0)
        self.assertTrue(pValidValue2 <= 1.0 and pValidValue2 >= 0)

    def test_suggestNMovies(self):
    	"""Tests 'prediction.suggestNMovies'."""
        suggestedEmpty = suggestNMovies(self.model, 0, **params)
        suggested20 = suggestNMovies(self.model, 20, **params)

        self.assertEqual(suggestedEmpty, [])
        self.assertEqual(len(suggested20), 20)
        self.assertEqual(type(suggested20), type([]))
     
