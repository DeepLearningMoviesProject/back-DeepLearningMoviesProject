#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 15:14:34 2017

@author: Kaito
"""

from MovieProject.preprocessing.preprocessing import People, Preprocessor, concatData,textToVect
from MovieProject.preprocessing.tools import loadGloveDicFromFile, SIZE_VECTOR, loadD2VModel
from MovieProject.preprocessing import meanWords, wordsToGlove
from MovieProject.resources import GLOVE_DICT_FILE, OVERVIEW_MODEL
import numpy as np
import unittest
from MovieProject.preprocessing.tools.apiTMDB import *

class PreprocessingTest(unittest.TestCase):
    
    glove = loadGloveDicFromFile()
    d2vModel = loadD2VModel(OVERVIEW_MODEL)
    movies = getMovies([415, 280632, 404301])#, 387773])
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
    
#    def test_concatData(self):
#        self.assertEqual(np.array([]).shape, concatData([]).shape)
#        
#        array1 = np.empty((1,3))
#        array2 = np.empty((1,5))
#        self.assertEqual(array1.shape, concatData([array1]).shape)
#        
#        res = concatData([array1,array2])
#        result = np.array([[ 1.,  2.,  3.,  0.,  1.,  2.,  3.,  4.]])
#        self.assertEqual(res.shape, result.shape)
#
#        for i in range(result.shape[1]):
#            self.assertEqual(res[0][i], result[0][i])
#
#
#    def test_keywordsProcessing(self):
#        self.assertEqual(np.array([]).tolist(), self.p.keywordsProcessing([]).tolist())        
#        
#        keyword1 = getKeywords(self.keywords[0])
#        final1 = meanWords(*wordsToGlove(keyword1, self.glove))
#        final1 = final1.reshape((1,final1.shape[0]))
#        
#        keyword2 = getKeywords(self.keywords[1])
#        final2 = meanWords(*wordsToGlove(keyword2, self.glove))
#        final2 = final2.reshape((1,final2.shape[0]))
#
#        res1 = self.p.keywordsProcessing([self.keywords[0]])
#        self.assertEqual(final1.tolist(), res1.tolist())
#        
#        res2 = self.p.keywordsProcessing([ k for k in self.keywords[:2] ])
#        
#        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
#        
#        
#    def test_titlesProcessing(self):
#        self.assertEqual(np.array([]).tolist(), self.p.titlesProcessing([]).tolist())        
#        
#        title1 = getTitle(self.infos[0])
#        final1 = meanWords(*wordsToGlove(title1, self.glove))
#        final1 = final1.reshape((1,final1.shape[0]))
#
#        
#        title2 = getTitle(self.infos[1])
#        final2 = meanWords(*wordsToGlove(title2, self.glove))
#        final2 = final2.reshape((1,final2.shape[0]))
#
#        res1 = self.p.titlesProcessing([self.infos[0]])
#        self.assertEqual(final1.tolist(), res1.tolist())
#        
#        res2 = self.p.titlesProcessing([ k for k in self.infos[:2] ])
#        
#        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
#        
#        
#    def test_peopleProcessingActor(self):
#        self.assertEqual(np.array([]).tolist(), self.p.peopleProcessing([], People.ACTOR).tolist())        
#        
#        with self.assertRaises(ValueError):
#            self.p.peopleProcessing([], None)
#            
#        actor1 = [ name for actor in getActors(self.credits[0]) for name in actor.split() ]
#        final1 = meanWords(*wordsToGlove(actor1, self.glove))
#        final1 = final1.reshape((1,final1.shape[0]))
#        
#        actor2 = [ name for actor in getActors(self.credits[1]) for name in actor.split() ]
#        final2 = meanWords(*wordsToGlove(actor2, self.glove))
#        final2 = final2.reshape((1,final2.shape[0]))
#
#        res1 = self.p.peopleProcessing([self.credits[0]], People.ACTOR)
#        self.assertEqual(final1.tolist(), res1.tolist())
#        
#        res2 = self.p.peopleProcessing([ k for k in self.credits[:2] ], People.ACTOR)
#        
#        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
#        
#        
#    def test_peopleProcessingDirector(self):
#        self.assertEqual(np.array([]).tolist(), self.p.peopleProcessing([], People.DIRECTOR).tolist())        
#        
#        with self.assertRaises(ValueError):
#            self.p.peopleProcessing([], None)
#            
#        director1 = [ name for director in getDirectors(self.credits[0]) for name in director.split() ]
#        final1 = meanWords(*wordsToGlove(director1, self.glove))
#        final1 = final1.reshape((1,final1.shape[0]))
#        
#        director2 = [ name for director in getDirectors(self.credits[1]) for name in director.split() ]
#        final2 = meanWords(*wordsToGlove(director2, self.glove))
#        final2 = final2.reshape((1,final2.shape[0]))
#
#        res1 = self.p.peopleProcessing([self.credits[0]], People.DIRECTOR)
#        self.assertEqual(final1.tolist(), res1.tolist())
#        
#        res2 = self.p.peopleProcessing([ k for k in self.credits[:2] ], People.ACTOR)
#        
#        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
#        
#    
#    def test_compagniesProcessing(self):
#        self.assertEqual(np.array([]).tolist(), self.p.compagniesProcessing([]).tolist())        
#        
#        compagnies1 = [ compagnie for compagnies in getProdCompagnies(self.infos[0]) for compagnie in compagnies.split() ]
#        final1 = meanWords(*wordsToGlove(compagnies1, self.glove))
#        final1 = final1.reshape((1,final1.shape[0]))
#
#        
#        compagnies2 = [ compagnie for compagnies in getProdCompagnies(self.infos[1]) for compagnie in compagnies.split() ]
#        final2 = meanWords(*wordsToGlove(compagnies2, self.glove))
#        final2 = final2.reshape((1,final2.shape[0]))
#
#        res1 = self.p.compagniesProcessing([self.infos[0]])
#        self.assertEqual(final1.tolist(), res1.tolist())
#        
#        res2 = self.p.compagniesProcessing([ k for k in self.infos[:2] ])
#        
#        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
#        
#        
#    def test_genresProcessing(self):
#        self.assertEqual(np.array([]).tolist(), self.p.genresProcessing([]).tolist())  
#        
#        tmdbGenre = getTmdbGenres()
#       
#        genre1 = getGenres(self.infos[0])
#        
#        res1 = self.p.genresProcessing([self.infos[0]])
#        self.assertEqual(len(tmdbGenre.keys()),res1.shape[1])
#        for g in genre1:
#            index = tmdbGenre[g]
#            self.assertEqual(res1[0][index], 1.)
#        
#        res2 = self.p.genresProcessing([ k for k in self.infos[:2] ])
#        self.assertEqual((2, len(tmdbGenre.keys())),res2.shape)
#        self.assertEqual(np.zeros(len(tmdbGenre.keys())).tolist(), res2[1].tolist())
#        
#    
#    def test_overviewProcessing(self):
#        self.assertEqual(np.array([]).tolist(), self.p.overviewProcessing([]).tolist()) 
#        
#        overview1 = getOverview(self.infos[0])
#        self.assertNotEqual(overview1, "")
#        
#        final1 = meanWords(*wordsToGlove(overview1.split(), self.glove))
#        final1 = final1.reshape((1,final1.shape[0]))
#        
#        res1 = self.p.overviewProcessing([self.infos[0]])
#        self.assertEqual(final1.tolist(), res1.tolist())
#        
#        overview2 = getOverview(self.infos[1])
#        self.assertEqual(overview2, "")
#        final2 = np.zeros((1, final1.shape[1]))
#        
#        res2 = self.p.overviewProcessing([ i for i in self.infos[:2] ])
#        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
#        self.assertEqual(final2[0].tolist(), res2[1].tolist())
        
        
    def test_overviewProcessingD2V(self):
        self.assertEqual(np.array([]).tolist(), self.p.overviewProcessingD2V([]).tolist()) 
        
        overview1 = getOverview(self.infos[0])
        self.assertNotEqual(overview1, "")
        
        vect1 = textToVect(overview1, self.d2vModel)
        final1 = vect1.reshape((1,vect1.shape[0]))
        
        res1 = self.p.overviewProcessingD2V([self.infos[0]])
        self.assertEqual(final1.tolist(), res1.tolist())
        
        overview2 = getOverview(self.infos[1])
        self.assertEqual(overview2, "")
        final2 = np.zeros((1, SIZE_VECTOR))
        
        res2 = self.p.overviewProcessingD2V([ i for i in self.infos[:2] ])
        self.assertEqual((final1.shape[0] + final2.shape[0], final1.shape[1]), res2.shape)
        self.assertEqual(final2[0].tolist(), res2[1].tolist())
        
        
    def test_languageProcessing(self):
        self.assertEqual(np.array([]).tolist(), self.p.languageProcessing([]).tolist())
        
        langs1 = [ lang for langs in getLanguage(self.infos[0]) for lang in langs.split() ]
        self.assertNotEqual(langs1, [])
        
        final1 = meanWords(*wordsToGlove(langs1, self.glove))
        final1 = final1.reshape((1,final1.shape[0]))
        
        res1 = self.p.languageProcessing([self.infos[0]])
        self.assertEqual(final1.shape, res1.shape)
        self.assertEqual(final1.tolist(), res1.tolist())
        
        langs1 = [ lang for langs in getLanguage(self.infos[2]) for lang in langs.split() ]
        self.assertEqual(langs1, [])
        final2 = np.zeros((1, final1.shape[1]))
        
        res2 = self.p.languageProcessing([self.infos[2]])
        self.assertEqual(final2.shape, res2.shape)
        self.assertEqual(final2.tolist(), res2.tolist())


    def test_belongsToProcessing(self):
        self.assertEqual(np.array([]).tolist(), self.p.belongsToProcessing([]).tolist())
        
        belong1 = getBelongsTo(self.infos[0])
        self.assertNotEqual(belong1, None)
        isBelong1 = int(belong1 is not None)
        final1 = np.array([isBelong1]).reshape((1,1))
        
        res1 = self.p.belongsToProcessing([self.infos[0]])
        self.assertEqual(final1.shape, res1.shape)
        self.assertEqual(final1.tolist(), res1.tolist())        
        
        belong2 = getBelongsTo(self.infos[1])
        self.assertEqual(belong2, None)
        isBelong2 = int(belong2 is not None)
        final2 = np.array([isBelong2]).reshape((1,1))
        
        res2 = self.p.belongsToProcessing([ i for i in self.infos[:2]])
        self.assertEqual((2,1), res2.shape)
        self.assertEqual(final2[0].shape, res2[1].shape)
        self.assertEqual(final2[0].tolist(), res2[1].tolist())
        
        
    def test_runtimeProcessing(self):
        self.assertEqual(np.array([]).tolist(), self.p.runtimeProcessing([]).tolist())
        
        runtime1 = getRuntime(self.infos[0])
        self.assertNotEqual(runtime1, 0)
        final1 = np.array([runtime1]).reshape((1,1))
        
        res1 = self.p.runtimeProcessing([self.infos[0]])
        self.assertEqual(final1.shape, res1.shape)
        self.assertEqual(final1.tolist(), res1.tolist())        
        
        runtime2 = getRuntime(self.infos[1])
        self.assertEqual(runtime2, 0)
        final2 = np.array([runtime2]).reshape((1,1))
        
        res2 = self.p.runtimeProcessing([ i for i in self.infos[:2]])
        self.assertEqual((2,1), res2.shape)
        self.assertEqual(final2[0].shape, res2[1].shape)
        self.assertEqual(final2[0].tolist(), res2[1].tolist())


    def test_dateProcessing(self):
        self.assertEqual(np.array([]).tolist(), self.p.dateProcessing([]).tolist())
        
        date1 = getYear(self.infos[0])
        self.assertNotEqual(date1, 0)
        final1 = np.array([date1]).reshape((1,1))
        
        res1 = self.p.dateProcessing([self.infos[0]])
        self.assertEqual(final1.shape, res1.shape)
        self.assertEqual(final1.tolist(), res1.tolist())        
        
        date2 = getYear(self.infos[1])
        self.assertEqual(date2, 1988)
        final2 = np.array([date2]).reshape((1,1))
        
        res2 = self.p.dateProcessing([ i for i in self.infos[:2]])
        self.assertEqual((2,1), res2.shape)
        self.assertEqual(final2[0].shape, res2[1].shape)
        self.assertEqual(final2[0].tolist(), res2[1].tolist())


    def test_budgetProcessing(self):
        self.assertEqual(np.array([]).tolist(), self.p.budgetProcessing([]).tolist())
        
        budget1 = getBudget(self.infos[0])
        final1 = np.array([0, 0, 0, 0, 1]).reshape((1,5))
        
        res1 = self.p.budgetProcessing([self.infos[0]])
        self.assertEqual(final1.shape, res1.shape)
        self.assertEqual(final1.tolist(), res1.tolist())        
        
        budget2 = getBudget(self.infos[1])
        final2 = np.array([1, 0, 0, 0, 0]).reshape((1,5))
        
        res2 = self.p.budgetProcessing([ i for i in self.infos[:2]])
        self.assertEqual((2,5), res2.shape)
        self.assertEqual(final2[0].shape, res2[1].shape)
        self.assertEqual(final2[0].tolist(), res2[1].tolist())
        
        
if __name__ == "__main__":
    unittest.main()