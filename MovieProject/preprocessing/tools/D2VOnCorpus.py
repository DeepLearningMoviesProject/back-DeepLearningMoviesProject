#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
-- Script allowed to train the Doc2Vec model on data base --

To train it, we use documents, each one taking up one entire line. So, each document should be on one line, separated by new lines.

The input to Doc2Vec need to be an iterator of LabeledSentence objects. Each such object consists of a list of words and a list of labels. 
The algorithm then runs through the sentences iterator twice: once to build the vocab, and once to train the model on the input data, 
learning a vector representation for each word and for each label in the dataset.

Created on Mon Jan 30
@author: coralie

"""

# gensim
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec

# numpy
import numpy

from MovieProject.resources import TRAIN_TWITTER_NEG_TR_FILE, TRAIN_TWITTER_POS_TR_FILE, TEST_TWITTER_NEG_TR_FILE, TEST_TWITTER_POS_TR_FILE, SENTIMENT_TWITTER_MODEL, LABEL_TEST_NEG, LABEL_TEST_POS, LABEL_TRAIN_NEG, LABEL_TRAIN_POS
#from MovieProject.resources import OVERVIEW_MODEL, LABEL_TRAIN_ABTRACTS, OVERVIEWS_TR_FILE



class LabeledLineSentence(object):
    
    def __init__(self,sources):
        """
        Constructor of LabeledLineSentence
        """
        # take a dictionary of many text file as parameter (insteed of a single text file. 
        # the dictionary defines the files to read and the label prefixes sentences from that document should take on
        self.sources = sources
        dictionary = {}
        # make sure that keys (label prefixes sentences) are unique for each text file
        for key, value in sources.items():
            if value not in dictionary:
                dictionary[value] = [key]
            else:
                raise Exception('Error encountered : make sure that key(prefix) are unique for each text file.')

    def __iter__(self):
        """
        Iterator of LabeledLineSentence
        """
        # each document should be on one line, separated by new lines
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])

    def to_array(self): 
        """
        Create an array of LabeledLineSentence : the method "build_vocab(self)" 
        takes an array of LabeledLineSentence
        
        Return : an array of LabeledLineSentence
        """
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as txtFile:
                for item_no, line in enumerate(txtFile):
                    self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        """ 
        Randomize the sequence of sentences : the model is better trained if in each 
        training epoch, the sequence of sentences fed to the model is randomized
        
        Return : a random suffle of sequence into a numpy array
        """
        numpy.random.shuffle(self.sentences)
        return self.sentences

        


def _buildModel(sources, modelPath) :
    """
    Build the model and store it
        Parameters :
            - sources : dictionnary of sources with files path and labels associated at each file
            - modelPath : path to store the model built
    """
    
    sentences = LabeledLineSentence(sources)
    
    # min_count: ignore all words with total frequency lower than this. We have to set this to 1, since the sentence labels only appear once.
    # window: the maximum distance between the current and predicted word within a sentence. Word2Vec uses a skip-gram model, and this is simply the window size of the skip-gram model.
    # size: dimensionality of the feature vectors in output. 100 is a good number. If you're extreme, you can go up to around 400.
    # sample: threshold for configuring which higher-frequency words are randomly downsampled
    # workers: use this many worker threads to train the model
    # DBOW mode (dm=0) is faster and creates better vectors for many purposes/datasets ?!? <- Bad idea !
    model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=7, alpha=0.025, min_alpha=0.025)
    
    model.build_vocab(sentences.to_array())
    
    i=0
    for epoch in range(10):
        print(i)
        model.train(sentences.sentences_perm())
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha  # fix the learning rate, no decay
        i = i+1
        
    model.save(modelPath) # storing the model to mmap-able files

    

def loadD2VModel(modelPath):
    """
    Load a preexisting Doc2Vec model
        Parameter:
            - modelPath : model file path to load 
        Return:
            - Doc2Vec model object
    """
    return Doc2Vec.load(modelPath)
    
    
    
if __name__ == "__main__":    
    
    # To train on sentiments database (Tweets)
    print "Training on sentiment tweet database :"
    sources = {TEST_TWITTER_NEG_TR_FILE:LABEL_TEST_NEG, TEST_TWITTER_POS_TR_FILE:LABEL_TEST_POS, TRAIN_TWITTER_NEG_TR_FILE:LABEL_TRAIN_NEG, TRAIN_TWITTER_POS_TR_FILE:LABEL_TRAIN_POS}
    modelPath = SENTIMENT_TWITTER_MODEL    

    """
    #print "Training on sentiment review database :"
    #sources = {'../../resources/train_imdb_neg.txt':'TRAIN_NEG', '../../resources/train_imdb_pos.txt':'TRAIN_POS'}
    #sources = {'../../resources/test-neg.txt':'TEST_NEG', '../../resources/test-pos.txt':'TEST_POS', '../../resources/train-neg.txt':'TRAIN_NEG', '../../resources/train-pos.txt':'TRAIN_POS', '../../resources/train-unsup.txt':'TRAIN_UNS'}
    #modelPath = '../../resources/sentimentsImdb10EpochSize100.d2v'
    """
    
    """
    print "Training on abstracts database :"
    sources = {OVERVIEWS_TR_FILE:'TRAIN_ABSTRACTS'}
    modelPath = OVERVIEW_MODEL
    """
    
    _buildModel(sources, modelPath)
    

            