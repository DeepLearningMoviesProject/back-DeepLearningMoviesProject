# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 23:32:06 2017

@author: darke
"""

from MovieProject.preprocessing.preprocessing import *



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
    
    print result

    
        
if __name__ == "__main__" :
    main()
    
