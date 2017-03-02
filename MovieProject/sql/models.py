#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 22:44:09 2017

@author: Julian
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, name="id", primary_key=True, nullable=False)
    name = Column(String(64), unique=True, nullable=False)
    email = Column(String(128), unique=False, nullable=False)
    tmdbKey = Column(String(32), unique=False, nullable=True)
    password = Column(String(128), unique=False, nullable=False)
    birthday = Column(Date, nullable=True)
    sexe = Column(Boolean, nullable=True)
    idCountry = Column(Integer, ForeignKey('region.id'))
    idOccupation = Column(Integer, ForeignKey('occupation.id'))
    
    movies = relationship("UserMovie", back_populates="user", cascade="save-update, merge, delete")
    
    def __init__(self, name, password, email, tmdbKey=None, birthday=None, sexe=None, idCountry=None, idOccupation=None):
        self.name = name
        self.email = email
        self.tmdbKey = tmdbKey
        self.password = password
        self.birthday = birthday
        self.sexe = sexe
        self.idCountry = idCountry
        self.idOccupation = idOccupation

    def __repr__(self):
        return '<User %r>' % (self.name)
    
    
class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, name="id", primary_key=True, nullable=False)
    idMovie = Column(Integer, unique=True, nullable=False)
    users = relationship("UserMovie", back_populates="movie", cascade="save-update, merge, delete")
    
    def __init__(self, idMovie):
        self.idMovie = idMovie

    def __repr__(self):
        return '<Movie %d>' % (self.idMovie)
    
class UserMovie(Base):
    __tablename__ = 'usermovie'
    idUser = Column(Integer, ForeignKey('user.id'), primary_key=True)
    idMovie = Column(Integer, ForeignKey('movie.idMovie'), primary_key=True)
    liked = Column(Boolean, default=None)
    
    movie = relationship("Movie", back_populates="users")
    user = relationship("User", back_populates="movies")

    def __init__(self, idUser, idMovie, liked=None):
        self.idUser = idUser
        self.idMovie = idMovie
        self.liked = liked
        
    def __repr__(self):
        return "<UserMovie %d %d %s>" %(self.idUser, self.idMovie, self.liked)
        
        
class Occupation(Base):
    __tablename__ = "occupation"
    id = Column(Integer, name="id", primary_key=True, nullable=False)
    type = Column(String(64), unique=True, nullable=True)
    users =  relationship("User")
    
    def __init__(self, type):
        self.type = type
        

class Region(Base):
    __tablename__ = "region"
    id = Column(Integer, name="id", primary_key=True, nullable=False)
    country = Column(String(64), unique=True, nullable=True)
    users =  relationship("User")
    
    def __init__(self, country):
        self.country = country
        
        
        
        
        