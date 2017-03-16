from MovieProject.sql import *
from collections import Counter
import unittest

class SqlTest(unittest.TestCase):
    """Test case used to test the module 'MovieProject.sql'."""
     
    manager = DatabaseManager()
    def test_insertGetUser(self):
        """Test to check is an User is correctly inserted into the database"""
        
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        self.manager.insertUser(user)
        user = self.manager.getUser(user.name)
        
        self.assertEquals(user.name, "Edwin")
        self.assertEquals(user.email, "mail2")
        self.assertEquals(user.tmdbKey, "dsklqs")
        self.assertEquals(user.password, "abc")

        #Check if trying to insert same User raise the correct exception
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")

        with self.assertRaises(RuntimeError):
            self.manager.insertUser(user)

        self.manager.removeUser(user.name)
 
        #Trying to get a nonexisting user
        user = self.manager.getUser("Edwin")
        self.assertEquals(user, None)
       
    def test_getNotRatedMoviesfromUser(self):
         """Test to check is the function return only non rated movies for a given user"""
         
         user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
         self.manager.insertUser(user)
         self.manager.updateLikedMoviesForUser(user.name, {"11":1,"12":0, "18":1}) 
         idUser = user.id
         lNR = self.manager.getNotRatedMoviesfromUser(idUser) 
         lMovies = self.manager.getAllMovies()

         #Checking list lenght difference
         self.assertEquals(len(lMovies), len(lNR)+3)
        
         #Checking there is no dupplicated valued
         n = [k for k,v in Counter(lMovies).items() if v>1]
         self.assertEquals(len(n), 0)         
         
         #Checking liked movies from user are not in the result list              
         self.assertEquals(11 not in lMovies, True)
         self.assertEquals(12 not in lMovies, True)
         self.assertEquals(18 not in lMovies, True)
        
         self.manager.removeUser(user.name)
               
         
    def test_updateLikedMoviesForUser(self):
        """Test to check is a list of movies rated by the user are correctly inserted into the database"""

        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        self.manager.insertUser(user)
        self.manager.updateLikedMoviesForUser(user.name, {"1000":1,"1500":0, "45":1})
        user = self.manager.getUser(user.name)
        self.manager.removeUser(user.name)
        
        self.assertEquals(str(user.movies),"[<UserMovie "+str(user.id)+" 45 True>, <UserMovie "+str(user.id)+" 1000 True>, <UserMovie "+str(user.id)+" 1500 False>]")

        #Check if trying to update nonexisting User
        with self.assertRaises(RuntimeError): 
            self.manager.updateLikedMoviesForUser(user.name, {"1000":1,"1500":0, "45":1})
        
    
    def test_getMoviesLikedByUser(self):
        """Test to check is movies rated by a user are correctly selected from the database"""      
 
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        self.manager.insertUser(user)
        self.manager.updateLikedMoviesForUser(user.name, {"1000":1,"1500":0, "45":1})
        
        #List of all movies rated by the user and their rating
        allMovies = self.manager.getMoviesLikedByUser(user.name)
        #List of all Liked movies rated by the user and their rating
        liked = self.manager.getMoviesLikedByUser(user.name, liked = True)
        #List of all disliked movies rated by the user and their rating
        disliked = self.manager.getMoviesLikedByUser(user.name, liked = False)
      
        self.assertEquals(str(allMovies),"[<UserMovie "+str(user.id)+" 45 True>, <UserMovie "+str(user.id)+" 1000 True>, <UserMovie "+str(user.id)+" 1500 False>]")
        self.assertEquals(str(liked),"[<UserMovie "+str(user.id)+" 45 True>, <UserMovie "+str(user.id)+" 1000 True>]")
        self.assertEquals(str(disliked),"[<UserMovie "+str(user.id)+" 1500 False>]")
        
        #Trying to send wrong argument to the function
        with self.assertRaises(RuntimeError):         
            self.manager.getMoviesLikedByUser(user.name, liked = "test")

        self.manager.removeUser(user.name)

        #Trying to use function with nonexisting user
        with self.assertRaises(RuntimeError): 
            self.manager.getMoviesLikedByUser(user.name)

 
    def test_updateLikedMoviesforUser(self):
        """Test to check is the function updateLikedMoviesforUser works"""

        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        self.manager.insertUser(user)
        self.manager.updateLikedMoviesForUser(user.name, {"1000":1,"1500":0, "45":1})
        #updating rated movies of Edwin
        self.manager.updateLikedMoviesForUser(user.name, {"1000":0,"1500":0, "45":1,"46":1})
        allMovies = self.manager.getMoviesLikedByUser(user.name)
        
        self.assertEquals(str(allMovies),"[<UserMovie "+str(user.id)+" 45 True>, <UserMovie "+str(user.id)+" 46 True>, <UserMovie "+str(user.id)+" 1000 False>, <UserMovie "+str(user.id)+" 1500 False>]")

        #Trying to use function with wrong argument
        with self.assertRaises(RuntimeError): 
            self.manager.updateLikedMoviesForUser(user.name, {"1000":"sdlk","1500":"dssdkl", "45":"ssddkl"})

        self.manager.removeUser(user.name)

        #Trying to use function with nonexisting user
        with self.assertRaises(RuntimeError): 
           self.manager.updateLikedMoviesForUser(user.name, {"1000":1,"1500":0, "45":1})
           
        
    def test_updateLikedMovieForUser(self):
        """Test to check is the function updateLikedMovieforUser works"""

        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        self.manager.insertUser(user)
        self.manager.updateLikedMoviesForUser(user.name, {"1000":1,"1500":0, "45":1})
        #Inserting individual data
        self.manager.updateLikedMovieForUser(user.name, 1000, False)
        self.manager.updateLikedMovieForUser(user.name, 46, True)
        allMovies = self.manager.getMoviesLikedByUser(user.name)
        
        self.assertEquals(str(allMovies),"[<UserMovie "+str(user.id)+" 45 True>, <UserMovie "+str(user.id)+" 46 True>, <UserMovie "+str(user.id)+" 1000 False>, <UserMovie "+str(user.id)+" 1500 False>]")

        #Trying to use function with wrong argument
        with self.assertRaises(RuntimeError): 
            self.manager.updateLikedMovieForUser(user.name, 1000, "test")

        self.manager.removeUser(user.name)

        #Trying to use function with nonexisting user
        with self.assertRaises(RuntimeError): 
           self.manager.updateLikedMovieForUser(user.name, 1000, 1)        
        
         
            
    def test_removeUser(self):
        """"Test to check if removeUser remove a user and its usermovies """
        
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        self.manager.insertUser(user)
        self.manager.updateLikedMovieForUser(user.name, 46, True)
        user = self.manager.getUser(user.name)
        idUser = user.id
        self.manager.removeUser(user.name)
        user = self.manager.getUser(user.name)
        um = self.manager.getUserMovie(idUser, 46)
        
        self.assertEquals(um, None)
        self.assertEquals(user, None)
        
        #Trying to remove nonexisting user
        with self.assertRaises(RuntimeError): 
            self.manager.removeUser("Edwin")
        

    def test_insertGetMovie(self):
         """Test to check if a movie is correctly inserted into the database"""
     
         movie = Movie(100)
         self.manager.insertMovie(movie.idMovie)
         movie = self.manager.getMovie(movie.idMovie)
        
         self.assertEquals(str(movie),"<Movie 100>")

         #Trying to insert already existing movie
         with self.assertRaises(RuntimeError):
             self.manager.insertMovie(100)
            
         self.manager.removeMovie(movie.idMovie)
        
         #Get a nonexisting movie
         movie = self.manager.getMovie(movie.idMovie)
         self.assertEquals(movie,None)
        
        
    def test_removeMovie(self):
        """Test to check if a movie is correctly removed from the database"""
        
        movie = Movie(100)
        self.manager.insertMovie(movie.idMovie)
        self.manager.removeMovie(movie.idMovie)
        movie = self.manager.getMovie(movie.idMovie)

        self.assertEquals(movie,None)
        
        #Trying to remove nonexisting movie
        with self.assertRaises(RuntimeError):
            self.manager.removeMovie(100)


    def test_insertGetUserMovie(self):
        """"Test to check if insertUserMovie and getUserMovie work"""
        
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        self.manager.insertUser(user)
        movie = Movie(100)  
        self.manager.insertMovie(movie.idMovie)
        
        #Trying to insert with a wrong value
        with self.assertRaises(RuntimeError):
            self.manager.insertUserMovie(user.name, movie.idMovie, "test")
            
        self.manager.insertUserMovie(user.name, movie.idMovie, True)
        user = self.manager.getUser(user.name)
        um = self.manager.getUserMovie(user.id, movie.idMovie)

        self.assertEquals(str(um),"<UserMovie "+str(user.id)+" 100 True>")
            
        #Trying to insert with a non existing user
        with self.assertRaises(RuntimeError):
            self.manager.insertUserMovie( "WrongName", movie.idMovie, True)
            
        self.manager.removeMovie(movie.idMovie)
        self.manager.removeUser(user.name)
        
        #Trying to get a nonexisting usermovie
        um = self.manager.getUserMovie(user.id, movie.idMovie)
        self.assertEquals(um,None)
#
       
    def test_removeAllUserMovieFromUser(self):
        """Test to check if removeAllUserMovieFromUser works"""      

 
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        self.manager.insertUser(user)
        movie = Movie(100)  
        movie2 = Movie(200)  
        self.manager.insertMovie(movie.idMovie)
        self.manager.insertMovie(movie2.idMovie)
        self.manager.insertUserMovie(user.name, movie.idMovie, True)
        self.manager.insertUserMovie(user.name, movie2.idMovie, True)
        user = self.manager.getUser(user.name)
        self.manager.removeAllUserMovieFromUser(user.name)
        um = self.manager.getUserMovie(user.id, movie.idMovie)
        um2 = self.manager.getUserMovie(user.id, movie2.idMovie)
        
        self.assertEquals(um,None)  
        self.assertEquals(um2,None)        
        
        self.manager.removeMovie(movie.idMovie)
        self.manager.removeMovie(movie2.idMovie)
        self.manager.removeUser(user.name)
        
        #Trying to remove from a non existing user
        with self.assertRaises(RuntimeError):
            self.manager.removeAllUserMovieFromUser("Edwin")

#    
    def test_getRegion(self):
        """"Test to check if getRegion works"""    
    
        test = Region("France")
        r = self.manager.getRegion("France")
        r2 = self.manager.getRegion("PLUTON")  
        
        self.assertEquals(r.country,test.country)  
        self.assertEquals(r2,None)  


if __name__ == '__main__':
    unittest.main()
