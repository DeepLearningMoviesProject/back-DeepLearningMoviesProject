#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Script allowed to load abstracts on TMDB and write them in text file

Created on Mon Jan 30 15:08:47 2017
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


tmdb.API_KEY = 'ff3f07bf3577a496a2f813488eb29980'

def loadResumes(filename, pagesMax):
    """
        Load and store abstracts on TMDB, in text file
        
        Parameters:
            filename -> String, name of the file where resumes will be stored
            pagesMax -> int, number of page to download from tmdb
    """
    
    fileAbstracts = codecs.open(filename, "w", 'utf-8')
    
    # Download stopwords if not present
    if not isdir(path[0]):
        from nltk import download
        download("stopwords")
    
    cachedStopWords = stopwords.words("english")
    
    for i in range(1,pagesMax):
        response = discover.movie(page=i)
        filmsNb = len(response[u'results'])
        for j in range (filmsNb):
            abstract = response[u'results'][j][u'overview']
            abstract = texts.preProcessingAbstracts(abstract)
            fileAbstracts.write(abstract+'\n')
        print i
    
    fileAbstracts.close()
    
    
if __name__ == "__main__":
    from MovieProject.resources import RES_PATH
    
    filePath = join(RES_PATH, "train_overviews_treated.txt")

    loadResumes(filePath, 1000)
    

