#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Allows to shuffle datas and labels on the same ways, in order to improve learning

Created on Wed Feb  8 14:21:01 2017
@author: coralie
"""

import random
from sklearn.utils import shuffle


def shuffleDataLabeled(datas, labels):
    """
    Shuffle the datas and the labels on the same ways thank's to a random state
        parameters : 
            - ids : ndarray of data like ids, to shuffle
            - labels : ndarray of labels associated to shuffle
        return :
            - a tuple containing the ids and the labels shuffled
    """
    r = random.randint(1, 10)
    datas,labels = shuffle(datas, labels, random_state=r)    
    return datas,labels
    
