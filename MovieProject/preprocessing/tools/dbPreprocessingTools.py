"""
Created on Thu Mar  9 15:43:32 2017

@author: edwin
"""

from MovieProject.sql import *
import numpy as np

class dbPreprocessingTools():
  
    manager = DatabaseManager()

    def preprocessingUserMovies(self):
        """
            Return all UserMovies from the database
            
            return:
                3 lists : users list, movies list, rating list
                NB : for i UserMovie(u,m,r), datas in lists will be :
                    u = usersList[i], m = moviesList[i], r = ratingList[i]
        """
      
        listUM = self.manager.getAllUsersMovies()
        
        usersList = np.empty(len(listUM), dtype = "int")
        moviesList = np.empty(len(listUM), dtype = "int")
        ratingList = np.empty(len(listUM), dtype = "int")
                
        for i, um in enumerate(listUM):
            usersList[i] = um.idUser
            moviesList[i] = um.idMovie
            ratingList[i] = um.liked
        
        return usersList, moviesList, ratingList
    
    