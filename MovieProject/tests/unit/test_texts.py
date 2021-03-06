#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Test for MovieProject/preprocessing/text

Created on Tue Feb  7 10:09 2017
@author: elsa
"""

from MovieProject.preprocessing import texts
import unittest

class TextTest(unittest.TestCase):

    """Test case used to test the module 'preprocessing.text'."""

    def test_withAccents(self):
        """Tests 'text.withoutAccents'."""
        wordInit = "àAâäO0jkfåçsgqéhgèêhëjîjïkôöùkûèoüÿxcğ"
        wordFinal = "aAaaO0jkfacsgqehgeehejijikooukueouyxcg"
        word = texts.withoutAccents(wordInit)
        self.assertEquals(word, wordFinal)
        
    def test_withoutAccents(self):
        """Tests 'text.withoutAccents'."""
        wordInit = "aAaaO0jkfacsgqehgeehejijikooukueouyxcg"
        wordFinal = "aAaaO0jkfacsgqehgeehejijikooukueouyxcg"
        word = texts.withoutAccents(wordInit)
        self.assertEquals(word, wordFinal)
        
    def test_acsii(self):
        """Tests 'text.withoutAccents'."""
        wordInit = u'aefzgrag'.encode("ascii")
        wordFinal = "aefzgrag"
        word = texts.withoutAccents(wordInit)
        self.assertEquals(word, wordFinal)

    def test_unicode(self):
        """Tests 'text.withoutAccents'."""
        wordInit = u'aefzgrag'
        wordFinal = "aefzgrag"
        word = texts.withoutAccents(wordInit)
        self.assertEquals(word, wordFinal)
        
    def test_empty(self):
        """Tests 'text.withoutAccents'."""
        wordInit = ""
        wordFinal = ""
        word = texts.withoutAccents(wordInit)
        self.assertEquals(word, wordFinal)
        
    def test_preProcessingAbstracts(self):
    	"""Tests 'text.preProcessingAbstracts'."""
        abstractInit = "Hello here! J'ai demandé un café noir... C'est pour demain ?"
        abstractFinal = "hello here j'ai demande un cafe noir c'est pour demain "
        abstract = texts.preProcessingAbstracts(abstractInit)
        self.assertEquals(abstract, abstractFinal)

        
if __name__ == '__main__':
    
    unittest.main()    