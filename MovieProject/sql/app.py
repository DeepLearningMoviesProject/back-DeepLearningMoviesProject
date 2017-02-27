#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 22:44:09 2017

@author: Julian
"""

#from database import dbSession, init_db
from models import User, Movie, UserMovie
from manager import DatabaseManager


#init_db()

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



#users = [ User("Kaito", email="test1") ,
#          User("Juhn", email="test2")
#        ]
#
#movies = [ Movie(11),
#           Movie(415)
#         ]
#
#
#try:
#    for u in users: dbSession.add(u)
#    
#    dbSession.commit()
#    print "users inserted"
#except:
#    print "users already inserted"
#    
#try:
#    for m in movies: dbSession.add(m)
#    
#    dbSession.commit()
#    print "movies inserted"
#except:
#    print "movies already inserted"
#
#try:
#    um = UserMovie(User.query.filter_by(name="Kaito").first().id,
#                   Movie.query.filter_by(idMovie=415).first().idMovie,
#                   liked=True)
#
#    dbSession.add(um)
#    dbSession.commit()
#    print "info inserted"
#except:
#    print "info already inserted"
#
#print "Information inserted"


manager = DatabaseManager()

user = User("Kaito", email="test1")

print "Insertion of user %s" %(user)
manager.insertUser(user.name, email=user.email)

print "Getting user %s..." %(user.name),
user = manager.getUser(user.name)
print user

print "Updating user %s with new email..." %(user.name),
manager.updateUser(user.name, email="test@yahoo.fr")

print manager.getUser(user.name).email

  
    
print 
movie = Movie(415)

print "Insertion of movie %s" %(movie)
manager.insertMovie(movie.idMovie)

print "Getting movie %d..." %(movie.idMovie),
movie = manager.getMovie(movie.idMovie)
print movie



um = UserMovie(user.id, movie.idMovie, 1)

print "Insertion of usermovie %s" %(um)
manager.insertUserMovie(user.name, movie.idMovie, 1)

print "Getting movie %d..." %(movie.idMovie),
um = manager.getUserMovie(user.name, movie.idMovie)
print um

print "Updating UserMovie", 
likedMovies = {"415":1,"11":0}
print likedMovies
manager.updateLikedMoviesForUser(user.name, likedMovies)

print "List all UserMovies: ",
print manager.getMoviesLikedByUser(user.name)

print "Movies liked by user %s" %(user.name)
print manager.getMoviesLikedByUser(user.name, True)

print "Movies disliked by user %s" %(user.name)
print manager.getMoviesLikedByUser(user.name, False)


print "Removing usermovies ...",
manager.removeAllUserMovieFromUser(user.name)

if len(manager.getMoviesLikedByUser(user.name)) == 0:
    print "Successfull"
else:
    print "Error"  


print "Removing user %s..." %(user.name),
manager.removeUser(user.name)

if manager.getUser(user.name) is None:
    print "Successfull"
else:
    print "Error"  


print "Removing movies %s..." %(likedMovies.keys()), 
for idMovie in likedMovies:                              
    manager.removeMovie(idMovie)

if manager.getMovie(movie.idMovie) is None:
    print "Successfull"
else:
    print "Error"    
