#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:41:13 2017

@author: Julian
"""

import tmdbsimple as tmdb
import numpy as np

from MovieProject.Resources import GENRES_FILE




tmdb.API_KEY = 'ff3f07bf3577a496a2f813488eb29980'

def saveTmdbGenres():
        
    listGenres = tmdb.Genres().list()["genres"]
    genres = {}
    for i in range(len(listGenres)):
        genre = listGenres[i]["name"].lower().encode('UTF-8')
        genres[genre] = i
    
    np.save(GENRES_FILE, np.asarray([genres]))



if __name__ == "__main__":
    saveTmdbGenres()