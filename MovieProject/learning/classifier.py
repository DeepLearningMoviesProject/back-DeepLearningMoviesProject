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
from keras.constraints import maxnorm
from MovieProject.preprocessing import preprocess
from sklearn.cross_validation import StratifiedKFold

epoch = 800
batch = 128

def createModel(dataLen = 0, titlesLen = 0, keywordsLen = 0, ratingLen = 0, overviewsLen = 0, genresLen=0, actorsLen=0, directorsLen=0):
    '''
        Creates the model

        Parameters : the length of the matrix we want to fit our model on, at least one must be > 0

        return : The model, ready to be fit
    '''
    
    totalLen = dataLen + titlesLen + keywordsLen + ratingLen + overviewsLen + genresLen + actorsLen + directorsLen

#    dataInputDim = 1000
    dataOutputDim = dataLen
    titlesOutputDim = titlesLen
    keywordsOutputDim = keywordsLen
    ratingOutputDim = ratingLen
    overviewsOutputDim = overviewsLen
    genresOutputDim = genresLen
    actorsOutputDim = actorsLen
    directorsOutputDim = directorsLen
    
    branches = []
    
    if(dataLen > 0):
        dataBranch = Sequential()
#        dataBranch.add(Embedding(dataInputDim, dataOutputDim, input_length=dataLen))
#        dataBranch.add(Flatten())
        dataBranch.add(Dense(dataOutputDim, input_shape =  (dataLen,) , activation = 'relu'))
        dataBranch.add(BatchNormalization())
        branches.append(dataBranch)
        
    if(titlesLen > 0):
        titlesBranch = Sequential()
        titlesBranch.add(Dense(titlesOutputDim, input_shape =  (titlesLen,) , activation = 'relu'))
        titlesBranch.add(BatchNormalization())
        branches.append(titlesBranch)
        
    if(keywordsLen > 0):
        keywordsBranch = Sequential()
        keywordsBranch.add(Dense(keywordsOutputDim, input_shape =  (keywordsLen,) , activation = 'relu'))
        keywordsBranch.add(BatchNormalization())
        branches.append(keywordsBranch)
        
    if(ratingLen > 0):
        ratingBranch = Sequential()
        ratingBranch.add(Dense(ratingOutputDim, input_shape =  (ratingLen,) , activation = 'relu'))
        ratingBranch.add(BatchNormalization())
        branches.append(ratingBranch)
    
    if(overviewsLen > 0):
        overviewsBranch = Sequential()
        overviewsBranch.add(Dense(overviewsOutputDim, input_shape = (overviewsLen,), init='normal', activation='relu'))
        overviewsBranch.add(BatchNormalization())
        branches.append(overviewsBranch)
        
    if(genresLen > 0):
        genresBranch = Sequential()
        genresBranch.add(Dense(genresOutputDim, input_shape = (genresLen,), init='normal', activation='relu'))
        genresBranch.add(BatchNormalization())
        branches.append(genresBranch)
    
    if(actorsLen > 0):
        actorsBranch = Sequential()
        actorsBranch.add(Dense(actorsOutputDim, input_shape =  (actorsLen,) , activation = 'relu'))
        actorsBranch.add(BatchNormalization())
        branches.append(actorsBranch)
    
    if(directorsLen > 0):
        dirBranch = Sequential()
        dirBranch.add(Dense(directorsOutputDim, input_shape =  (directorsLen,) , activation = 'relu'))
        dirBranch.add(BatchNormalization())
        branches.append(dirBranch)

    if(len(branches)==0):
        raise ValueError('The model can\'t be created if there is no matrix !')
    
    #We merge in cascade
    finalBranch = dataBranch
#    finalBranch = _mergeBranches(*branches)
    finalBranch.add(Dense(totalLen, activation = 'relu')) # Done in _mergeBranches
    
    #Here are all of our layers, we can apply our hidden layers
#    finalBranch.add(Dense(totalLen, activation = 'relu'))
    finalBranch.add(Dropout(0.2))
    
    finalBranch.add(Dense(1,  activation = 'sigmoid', W_constraint = maxnorm(3)))
    
    sgd = SGD(lr = 0.1, momentum = 0.9, decay = 0, nesterov = False)
    finalBranch.compile(loss = 'binary_crossentropy', optimizer = sgd, metrics = ['accuracy'])

    return finalBranch

def createTrainTestModel(textTrain, genresTrain, labelsTrain, textTest, genresTest, labelsTest):
    """
        Deprecated - Creates, fits and returns the specific model fitting the entries
        
        Parameters : 
            textTrain, genresTrain : the data to train on, the first one only needs embedding, the other one(s) needs dense layer before merge
            labelsTrain : the labels of the data to train
            textTest, genresTest : data to use for the test of the classifier
            labelsTest : the labels of the data to test
            
        return :
            the model is trained with the parameters
            
    """
    print len(textTrain[0])     #201
    print len(genresTrain[0])   #19
    
    #Create the model
    model = createModel(dataLen = len(textTrain[0]))#, genresLen = len(genresTrain[0]))
    
    #Train model
#    model.fit([textTrain], labelsTrain, batch_size = batch, nb_epoch = epoch, verbose = 1)
    model.fit([textTrain, genresTrain], labelsTrain, batch_size = batch, nb_epoch = epoch, verbose = 1)
#    finalBranch.fit([textEntries, genresEntries, actorsEntries, realEntries], classEntries, batch_size = 2000, nb_epoch = 100, verbose = 1)

    # evaluate the model
#    scores = model.evaluate([textTest, genresTest],labelsTest, verbose=0)
    scores = model.evaluate([textTest],labelsTest, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    return model, scores
    
    
def createTrainModelDico(dico, labels, iTest = [], iTrain = [], doTest=False):
    """
        Creates, fits and returns the specific model fitting the entries
        
        Parameters : 
            dico : a dictionary of the data to train on - np.array
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

    if(doTest):
        labelsTrain = labels[iTrain]
        labelsTest = labels[iTest]
    else:
        labelsTrain = labels

    #Get the data from the dico
    Data = dico.get("data", None)     #Data
    T = dico.get("titles", None)       #title
    K = dico.get("keywords", None)     #keywords
    O = dico.get("overviews", None)    #overviews
    R = dico.get("rating", None)       #rating
    G = dico.get("genres", None)       #Genres
    A = dico.get("actors", None)       #Actors
    D = dico.get("directors", None)    #Directors
    
    dataL = 0
    tL = 0
    kL = 0
    oL = 0
    rL = 0
    gL = 0
    aL = 0
    dL = 0
    
    if Data is not None:
        if(doTest):
            matTrain.append(Data[iTrain])
            matTest.append(Data[iTest])
        else:
            matTrain.append(Data)
        dataL = len(Data[0])
    
    if T is not None:
        if(doTest):
            matTrain.append(T[iTrain])
            matTest.append(T[iTest])
        else:
            matTrain.append(T)
        tL = len(T[0])
        
    if K is not None:
        if(doTest):
            matTrain.append(K[iTrain])
            matTest.append(K[iTest])
        else:
            matTrain.append(K)
        kL = len(K[0])
        
    if R is not None:
        if(doTest):
            matTrain.append(R[iTrain])
            matTest.append(R[iTest])
        else:
            matTrain.append(R)
        rL = len(R[0])
        
    if O is not None:
        if(doTest):
            matTrain.append(O[iTrain])
            matTest.append(O[iTest])
        else:
            matTrain.append(O)
        oL = len(O[0])
    
    if G is not None:
        if(doTest):
            matTrain.append(G[iTrain])
            matTest.append(G[iTest])
        else:
            matTrain.append(G)
        gL = len(G[0])
     
    if A is not None:
        if(doTest):
            matTrain.append(A[iTrain])
            matTest.append(A[iTest])
        else:
            matTrain.append(A)
        aL = len(A[0])
     
    if D is not None:
        if(doTest):
            matTrain.append(D[iTrain])
            matTest.append(D[iTest])
        else:
            matTrain.append(D) 
        dL = len(D[0])

    #Create the model
    model = createModel(dataLen = dataL, titlesLen = tL, keywordsLen = kL, ratingLen = rL, overviewsLen = oL, genresLen = gL, actorsLen = aL, directorsLen = dL)
    
    #Train model
#    model.fit([textTrain], labelsTrain, batch_size = batch, nb_epoch = epoch, verbose = 1)
    model.fit(matTrain, labelsTrain, batch_size = batch, nb_epoch = epoch, verbose = 1)

    # evaluate the model
    scores = None
    if(doTest):
    #    scores = model.evaluate([textTest, genresTest],labelsTest, verbose=0)
        scores = model.evaluate(matTest,labelsTest, verbose=0)
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    return model, scores

def buildModel(dico, labels):
    '''
        Builds the model that matches the movies (ids) and the like/dislike
        
        Parameters : 
            dico : a dict of the matrix we want to build the model on
                "data" : matrix with all the data that will go through the embedding layer
                "genres" : matrix of binary values for each genre
                "actors" : matrix of binary values for each actor
                "directors" : matrix of binary values for each director
            labels : tells whether the movie is liked or not (binary)           
            
        return :
            the model trained on the movies
    '''

    model, _ = createTrainModelDico(dico, labels)
    return model
    
def buildTestModel(dico, labels, folds):
    '''
        Builds the model that matches the matrix contained in dico and the like/dislike
        Tests it with k-cross validation
        T and G matrix must have been preprocessed correctly
        
        Parameters : 
            T, G : the characteristics of the movies we want to build the model on
            labels : tells whether the movie is liked or not (binary)       
            folds :
            
        return :
            the model trained on the movies
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
       # model, scores = createTrainTestModel(T[indices], G[indices], labels[indices], T[tIndice], G[tIndice], labels[tIndice])
        model, scores = createTrainModelDico(dico, labels, iTest, iTrain, doTest=True)
        cvscores.append(scores[1] * 100)

    mean_score = np.mean(cvscores)
    print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
    return model, mean_score


def _mergeBranches(*listBranch):
    '''
        Merge branches of listBranch in cascade (recursively)

        Parameters : a list of the branches we want to merge

        returns : the final branch that results of all the merges
    '''
    
    if(len(listBranch) == 0):
        #TODO : raise an error
        print "You can't merge 0 branches !"
        return None
        
    if(len(listBranch) == 1):
        finalBranch = Sequential()
        finalBranch = listBranch[0]
        return finalBranch
        
    if(len(listBranch) == 2):
        finalBranch = Sequential()
        finalBranch.add(Merge([listBranch[0], listBranch[1]], mode = 'concat'))
        return finalBranch
    
    merge2Branches = Sequential()
    merge2Branches.add(Merge([listBranch[0], listBranch[1]], mode = 'concat'))
    merge2Branches.add(Dense(1,  activation = 'sigmoid'))
    
    return _mergeBranches(merge2Branches, *listBranch[2:])
    