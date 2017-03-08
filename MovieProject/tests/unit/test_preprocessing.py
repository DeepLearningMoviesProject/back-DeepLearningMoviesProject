#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 15:14:34 2017

@author: Kaito
"""

from MovieProject.preprocessing.preprocessing import People, Preprocessor, concatData
from MovieProject.preprocessing.tools import loadGloveDicFromFile
from MovieProject.preprocessing.words import meanWords, wordsToGlove
from MovieProject.resources import GLOVE_DICT_FILE
import numpy as np
import unittest
from MovieProject.preprocessing.tools.apiTMDB import *

class PreprocessingTest(unittest.TestCase):
    
    glove = loadGloveDicFromFile()
    movies = getMovies([415, 280632])#, 387773, 404301])
    infos = [ m.info() for m in movies]
    keywords = [ m.keywords() for m in movies]
    credits = [ m.credits() for m in movies]
    
    def setUp(self):
        self.p = Preprocessor(**{ "titles" : True,
                              "rating" : True,
                              "overviews" : True,
                              "keywords" : True,
                              "genres" : True,
                              "actors" : True,
                              "directors" : True,
                              "compagnies" : True,
                              "language" : True,
                              "belongs" : True,
                              "runtime" : True,
                              "date" : True,
                              "budget" : True })
    
        
        
    def tearDown(self):
        pass
    
    def test_concatData(self):
        self.assertEqual(np.array([]).shape, concatData([]).shape)
        
        array1 = np.empty((1,3))
        array2 = np.empty((1,5))
        self.assertEqual(array1.shape, concatData([array1]).shape)
        
        res = concatData([array1,array2])
        result = np.array([[ 1.,  2.,  3.,  0.,  1.,  2.,  3.,  4.]])
        self.assertEqual(res.shape, result.shape)

        for i in range(result.shape[1]):
            self.assertEqual(res[0][i], result[0][i])


    def test_keywordsProcessing(self):
        self.assertEqual(np.array([]).tolist(), self.p.keywordsProcessing([]).tolist())        
        
        keyword1 = getKeywords(self.keywords[0])
        final1 = meanWords(*wordsToGlove(keyword1, self.glove))
        final1 = final1.reshape((1,final1.shape[0]))
        
        keyword2 = getKeywords(self.keywords[1])
        final2 = meanWords(*wordsToGlove(keyword2, self.glove))
        final2 = final2.reshape((1,final2.shape[0]))

        res1 = self.p.keywordsProcessing([self.keywords[0]])
        self.assertEqual(final1.tolist(), res1.tolist())
        
        res2 = self.p.keywordsProcessing([ k for k in self.keywords[:2] ])
        
        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
        
        
    def test_titlesProcessing(self):
        self.assertEqual(np.array([]).tolist(), self.p.titlesProcessing([]).tolist())        
        
        title1 = getTitle(self.infos[0])
        final1 = meanWords(*wordsToGlove(title1, self.glove))
        final1 = final1.reshape((1,final1.shape[0]))

        
        title2 = getTitle(self.infos[1])
        final2 = meanWords(*wordsToGlove(title2, self.glove))
        final2 = final2.reshape((1,final2.shape[0]))

        res1 = self.p.titlesProcessing([self.infos[0]])
        self.assertEqual(final1.tolist(), res1.tolist())
        
        res2 = self.p.titlesProcessing([ k for k in self.infos[:2] ])
        
        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
        
        
    def test_peopleProcessingActor(self):
        self.assertEqual(np.array([]).tolist(), self.p.peopleProcessing([], People.ACTOR).tolist())        
        
        with self.assertRaises(ValueError):
            self.p.peopleProcessing([], None)
            
        actor1 = [ name for actor in getActors(self.credits[0]) for name in actor.split() ]
        final1 = meanWords(*wordsToGlove(actor1, self.glove))
        final1 = final1.reshape((1,final1.shape[0]))
        
        actor2 = [ name for actor in getActors(self.credits[1]) for name in actor.split() ]
        final2 = meanWords(*wordsToGlove(actor2, self.glove))
        final2 = final2.reshape((1,final2.shape[0]))

        res1 = self.p.peopleProcessing([self.credits[0]], People.ACTOR)
        self.assertEqual(final1.tolist(), res1.tolist())
        
        res2 = self.p.peopleProcessing([ k for k in self.credits[:2] ], People.ACTOR)
        
        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
        
        
    def test_peopleProcessingDirector(self):
        self.assertEqual(np.array([]).tolist(), self.p.peopleProcessing([], People.DIRECTOR).tolist())        
        
        with self.assertRaises(ValueError):
            self.p.peopleProcessing([], None)
            
        director1 = [ name for director in getDirectors(self.credits[0]) for name in director.split() ]
        final1 = meanWords(*wordsToGlove(director1, self.glove))
        final1 = final1.reshape((1,final1.shape[0]))
        
        director2 = [ name for director in getDirectors(self.credits[1]) for name in director.split() ]
        final2 = meanWords(*wordsToGlove(director2, self.glove))
        final2 = final2.reshape((1,final2.shape[0]))

        res1 = self.p.peopleProcessing([self.credits[0]], People.DIRECTOR)
        self.assertEqual(final1.tolist(), res1.tolist())
        
        res2 = self.p.peopleProcessing([ k for k in self.credits[:2] ], People.ACTOR)
        
        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
        
    
    def test_compagniesProcessing(self):
        self.assertEqual(np.array([]).tolist(), self.p.compagniesProcessing([]).tolist())        
        
        compagnies1 = [ compagnie for compagnies in getProdCompagnies(self.infos[0]) for compagnie in compagnies.split() ]
        final1 = meanWords(*wordsToGlove(compagnies1, self.glove))
        final1 = final1.reshape((1,final1.shape[0]))

        
        compagnies2 = [ compagnie for compagnies in getProdCompagnies(self.infos[1]) for compagnie in compagnies.split() ]
        final2 = meanWords(*wordsToGlove(compagnies2, self.glove))
        final2 = final2.reshape((1,final2.shape[0]))

        res1 = self.p.compagniesProcessing([self.infos[0]])
        self.assertEqual(final1.tolist(), res1.tolist())
        
        res2 = self.p.compagniesProcessing([ k for k in self.infos[:2] ])
        
        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
        
#    def test_genresProcessing(self):
#        self.assertEqual(np.array([]).tolist(), self.p.genresProcessing([]).tolist())        
#        
#        genre1 = getGenres(self.infos[0])
#        final1 = meanWords(*wordsToGlove(genre1, self.glove))
#        final1 = final1.reshape((1,final1.shape[0]))
#
#        
#        genre2 = getGenres(self.infos[1])
#        final2 = meanWords(*wordsToGlove(genre2, self.glove))
#        final2 = final2.reshape((1,final2.shape[0]))
#
#        res1 = self.p.genresProcessing([self.infos[0]])
#        self.assertEqual(final1.tolist(), res1.tolist())
#        
#        res2 = self.p.genresProcessing([ k for k in self.infos[:2] ])
#        
#        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
        
if __name__ == "__main__":
    unittest.main()