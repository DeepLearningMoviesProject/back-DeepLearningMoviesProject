#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Allows to shuffle datas and labels on the same ways, in order to improve learning

Created on Wed Feb  8 14:21:01 2017
@author: coralie
"""

import numpy as np
import random
from sklearn.utils import shuffle


def shuffleIdLabeled(ids, labels):
    """
    Shuffle the ids and the labels on the same ways thank's to a random state
    
    Parameters : 
        ids : numpy array of ids to shuffle
        labels : numpy array of labels to shuffle
    
    Return :
        a tuple containing the ids and the labels shuffled

    """
    r = random.randint(1, 10)
    ids,labels = shuffle(ids, labels, random_state=r)    
    return ids,labels
    
    
    
if __name__ == "__main__": 
    
    #x = np.array([[0., 0.], [1., 1.], [2., 2.], [3., 3.]])
    x = np.array([0, 1, 2, 3])
    y = np.array([0, 1, 2, 3])
    x,y = shuffleIdLabeled(x,y)
    print x
    print y