#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Script allowed to load abstracts on TMDB and write them in text file

Created on Mon Jan 30 15:08:47 2017
@author: coralie

"""

# Library to write utf-8 text file
import codecs

# TMDB simple (TMDB API wrapper)
import tmdbsimple as tmdb

# To pre-process texte in each abtract
from MovieProject.preprocessing import texts
from MovieProject.resources import OVERVIEWS_TR_FILE
#from nltk.corpus import stopwords # Library to remove all stop words

from os.path import isdir
from nltk.data import path



tmdb.API_KEY = 'ff3f07bf3577a496a2f813488eb29980'

def createCorpus(filename, pagesMax=1000):
    """
        Load and store abstracts on TMDB, in text file
        
        Parameters:
            filename -> String, name of the file where resumes will be stored
            pagesMax -> int, number of page to download from tmdb (default: pagesMax=1000)
    """
    
    fileAbstracts = codecs.open(filename, "w", 'utf-8')
    
    # Download stopwords if not present
    if not isdir(path[0]):
        from nltk import download
        download("stopwords")
    
#    cachedStopWords = stopwords.words("english")
    
    for i in range(1,pagesMax):
#        response = tmdb.discover.movie(page=i)
        response = tmdb.Discover().movie(page=i)
        filmsNb = len(response[u'results'])
        for j in range (filmsNb):
            abstract = response[u'results'][j][u'overview']
            abstract = texts.preProcessingAbstracts(abstract)
            fileAbstracts.write(abstract+'\n')
        print "Creation of abstracts corpus : page %d / %d" % (i,pagesMax)
    
    fileAbstracts.close()
    
    
if __name__ == "__main__":

    createCorpus(OVERVIEWS_TR_FILE)