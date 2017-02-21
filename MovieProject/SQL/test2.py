#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 19:18:34 2017

@author: edwin
"""

from apiSQL import *
import User
#createDB("prout234","sdqsd")
loadDB("prout234","test.sql")

dic5 = {20:1, 10:0, 12:0,15:1,22:1}
u = User.User(2,"jose","manolito","email","pwsd")
insertUser(u)
u = User.User(3,"jose","manolito","emsdfail","pwsd")
insertUser(u)
u = User.User(4,"jose","mandsfolito","email","pwsd")
insertUser(u)
u = User.User(5,"jodse","manolito","email","pwsd")
insertUser(u,dic5)


insertMovies([10,11,12,13,14])


insertUserMovie(1,10,1)
insertUserMovie(1,12,1)
insertUserMovie(1,14,1)
insertUserMovie(1,13,0)
insertUserMovie(2,12,0)

result = getAllUsers()
print "avant"
for u in result:
    u.showInfo()
print "before"

u = User.User(2,"test","nouveauemail","sd","pwsd")
updateUser(u.userId, userTmdbkey= "sdjqsk")
result = getAllUsers()
print "avant"
for u in result:
    u.showInfo()
print "avant"
insertUserMovie(3,12,0)
showAllUsersMovies()
print("AFTER")
removeMovie(12)
showAllUsersMovies()
removeUser(5)
print("AFTER")
showAllUsersMovies()



result = getLikedUsersFromMovie(12,0)
for r in result:
    print(str(r))

