#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 22:44:09 2017

@author: Julian
"""

from database import db_session, init_db
from models import User, Movie, UserMovie


init_db()

#u = User("Kaito", "test@gmail.com")
#db_session.add(u)
#db_session.commit()

#users = User.query.all()
#
#uKaito = users[0]
#
## update value
#uKaito.name = "Kaito Kuroba"
#
## print new value 
#print db_session.dirty
#
##commit changes
#db_session.commit()



#for m in Movie.query.all():
#    db_session.delete(m)
#db_session.commit()



users = [ User("Kaito", email="test1") ,
          User("Juhn", email="test2")
        ]

movies = [ Movie(11),
           Movie(415)
         ]



for u in users: db_session.add(u)

db_session.commit()
    
for m in movies: db_session.add(m)

db_session.commit()

um = UserMovie(user= User.query.filter_by(name="Kaito").first(),
               movie=Movie.query.filter_by(idMovie=415).first(),
               liked=True)

db_session.add(um)
db_session.commit()

print "Information inserted"
    
