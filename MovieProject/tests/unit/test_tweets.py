#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 15:08:55 2017

@author: coralie
"""

from MovieProject.preprocessing import tweets
from MovieProject.preprocessing.tools import opinionDict
import unittest

class TweetsTest(unittest.TestCase):
    """Test case used to test the module 'preprocessing.tweets'."""
    
        
    def test_removeMovieTitle(self):
        """Tests 'text.removeMovie'."""
        tweet = "Inception is really a fucking good movie !"
        title = "Inception"
        expectedWord = u" is really a fucking good movie !"
        wordFinal = tweets.removeMovie(tweet, title)
        self.assertEquals(wordFinal, expectedWord)
        
    def test_removeAccentuedMovieTitle(self):
        """Tests 'text.removeMovie'."""
        tweet = "Äcceñtûed is really a fucking good movie !"
        title = "Äcceñtûed"
        expectedWord = u" is really a fucking good movie !"
        wordFinal = tweets.removeMovie(tweet, title)
        self.assertEquals(wordFinal, expectedWord)
        
    def test_removeComposedMovieTitle(self):
        """Tests 'text.removeMovie'."""
        tweet = "Source code is really a fucking good movie !"
        title = "Source code"
        expectedWord = u" is really a fucking good movie !"
        wordFinal = tweets.removeMovie(tweet, title)
        self.assertEquals(wordFinal, expectedWord)
        
    def test_removeEmptyMovieTitle(self):
        """Tests 'text.removeMovie'."""
        tweet = "Inception is really a fucking good movie !"
        title = ""
        expectedWord = u"inception is really a fucking good movie !"
        wordFinal = tweets.removeMovie(tweet, title)
        self.assertEquals(wordFinal, expectedWord)
        
    def test_removeBadMovieTitle(self):
        """Tests 'text.removeMovie'."""
        tweet = "Source Code is really a fucking good movie !"
        title = "Inception"
        expectedWord = u"source code is really a fucking good movie !"
        wordFinal = tweets.removeMovie(tweet, title)
        self.assertEquals(wordFinal, expectedWord)
        
        
    def test_convertUselessWords(self):
        """Tests 'text.preprocessTweet'."""
        dico = opinionDict.loadDicFromFile()
        wordInit = "@good!!!#@ : #good bad www.bad https://sosecure'url good #weird #beautifül @it'sme* * !! ? ,; +:/!\ # @&§!ça)°-_"
        expectedWord = u"good bad good weird beautiful"
        wordFinal = tweets.preprocessTweet(wordInit, dico)
        self.assertEquals(wordFinal, expectedWord)
    
            
    def test_removeRepetitions(self):
        """Tests 'text.removeRepetitions'."""
        dico = opinionDict.loadDicFromFile()
        wordInit = "bàAââääääääääääd gjkfåçsgqéh ğöôd wèêëîïird"
        expectedWord = u"bad good weird"
        wordFinal = tweets.preprocessTweet(wordInit,dico)
        self.assertEquals(wordFinal, expectedWord)
        
    
        
if __name__ == '__main__':
    
    unittest.main() 