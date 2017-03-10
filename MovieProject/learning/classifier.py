# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 16:33:30 2017

@author: elsa
"""

#from __future__ import print_function

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Merge, Reshape, BatchNormalization, Embedding, Flatten, Dropout
from keras.optimizers import SGD, Adam
from keras.constraints import maxnorm
from sklearn.cross_validation import StratifiedKFold
from MovieProject.preprocessing.tools import dbPreprocessingTools
from keras.callbacks import Callback, EarlyStopping, ModelCheckpoint
import math

K_FACTORS = 50
RNG_SEED = 1446557
MODEL_WEIGHTS_FILE = 'ml1m_weights.h5'

epoch = 800
batch = 64

class DeepModel(Sequential):

    def __init__(self, n_users, m_items, k_factors, p_dropout=0.2, **kwargs):
        P = Sequential()
        P.add(Embedding(n_users, k_factors, input_length=1))
        P.add(Reshape((k_factors,)))
        Q = Sequential()
        Q.add(Embedding(m_items, k_factors, input_length=1))
        Q.add(Reshape((k_factors,)))
        super(DeepModel, self).__init__(**kwargs)
        self.add(Merge([P, Q], mode='concat'))
        self.add(Dropout(p_dropout))
        self.add(Dense(k_factors, activation='relu'))
        self.add(Dropout(p_dropout))
        self.add(Dense(k_factors/2, activation='relu'))
        self.add(Dropout(p_dropout))
        self.add(Dense(1, activation='sigmoid'))

    def rate(self, user_id, item_id):
        return self.predict([np.array([user_id]), np.array([item_id])])[0][0]
    
def createModelUniq():
    #Récupérer les données depuis la BD
    
    t = dbPreprocessingTools()
    users, movies, ratings = t.preprocessingUserMovies()
    
    	# Créer 3 arrays user, movies, ratings
    
    #	users = np.array([1,1,1,2,2,3,15,15])
    #	movies = np.array([5,6,7,5,8,6,6,7])
    #	ratings = np.array([0,1,1,0,0,1,0,1])
    
    
    max_userid = np.amax(users)
    max_movieid = np.amax(movies)
    print len(ratings), 'ratings loaded.'
    print "max user id :", max_userid
    print "max movie id :", max_movieid
    
    print 'Users:', users, ', shape =', len(users)
    print 'Movies:', movies, ', shape =', len(movies)
    print 'Ratings:', ratings, ', shape =', len(ratings)
    
    	#Faire le modèle
    model = DeepModel(max_userid + 1, max_movieid + 1, K_FACTORS)
    model.compile(loss='mse', optimizer='adamax')
    
    callbacks = [EarlyStopping('val_loss', patience=5), 
    	             ModelCheckpoint(MODEL_WEIGHTS_FILE, save_best_only=True)]
    history = model.fit([users, movies], ratings, nb_epoch=10, validation_split=.1, verbose=2, callbacks=callbacks)
        
    min_val_loss, idx = min((val, idx) for (idx, val) in enumerate(history.history['val_loss']))
    print 'Minimum RMSE at epoch', '{:d}'.format(idx+1), '=', '{:.4f}'.format(math.sqrt(min_val_loss))
    
    return model

def createModel(dataLen = 0):
    '''
        Creates the model

        Parameters : the length of the matrix we want to fit our model on, must be > 0

        return : The model, ready to be fit
    '''
    
    dataOutputDim = dataLen

    if(dataLen==0):
        raise ValueError('The model can\'t be created if there is no matrix !')
    
    finalBranch = Sequential()
    #finalBranch.add(Dropout(0.2, input_shape=(dataLen,)))
    finalBranch.add(Dense(dataOutputDim, input_dim=dataLen, activation = 'relu'))
    finalBranch.add(BatchNormalization())
    
    #TODO : maybe change this dropout
    finalBranch.add(Dropout(0.2))
    finalBranch.add(Dense((dataOutputDim/2),  activation = 'relu', W_constraint = maxnorm(3)))
    # finalBranch.add(Dropout(0.2))
    # finalBranch.add(Dense((dataOutputDim/2),  activation = 'relu', W_constraint = maxnorm(3)))
    finalBranch.add(Dropout(0.2))
    finalBranch.add(Dense(1,  activation = 'sigmoid', W_constraint = maxnorm(3)))
    
    #TODO : Change optimizer
#    sgd = SGD(lr = 0.1, momentum = 0.9, decay = 0, nesterov = False)
    adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    finalBranch.compile(loss = 'binary_crossentropy', optimizer = adam, metrics = ['accuracy'])

    return finalBranch

def createTrainModelDico(mat, labels, iTest = [], iTrain = [], doTest=False):
    """
        Creates, fits and returns the specific model fitting the entries
        
        Parameters : 
            mat : a matrix of the data to train on - np.array
            labels : the labels of the data to train (binary) - np.array
            iTrain : an array of indexes for the training
            iTest : an array of indexes for the tests
            doTest : set to true if you want to test the model
            
        return :
            the model that is trained with the parameters
            
    """
    matTrain = []
    matTest = []

    labelsTrain = []
    labelsTest = []
    
    if mat is None :
        #TODO : raise an exception
        print "there is no data to build the model on !"

    dataLen = len(mat[0])
    
    if (dataLen==0):
        #TODO : raise an exception
        print "the matrix is empty, the model can't be done"

    if(doTest):
        labelsTrain = labels[iTrain]
        labelsTest = labels[iTest]
        matTrain = mat[iTrain]
        matTest = mat[iTest]
    else:
        labelsTrain = labels
        matTrain = mat

    #Create the model
    model = createModel(dataLen = dataLen)
    
    #Train model
    model.fit(matTrain, labelsTrain, batch_size = batch, nb_epoch = epoch, verbose = 1)

    # evaluate the model
    scores = None
    if(doTest):
        scores = model.evaluate(matTest,labelsTest, verbose=0)
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    return model, scores

def buildModel(mat = [], labels = []):
    '''
        Builds the model that matches the movies represented in mat and the labels (like/dislike)
        
        Parameters : 
            mat : contains the characteristics of the movies we want to build the model on
            labels : tells whether the movie is liked or not (binary)           
            
        return :
            the model trained on the movies
    '''

#    model, _ = createTrainModelDico(mat, labels)
    model = createModelUniq()
    return model
    
def buildTestModel(mat, labels, folds):
    '''
        Builds the model that matches the data of movies contained in mat and the like/dislike (labels)
        Tests it with k-cross validation
        mat must have been preprocessed correctly
        
        Parameters : 
            mat : contains the characteristics of the movies we want to build the model on
            labels : tells whether the movie is liked or not (binary)       
            folds : the number of k-cross validation we want to do (no more than the no of labels, 5 to 9 is fine)
            
        return :
            the model trained on the movies, the medium score of the k-cross validation
    '''
    
    cvscores = []
    model = None # Clearing the NN.

    n_folds = folds
    skf = StratifiedKFold(labels, n_folds=n_folds, shuffle=True)

    for i, (train, test) in enumerate(skf):
        print "Running Fold", i+1, "/", n_folds
        # print " train, test : ", train, " ", test
        iTrain = np.array(train)
        iTest = np.array(test)
        model = None # Clearing the NN.
        model, scores = createTrainModelDico(mat, labels, iTest, iTrain, doTest=True)
        cvscores.append(scores[1] * 100)

    mean_score = np.mean(cvscores)
    print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
    return model, mean_score
