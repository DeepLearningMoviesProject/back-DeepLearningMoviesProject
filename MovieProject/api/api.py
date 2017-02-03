#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:16:32 2017

@author: Kaito
"""
from flask import Flask, jsonify, request, abort, json
#from testTMDB import searchData, trainData
from MovieProject.learning import buildModel, buildTestModel
import numpy as np

app = Flask(__name__)


movieIds = {"415":1, "9320":0, "26914":1, "11059":1}

@app.route('/testId', methods=['GET'])
def get_tasks():
    return jsonify(movieIds)


@app.route('/train', methods=['POST'])
def trainModel():    
    
    dico = json.loads(request.data)
    ids = [int(key) for key in dico]
    
    #X_train = searchData(ids)
    Y_train = np.array([dico[key] for key in dico])
    
    print "Movies loaded"
    
    model = buildModel(ids, Y_train)
    
    return jsonify({'result': "ok"})

if __name__ == '__main__':
    app.run(debug=False, host= '0.0.0.0')


trainModel()
