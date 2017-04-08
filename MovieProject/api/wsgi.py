#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 17:47:52 2017

@author: elsa
"""

from api import app, initAPI

if __name__ == '__main__':
    print "initAPI"
    initAPI()
    print "app.run"
    app.run(debug=False, host= '0.0.0.0')