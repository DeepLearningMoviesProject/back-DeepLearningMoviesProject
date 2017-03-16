#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Test for MovieProject/preprocessing/tools/apiTMDB

Created on Tue Feb  7 11:21 2017
@author: elsa
"""

from MovieProject.preprocessing.tools.apiTMDB import *
import unittest

class ApiTMDBTest(unittest.TestCase):
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
        self.assertEquals(infoAlice["title"], "Alice")
        self.assertEquals(infoAlice["genres"], [])
        self.assertEquals(infoAlice["production_countries"], [])

        self.assertEquals(infoNemo["title"], "Finding Nemo")
        self.assertEquals(infoNemo["runtime"], 100)

        self.assertEquals(moviesEmpty, [])

    def test_getCredits(self):
        """ Tests 'apiTMDB.getCredits' """

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
        with self.assertRaises(AttributeError):
            noKeywords = getKeywords({})

        #Keywords for invalid object
        with self.assertRaises(AttributeError):
            invalidKeywords = getKeywords({"hello" : True})

    def test_getGenres(self):
        """ Tests 'apiTMDB.getGenres' """

        genres = getGenres({"genres": [{"id": 16,"name": "Animation"},
                                        {"id": 10751,"name": "Family"}]})
        self.assertGreater(len(genres), 0)
        self.assertEqual(genres[0], "animation")
        self.assertEqual(genres[1], "family")

        noGenres = getGenres({"genres" : []})
        self.assertEquals(noGenres, [])

        with self.assertRaises(AttributeError):
            invalidGenres = getGenres({"hello" : True})
        with self.assertRaises(AttributeError):
            invalidGenres = getGenres({})


    def test_getRating(self):
        """ Tests 'apiTMDB.getRating' """
        movieInfoLambda = {"vote_average" : 0}
        movieInfoFake = {"vote_average" : "coucou"}

        movieRatingLambda = getRating(movieInfoLambda)
        movieRatingFake = getRating(movieInfoFake)

        self.assertEquals(movieRatingLambda, 0)
        self.assertEquals(movieRatingFake, "coucou") 
    
    def test_getTitle(self):
        """ Tests 'apiTMDB.getTitle """
        movieInfoLambda = {"title" : "hello there !"}
        movieInfoSpecials = {"title" : "WhAt is thAt ?"}

        movieTitleLambda = getTitle(movieInfoLambda)
        movieTitleSpecials = getTitle(movieInfoSpecials)

        self.assertEquals(movieTitleLambda, ["hello", "there"])
        self.assertEquals(movieTitleSpecials, ["what", "is", "that"]) 


    def test_getMovie(self):
        """ Tests 'apiTMDB.getMovies' """
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

    def test_getTmdbGenres(self):
        """ Tests 'apiTMDB.getTmdbGenres' """
        genres = getTmdbGenres()
        self.assertEquals(len(genres), 19)

    def test_getDirectors(self):
        """ Tests 'apiTMDB.getDirectors' """
        
        movie = getMovie(11)
        
        directors = ["george lucas"]
        directorsTest = getDirectors(movie.credits())
        
        self.assertEqual(len(directors), len(directorsTest))
        self.assertEqual(directorsTest[0], directors[0])
    
    def test_getOverview(self):
        overview = getOverview({"overview" : "Hello!"})
        self.assertEqual(len(overview), 5)
        self.assertEqual(overview, "hello")

        #If we call getOverview with a dict that has no attribute overview it must raise an error
        with self.assertRaises(AttributeError):
            overviewInvalidValue = getCredits({"hello" : True})

        #If we send an empty info of movies to getOverview, it must raise an error
        with self.assertRaises(AttributeError):
            overviewNoMovie = getOverview({})

        overviewEmpty = getOverview({"overview" : ""})
        self.assertEqual(overviewEmpty, "")

    def test_getActors(self):
        """ Tests 'apiTMDB.getActors' """
        
        #Test OK
        cast = [{"name": "Mark Hamill"},{"name": "Harrison Ford"},{"name": "Carrie Fisher"},{"name": "Peter Cushing"},{"name": "Actor Test"}]  
        actors = ["Mark Hamill", "Harrison Ford", "Carrie Fisher", "Peter Cushing", "Actor Test"]
        actorsTest = getActors({"cast" : cast})
        
        self.assertEqual(len(actors)-1, len(actorsTest))
        for i in range(len(actorsTest)):
            self.assertEqual(actors[i].lower(), actorsTest[i])

        #Test empty cast
        actorsEmpty = getActors({"cast" : []})
        self.assertEqual(actorsEmpty, [])

        #Test invalid attribute
        with self.assertRaises(AttributeError):
            actorsInvalidValue = getActors({"hello" : True})

        #Test empty attribute
        with self.assertRaises(AttributeError):
            actorsNoValue = getActors({})

    def test_getRuntime(self):
        """ Tests 'apiTMDB.getRuntime' """
        
        #Test OK
        runtime = getRuntime({"runtime" : 158})
        self.assertEqual(runtime, 158)

        #Test None
        runtimeNone = getRuntime({"runtime" : None})
        self.assertEqual(runtimeNone, 0)

        #Test invalid attribute
        with self.assertRaises(AttributeError):
            runtimeInvalidValue = getRuntime({"hello" : True})

        #Test empty attribute
        with self.assertRaises(AttributeError):
            runtimeNoValue = getRuntime({})


    def test_getYear(self):
        """ Tests 'apiTMDB.getYear' """
        
        #Test OK
        runtime = getYear({"release_date" : "2012-09-30"})
        self.assertEqual(runtime, 2012)

        #Test None - Movie 280632 has no release date
        movie = getMovie(387773)
        runtimeNone = getYear(movie.info())
        self.assertEqual(runtimeNone, 0)

        #Test invalid attribute
        with self.assertRaises(AttributeError):
            runtimeInvalidValue = getYear({"hello" : True})

        #Test empty attribute
        with self.assertRaises(AttributeError):
            runtimeNoValue = getYear({})

    def test_getBudget(self):
        """ Tests 'apiTMDB.getBudget' """
        
        #Test OK - Nemo has a budget > 0
        movie1 = getMovie(12)
        budget = getBudget(movie1.info())
        self.assertGreater(budget, 0)

        #Test None - Movie 280632 has no budget
        movie2 = getMovie(387773)
        budgetNone = getBudget(movie2.info())
        self.assertEqual(budgetNone, 0)

        #Test invalid attribute
        with self.assertRaises(AttributeError):
            budgetInvalidValue = getBudget({"hello" : True})

        #Test empty attribute
        with self.assertRaises(AttributeError):
            budgetNoValue = getBudget({})

    def test_getProdCompagnies(self):
        """ Tests 'apiTMDB.getProdCompagnies' """
        
        #Test OK - Nemo has production companies (Disney, Pixar)
        movie1 = getMovie(12)
        prodcomp = getProdCompagnies(movie1.info())
        self.assertGreater(len(prodcomp), 0)

        #Test None - Movie 280632 has no production companies
        movie2 = getMovie(387773)
        prodcompNone = getProdCompagnies(movie2.info())
        self.assertEqual(prodcompNone, [])

        #Test invalid attribute
        with self.assertRaises(AttributeError):
            prodcompInvalidValue = getProdCompagnies({"hello" : True})

        #Test empty attribute
        with self.assertRaises(AttributeError):
            prodcompNoValue = getProdCompagnies({})

    def test_getLanguage(self):
        """ Tests 'apiTMDB.getLanguage' """
        
        #Test OK - Nemo has language
        movie1 = getMovie(12)
        lang = getLanguage(movie1.info())
        self.assertGreater(len(lang), 0)

        #Test None - Movie that has no language
        info = {"spoken_languages": []}
        langNone = getLanguage(info)
        self.assertEqual(langNone, [])

        #Test invalid attribute
        with self.assertRaises(AttributeError):
            langInvalidValue = getLanguage({"hello" : True})

        #Test empty attribute
        with self.assertRaises(AttributeError):
            langNoValue = getLanguage({})

    def test_getBelongsTo(self):
        """ Tests 'apiTMDB.getBelongsTo' """
        
        #Test OK - Star Wars has belongs to attribute
        movie1 = getMovie(11)
        belongs = getBelongsTo(movie1.info())
        self.assertTrue(belongs)

        #Test None - Movie that has no belongs to attribute
        info = {"belongs_to_collection": None}
        belongsNone = getBelongsTo(info)
        self.assertFalse(belongsNone)

        #Test invalid attribute
        with self.assertRaises(AttributeError):
            belongsInvalidValue = getBelongsTo({"hello" : True})

        #Test empty attribute
        with self.assertRaises(AttributeError):
            belongsNoValue = getBelongsTo({})


    def test_requests(self):
        ids = [415, 11, 374080]
        
        infos, keywords, credits = requests(ids)
        
        self.assertEqual(len(infos), 2)
        self.assertEqual(len(keywords), 2)
        self.assertEqual(len(credits), 2)


if __name__ == '__main__':
    unittest.main()