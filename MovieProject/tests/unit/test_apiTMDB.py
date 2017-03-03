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
    """Test case used to test 'preprocessing.tools.apiTMDB'."""

    moviesId = []
    # movies = []

    # This method will be called BEFORE every test
    def setUp(self):
        if(len(self.moviesId) == 0):
            self.moviesId.append(1)         #Movie doesn't exists
            self.moviesId.append(404031)    #Movie with no votes, no compagnies, no country, no genres, no collection
            self.moviesId.append(12)        #Movie exists
            # self.movies = getMovies(self.moviesId)
            # print self.movies
        
    def test_getMovies(self):
        """Tests 'apiTMDB.getMovies'."""
        movies = getMovies(self.moviesId)
        moviesEmpty = getMovies([])

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
        infoAlice = movies[1].info()
        infoNemo = movies[2].info()
        #Check that it is the correct id
        self.assertEquals(infoAlice["id"], self.moviesId[1])
        self.assertEquals(infoNemo["id"], self.moviesId[2])
        #Check that the ids match the movies, otherwise the ids has changed
        self.assertEquals(infoAlice["genres"], [])
        self.assertEquals(infoAlice["production_countries"], [])

        self.assertEquals(infoNemo["title"], "Finding Nemo")
        self.assertEquals(infoNemo["runtime"], 100)

        self.assertEquals(moviesEmpty, [])

    def test_getCredits(self):
        #This movie has credits
        movies = getMovies(self.moviesId)
        credits = getCredits([movies[2]])
        self.assertGreater(len(credits), 0)

        #If we call getCredits with an invalid attribute it must raise an error
        with self.assertRaises(AttributeError):
            credInvalidValue = getCredits("hello")

        #If we send an empty list of movies to getcredits, it must return an empty list
        credNoMovie = getCredits([])
        self.assertEquals(credNoMovie, [])


    def test_getKeywords(self):
    	"""Tests 'apiTMDB.getKeywords'."""
        nemo = getMovie(12) #movies[2]
        keywords = getKeywords(nemo.keywords())

        #12 is finding nemo,
        #must have keywords :
        #pixar, clownfish, dentist, harbor
        self.assertGreater(len(keywords), 0)
        self.assertTrue("pixar" in keywords)
        self.assertTrue("clownfish" in keywords)
        self.assertTrue("dentist" in keywords)
        self.assertTrue("harbor" in keywords)

        #Alice has no keywords
        alice = getMovie(404031) #self.movies[1]
        noKeywords = getKeywords(alice.keywords())
        self.assertEquals(noKeywords, [])

        #Keywords for empty object
        noKeywords = getKeywords()
        self.assertEquals(noKeywords, [])

    def test_getGenres(self):
        nemo = getMovie(12) #Nemo
        alice = getMovie(404031) #Alice, no genres

        genres = getGenres(nemo.info())
        noGenres = getGenres(alice.info())

        self.assertEquals(noGenres, [])
        self.assertGreater(len(genres), 0)

    def test_getRating(self):
        movieInfoLambda = {"vote_average" : 0}
        movieInfoFake = {"vote_average" : "coucou"}

        movieRatingLambda = getRating(movieInfoLambda)
        movieRatingFake = getRating(movieInfoFake)

        self.assertEquals(movieRatingLambda, 0)
        self.assertEquals(movieRatingFake, "coucou") 
    
    def test_getTitle(self):
        movieInfoLambda = {"title" : "hello there !"}
        movieInfoSpecials = {"title" : "WhAt is thAt ?"}

        movieTitleLambda = getTitle(movieInfoLambda)
        movieTitleSpecials = getTitle(movieInfoSpecials)

        self.assertEquals(movieTitleLambda, ["hello", "there"])
        self.assertEquals(movieTitleSpecials, ["what", "is", "that"]) 


    def test_getMovie(self):
        movie1 = getMovie(0)
        movie2 = getMovie(12)

        self.assertEquals(movie2.info()['id'], 12)

        success = True
        try:
            info1 = movie1.info()
        except:
            success = False
        #We must not succeed
        self.assertFalse(success)

    def test_getDirectors(self):
        """ Tests 'apiTMDB.getDirectors' """
        
        movie = getMovie(11)
        
        directors = ["George Lucas"]
        directorsTest = getDirectors(movie.credits())
        
        self.assertEqual(len(directors), len(directorsTest))
        self.assertEqual(directorsTest[0], directors[0])
        
    def test_getActors(self):
        """ Tests 'apiTMDB.getActors' """
        
        movie = getMovie(11)
        
        actors = ["Mark Hamill", "Harrison Ford", "Carrie Fisher", "Peter Cushing"]
        actorsTest = getActors(movie.credits())
        
        self.assertEqual(len(actors), len(actorsTest))
        for i in range(len(actors)):
            self.assertEqual(actors[i], actors[i])

if __name__ == '__main__':
    unittest.main()