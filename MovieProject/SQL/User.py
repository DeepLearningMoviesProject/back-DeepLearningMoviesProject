#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 22:18:12 2017

@author: edwin
"""

class User:

    def __init__(self, userId, userName, userMail, tmdbKey, pw ):

        """Constructeur de notre classe"""

        self.userId = userId

        self.userName = userName

        self.userMail = userMail

        self.tmdbKey = tmdbKey
        
        self.pw = pw
        
        
    def getInfo(self):
        return self.userId, self.userName, self.userMail, self.tmdbKey, self.pw