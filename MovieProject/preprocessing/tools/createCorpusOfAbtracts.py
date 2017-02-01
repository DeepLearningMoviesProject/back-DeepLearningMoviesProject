#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Script allowed to load abstracts on TMDB and write them in text file

Created on Mon Jan 30 15:08:47 2017
@author: coralie

"""

# Library to write utf-8 text file
import codecs
# Library to remove all ponctuations
import string
# Library to remove all stop words
from nltk.corpus import stopwords
# TMDB simple (TMDB API wrapper)
import tmdbsimple as tmdb

tmdb.API_KEY = 'ff3f07bf3577a496a2f813488eb29980'
filePath = "../../resources/train_overviews_treated.txt"
#filePath = "../../resources/train_overviews_noStopWords.txt"

# Remove specific accents
def withoutAccents(ch, encod='utf-8'):
    alpha1 = u"àâäåçéèêëîïôöùûüÿğ"
    alpha2 = u"aaaaceeeeiioouuuyg"
    conv = False
    if not isinstance(ch, unicode):
        ch = unicode(ch, encod,'replace')
        conv = True
    tableconv = {ord(a):b for a, b in zip(alpha1, alpha2)} # <== nouveau maketrans
    x = ch.translate(tableconv)
    if conv:
        x = x.encode(encod)
    return x


# Load and store resumes on TMDB thanks to discover method
def loadResumes(fileName, pages_max):
    
    file_abstracts = codecs.open(fileName, "w", 'utf-8')
    cachedStopWords = stopwords.words("english")
    
    for i in range(1,pages_max):
        response = discover.movie(page=i)
        films_nb = len(response[u'results'])
        for j in range (0,films_nb):
            abstract = response[u'results'][j][u'overview']
            #Convert to lower case
            abstract = abstract.lower()
            #Replace specific things
            abstract.replace(" -", " ")
            abstract.replace(" --", " ")
            abstract.replace("'s", "")
            abstract.replace("  ", " ")
            abstract = withoutAccents(abstract)
            #Remove all punctuation
            abstract = "".join(c for c in abstract if c not in string.punctuation)
            #Remove all stop words
            #for word in abstract.split():
            #    if word not in cachedStopWords:
            #        file_abstracts.write(word+' ')
            #file_abstracts.write('\n')
            file_abstracts.write(abstract+'\n')
        print i
    
    file_abstracts.close()
    
    
if __name__ == "__main__":
    
    discover = tmdb.Discover()
    response = discover.movie(page=1)
    #pages_nb = int(response[u'total_pages'])
    #print pages_nb   
    
    loadResumes(filePath, 1000)
    

