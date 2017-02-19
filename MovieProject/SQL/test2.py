#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 19:18:34 2017

@author: edwin
"""

from apiSQL import *
import User
#createDB("prout234","sdqsd")
loadDB("prout234","lol.sql")

u = User.User(2,"jose","manolito","email","pwsd")
createUser(u)
showAllUsers()
