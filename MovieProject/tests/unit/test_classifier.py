#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Test for MovieProject/learning/classifier

Created on Wed Feb  8 15:19 2017
@author: elsa
"""

from MovieProject.preprocessing.tools.apiTMDB import *
import unittest

class TextTest(unittest.TestCase):

    """Test case utilisé pour tester les fonctions du module 'learning.classifier'."""

    def test_getMatrix(self):
        """Teste le fonctionnement de la fonction 'classifier.getMatrix'."""
        
        matrix = {}
        matrix['genres'] = [0,1,0]
        matrix['titles'] = [1,0,0]
        matrix['rating'] = [0,0,0]
        matrix['directors'] = [0,0,1]
        matrix['Pédoncule'] = [0,0,0]

        matrixTrain, matrixTest = getMatrix(matrix, 2, 1)

        #Check that it is the correct id
        self.assertEquals(info11["id"], moviesId[1])
        self.assertEquals(info12["id"], moviesId[2])
        #Check that the ids match the movies, otherwise the ids has changed
        self.assertEquals(info11["title"], "Star Wars")
        self.assertEquals(info12["title"], "Finding Nemo")

    def test_getKeywords(self):
    	"""Teste le fonctionnement de la fonction 'apiTMDB.getKeywords'."""
        nemo = getMovie(12)
        keywords = getKeywords(nemo.keywords())
        #12 is finding nemo, 
        #must have keywords : 
        #pixar, clownfish, dentist, harbor
        self.assertTrue("pixar" in keywords)
        self.assertTrue("clownfish" in keywords)
        self.assertTrue("dentist" in keywords)
        self.assertTrue("harbor" in keywords)

    # def test_textToVect(self):
        
    def test_getDirectors(self):
        """ Teste le fonctionnement de la fonction 'apiTMDB.getDirectors' """
        
        movie = getMovie(11)
        
        directors = ["George Lucas"]
        directorsTest = getDirectors(movie.credits())
        
        self.assertEqual(len(directors), len(directorsTest))
        self.assertEqual(directorsTest[0], directors[0])
        
    def test_getActors(self):
        """ Teste le fonctionnement de la fonction 'apiTMDB.getActors' """
        
        movie = getMovie(11)
        
        actors = ["Mark Hamill", "Harrison Ford", "Carrie Fisher", "Peter Cushing"]
        actorsTest = getActors(movie.credits())
        
        self.assertEqual(len(actors), len(actorsTest))
        for i in range(len(actors)):
            self.assertEqual(actors[i], actors[i])
