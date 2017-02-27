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


OPINION_FILE = join(RES_PATH, "opinionWords.txt")

OPINION_DICT_FILE = join(RES_PATH, "opinionWordsDict.npy")


OVERVIEWS_FILE = join(RES_PATH, "train_overviews.txt")

TRAIN_TWITTER_NEG_FILE = join(RES_PATH, "train_twitter_neg.txt")

TRAIN_TWITTER_POS_FILE = join(RES_PATH, "train_twitter_pos.txt")

TEST_TWITTER_NEG_FILE = join(RES_PATH, "test_twitter_neg.txt")

TEST_TWITTER_POS_FILE = join(RES_PATH, "test_twitter_pos.txt")


OVERVIEWS_TR_FILE = join(RES_PATH, "train_overviews_treated.txt")

TRAIN_TWITTER_NEG_TR_FILE = join(RES_PATH, "train_twitter_neg_tr.txt")

TRAIN_TWITTER_POS_TR_FILE = join(RES_PATH, "train_twitter_pos_tr.txt")

TEST_TWITTER_NEG_TR_FILE = join(RES_PATH, "test_twitter_neg_tr.txt")

TEST_TWITTER_POS_TR_FILE = join(RES_PATH, "test_twitter_pos_tr.txt")


OVERVIEW_MODEL = join(RES_PATH, "overviewModel.d2v")

#SENTIMENT_TWITTER_MODEL = join(RES_PATH, "sentimentTwitterModel.d2v")

SENTIMENT_ANALYSIS_MODEL = join(RES_PATH, "sentimentAnalysisModel.h5")


LABEL_TRAIN_ABTRACTS = 'TRAIN_ABSTRACTS'

LABEL_TEST_NEG = 'TEST_NEG'

LABEL_TEST_POS = 'TEST_POS'

LABEL_TRAIN_NEG = 'TRAIN_NEG'

LABEL_TRAIN_POS = 'TRAIN_POS'



