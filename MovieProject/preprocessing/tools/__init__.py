#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 11:09:56 2017

@author: Julian
"""

from .gloveDict import *  
from .createCorpusOfAbtracts import * 
from .D2VOnCorpus import * 
from .apiTMDB import * 
 
__all__ = [s for s in dir() if not s.startswith('_')]