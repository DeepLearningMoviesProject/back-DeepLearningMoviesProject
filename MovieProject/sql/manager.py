#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 16:23:02 2017

@author: Julian
"""

from models import User, Movie, UserMovie
from database import initDb, dbSession as db
from exceptions import RuntimeError


class DatabaseManager():
    
    def __init__(self):
        """
            initialize the database, creates tables if not exists
        """
        initDb()
        
        
    def getUser(self, username):
        """
            Get user from database by its username
            
            Parameters:
                username -> String, name of user
            return:
                User object or None if not exist
        """
        
        return User.query.filter_by(name=username).first()
        
        
    def insertUser(self, name, email="", tmdbKey="", password=""):
        """
            Insert a new user in database, raise a RunTimeError if already exist
            
            Parameters:
                name -> String, name of the user
                email -> String
                tmdbkey -> String, key of TMDB account (length of 32)
                password -> String, hashed password
        """
        
        if self.getUser(name) is not None: 
            raise RuntimeError("User %s already exist in database" %(name))
        
        newUser = User(name, email, tmdbKey, password)
        db.add(newUser)
        db.commit()
        
        
    def updateUser(self, name, email=None, tmdbKey=None, password=None):
        """
            Update information for user specified by its name
            
            Parameters:
                name -> String, name of the user
                email -> String
                tmdbkey -> String, key of TMDB account (length of 32)
                password -> String, hashed password
        """
        
        user = self.getUser(name)
        
        if user is None:
            raise RuntimeError("User %s is not in the database" %(name))
            
        if email is not None: user.email = email
        if tmdbKey is not None: user.tmdbKey = tmdbKey
        if password is not None: user.password = password
        
        db.commit()
        
        
    def removeUser(self, name):
        """
             Remove user specified by its name
        """
        
        user = self.getUser(name)
        
        if user is None:
            raise RuntimeError("User %s is not present into the database")
            
        db.delete(user)
        db.commit()
        
        
    def getMovie(self, idMovie):
        """
            Get movie from database by its id
            
            Parameters:
                idMovie -> int, id of movie from TDMB
            return:
                Movie object or None if not exist
        """
        
        return Movie.query.filter_by(idMovie=idMovie).first()
    
    
    def insertMovie(self, idMovie):
        """
            Insert a new movie in database, raise a RunTimeError if already exist
            
            Parameters:
                idMovie -> int, id of movie from TDMB
        """
        
        if self.getMovie(idMovie) is not None:
            raise RuntimeError("Movie %d already exist in database" %(idMovie))
            
        newMovie = Movie(idMovie)
        db.add(newMovie)
        db.commit()
        
        
    def removeMovie(self, idMovie):
        """
             Remove movie specified by its id
        """
        
        movie = self.getMovie(idMovie)
        
        if movie is None:
            raise RuntimeError("Movie %d is not present into the database" %(idMovie))
            
        db.delete(movie)
        db.commit()
    
    
    def getUserMovie(self, idUser, idMovie):
        """
            Get usermovie from database by its idUser and idMovie
            
            Parameters:
                idUser -> int, id of user
                idMovie -> int, id of movie from TMDB
            return:
                UserMovie object or None if not exist
        """
        
        return UserMovie.query.filter_by(idUser=idUser, idMovie=idMovie).first()
        
        
    
    def insertUserMovie(self, username, idMovie, liked=None):
        """
            Insert a new usermovie in database, raise a RunTimeError if already exist
            
            Parameters:
                username -> String, name of user 
                idMovie -> int, id of movie from TDMB
        """
        
        print username, idMovie, liked
        
        user = self.getUser(username)
        
        if user is None:
            raise RuntimeError("User %s is not in the database" %(username))
            
        if self.getUserMovie(user.id, idMovie):
            raise RuntimeError("UserMovie %s, %s already exist in database" %(user.id, idMovie))
        
        if self.getMovie(idMovie) is None:
            self.insertMovie(idMovie)
        
        print user, self.getMovie(idMovie)
        
        usermovie = UserMovie(user.id, idMovie, liked)
        db.add(usermovie)
        db.commit()
        
    
    def updateLikedMoviesForUser(self, username, likedMovies):
        """
            Update all movies liked by user
            
            Parameters:
                username -> String, name of user
                likedMovies -> dict, {idMovie:True/False}
        """
        
        self.removeAllUserMovieFromUser(username)
        for idMovie, liked in likedMovies.items():
            self.insertUserMovie(username, idMovie, liked)
        
        
    def removeAllUserMovieFromUser(self, username):
        """
            Delete all informations about movies liked by specified user
            
            Parameters:
                username -> String, name of user
        """
        
        user = self.getUser(username)
        
        if user is None:
            raise RuntimeError("User %s is not in the database" %(username))
            
        for usermovie in user.movies:
            db.delete(usermovie)
        db.commit()
        
        
    def getMoviesLikedByUser(self, username, liked=None):
        """
            Get all movies liked or not by user
            
            Parameters:
                username -> String, name of user
                liked -> Boolean, True to get all movies liked by user, False not liked
                         None for all movies
            return 
                array of Movie object 
        """
        
        user = self.getUser(username)
        
        if user is None:
            raise RuntimeError("User %s is not in the database" %(username))
            
        if liked is None:
            return user.movies
        else:
            return [ movie for movie in user.movies if movie.liked == liked ]
