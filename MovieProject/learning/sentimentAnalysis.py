#!/usr/bin/env python2 
# -*- coding: utf-8 -*- 
""" 
Script to build sentiment analysis model, thanks to Doc2Vec model,  
train on sentiment tweets or imdb reviews
 
Created on Tue Feb  7 14:09:39 2017 
@author: coralie 
""" 

import numpy 
 
from gensim.models import Doc2Vec 

from keras.models import Sequential 
from keras.layers.core import Dense, Dropout, Activation
from keras.layers import LSTM, Convolution1D, GlobalMaxPooling1D
 
from MovieProject.resources import SENTIMENT_ANALYSIS_MODEL, SENTIMENT_TWITTER_MODEL
 

def preprocessDatasModel(model, trainDatasNb, testDatasNb, dataSize): 
    """
    Preprocesses data of the Doc2Vec model, in order to build a training and testing data set allowed to
    trains and tests the sentiment analysis neural network
        Parameters : 
            - model : the Doc2Vec model trained on corpus of sentiments
            - trainDatasNb : int number of training datas
            - testDatasNb : int number of testing datas
            - dataSize : int number of data dimension
        Return : 
            - a dictionary {label:ndarray}. 
            The label "trainX" is associated with a ndarray of training data
            The label "trainY" is associated with a ndarray of labels associated with training data
            The label "testX" is associated with a ndarray of testing data
            The label "testY" is associated with a ndarray of labels associated with testing data
    """
    trainDataPosNb = trainDatasNb/2; 
    testDataPosNb = testDatasNb/2; 
     
    print "Build training dataset" 
    # BUILD TRAINING DATASET 
     
    train_arrays = numpy.zeros((trainDatasNb, dataSize)) 
    train_labels = numpy.zeros(trainDatasNb) 
     
    for i in range(trainDataPosNb): 
        prefix_train_pos = 'TRAIN_POS_' + str(i) 
        prefix_train_neg = 'TRAIN_NEG_' + str(i) 
        train_arrays[i] = model.docvecs[prefix_train_pos] 
        train_arrays[trainDataPosNb + i] = model.docvecs[prefix_train_neg] 
        train_labels[i] = 1 
        train_labels[trainDataPosNb + i] = 0 
     
 
    # Shuffle data 
    shuffle_indices = numpy.random.permutation(numpy.arange(trainDatasNb)) 
    x_shuffled = train_arrays[shuffle_indices] 
    y_shuffled = train_labels[shuffle_indices] 
    train_arrays = x_shuffled 
    train_labels = y_shuffled 
     
 
    print "Build testing dataset" 
    # BUILD TESTING DATASET 
     
    test_arrays = numpy.zeros((testDatasNb, dataSize)) 
    test_labels = numpy.zeros(testDatasNb) 
     
    for i in range(testDataPosNb): 
        prefix_test_pos = 'TEST_POS_' + str(i) 
        prefix_test_neg = 'TEST_NEG_' + str(i) 
        test_arrays[i] = model.docvecs[prefix_test_pos] 
        test_arrays[testDataPosNb + i] = model.docvecs[prefix_test_neg] 
        test_labels[i] = 1 
        test_labels[testDataPosNb + i] = 0 
     
     
    #dataset = {train_arrays:'TRAIN_ARRAYS', train_labels:'TRAIN_LABELS', test_arrays:'TEST_ARRAYS', test_labels:'TEST_LABELS'}  
    #return dataset 
     
     
    train_arrays = train_arrays.reshape(trainDatasNb, dataSize) 
    test_arrays = test_arrays.reshape(testDatasNb, dataSize) 
    train_arrays = train_arrays.astype('float32') 
    test_arrays = test_arrays.astype('float32') 
     
    return {"trainX":train_arrays, "trainY":train_labels, "testX":test_arrays, "testY":test_labels}

    
def reshapeData3D(trainX, testX):
    """
    Rashape data : 2D -> 3D
        Parameters : 
            - trainX : ndarray of training data
            - testX : ndarray of testing data
        Return : 
            - a dictionary {label:ndarray}. The label "trainX" is associated with a 3D ndarray of training data
            and the label "testX" is associated with a 3D ndarray of testing data
    """
    # reshape input to be [samples, time steps, features]
    train_arrays = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    test_arrays = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
    
    return {"trainX":train_arrays, "testX":test_arrays}

    
def LSTMModelRN(trainX ,trainY, testX, testY):
    """
    Build a LSTM + 2 layer fully connected neural network
    > On IMDB : Dense(50), nb_epoch=3, batch_size=32 : Acc:0.86
    > On Twitter : Dense(50), nb_epoch=10, batch_size=32 : Acc:0.72
        Parameters : 
            - trainX : ndarray of training data
            - trainY : ndarray of labels associated with training data
            - testX : ndarray of testing data
            - testY : ndarray of labels associated with testing data
        Return : 
            - the model trained
    """
    model = Sequential()
    model.add(LSTM(50, input_dim=100))
        
    # We add a vanilla hidden layer:
    model.add(Dense(25))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))
    
    # We project onto a single unit output layer, and squash it with a sigmoid:
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    #model.compile(loss='mean_squared_error', optimizer='adam')
    model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])
    model.fit(trainX, trainY, nb_epoch=3, batch_size=32, verbose=1, validation_data=(testX, testY))   
    
    return model
    
    
def ConvolutionalRN(trainX, trainY, testX, testY) :
    """
    Doesn't work !!! =(
    Build a convolutional1D + 2 layer fully connected neural network
        Parameters : 
            - trainX : ndarray of training data
            - trainY : ndarray of labels associated with training data
            - testX : ndarray of testing data
            - testY : ndarray of labels associated with testing data
        Return : 
            - the model trained
    """
    # set parameters:
    maxlen = 100
    batch_size = 32
    nb_filter = 50
    filter_length = 3
    hidden_dims = 50
    nb_epoch = 2
    
    model = Sequential()
    
    # we start off with an efficient embedding layer which maps
    # our vocab indices into embedding_dims dimensions
    """
    model.add(Embedding(max_features,
                        embedding_dims,
                        input_length=maxlen,
                        dropout=0.2))
    """
    # we add a Convolution1D, which will learn nb_filter
    # word group filters of size filter_length:
    model.add(Convolution1D(nb_filter=nb_filter,
                            filter_length=filter_length,
                            border_mode='valid',
                            activation='relu',
                            input_dim = maxlen,
                            subsample_length=1))
    # we use max pooling:
    model.add(GlobalMaxPooling1D())
    
    # We add a vanilla hidden layer:
    model.add(Dense(hidden_dims))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))
    
    # We project onto a single unit output layer, and squash it with a sigmoid:
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(trainX, trainY, batch_size=batch_size, nb_epoch=nb_epoch, validation_data=(testX, testY))
 
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
    model.add(Dense(output_dim=50, input_dim=100, init='normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(output_dim=10, input_dim=50, init='normal', activation='softmax'))
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=["accuracy"]) 
    model.fit(trainX, trainY, batch_size=32, nb_epoch=4, verbose=1, validation_data=(testX, testY)) 
    
    return model
    
    
def evaluate(model, testX, testY) :
    """ 
    Evaluate model performance
        Parameters :
            - model : the model created by Keras to test
            - testX : ndarray of testing data
            - testY : ndarray of labels associated with testing data
        Return :
            - the model score (loss, accuracy)
            
    """ 
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
   
    
    # Doc2Vec trained on Twitter Corpus
    modelPath = SENTIMENT_ANALYSIS_MODEL
    modelD2V = Doc2Vec.load(SENTIMENT_TWITTER_MODEL) 
    trainDatasNb = 750000 
    testDatasNb = 750000 
    dataSize = 100 
    
    
    """
    # Doc2Vec trained on IMDB Corpus
    modelPath = '../resources/sentimentAnalysisModelIMDB.h5'
    modelD2V = Doc2Vec.load('../resources/sentimentsImdb10EpochSize100.d2v') 
    trainDatasNb = 25000
    testDatasNb = 25000
    dataSize = 100 
    """
    
    data = preprocessDatasModel(modelD2V, trainDatasNb, testDatasNb, dataSize) 
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
    data3D = reshapeData3D(trainX, testX)
    trainX3D = data3D["trainX"]
    testX3D = data3D["testX"]
    model = LSTMModelRN(trainX3D ,trainY, testX3D, testY)
    print(model.summary())
    evaluate(model, testX3D, testY)
    
    
    """
    # Convolutional RN
    print "Test Convolution1D : \n"
    data3D = reshapeData3D(trainX, testX)
    trainX3D = data3D["trainX"]
    testX3D = data3D["testX"]
    model = ConvolutionalRN(trainX3D, trainY, testX3D, testY)
    print(model.summary())
    evaluate(model, testX3D, testY)
    """
    
    model.save(modelPath)  
    
    