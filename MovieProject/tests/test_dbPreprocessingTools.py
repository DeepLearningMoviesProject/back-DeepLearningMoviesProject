#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 15:43:32 2017

@author: edwin
"""

from MovieProject.preprocessing.tools import dbPreprocessingTools
from MovieProject.sql import *

manager = DatabaseManager()
user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
manager.insertUser(user)
manager.updateLikedMoviesForUser(user.name, {"11":1,"12":0, "18":1}) 
user = manager.getUser(user.name)
l = manager.getNotRatedMoviesfromUser(user.id) 
print(len(l))

t = dbPreprocessingTools()
u,m,r = t.preprocessingUserMovies()

#for e1, e2, e3 in zip(u,m,r):
    #print(e1,e2,e3)
    
manager.removeUser(user.name)
