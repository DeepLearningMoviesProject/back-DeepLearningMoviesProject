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

from os.path import isdir

tmdb.API_KEY = 'ff3f07bf3577a496a2f813488eb29980'
filePath = "../../resources/train_overviews_treated.txt"
#filePath = "../../resources/train_overviews_noStopWords.txt"


"""
Load and store abstracts on TMDB, in texte file
"""
def loadResumes(fileName, pages_max):
    
    file_abstracts = codecs.open(fileName, "w", 'utf-8')
    
    # Download stopwords if not present
    if not isdir(path[0]):
        from nltk import download
        download("stopwords")
    
    cachedStopWords = stopwords.words("english")
    
    for i in range(1,pages_max):
        response = discover.movie(page=i)
        films_nb = len(response[u'results'])
        for j in range (0,films_nb):
            abstract = response[u'results'][j][u'overview']
            abstract = texts.preProcessingAbstracts(abstract)
            file_abstracts.write(abstract+'\n')
        print i
    
    file_abstracts.close()
    
    
if __name__ == "__main__":
    
    discover = tmdb.Discover()
    response = discover.movie(page=1)
    #pages_nb = int(response[u'total_pages'])
    #print pages_nb   
    
    loadResumes(filePath, 1000)
    

