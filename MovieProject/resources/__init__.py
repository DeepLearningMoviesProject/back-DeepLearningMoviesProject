#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 11:09:56 2017

@author: Julian
"""

from os.path import dirname, abspath, join

RES_PATH = dirname(abspath(__file__))

GENRES_FILE = join(RES_PATH, "genres.npy")

GLOVE_CORPUS_FILE = join(RES_PATH, "glove.6B.50d.txt")
GLOVE_DICT_FILE = join(RES_PATH, "glove_dict.npy")

D2V_FILE = join(RES_PATH, "abstracts20EpochSize100.d2v")
