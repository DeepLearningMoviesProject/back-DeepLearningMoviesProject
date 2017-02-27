#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:41:13 2017

@author: Julian
"""

import tmdbsimple as tmdb
import numpy as np

from os.path import isfile
from MovieProject.resources import GENRES_FILE




tmdb.API_KEY = 'ff3f07bf3577a496a2f813488eb29980'

def saveTmdbGenres():
    """
        Download genres from TMDB and save it into binary file
    """
        
    listGenres = tmdb.Genres().list()["genres"]
    genres = {}
    for i in range(len(listGenres)):
        genre = listGenres[i]["name"].lower().encode('UTF-8')
        genres[genre] = i
    
    np.save(GENRES_FILE, np.asarray([genres]))
    
    
    
def getTmdbGenres():
    """
        Get dictionary of genres from TMDB associated with an index
        
        return:
            dict object {"String":int,...}
    """

    #If the file is not present in the resource, creates it 
    if not isfile(GENRES_FILE):
        saveTmdbGenres()

    return np.load(GENRES_FILE)[0]


if __name__ == "__main__":
    
    print "Creation of the file containing all genres from TMDB"
    saveTmdbGenres()