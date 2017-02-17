#!/usr/bin/env python2 
# -*- coding: utf-8 -*- 
""" 
Script to build sentiment analysis model, thanks to Doc2Vec model,  
train on sentiment tweets or imdb reviews
 
Created on Tue Feb  7 14:09:39 2017 
@author: coralie 
""" 

from __future__ import unicode_literals 
# Library to write utf-8 text file
import codecs

import numpy 

from keras.models import Sequential 
from keras.layers.core import Dense, Dropout, Activation
from keras.layers import LSTM
 
from MovieProject.resources import TRAIN_TWITTER_NEG_TR_FILE, TRAIN_TWITTER_POS_TR_FILE, TEST_TWITTER_NEG_TR_FILE, TEST_TWITTER_POS_TR_FILE, GLOVE_DICT_FILE, SENTIMENT_ANALYSIS_MODEL
from MovieProject.preprocessing import tweets as tw
from MovieProject.preprocessing.tools import gloveDict


def preprocessDatasModel(): 
    """
    Preprocesses tweets corpus, in order to build a training and testing data set allowed to
    trains and tests the sentiment analysis neural network
        Return : 
            - a dictionary {label:ndarray}: 
            The label "trainX" is associated with a ndarray of training data.
            The label "trainY" is associated with a ndarray of labels associated with training data.
            The label "testX" is associated with a ndarray of testing data.
            The label "testY" is associated with a ndarray of labels associated with testing data.
    """

    fSourceTrainPos = codecs.open(TRAIN_TWITTER_POS_TR_FILE, 'r', 'utf-8')
    linesTrainPos = fSourceTrainPos.readlines()
    trainDataPosNb = len(linesTrainPos) 
    fSourceTrainNeg = codecs.open(TRAIN_TWITTER_NEG_TR_FILE, 'r', 'utf-8')
    linesTrainNeg = fSourceTrainNeg.readlines()
    trainDataNegNb = len(linesTrainNeg) 
    fSourceTestPos = codecs.open(TEST_TWITTER_POS_TR_FILE, 'r', 'utf-8')
    linesTestPos = fSourceTestPos.readlines()
    testDataPosNb = len(linesTestPos)
    fSourceTestNeg = codecs.open(TEST_TWITTER_NEG_TR_FILE, 'r', 'utf-8')
    linesTestNeg = fSourceTestNeg.readlines()
    testDataNegNb = len(linesTestNeg)
           
    dicoGlove = gloveDict.loadGloveDicFromFile(GLOVE_DICT_FILE)
    dataSize=len(tw.tweetToVect('size', dicoGlove))
    
    # BUILD TRAINING DATASET --------------------------------------------------
     
    train_arrays = numpy.zeros((trainDataPosNb+trainDataNegNb, dataSize)) 
    train_labels = numpy.zeros(trainDataPosNb+trainDataNegNb) 
    
    # Fills training matrices with positives data and labels 1
    for i,line in enumerate(linesTrainPos):
        if i%1000 == 0 : 
            print "Build training positive dataset : %d / %d" % (i,trainDataPosNb)
        train_arrays[i] = tw.tweetToVect(line, dicoGlove)
        train_labels[i] = 1 

    # Fills training matrices with negatives data and labels 0
    for i,line in enumerate(linesTrainNeg):
        if i%1000 == 0 :
            print "Build training negative dataset : %d / %d" % (i,trainDataNegNb)
        train_arrays[trainDataPosNb + i] = tw.tweetToVect(line, dicoGlove)
        train_labels[trainDataPosNb + i] = 0 

    # Shuffle data 
    shuffle_indices = numpy.random.permutation(numpy.arange(trainDataPosNb+trainDataNegNb)) 
    x_shuffled = train_arrays[shuffle_indices] 
    y_shuffled = train_labels[shuffle_indices] 
    train_arrays = x_shuffled 
    train_labels = y_shuffled 
     
    # BUILD TESTING DATASET ---------------------------------------------------
     
    test_arrays = numpy.zeros((testDataPosNb+testDataNegNb, dataSize)) 
    test_labels = numpy.zeros(testDataPosNb+testDataNegNb) 
    
    # Fills testing matrices with positives data and labels 1
    for i,line in enumerate(linesTestPos):
        if i%1000 == 0 :
            print "Build testing positive dataset : %d / %d" % (i,testDataPosNb)
        test_arrays[i] = tw.tweetToVect(line, dicoGlove)
        test_labels[i] = 1 

    # Fills testing matrices with negatives data and labels 0
    for i,line in enumerate(linesTestNeg):
        if i%1000 == 0 :
            print "Build testing negative dataset : %d / %d" % (i,testDataNegNb)
        test_arrays[testDataPosNb + i] = tw.tweetToVect(line, dicoGlove)
        test_labels[testDataPosNb + i] = 0 
     
    # Shuffle data 
    shuffle_indices = numpy.random.permutation(numpy.arange(testDataPosNb+testDataNegNb)) 
    x_shuffled = test_arrays[shuffle_indices] 
    y_shuffled = test_labels[shuffle_indices] 
    test_arrays = x_shuffled 
    test_labels = y_shuffled 
    
    # RESHAPE DATASET ---------------------------------------------------------
    
    train_arrays = train_arrays.reshape(trainDataPosNb+trainDataNegNb, dataSize) 
    test_arrays = test_arrays.reshape(testDataPosNb+testDataNegNb, dataSize) 
    train_arrays = train_arrays.astype('float32') 
    test_arrays = test_arrays.astype('float32') 
    
    fSourceTrainPos.close()
    fSourceTrainNeg.close()
    fSourceTestPos.close()
    fSourceTestNeg.close()
    
    return {"trainX":train_arrays, "trainY":train_labels, "testX":test_arrays, "testY":test_labels}


    
def reshapeData3D(data):
    """
    Rashape data : 2D -> 3D
        Parameters : 
            - data : ndarray 2D of training data
        Return : 
            - ndarray 3D of training data
    """
    # reshape input to be [samples, time steps, features]
    dataReshape = numpy.reshape(data, (data.shape[0], 1, data.shape[1]))
    
    return dataReshape

    

def LSTMModelRN(trainX ,trainY, testX, testY):
    """
    Build a LSTM + 2 layer fully connected neural network
    > On IMDB : Dense(50), nb_epoch=3, batch_size=32 : Acc:0.86
    > On Twitter : Dense(50), nb_epoch=10, batch_size=32 : Acc:0.72 -> 0.80
        Parameters : 
            - trainX : ndarray of training data
            - trainY : ndarray of labels associated with training data
            - testX : ndarray of testing data
            - testY : ndarray of labels associated with testing data
        Return : 
            - the model trained
    """
    # Reshape data matrices before LSTM layer
    trainX = reshapeData3D(trainX)
    testX = reshapeData3D(testX)
    
    dataSize = trainX.shape[2]
    
    model = Sequential()
    model.add(LSTM(50, input_dim=dataSize))
        
    # We add a vanilla hidden layer:
    model.add(Dense(25))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))
    
    # We project onto a single unit output layer, and squash it with a sigmoid:
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    #model.compile(loss='mean_squared_error', optimizer='adam')
    model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])
    model.fit(trainX, trainY, nb_epoch=10, batch_size=100, verbose=1, validation_data=(testX, testY))   
    
    return model
    
    
    
def fullyConnectedRN(trainX, trainY) :
    """
    Build a simple 3 layer fully connected neural network
    > On IMDB : Dense(output_dim=50, input_dim=100, init='normal', activation='relu'), Dropout(0.2), Dense(output_dim=10, input_dim=50, init='normal', activation='softmax'), nb_epoch=4, batch_size=32 : Acc:0.86
        Parameters : 
            - trainX : ndarray of training data
            - trainY : ndarray of labels associated with training data
        Return : 
            - the model trained
    """
    model = Sequential() 
    model.add(Dense(output_dim=25, input_dim=50, init='normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(output_dim=10, input_dim=25, init='normal', activation='softmax'))
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=["accuracy"]) 
    model.fit(trainX, trainY, batch_size=32, nb_epoch=4, verbose=1, validation_data=(testX, testY)) 
    
    return model
    
    
    
def evaluateLSTM(model, testX, testY) :
    """ 
    Evaluate model performance
        Parameters :
            - model : the model created by Keras to test
            - testX : ndarray of testing data
            - testY : ndarray of labels associated with testing data
        Return :
            - the model score (loss, accuracy)
            
    """ 
    # Reshape data matrices before LSTM layer
    testX = reshapeData3D(testX)
    
    score = model.evaluate(testX, testY, verbose=0) 
    print('Loss on tests:', score[0]) 
    print('Accuracy on test:', score[1])   
    
    return score
    
    
    
def saveModel(model, filename):
    """
    Save a Keras model into a single HDF5 file which will contain all that we need to re-create this model
        Parameters:
            - model : keras model to store
            - filename : the filename of the HDF5 file (.h5)
    """
    # creates a HDF5 file
    model.save(filename)  
    # deletes the existing model
    del model
    
    
    
if __name__ == "__main__":   
   
    modelPath = SENTIMENT_ANALYSIS_MODEL
    
    data = preprocessDatasModel()
    trainX = data["trainX"]
    trainY = data["trainY"]
    testX = data["testX"]
    testY = data["testY"]
 
    """
    # Simple RN fully connected
    print "Test a simple 3 layer fully connected network : \n"
    model = fullyConnectedRN(trainX,trainY)
    evaluate(model, testX, testY)
    """
    
    # LSTM RN
    print "Test LSTM : \n"
    model = LSTMModelRN(trainX ,trainY, testX, testY)
    print(model.summary())
    evaluateLSTM(model, testX, testY)
    
    model.save(modelPath)  
    
    