#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 15:36:28 2017

@author: Kaito
"""

from manager import DatabaseManager
from models import Occupation, Region
from MovieProject.resources import COUNTRIES_FILE
from os.path import isfile
from json import loads, dumps
import codecs


manager = DatabaseManager()

def parseJsonCountries(filename):
    """
        Parse json file containing all Country with some properties
        
        Parameters:
            filename -> String, name of the json file
        return sorted list of unique countries in french translation
    """

    with codecs.open(filename, "r", "utf-8")  as f:
        jsonCountries = loads(f.read())
    
    countries = [ country["translations"]["fra"]["common"].encode("utf-8") for country in jsonCountries ]    
    return sorted( list( set(countries) ) )


def populateDbWithCountries():
    """
        Insert country from json file into database
    """
    
    print "Parsing json"
    countries = parseJsonCountries(COUNTRIES_FILE)
    
    print "insertion of new regions"
    for country in countries:
        manager.insertRegion(Region(country))

        
    


def populateDbWithOccupations():
    """
        insert occupations into database
    """
    
    OCCUPATIONS = ["agriculteurs",
                   "artisan - commerçant - chef d\'entreprise",
                   "autre",
                   "cadre",
                   "employé",
                   "étudiant",
                   "ouvrier",
                   "profession intermédiaire",
                   "retraité"]
    
    print "insertion of new occupations"
    for occupation in sorted(OCCUPATIONS):
        manager.insertOccupation(Occupation(occupation))

if __name__ == "__main__":
    populateDbWithCountries()    
    populateDbWithOccupations()
