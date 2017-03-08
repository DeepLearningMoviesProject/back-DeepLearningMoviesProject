#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 15:09:55 2017

@author: coralie
"""

from MovieProject.preprocessing import words as w
from MovieProject.preprocessing.tools import gloveDict

import numpy as np
import unittest


class WordsTest(unittest.TestCase):
    """Test case used to test 'preprocessing.words'."""

    
    def test_wordIntoGlove(self):
        """Tests 'words.wordsToGlove'."""
        gloveDic = gloveDict.loadGloveDicFromFile()
        word = ["scat"]
        resultArray, expectedSize = w.wordsToGlove(word, gloveDic)
        size = resultArray.shape[1]
        expectedArray = np.array([[0.026201, -0.037278, -0.58936, -0.28615, -0.47301, 0.69033, -0.22468, 0.029743, 0.2246, 0.94357,
                      -0.054357, 0.48323, 0.9538, 0.38345, -0.69918, -0.64195, -0.088268, 0.48621, 0.42364, -0.51704,
                      -0.44851, -0.21705, 0.25903, -0.088207, 0.59777, 0.54634, -0.99789, 0.2576, -0.256, -1.7088,
                      0.19006, 0.19731, 0.13614, 1.2829, 0.41883, 0.027112, 0.45165, -0.48737, 0.31797, 0.14142,
                      -0.30245, -0.33968, -0.85194, 0.015752, 0.75979, -1.0888, 0.64471, -0.33908, -0.022592, 0.33961]],dtype="float32")
        self.assertEquals(resultArray.tolist(), expectedArray.tolist())
        self.assertEquals(resultArray.shape, expectedArray.shape)
        self.assertEquals(expectedSize, size)

    def test_twoWordsIntoGlove(self):
        """Tests 'words.wordsToGlove'."""
        gloveDic = gloveDict.loadGloveDicFromFile()
        words = ["sugar","daddy"]
        resultArray, expectedSize = w.wordsToGlove(words, gloveDic)
        size = resultArray.shape[1]
        array_sugar = [-1.1832, -0.22543, -0.54312, 0.42731, 0.21005, 0.65685, -0.25581, -0.1135, 0.59814, 0.61958, 0.52322, 0.39701, 1.0169, -0.66816, 0.27134, 0.57248, 0.34042, 0.44322, 0.15522, -1.177, 0.47931, -0.84173, 1.606, -0.13093, -0.91463, -0.37885, 0.29453, 0.35073, 1.3894, 0.49269, 2.427, -0.30031, -0.75508, 1.0198, 0.52147, -0.067951, -0.87317, 0.53923, 1.587, -0.31108, -0.031213, -0.056557, -0.13681, -0.33986, 0.55316, 1.5014, -0.54895, -0.81287, -0.22265, -0.2547]
        array_daddy = [-0.72194, 0.31107, 0.12859, -0.0046166, 0.45015, 0.23396, -0.22262, 0.29077, -0.55985, 0.8146, -0.2496, 1.0958, -0.16488, 0.27881, 0.69166, 0.035146, -0.17416, 0.94723, 0.85716, -0.22603, -0.38178, 0.11424, 0.72613, 0.40135, 0.56518, -0.7427, -1.5062, 0.20571, 0.79272, -1.3691, 0.93696, 0.44818, -0.39311, 1.2478, -0.0095384, 0.083801, 0.21949, -0.68483, 1.0895, -0.456, -0.83926, 0.017797, -1.453, -0.25652, 0.60549, -0.26667, -0.016655, -1.3032, 0.26798, 0.68606] 
        expectedArray = np.array([array_sugar,array_daddy],dtype="float32")
        self.assertEquals(resultArray.tolist(), expectedArray.tolist())
        self.assertEquals(resultArray.shape, expectedArray.shape )
        self.assertEquals(expectedSize, size)     
        
    def test_wordNonIntoGlove(self):
        """Tests 'words.wordsToGlove'."""
        gloveDic = gloveDict.loadGloveDicFromFile()
        word = ["bgfierbgkrhqgkdsfgh"]
        resultArray, expectedSize = w.wordsToGlove(word, gloveDic)
        expectedArray = np.array([np.zeros(expectedSize)])
        size = resultArray.shape[1]
        self.assertEquals(resultArray.tolist(), expectedArray.tolist())  
        self.assertEquals(resultArray.shape, expectedArray.shape )
        self.assertEquals(expectedSize, size)
        
    def test_threeWordsWithOnNonIntoGlove(self):
        """Tests 'words.wordsToGlove'."""
        gloveDic = gloveDict.loadGloveDicFromFile()
        words = ["exorcise","myyyyy","mind"]
        array_exorcise = [0.90453, -0.66421, -0.19885, -0.00308, 0.31172, -0.19454, 0.58405, 0.93154, -0.48515, 0.56473, -0.32737, 1.4737, 0.10382, 0.36074, -0.16878, 0.06798, -0.13047, -0.11888, -0.14398, 0.20742, -0.22826, 0.30485, 0.088221, -0.42125, 0.39886, 0.030054, -0.84056, -1.1284, 0.82387, -0.67928, -1.0068, 0.86019, -0.72044, -0.43578, -0.42634, 0.78181, -1.2359, -1.2484, 0.19313, -1.0121, -0.41839, -0.88031, 0.010522, 0.73979, 0.26345, 0.90388, 0.53014, -0.84816, -0.21002, -1.0578]
        array_mind = [0.12736, 0.25601, -0.23177, -0.48479, 0.75119, 0.056632, -0.11353, 0.017199, -0.18804, 0.58092, -0.075802, 0.69718, -0.90388, 0.36724, 0.48317, 0.30677, 0.27291, 0.073619, 0.08733, -0.43091, -0.17529, 0.97376, 0.37287, 0.097753, 1.1566, -1.5373, -0.82229, 0.24963, 0.9547, -0.40511, 2.5696, 0.13315, -0.43978, -0.89625, -0.36645, 0.054338, -0.27892, 0.32988, 0.2132, -0.47943, -0.086666, -0.19604, -0.32741, 0.65713, -0.099649, 0.29358, 0.56006, -0.30425, -0.082771, 0.24289]
        expectedArray = np.array([array_exorcise, array_mind],dtype="float32")
        resultArray, expectedSize = w.wordsToGlove(words, gloveDic)
        size = resultArray.shape[1]
        self.assertEquals(resultArray.tolist(), expectedArray.tolist())
        self.assertEquals(resultArray.shape, expectedArray.shape )
        self.assertEquals(expectedSize, size)
        
        
    def test_meanTwoWordsIntoGlove(self):
        """Tests 'words.meanWords'."""
        gloveDic = gloveDict.loadGloveDicFromFile()
        words = ["sugar","daddy"]
        array_sugar = [-1.1832, -0.22543, -0.54312, 0.42731, 0.21005, 0.65685, -0.25581, -0.1135, 0.59814, 0.61958, 0.52322, 0.39701, 1.0169, -0.66816, 0.27134, 0.57248, 0.34042, 0.44322, 0.15522, -1.177, 0.47931, -0.84173, 1.606, -0.13093, -0.91463, -0.37885, 0.29453, 0.35073, 1.3894, 0.49269, 2.427, -0.30031, -0.75508, 1.0198, 0.52147, -0.067951, -0.87317, 0.53923, 1.587, -0.31108, -0.031213, -0.056557, -0.13681, -0.33986, 0.55316, 1.5014, -0.54895, -0.81287, -0.22265, -0.2547]
        array_daddy = [-0.72194, 0.31107, 0.12859, -0.0046166, 0.45015, 0.23396, -0.22262, 0.29077, -0.55985, 0.8146, -0.2496, 1.0958, -0.16488, 0.27881, 0.69166, 0.035146, -0.17416, 0.94723, 0.85716, -0.22603, -0.38178, 0.11424, 0.72613, 0.40135, 0.56518, -0.7427, -1.5062, 0.20571, 0.79272, -1.3691, 0.93696, 0.44818, -0.39311, 1.2478, -0.0095384, 0.083801, 0.21949, -0.68483, 1.0895, -0.456, -0.83926, 0.017797, -1.453, -0.25652, 0.60549, -0.26667, -0.016655, -1.3032, 0.26798, 0.68606] 
        expectedArray = np.array([array_sugar,array_daddy],dtype="float32")
        expectedMean = np.mean(expectedArray, axis=0)
        resultArray, expectedSize = w.wordsToGlove(words, gloveDic)
        resultMean = w.meanWords(resultArray, expectedSize)
        size = resultMean.shape[0]
        self.assertEquals(resultMean.tolist(), expectedMean.tolist()) 
        self.assertEquals(resultArray.shape, expectedArray.shape )
        self.assertEquals(expectedSize, size)
        
    def test_meanThreeWordsWithOnNonIntoGlove(self):
        """Tests 'words.meanWords'."""
        gloveDic = gloveDict.loadGloveDicFromFile()
        words = ["exorcise","myyyyy","mind"]
        array_exorcise = [0.90453, -0.66421, -0.19885, -0.00308, 0.31172, -0.19454, 0.58405, 0.93154, -0.48515, 0.56473, -0.32737, 1.4737, 0.10382, 0.36074, -0.16878, 0.06798, -0.13047, -0.11888, -0.14398, 0.20742, -0.22826, 0.30485, 0.088221, -0.42125, 0.39886, 0.030054, -0.84056, -1.1284, 0.82387, -0.67928, -1.0068, 0.86019, -0.72044, -0.43578, -0.42634, 0.78181, -1.2359, -1.2484, 0.19313, -1.0121, -0.41839, -0.88031, 0.010522, 0.73979, 0.26345, 0.90388, 0.53014, -0.84816, -0.21002, -1.0578]
        array_mind = [0.12736, 0.25601, -0.23177, -0.48479, 0.75119, 0.056632, -0.11353, 0.017199, -0.18804, 0.58092, -0.075802, 0.69718, -0.90388, 0.36724, 0.48317, 0.30677, 0.27291, 0.073619, 0.08733, -0.43091, -0.17529, 0.97376, 0.37287, 0.097753, 1.1566, -1.5373, -0.82229, 0.24963, 0.9547, -0.40511, 2.5696, 0.13315, -0.43978, -0.89625, -0.36645, 0.054338, -0.27892, 0.32988, 0.2132, -0.47943, -0.086666, -0.19604, -0.32741, 0.65713, -0.099649, 0.29358, 0.56006, -0.30425, -0.082771, 0.24289]
        expectedArray = np.array([array_exorcise, array_mind],dtype="float32")
        expectedMean = np.mean(expectedArray, axis=0)
        resultArray, expectedSize = w.wordsToGlove(words, gloveDic)
        resultMean = w.meanWords(resultArray, expectedSize)
        size = resultMean.shape[0]
        self.assertEquals(resultMean.tolist(), expectedMean.tolist())
        self.assertEquals(resultMean.shape, expectedMean.shape )
        self.assertEquals(expectedSize, size)
        
    def test_meanWordIntoGlove(self):
        """Tests 'words.meanWords'."""
        gloveDic = gloveDict.loadGloveDicFromFile()
        word = ["scat"]
        expectedArray = np.array([0.026201, -0.037278, -0.58936, -0.28615, -0.47301, 0.69033, -0.22468, 0.029743, 0.2246, 0.94357,
                      -0.054357, 0.48323, 0.9538, 0.38345, -0.69918, -0.64195, -0.088268, 0.48621, 0.42364, -0.51704,
                      -0.44851, -0.21705, 0.25903, -0.088207, 0.59777, 0.54634, -0.99789, 0.2576, -0.256, -1.7088,
                      0.19006, 0.19731, 0.13614, 1.2829, 0.41883, 0.027112, 0.45165, -0.48737, 0.31797, 0.14142,
                      -0.30245, -0.33968, -0.85194, 0.015752, 0.75979, -1.0888, 0.64471, -0.33908, -0.022592, 0.33961],dtype="float32")
        resultArray, expectedSize = w.wordsToGlove(word, gloveDic)
        resultMean = w.meanWords(resultArray, expectedSize)
        size = resultMean.shape[0]
        self.assertEquals(resultMean.tolist(), expectedArray.tolist())
        self.assertEquals(resultMean.shape, expectedArray.shape )
        self.assertEquals(expectedSize, size)
        
    def test_meanWordNonIntoGlove(self):
        """Tests 'words.wordsToGlove'."""
        gloveDic = gloveDict.loadGloveDicFromFile()
        word = ["bgfierbgkrhqgkdsfgh"]
        resultArray, expectedSize = w.wordsToGlove(word, gloveDic)
        resultMean = w.meanWords(resultArray, expectedSize)
        expectedArray = np.zeros(expectedSize)
        size = resultMean.shape[0]
        self.assertEquals(resultMean.tolist(), expectedArray.tolist())         
        self.assertEquals(resultMean.shape, expectedArray.shape )
        self.assertEquals(expectedSize, size)
        
        
        
if __name__ == '__main__':
    
    unittest.main()        