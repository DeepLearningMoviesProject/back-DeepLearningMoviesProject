#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 11:09:56 2017

@author: Julian
"""

from os.path import dirname, abspath, join

RES_PATH = dirname(abspath(__file__))

GENRES_FILE = join(RES_PATH, "genres.npy")

OPINION_FILE = join(RES_PATH, "opinionWords.txt")

OPINION_DICT_FILE = join(RES_PATH, "opinionWordsDict.npy")

TRAIN_TWITTER_NEG_FILE = join(RES_PATH, "train_twitter_neg.txt")

TRAIN_TWITTER_POS_FILE = join(RES_PATH, "train_twitter_pos.txt")

TEST_TWITTER_NEG_FILE = join(RES_PATH, "test_twitter_neg.txt")

TEST_TWITTER_POS_FILE = join(RES_PATH, "test_twitter_pos.txt")

TRAIN_TWITTER_NEG_TR_FILE = join(RES_PATH, "train_twitter_neg_tr.txt")

TRAIN_TWITTER_POS_TR_FILE = join(RES_PATH, "train_twitter_pos_tr.txt")

TEST_TWITTER_NEG_TR_FILE = join(RES_PATH, "test_twitter_neg_tr.txt")

TEST_TWITTER_POS_TR_FILE = join(RES_PATH, "test_twitter_pos_tr.txt")

