#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:30:10 2017

@author: coralie
"""

# Library to write utf-8 text file
import codecs
# Library to remove all stop words
from nltk.corpus import stopwords
# TMDB simple (TMDB API wrapper)
import tmdbsimple as tmdb
# To pre-process texte in each abtract
from MovieProject.preprocessing import texts

from os.path import isdir, join
from nltk.data import path

from MovieProject.preprocessing import tweets 



tmdb.API_KEY = 'ff3f07bf3577a496a2f813488eb29980'

def loadReviews(idMovie):
    """
        Load and store abstracts on TMDB, in text file
        
        Parameters:
            filename -> String, name of the file where resumes will be stored
            pagesMax -> int, number of page to download from tmdb
    """
    
    movie = getMovie(11)
    reviews = movie.reviews()

    return reviews
    
    
if __name__ == "__main__":
    
    print loadReviews(27205)