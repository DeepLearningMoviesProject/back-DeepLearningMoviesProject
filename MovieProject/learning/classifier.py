# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 16:33:30 2017

@author: elsa
"""

#from __future__ import print_function

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Merge, BatchNormalization, Embedding, Flatten, Dropout
from keras.optimizers import SGD
from MovieProject.preprocessing import preprocess
from sklearn.cross_validation import StratifiedKFold

def createModel(textLen, genresLen):
    
    totalLen = textLen + genresLen

    textInputDim = 1000
    textOutputDim = 64
    genresOutputDim = genresLen
    
    textBranch = Sequential()
    textBranch.add(Embedding(textInputDim, textOutputDim, input_length=textLen))
    textBranch.add(Flatten())
    
    genresBranch = Sequential()
    genresBranch.add(Dense(genresOutputDim, input_shape = (genresLen,), init='normal', activation='relu'))
    genresBranch.add(BatchNormalization())
    
#    actorsBranch = Sequential()
#    actorsBranch.add(Dense(10, input_shape =  (3,) , activation = 'relu'))
#    actorsBranch.add(BatchNormalization())
    
#    realBranch = Sequential()
#    realBranch.add(Dense(10, input_shape =  (4,) , activation = 'relu'))
#    realBranch.add(BatchNormalization())
    
    #We merge in cascade
    
#    merge1Branch = Sequential()
#    merge1Branch.add(Merge([genresBranch, actorsBranch], mode = 'concat'))
#    merge1Branch.add(Dense(1,  activation = 'sigmoid'))
    
#    merge2Branch = Sequential()
#    merge2Branch.add(Merge([realBranch, merge1Branch], mode = 'concat'))
#    merge2Branch.add(Dense(1,  activation = 'sigmoid'))  

    finalBranch = Sequential()
    finalBranch.add(Merge([textBranch, genresBranch], mode = 'concat'))
    
    #Here are all of our layers, the preprocessing is over
    finalBranch.add(Dense(totalLen, activation = 'relu'))
    finalBranch.add(Dropout(0.2))
    tempLen = totalLen/2    #85 si glove    #160 si d2v
    finalBranch.add(Dense(tempLen, activation = 'relu'))
    tempLen = tempLen/2     #42 si glove    #80 si d2v
    finalBranch.add(Dense(tempLen, activation = 'relu'))
    tempLen = tempLen/2     #21 si glove    #40 si d2v
    finalBranch.add(Dense(tempLen, activation = 'relu'))
    tempLen = tempLen/2     #10 si glove    #20 si d2v
    finalBranch.add(Dense(tempLen, activation='relu'))
    tempLen = tempLen/2     #5 si glove    #10 si d2v
    finalBranch.add(Dense(tempLen, activation='relu'))
    tempLen = tempLen/2     #2 si glove    #5 si d2v
    finalBranch.add(Dense(tempLen, activation='relu'))
    finalBranch.add(Dense(1,  activation = 'sigmoid'))
    
    sgd = SGD(lr = 0.1, momentum = 0.9, decay = 0, nesterov = False)
    finalBranch.compile(loss = 'binary_crossentropy', optimizer = sgd, metrics = ['accuracy'])

    return finalBranch

def createTrainTestModel(textTrain, genresTrain, labelsTrain, textTest, genresTest, labelsTest):
    """
        Creates, fits and returns the specific model fitting the entries
        
        Parameters : 
            textTrain, genresTrain : the data to train on, the first one only needs embedding, the other one(s) needs dense layer before merge
            labelsTrain : the labels of the data to train
            textTest, genresTest : data to use for the test of the classifier
            labelsTest : the labels of the data to test
            
        return :
            the model is trained with the parameters
            
    """

    #Create the model
    model = createModel(len(textTrain[0]), len(genresTrain[0]))

    epoch = 5000
    batch = 500

    #Train model
    model.fit([textTrain, genresTrain], labelsTrain, batch_size = batch, nb_epoch = epoch, verbose = 1)
#    finalBranch.fit([textEntries, genresEntries, actorsEntries, realEntries], classEntries, batch_size = 2000, nb_epoch = 100, verbose = 1)

    # evaluate the model
    scores = model.evaluate([textTest, genresTest],labelsTest, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    return model, scores


def createTrainModel(textTrain, genresTrain, labelsTrain, textTest, genresTest, labelsTest):
    """
        Creates, fits and returns the specific model fitting the entries
        
        Parameters : 
            textTrain, genresTrain : the data to train on, the first one only needs embedding, the other one(s) needs dense layer before merge
            labelsTrain : the labels of the data to train
            textTest, genresTest : data to use for the test of the classifier
            labelsTest : the labels of the data to test
            
        return :
            the model is trained with the parameters
            
    """

    #Create the model
    model = createModel(len(textTrain[0]), len(genresTrain[0]))

    epoch = 5000
    batch = 500

    #Train model
    model.fit([textTrain, genresTrain], labelsTrain, validation_data=([textTest, genresTest],labelsTest), batch_size = batch, nb_epoch = epoch, verbose = 1)
#    model.fit([textEntries, genresEntries, actorsEntries, realEntries], classEntries, batch_size = 2000, nb_epoch = 100, verbose = 1)

    return model


def buildModel(ids, labels):
    '''
        Builds the model that matches the movies (ids) and the like/dislike
        
        Parameters : 
            ids : the ids of the movies we want to build the model on
            labels : tells whether the movie is liked or not (binary)           
            
        return :
            the model trained on the movies
    '''
    
    T, G = preprocess(ids)

    model = createTrainModel(T, G, labels, T, G, labels)




def buildTestModel(T, G, labels):
    '''
        Builds the model that matches the movies (ids) and the like/dislike
        Tests it with k-cross validation
        
        Parameters : 
            ids : the ids of the movies we want to build the model on
            labels : tells whether the movie is liked or not (binary)           
            
        return :
            the model trained on the movies
    '''
    
   # T, G = preprocess(ids)
    cvscores = []

    n_folds = 2
    skf = StratifiedKFold(labels, n_folds=n_folds, shuffle=True)

    for i, (train, test) in enumerate(skf):
        print "Running Fold", i+1, "/", n_folds
        print " train, test : ", train, " ", test
        indices = np.array(train)
        tIndice = np.array(test)
        model = None # Clearing the NN.
        model, scores = createTrainTestModel(T[indices], G[indices], labels[indices], T[tIndice], G[tIndice], labels[tIndice])
        cvscores.append(scores[1] * 100)

    print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
