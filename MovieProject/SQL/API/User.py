#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 22:18:12 2017

@author: edwin
"""

"""
    This class is made for saving user informations
"""
class User:

    
    def __init__(self, userId, userName, userMail, userTmdbKey, userPassword):
        """
            User init
        """

        self.userId = userId

        self.userName = userName

        self.userMail = userMail

        self.userTmdbKey = userTmdbKey
        
        self.userPassword = userPassword
        
        
    def getInfos(self):
        """
            Return user informations
        """
        
        return self.userId, self.userName, self.userMail, self.userTmdbKey, self.userPassword
    
    def setInfoList(self,l):
        """
            Update user informations
            Parameter:
                l -> List ordered as: userId, userName, userMail, userTmdbKey, userPassword
        """
        
        self.userId = int(l[0])

        self.userName = l[1]

        self.userMail = l[2]

        self.userTmdbKey = l[3]
        
        self.userPassword = l[4]
        
    
    def showInfos(self):
        """
            Print user informations
        """
        
        print ('userId: "'+ str(self.userId) + '", userName: "' + self.userName + '", userMail: "' 
            + self.userMail + '", tmdbKey: "' + self.userTmdbKey +'", pw: "' + self.userPassword + '"')