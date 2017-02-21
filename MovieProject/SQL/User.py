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
    
    def setInfoList(self,l):
        self.userId = int(l[0])

        self.userName = l[1]

        self.userMail = l[2]

        self.tmdbKey = l[3]
        
        self.pw = l[4]
        
    
    def showInfo(self):
        print ('userId: '+ str(self.userId) + ', userName: ' + self.userName + ', userMail: ' 
            + self.userMail + ', tmdbKey: ' + self.tmdbKey +', pw: ' + self.pw)