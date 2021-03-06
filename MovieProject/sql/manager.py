#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Manager to interact with the database

Created on Sun Feb 26 16:23:02 2017
@author: Julian
"""

from models import User, Movie, UserMovie, Occupation, Region
from database import initDb, dbSession as db
from sqlalchemy.orm import join

from exceptions import RuntimeError


class DatabaseManager():
    
    def __init__(self):
        """
            initialize the database, creates tables if not exists
        """
        initDb()
        
    def getAllUsers(self):
        """
            Get all users from database
            
            return:
                list of User objects or None if not exist
        """
        
        return User.query.all()
    
    def getUser(self, username):
        """
            Get user from database by its username
            
            Parameters:
                username -> String, name of user
            return:
                User object or None if not exist
        """
        
        return User.query.filter_by(name=username).first()
        
        
    def insertUser(self, newUser):
        """
            Insert a new user in database, raise a RunTimeError if already exist
            
            Parameters:
                newUser -> User object, new user to be insterted into database 
        """
        
        if self.getUser(newUser.name) is not None: 
            raise RuntimeError("User %s already exist in database" %(newUser.name))
        
        db.add(newUser)
        db.commit()
        
        
    def updateUser(self, updatedUser):
        """
            Update information for user
            
            Parameters:
                updatedUser -> User object created with updated values
        """
        
        user = self.getUser(updatedUser.name)
        
        if user is None:
            raise RuntimeError("User %s is not in the database" %(updatedUser.name))
            
        if updatedUser.password and updatedUser.password != user.password: 
            user.password = updatedUser.password
        if updatedUser.email and updatedUser.email != user.email: 
            user.email = updatedUser.email
        if updatedUser.tmdbKey and updatedUser.tmdbKey != user.tmdbKey: 
            user.tmdbKey = updatedUser.tmdbKey
        if updatedUser.birthday and updatedUser.birthday != user.birthday: 
            user.birthday = updatedUser.birthday
        if updatedUser.sexe and updatedUser.sexe != user.sexe: 
            user.sexe = updatedUser.sexe
        if updatedUser.idCountry and updatedUser.idCountry != user.idCountry:
            user.idCountry = updatedUser.idCountry
        if updatedUser.idOccupation and updatedUser.idOccupation != user.idOccupation:
            user.idOccupation = updatedUser.idOccupation
        
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
        
    def getAllMovies(self):
        """
            Get all movies from database
            
            return:
                list of Movie objects or None if not exist
        """
        
        return Movie.query.all()
        
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
    
    def getAllUsersMovies(self):
        """
            Get all usermovies from database 

            return:
                list of UserMovie objects or None if not exist
        """
        
        return UserMovie.query.all()
 
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
        
    def getIdFromLikedMovies(self, username, isLiked):
        """
            Get all movies liked or not by user
            
            Parameters:
                username -> String, name of user
                isLiked -> Boolean, True to get all movies liked by user, False not liked
                         None for all movies
            return 
                dict with the movie (key) and its like label (value)
        """
        movies = self.getMoviesLikedByUser(username,isLiked)
        return { str(movie.idMovie) : int(movie.liked) for movie in movies}
    
    def getNotRatedMoviesfromUser(self,idU):  
        """
            Get list of movies not rated for an user            
            Parameters:
                idUser -> int, id of user
            return:
                list of idMovies
        """
       
        t = db.query(Movie.idMovie).select_from(join(Movie, UserMovie)).filter(UserMovie.idUser==idU)
        result = Movie.query.filter(~Movie.idMovie.in_(t)).all()    
        listId = []
        for r in result:
            listId.append(r.idMovie)
        return listId
    
    def insertUserMovie(self, username, idMovie, liked):
        """
            Insert a new usermovie in database, raise a RunTimeError if already exist
            
            Parameters:
                username -> String, name of user 
                idMovie -> int, id of movie from TDMB
        """
        if (liked is not bool) and (liked != 0) and (liked != 1):
            raise RuntimeError("Var %s is not a boolean" %(liked)) 
            
        user = self.getUser(username)
        
        if user is None:
            raise RuntimeError("User %s is not in the database" %(username))
            
        if self.getUserMovie(user.id, idMovie):
            raise RuntimeError("UserMovie %s, %s already exist in database" %(user.id, idMovie))
        
        if self.getMovie(idMovie) is None:
            self.insertMovie(idMovie)
        
        usermovie = UserMovie(user.id, idMovie, liked)
        db.add(usermovie)
        db.commit()

    def updateLikedMovieForUser(self, name, idMovie, liked): 
        """ 
            Update on liked movie for a user 
             
            Paramaters: 
                name -> String, name of a user 
                idMovie -> int, movie's id from TMDB 
                liked -> boolean, True if movie is liked, False otherwise 
        """ 
         
        if (liked is not bool) and (liked != 0) and (liked != 1):
            raise RuntimeError("Var liked with value %s is not a boolean" %(liked)) 

        user = self.getUser(name) 
         
        if user is None: 
            raise RuntimeError("User %s is not in the database" %(name)) 
         
        userMovie = self.getUserMovie(user.id, idMovie) 
         
        if not userMovie: 
            self.insertUserMovie(name, idMovie, liked) 
        else: 
            userMovie.liked = liked 
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
    
            
    def removeUserMovieFromUser(self, name, idMovie): 
        """ 
            Delete one usermovie from username and idMovie
            
            Parameters:
                name -> String, name of the user
                idMovie -> int, movie's id from TMDB
        """ 
         
        user = self.getUser(name) 
         
        if user is None: 
            raise RuntimeError("User %s is not in the database" %(name)) 
             
        userMovie = self.getUserMovie(user.id, idMovie) 
         
        if userMovie: 
            db.delete(userMovie) 
            db.commit() 
            
        
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
        
        if (liked is not bool) and (liked != 0) and (liked != 1) and (liked is not None):
            raise RuntimeError("Var %s is not a boolean" %(liked)) 
            
        user = self.getUser(username)
        
        if user is None:
            raise RuntimeError("User %s is not in the database" %(username))
            
        if liked is None:
            return user.movies
        else:
            return [ movie for movie in user.movies if movie.liked == liked ]
        
    def getAllOccupations(self):
        """
            Get all occupations from database 

            return:
                list of Occupation objects or None if not exsist
        """
        
        return Occupation.query.all()
 
    def getOccupation(self, typeOccupation):
        """
            Get occupation from database by its type
            
            Parameters:
                typeOccupation -> String, type of an occupation
            return:
                Occupation object or None if not exist
        """
        
        return Occupation.query.filter_by(type=typeOccupation).first()
        
    
    def insertOccupation(self, newOccupation):
        """
            Insert a new occupation in database, raise a RunTimeError if already exist
            
            Parameters:
                newOccupation -> Occupation object, new occupation to be insterted into database 
        """
        
        if self.getOccupation(newOccupation.type) is not None: 
            raise RuntimeError("Occupation %s already exist in database" %(newOccupation.type))
        
        db.add(newOccupation)
        db.commit()
        
        
    def removeOccupation(self, typeOccupation):
        """
             Remove occupation specified by its id
        """
        
        occupation = self.getOccupation(typeOccupation)
        
        if occupation is None:
            raise RuntimeError("Occupation %d is not present into the database" %(typeOccupation))
            
        db.delete(occupation)
        db.commit()
        
    def getAllRegions(self):
        """
            Get all regions from database
            
            return:
                list of Region objects or None if not exist
        """
        
        return Region.query.all()
    
    def getRegion(self, country):
        """
            Get all regions from database
            
            Parameter:
                country -> String, country name           
            return:
                Region object or None if not exist
        """
        
        return Region.query.filter_by(country=country).first()
        
    
    def insertRegion(self, newRegion):
        """
            Insert a new region in database, raise a RunTimeError if already exist
            
            Parameters:
                newRegion -> Region object, new region to be insterted into database 
        """
        
        if self.getRegion(newRegion.country) is not None: 
            raise RuntimeError("Region %s already exist in database" %(newRegion.country))
        
        db.add(newRegion)
        db.commit()
        
        
        
    def removeRegion(self, country):
        """
             Remove region specified by its id
        """
        
        region = self.getRegion(country)
        
        if region is None:
            raise RuntimeError("Region %d is not present into the database" %(country))
            
        db.delete(region)
        db.commit()
        
    
        
