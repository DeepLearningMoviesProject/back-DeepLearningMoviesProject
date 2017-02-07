#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Test for MovieProject/preprocessing/tools/apiTMDB

Created on Tue Feb  7 11:21 2017
@author: elsa
"""

from MovieProject.preprocessing.tools.apiTMDB import *
import unittest

class TextTest(unittest.TestCase):

    """Test case utilisé pour tester les fonctions du module 'preprocessing.tools.apiTMDB'."""

    def test_getMovies(self):
        """Teste le fonctionnement de la fonction 'apiTMDB.getMovies'."""
        # 11 is Star Wars, 1 not found, 12 is Finding Nemo
        moviesId = [1,11,12]
        movies = getMovies(moviesId)

        #assert that there are 3 movies on the list
        self.assertEquals(len(movies), 3)

        #The first movie is "not found"
        success = True
        try:
            info1 = movies[0].info()
        except:
            success = False
        #We must not succeed
        self.assertFalse(success)

        #Get the movies
        info11 = movies[1].info()
        info12 = movies[2].info()
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
