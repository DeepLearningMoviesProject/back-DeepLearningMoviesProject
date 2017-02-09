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

epoch = 1000
batch = 128

def createModel(dataLen=0, genresLen=0, actorsLen=0, directorsLen=0):
    
    totalLen = dataLen + genresLen + actorsLen + directorsLen

    dataInputDim = 1000
    dataOutputDim = 64
    genresOutputDim = genresLen
    actorsOutputDim = actorsLen
    directorsOutputDim = directorsLen
    
    branches = []
    
    if(dataLen > 0):
        dataBranch = Sequential()
        dataBranch.add(Embedding(dataInputDim, dataOutputDim, input_length=dataLen))
        dataBranch.add(Flatten())
        branches.append(dataBranch)
    
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
    finalBranch = mergeBranches(*branches)
    finalBranch.add(Dense(totalLen, activation = 'relu'))
    finalBranch.add(Dropout(0.2, input_shape = (totalLen,)))
    
    #Here are all of our layers, we can apply our hidden layers
#    finalBranch.add(Dense(totalLen, activation = 'relu'))
    finalBranch.add(Dropout(0.2))
    
    finalBranch.add(Dense(1,  activation = 'sigmoid', W_constraint = maxnorm(3)))
    
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
            textTrain, genresTrain : the data to train on, the first one only needs embedding, the other one(s) needs dense layer before merge
            labelsTrain : the labels of the data to train
            textTest, genresTest : data to use for the test of the classifier
            labelsTest : the labels of the data to test
            
        return :
            the model is trained with the parameters
            
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
    Data = dico.get("data", None)      #Data
    G = dico.get("genres", None)       #Genres
    A = dico.get("actors", None)       #Actors
    D = dico.get("directors", None)    #Directors
    dataL = 0
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
    model = createModel(dataLen = dataL, genresLen = gL, actorsLen = aL, directorsLen = dL)
    
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

# def createTrainModel(textTrain, genresTrain, labelsTrain):
#     """
#         Creates, fits and returns the specific model fitting the entries
        
#         Parameters : 
#             textTrain, genresTrain : the data to train on, the first one only needs embedding, the other one(s) needs dense layer before merge
#             labelsTrain : the labels of the data to train
#             textTest, genresTest : data to use for the test of the classifier
#             labelsTest : the labels of the data to test
            
#         return :
#             the model is trained with the parameters
            
#     """

#     #Create the model
#     model = createModel(len(textTrain[0]), len(genresTrain[0]))

#     #Train model
#     model.fit([textTrain, genresTrain], labelsTrain, batch_size = batch, nb_epoch = epoch, verbose = 1)
# #    model.fit([textEntries, genresEntries, actorsEntries, realEntries], classEntries, batch_size = 2000, nb_epoch = 100, verbose = 1)

#     return model


def buildModel(dico, labels):
    '''
        Builds the model that matches the movies (ids) and the like/dislike
        
        Parameters : 
            ids : the ids of the movies we want to build the model on
            labels : tells whether the movie is liked or not (binary)           
            
        return :
            the model trained on the movies
    '''

    model, _ = createTrainModelDico(dico, labels)
    return model


# def buildTestModel(T, G, labels, folds):
#     '''
#         Builds the model that matches the matrix T and G and the like/dislike
#         Tests it with k-cross validation
#         T and G matrix must have been preprocessed correctly
        
#         Parameters : 
#             T, G : the characteristics of the movies we want to build the model on
#             labels : tells whether the movie is liked or not (binary)           
            
#         return :
#             the model trained on the movies
#     '''
    
#     cvscores = []
#     model = None # Clearing the NN.
#     d = {
#         'data': T,
#         'genres': G,
# #        'actors': 'value',
# #        'directors': 'value',
#     }

#     n_folds = folds
#     skf = StratifiedKFold(labels, n_folds=n_folds, shuffle=True)

#     for i, (train, test) in enumerate(skf):
#         print "Running Fold", i+1, "/", n_folds
#         # print " train, test : ", train, " ", test
#         iTrain = np.array(train)
#         iTest = np.array(test)
#         model = None # Clearing the NN.
#        # model, scores = createTrainTestModel(T[indices], G[indices], labels[indices], T[tIndice], G[tIndice], labels[tIndice])
#         model, scores = createTrainTestModelDico(d, labels, iTest, iTrain)
#         cvscores.append(scores[1] * 100)

#     mean_score = np.mean(cvscores)
#     print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
#     return model, mean_score
    
    
def buildTestModel(dico, labels, folds):
    '''
        Builds the model that matches the matrix T and G and the like/dislike
        Tests it with k-cross validation
        T and G matrix must have been preprocessed correctly
        
        Parameters : 
            T, G : the characteristics of the movies we want to build the model on
            labels : tells whether the movie is liked or not (binary)           
            
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


def mergeBranches(*listBranch):
    
    if(len(listBranch) == 0):
        #TODO : raise an error
        print "You can't merge 0 branches !"
        return None
        
    if(len(listBranch) == 1):
        return listBranch[0]
        
    if(len(listBranch) == 2):
        finalBranch = Sequential()
        finalBranch.add(Merge([listBranch[0], listBranch[1]], mode = 'concat'))
        return finalBranch
    
    merge2Branches = Sequential()
    merge2Branches.add(Merge([listBranch[0], listBranch[1]], mode = 'concat'))
    merge2Branches.add(Dense(1,  activation = 'sigmoid'))
    
    return mergeBranches(merge2Branches, *listBranch[2:])

        
#TODO after call of mergeBranches
#finalBranch.add(Dense(totalLen, activation = 'relu'))
    