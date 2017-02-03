# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 23:32:06 2017

@author: darke
"""

from MovieProject.preprocessing.preprocessing import *

import numpy as np
import pickle 

def main():
    """
       This is an example of how to use preprocess function
    """

    i = 1
    idArray = []
    while (i<15):
        idArray.append(i)
        i += 1
    result = preprocess(idArray)
    with open('test.data', 'w') as f:
        pickle.dump(result, f)


    with open('test.data', 'r') as f:
        new_data = pickle.load(f)
    print new_data

    
        
if __name__ == "__main__" :
    main()
    
