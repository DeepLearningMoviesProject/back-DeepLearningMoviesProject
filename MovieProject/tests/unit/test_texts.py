#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Test for MovieProject/preprocessing/text

Created on Tue Feb  7 10:09 2017
@author: elsa
"""

from MovieProject.preprocessing.texts import *
import unittest

class TextTest(unittest.TestCase):

    """Test case used to test the module 'preprocessing.text'."""

    def test_withoutAccents(self):
        """Tests 'text.withoutAccents'."""
        wordInit = "àAâäO0jkfåçsgqéhgèêhëjîjïkôöùkûèoüÿxcğ"
        wordFinal = "aAaaO0jkfacsgqehgeehejijikooukueouyxcg"
        word = withoutAccents(wordInit)
        self.assertEquals(word, wordFinal)

    def test_preProcessingAbstracts(self):
    	"""Tests 'text.preProcessingAbstracts'."""
        abstractInit = "Hello here! J'ai demandé un café noir... C'est pour demain ?"
        abstractFinal = "hello here j'ai demande un cafe noir c'est pour demain "
        abstract = preProcessingAbstracts(abstractInit)
        self.assertEquals(abstract, abstractFinal)

