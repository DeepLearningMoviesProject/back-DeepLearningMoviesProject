#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 11:09:56 2017

@author: Julian
"""

from os.path import dirname, abspath, join


RES_PATH = dirname(abspath(__file__))

RES_PERSIST_PATH = join(RES_PATH,"persist") 
RES_MODEL_PATH = join(RES_PERSIST_PATH,"model") 
RES_GLOBAL_PATH = join(RES_MODEL_PATH,"global") 
RES_PREDICTIONS_PATH = join(RES_GLOBAL_PATH,"predictions") 


GLOBAL_MODEL_FILE = join(RES_GLOBAL_PATH, "model_weighs.h5")

GENRES_FILE = join(RES_PATH, "genres.npy")

COUNTRIES_FILE = join(RES_PATH, "countries.json")

GLOVE_CORPUS_FILE = join(RES_PERSIST_PATH, "glove.6B.50d.txt")

GLOVE_DICT_FILE = join(RES_PATH, "glove_dict.npy")


OPINION_FILE = join(RES_PERSIST_PATH, "opinionWords.txt")

OPINION_DICT_FILE = join(RES_PATH, "opinionWordsDict.npy")


OVERVIEWS_TR_FILE = join(RES_PERSIST_PATH, "train_overviews_tr.txt")

OVERVIEW_MODEL = join(RES_PERSIST_PATH, "overviewModel.d2v")


TRAIN_TWITTER_NEG_TR_FILE = join(RES_PERSIST_PATH, "train_twitter_neg_tr.txt")

TRAIN_TWITTER_POS_TR_FILE = join(RES_PERSIST_PATH, "train_twitter_pos_tr.txt")

TEST_TWITTER_NEG_TR_FILE = join(RES_PERSIST_PATH, "test_twitter_neg_tr.txt")

TEST_TWITTER_POS_TR_FILE = join(RES_PERSIST_PATH, "test_twitter_pos_tr.txt")

SENTIMENT_ANALYSIS_MODEL = join(RES_PERSIST_PATH, "sentimentAnalysisModel.h5")


LABEL_TRAIN_ABTRACTS = 'TRAIN_ABSTRACTS'

LABEL_TEST_NEG = 'TEST_NEG'

LABEL_TEST_POS = 'TEST_POS'

LABEL_TRAIN_NEG = 'TRAIN_NEG'

LABEL_TRAIN_POS = 'TRAIN_POS'