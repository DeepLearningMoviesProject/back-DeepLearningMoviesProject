#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Allows to manage the users models

Created on Tue Mar 14 11:22:17 2017
@author: elsa
"""


from os.path import isfile, exists
from os import makedirs
from keras.models import model_from_json
from MovieProject.resources import RES_MODEL_PATH

def saveModel(username, model):
    """
        Save model on resource/persist/model/username_model.json

        username : unique key for a user, and a model is unique for a user
        model : the keras model for the user
    """
    filename =  username + '_model'
    path = RES_MODEL_PATH + '/'
    saveModelToPath(path, filename, model)


def loadModel(username):
    """
        Save model on resource/persist/model/username_model.json

        username : unique key for a user, and a model is unique for a user
        model : the keras model for the user
    """
    path = RES_MODEL_PATH + '/'
    filename = username + '_model'
    
    return loadModelFromPath(path, filename)
    
def saveModelToPath(path, filename, model):
    """
        Save model on resource/persist/model/username_model.json

        username : unique key for a user, and a model is unique for a user
        model : the keras model for the user
    """
    # serialize model to JSON
    model_json = model.to_json()
    model_filepath = path + filename
    
    #If the model directory doesn't exists, we create it
    if not exists(path):
        makedirs(path)

    with open(model_filepath + '.json', "w") as json_file:
        json_file.write(model_json)

    # serialize weights to HDF5
    model.save_weights(model_filepath + '.h5')

    print("Saved model to disk")
    
def loadModelFromPath(path, filename):
    """
        Save model on path/filename.json and its weighs on path/filename.h5
    """
    # serialize model to JSON
   # model_json = model.to_json()
    model_filepath = path + filename
    
    #If file doesn't exists, we return None
    if(isfile(model_filepath + '.json') and isfile(model_filepath + '.h5')):
        # load json and create model
        json_file = open(model_filepath + '.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(model_filepath + '.h5')
        print("Loaded model from disk")
        
        return loaded_model
    # evaluate loaded model on test data
    # loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    # score = loaded_model.evaluate(X, Y, verbose=0)
    else :
        print "The model doesn't exists"
        return None