#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 22:44:09 2017

@author: Julian
"""

from database import dbSession, init_db
from models import User, Movie, UserMovie


init_db()

#u = User("Kaito", "test@gmail.com")
#dbSession.add(u)
#dbSession.commit()

#users = User.query.all()
#
#uKaito = users[0]
#
## update value
#uKaito.name = "Kaito Kuroba"
#
## print new value 
#print dbSession.dirty
#
##commit changes
#dbSession.commit()



#for m in Movie.query.all():
#    dbSession.delete(m)
#dbSession.commit()



users = [ User("Kaito", email="test1") ,
          User("Juhn", email="test2")
        ]

movies = [ Movie(11),
           Movie(415)
         ]


try:
    for u in users: dbSession.add(u)
    
    dbSession.commit()
    print "users inserted"
except:
    print "users already inserted"
    
try:
    for m in movies: dbSession.add(m)
    
    dbSession.commit()
    print "movies inserted"
except:
    print "movies already inserted"

try:
    um = UserMovie(User.query.filter_by(name="Kaito").first().id,
                   Movie.query.filter_by(idMovie=415).first().idMovie,
                   liked=True)

    dbSession.add(um)
    dbSession.commit()
    print "info inserted"
except:
    print "info already inserted"

print "Information inserted"
    
