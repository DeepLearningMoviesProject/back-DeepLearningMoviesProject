#!/usr/bin/env python2 
# -*- coding: utf-8 -*- 
""" 
Script to build sentiment analysis model, thanks to Doc2Vec model,  
train on sentiment tweets 
 
Created on Tue Feb  7 14:09:39 2017 
@author: coralie 
""" 
 
from gensim.models import Doc2Vec 
import numpy 
 
from sklearn.linear_model import LogisticRegression 
 
from keras.datasets import mnist 
from keras.models import Sequential 
from keras.layers.core import Dense, Dropout, Activation 
from keras.utils import np_utils 
 
 
def trainModel(model, trainDatasNb, testDatasNb, dataSize): 
     
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
     
    print "begin training ..." 
 
     
     
    """ 
    Build the neural network : 
        a simple 3 layer fully connected network 
    """ 
     
    model = Sequential() 
     
    model.add(Dense(output_dim=200, input_dim=100, init='normal', activation='relu')) 
    model.add(Dense(output_dim=100, input_dim=200, init='normal', activation='relu')) 
    model.add(Dense(output_dim=10, input_dim=100, init='normal', activation='softmax')) 
     
    """ 
    model.add(Dense(512, input_shape=(100,))) 
     
    # An "activation" is just a non-linear function applied to the output of the layer above.  
    # Here, with a "rectified linear unit", we clamp all values below 0 to 0. 
    model.add(Activation('relu'))  
    # Dropout helps protect the model from memorizing or "overfitting" the training data                            
    model.add(Dropout(0.2))    
    model.add(Dense(512)) 
    model.add(Activation('relu')) 
    model.add(Dropout(0.2)) 
    model.add(Dense(10)) 
    # This special "softmax" activation among other things, ensures the output is  
    # a valid probaility distribution, that its values are all non-negative and sum to 1. 
    model.add(Activation('softmax'))  
    """ 
 
     
    """ 
    Compile the model 
    """ 
     
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=["accuracy"]) 
     
     
    """ 
    Train the model 
    """ 
     
    model.fit(train_arrays, train_labels, batch_size=1000, nb_epoch=50, show_accuracy=True, verbose=1, validation_data=(test_arrays, test_labels)) 
     
     
    """ 
    Evaluate its performance 
    """ 
     
    score = model.evaluate(test_arrays, test_labels, verbose=0) 
    print('Loss on tests:', score[0]) 
    print('Accuracy on test:', score[1]) 
     
     
    """ 
    classifier = LogisticRegression() 
    classifier.fit(train_arrays, train_labels) 
     
    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,intercept_scaling=1, penalty='l2', random_state=None, tol=0.0001) 
     
    score = classifier.score(test_arrays, test_labels) 
     
    print(score) 
    """ 
 
     
if __name__ == "__main__":   
 
    model = Doc2Vec.load('../resources/sentimentsv210EpochSize100.d2v') 
    trainDatasNb = 750000 
    testDatasNb = 750000 
    dataSize = 100 
     
    trainModel(model, trainDatasNb, testDatasNb, dataSize) 