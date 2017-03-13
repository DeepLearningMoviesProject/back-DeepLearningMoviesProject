from MovieProject.sql import *
import unittest

class SqlTest(unittest.TestCase):
    """Test case used to test the module 'MovieProject.sql'."""
              
    def test_insertGetUser(self):
        """Test to check is an User is correctly inserted into the database"""
        
        manager = DatabaseManager()
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        manager.insertUser(user)
        user = manager.getUser(user.name)
        
        self.assertEquals(user.name, "Edwin")
        self.assertEquals(user.email, "mail2")
        self.assertEquals(user.tmdbKey, "dsklqs")
        self.assertEquals(user.password, "abc")

        #Check if trying to insert same User raise the correct exception
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")

        with self.assertRaises(RuntimeError):
            manager.insertUser(user)

        manager.removeUser(user.name)
 
        #Trying to get a nonexisting user
        user = manager.getUser("Edwin")
        self.assertEquals(user, None)
       
    
    def test_updateLikedMoviesForUser(self):
        """Test to check is a list of movies rated by the user are correctly inserted into the database"""

        manager = DatabaseManager()
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        manager.insertUser(user)
        manager.updateLikedMoviesForUser(user.name, {"1000":1,"1500":0, "45":1})
        user = manager.getUser(user.name)
        manager.removeUser(user.name)
        
        self.assertEquals(str(user.movies),"[<UserMovie "+str(user.id)+" 45 True>, <UserMovie "+str(user.id)+" 1000 True>, <UserMovie "+str(user.id)+" 1500 False>]")

        #Check if trying to update nonexisting User
        with self.assertRaises(RuntimeError): 
            manager.updateLikedMoviesForUser(user.name, {"1000":1,"1500":0, "45":1})
        
    
    def test_getMoviesLikedByUser(self):
        """Test to check is movies rated by a user are correctly selected from the database"""      
 
        manager = DatabaseManager()
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        manager.insertUser(user)
        manager.updateLikedMoviesForUser(user.name, {"1000":1,"1500":0, "45":1})
        
        #List of all movies rated by the user and their rating
        allMovies = manager.getMoviesLikedByUser(user.name)
        #List of all Liked movies rated by the user and their rating
        liked = manager.getMoviesLikedByUser(user.name, liked = True)
        #List of all disliked movies rated by the user and their rating
        disliked = manager.getMoviesLikedByUser(user.name, liked = False)
      
        self.assertEquals(str(allMovies),"[<UserMovie "+str(user.id)+" 45 True>, <UserMovie "+str(user.id)+" 1000 True>, <UserMovie "+str(user.id)+" 1500 False>]")
        self.assertEquals(str(liked),"[<UserMovie "+str(user.id)+" 45 True>, <UserMovie "+str(user.id)+" 1000 True>]")
        self.assertEquals(str(disliked),"[<UserMovie "+str(user.id)+" 1500 False>]")
        
        #Trying to send wrong argument to the function
        with self.assertRaises(RuntimeError):         
            manager.getMoviesLikedByUser(user.name, liked = "test")

        manager.removeUser(user.name)

        #Trying to use function with nonexisting user
        with self.assertRaises(RuntimeError): 
            manager.getMoviesLikedByUser(user.name)

 
    def test_updateLikedMoviesforUser(self):
        """Test to check is the function updateLikedMoviesforUser works"""

        manager = DatabaseManager()
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        manager.insertUser(user)
        manager.updateLikedMoviesForUser(user.name, {"1000":1,"1500":0, "45":1})
        #updating rated movies of Edwin
        manager.updateLikedMoviesForUser(user.name, {"1000":0,"1500":0, "45":1,"46":1})
        allMovies = manager.getMoviesLikedByUser(user.name)
        
        self.assertEquals(str(allMovies),"[<UserMovie "+str(user.id)+" 45 True>, <UserMovie "+str(user.id)+" 46 True>, <UserMovie "+str(user.id)+" 1000 False>, <UserMovie "+str(user.id)+" 1500 False>]")

        #Trying to use function with wrong argument
        with self.assertRaises(RuntimeError): 
            manager.updateLikedMoviesForUser(user.name, {"1000":"sdlk","1500":"dssdkl", "45":"ssddkl"})

        manager.removeUser(user.name)

        #Trying to use function with nonexisting user
        with self.assertRaises(RuntimeError): 
           manager.updateLikedMoviesForUser(user.name, {"1000":1,"1500":0, "45":1})
         
     
        
    def test_updateLikedMovieForUser(self):
        """Test to check is the function updateLikedMovieforUser works"""

        manager = DatabaseManager()
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        manager.insertUser(user)
        manager.updateLikedMoviesForUser(user.name, {"1000":1,"1500":0, "45":1})
        #Inserting individual data
        manager.updateLikedMovieForUser(user.name, 1000, False)
        manager.updateLikedMovieForUser(user.name, 46, True)
        allMovies = manager.getMoviesLikedByUser(user.name)
        
        self.assertEquals(str(allMovies),"[<UserMovie "+str(user.id)+" 45 True>, <UserMovie "+str(user.id)+" 46 True>, <UserMovie "+str(user.id)+" 1000 False>, <UserMovie "+str(user.id)+" 1500 False>]")

        #Trying to use function with wrong argument
        with self.assertRaises(RuntimeError): 
            manager.updateLikedMovieForUser(user.name, 1000, "test")

        manager.removeUser(user.name)

        #Trying to use function with nonexisting user
        with self.assertRaises(RuntimeError): 
           manager.updateLikedMovieForUser(user.name, 1000, 1)        
        
         
            
    def test_removeUser(self):
        """"Test to check if removeUser remove a user and its usermovies """
        
        manager = DatabaseManager()
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        manager.insertUser(user)
        manager.updateLikedMovieForUser(user.name, 46, True)
        user = manager.getUser(user.name)
        idUser = user.id
        manager.removeUser(user.name)
        user = manager.getUser(user.name)
        um = manager.getUserMovie(idUser, 46)
        
        self.assertEquals(um, None)
        self.assertEquals(user, None)
        
        #Trying to remove nonexisting user
        with self.assertRaises(RuntimeError): 
            manager.removeUser("Edwin")
        

    def test_insertGetMovie(self):
         """Test to check if a movie is correctly inserted into the database"""
    
         manager = DatabaseManager()
         movie = Movie(100)
         manager.insertMovie(movie.idMovie)
         movie = manager.getMovie(movie.idMovie)
        
         self.assertEquals(str(movie),"<Movie 100>")

         #Trying to insert already existing movie
         with self.assertRaises(RuntimeError):
             manager.insertMovie(100)
            
         manager.removeMovie(movie.idMovie)
        
         #Get a nonexisting movie
         movie = manager.getMovie(movie.idMovie)
         self.assertEquals(movie,None)
        
        
    def test_removeMovie(self):
        """Test to check if a movie is correctly removed from the database"""
        
        manager = DatabaseManager()
        movie = Movie(100)
        manager.insertMovie(movie.idMovie)
        manager.removeMovie(movie.idMovie)
        movie = manager.getMovie(movie.idMovie)

        self.assertEquals(movie,None)
        
        #Trying to remove nonexisting movie
        with self.assertRaises(RuntimeError):
            manager.removeMovie(100)


    def test_insertGetUserMovie(self):
        """"Test to check if insertUserMovie and getUserMovie work"""
        
        manager = DatabaseManager()
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        manager.insertUser(user)
        movie = Movie(100)  
        manager.insertMovie(movie.idMovie)
        
        #Trying to insert with a wrong value
        with self.assertRaises(RuntimeError):
            manager.insertUserMovie(user.name, movie.idMovie, "test")
            
        manager.insertUserMovie(user.name, movie.idMovie, True)
        user = manager.getUser(user.name)
        um = manager.getUserMovie(user.id, movie.idMovie)

        self.assertEquals(str(um),"<UserMovie "+str(user.id)+" 100 True>")
            
        #Trying to insert with a non existing user
        with self.assertRaises(RuntimeError):
            manager.insertUserMovie( "WrongName", movie.idMovie, True)
            
        manager.removeMovie(movie.idMovie)
        manager.removeUser(user.name)
        
        #Trying to get a nonexisting usermovie
        um = manager.getUserMovie(user.id, movie.idMovie)
        self.assertEquals(um,None)
#
       
    def test_removeAllUserMovieFromUser(self):
        """Test to check if removeAllUserMovieFromUser works"""      

        manager = DatabaseManager()
        user = User("Edwin", password= "abc", email="mail2", tmdbKey= "dsklqs")
        manager.insertUser(user)
        movie = Movie(100)  
        movie2 = Movie(200)  
        manager.insertMovie(movie.idMovie)
        manager.insertMovie(movie2.idMovie)
        manager.insertUserMovie(user.name, movie.idMovie, True)
        manager.insertUserMovie(user.name, movie2.idMovie, True)
        user = manager.getUser(user.name)
        manager.removeAllUserMovieFromUser(user.name)
        um = manager.getUserMovie(user.id, movie.idMovie)
        um2 = manager.getUserMovie(user.id, movie2.idMovie)
        
        self.assertEquals(um,None)  
        self.assertEquals(um2,None)        
        
        manager.removeMovie(movie.idMovie)
        manager.removeMovie(movie2.idMovie)
        manager.removeUser(user.name)
        
        #Trying to remove from a non existing user
        with self.assertRaises(RuntimeError):
            manager.removeAllUserMovieFromUser("Edwin")

#    
    def test_getRegion(self):
        """"Test to check if getRegion works"""    
    
        manager = DatabaseManager()
        test = Region("France")
        r = manager.getRegion("France")
        r2 = manager.getRegion("PLUTON")  
        
        self.assertEquals(r.country,test.country)  
        self.assertEquals(r2,None)  
#

if __name__ == '__main__':
    unittest.main()
