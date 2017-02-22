from __future__ import print_function
import mysql.connector
import os
import User

db1 = mysql.connector.connect(host="localhost",user="root")
cursor = db1.cursor()
init = False

def createDB(DBName, overwrite = None):
    """
        Create the DBName. If it exists, raise an exception. 
        If overwrite = true, it will delete the oldd DBName if it exists and create
        the new one
        
        Parameters:
            DBName -> name of the database that needs to be created
            overwrite = if not None, it will overwrite old database with bddName
            if it exists
    """
    try:
        if overwrite is not None:
            if overwrite != "w+":
                raise Exception('INVALIDE ARGUMENT. Should be "w+"')
            sql = 'DROP DATABASE IF EXISTS ' + DBName
            cursor.execute(sql)
            db1.commit()
    
        sql = 'CREATE DATABASE ' + DBName
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is not None:
             print(row)
        db1.commit()
        
    except Exception as error:
        print('Error: ' + repr(error))  


def removeDB(DBName):
    """
        Remove the database with the name DBName if it exists
        
        Parameter:
            DBName -> name of the database that needs to be deleted
    """

    sql = "DROP DATABASE IF EXISTS " + DBName;
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is not None:
        print(row)
    db1.commit()
    
def showAllDB():
    """
        Printing name of all existing databases
    """
    
    sql = "show databases";
    cursor.execute(sql)
    row = cursor.fetchall()
    if row is not None:
        for r in row:
            print(r) #TODO : Unicode to utf8
            
def showDBName():
    """ 
        Printing name of the current database used
    """
    sql = "SELECT DATABASE() FROM DUAL;"
    cursor.execute(sql)
    row = cursor.fetchall()
    if row is not None:
        for r in row:
            print(r) #TODO : Unicode to utf8

def showTables():
    """
        Printing names of all tables of the currentDatabase
    """
    sql = "show tables";
    cursor.execute(sql)
    row = cursor.fetchall()
    if row is not None:
        for r in row:
            print(r) #TODO : Unicode to utf8
            
                 
def executeScriptsFromFile(filename):
    """
        Executing all SQL commands from filename SQL file
        Parameter:
            filename -> name of the SQL file. MUST BE A SQL FILE
    """
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        cursor.execute(command)

def loadDB(DBname, SQLname):
    """
        Loading in the database DBname datas from the file SQLname. It will also
        set DBname as the current DBname used
        DBname must be created before using this function
        Parameters:
            DBname -> name of the DBname. Has to be created before calling this 
            function
            SQLname -> name of the SQL file. MUST BE A SQL FILE
    """
    sql = "USE " + DBname;
    cursor.execute(sql)
    db1.commit()

    executeScriptsFromFile(SQLname)
    db1.commit()
    global init
    init = True

def changeDB(DBname):
    """
        Changing current database used
        Parameter:
            DBname -> name of the DBname. Has to be created before calling this 
            function
    """
    sql = "USE " + DBname;
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is not None:
        print(row)
    db1.commit()
    
def saveDB(DBname, SQLname):
    """
        Saving database DBname in the file SQLname
        Parameters:
            DBname -> Name of the database that need to be saved
            SQLname -> Name of the output SQL file
    """
    command = 'mysqldump -u root '+ DBname + '  > ' + SQLname
    os.system(command)
    
def insertUser(user, listMovies = None):
    """
        Creating a user. You can also add a list of movies and their 
        user rating. Database needs to be initalized
        Parameters:
            user -> User that will be inserted in the database
            listMovies -> Dictionnary of (K:id movie, V:Boolean like/dislike)
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
            
        userId, userName, userMail, tmdbKey, pw = user.getInfo()
        command = 'INSERT IGNORE into USER values('+str(userId)+',"'+userName+'","'+userMail+'","'+tmdbKey+'","'+pw+'")'
        cursor.execute(command) 
        row = cursor.fetchone()
        if row is not None:
            print(row)
        db1.commit()
        
        if(listMovies is not None):
            idMovies = listMovies.keys() 
            insertMovies(idMovies)
            for idMovie in idMovies:

                insertUserMovie(userId,idMovie,listMovies[idMovie])
        
    except Exception as error:
        print('Error: ' + repr(error))
        
def updateUser(idUser, userName = None, userTmdbkey = None, userMail = None, userPassword = None):
    """
        Update informations of a User. You can avoid not new informations.
        Parameters:
            idUser -> id of the user
            userName -> new name of the user
            userTmdbkey -> new tmdbkey of the user
            userMail -> new mail of the user
            userPassword -> new password of the user
            
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')  

        sql = "UPDATE USER SET " 
        added = False
           
        if(userName is not None):
            sql += 'name =  "' + userName + '"'
            added = True
        if(userTmdbkey is not None):
            if added == True:
                sql+=","
            sql += 'tmdbkey = "' +userTmdbkey + '"'
            added = True
        if(userMail is not None):
            if added == True:
                sql+=","
            sql += 'mail = "' +userMail + '"'
            added = True
        if(userPassword is not None):
            if added == True:
                sql+=","
            sql += 'password = "' +userPassword + '"'
 
        sql += " WHERE id = " + str(idUser)
 
        cursor.execute(sql) 
        row = cursor.fetchone()
        if row is not None:
            print(row)
        db1.commit()
             
    except Exception as error:
        print('Error: ' + repr(error))
        
def updateMoviesForUser(userId, listMovies):
    """
        update the USERMOVIE database for a user.
        Parameters:
            userId -> id of the user
            listMovies -> Dictionnary of (K:id movie, V:Boolean like/dislike)
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
            
        idMovies = listMovies.keys() 
        insertMovies(idMovies)
            
        for idMovie in idMovies:
            removeUserMovie(userId,idMovie)
            insertUserMovie(userId,idMovie,listMovies[idMovie])
            
    except Exception as error:
        print('Error: ' + repr(error))
        
def getUser(idUser):
    """
        Return the user with idUser. Return a user with id -1 if no user with
        idUser exists.
        Parameter:
            idUser -> id of the user
        Return: 
            user with id idUser in the database. 
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
            
        sql = "SELECT * from USER WHERE id = " + str(idUser)
        user = User.User(-1,"","","","")
        cursor.execute(sql)
        row = cursor.fetchall()
        if row is not None:
            empty = True
            for r in row:
                empty = False
                l = []
                for t in r:
                    l.append(t)
            if(not empty):
                user.setInfoList(l)
            return user
        
    except Exception as error:
        print('Error: ' + repr(error))
        
def getUsers(idUsers):
    """
        Return a list of users. Return a user with id -1 if no user with
        idUser exists.
        Parameter:
            idUsers -> list of id of users
        Return: 
            list of users
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
            
        users = []
        for idUser in idUsers:  
            user = getUser(idUser)
            users.append(user)
        return users
            
    except Exception as error:
        print('Error: ' + repr(error))
        
def getAllUsers():
    """
        return all users of the database
        Return:
            list of all users of the database
            
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        
        sql = "SELECT * from USER"
        cursor.execute(sql)
        row = cursor.fetchall()
        result = []
        if row is not None:
            for r in row:
                l = []
                user = User.User(-1,"","","","")
                for t in r:
                    l.append(t)
                user.setInfoList(l)
                result.append(user)
        return result
    
    except Exception as error:
        print('Error: ' + repr(error))
        
def showAllUsers():
    """
        show all Users
            
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        
        sql = "SELECT * from USER"
        cursor.execute(sql)
        row = cursor.fetchall()
        if row is not None:
            for r in row:
                print("userId: "+str(r[0])+", nameUser: "+str(r[1])+", userMail: "+ str(r[2]) + ", userTmdbKey: "+ str(r[3]) + ", userPassword: "+ str(r[4]) )
    
    except Exception as error:
        print('Error: ' + repr(error))
        
def removeUser(idUser):
    """
        Remove the user with idUser.
        Parameter:
            idUser -> id of the user
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        removeAllUserMoviefromUser(idUser)
        sql = "DELETE FROM USER WHERE id = " + str(idUser)
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is not None:
            for r in row:
                print(r)
        db1.commit()
        
    except Exception as error:
        print('Error: ' + repr(error))
        
def removeUsers(idUsers):
    """
        Remove a list of users
        Parameter:
            idUsers -> list of id of users
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')

        for idUser in idUsers:    
             removeUser(idUser)
        db1.commit()
        
    except Exception as error:
        print('Error: ' + repr(error))
        
def insertMovie(idMovie):
    """
        Creating a movie. Database needs to be initalized
        Parameter:
            movie -> id of the movie that will be added to the database
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
            
        command = 'INSERT IGNORE into MOVIE values('+str(idMovie) +')'
        cursor.execute(command)
        row = cursor.fetchone()
        if row is not None:
            print(row)
        db1.commit()

    except Exception as error:
        print('Error: ' + repr(error))
        
def insertMovies(idMovies):
    """
        Creating OR UPDATING a list of movies. Database needs to be initalized
        Parameter:
            movie -> list of id movies that will be added to the database
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
            
        for idMovie in idMovies:
            insertMovie(idMovie)
        db1.commit()

    except Exception as error:
        print('Error: ' + repr(error))
                   
def getAllMovies():
    """
        return all movies of the database
        Return:
            list of all movies of the database
            
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        
        sql = "SELECT * from MOVIE"
        cursor.execute(sql)
        row = cursor.fetchall()
        result = []
        if row is not None:
            for r in row:
                result.append(r[0])
        return result
    
    except Exception as error:
        print('Error: ' + repr(error))
        
def showAllMovies():
    """
        show all Movies of the database
            
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        
        sql = "SELECT * from MOVIE"
        cursor.execute(sql)
        row = cursor.fetchall()
        if row is not None:
            for r in row:
                print("Movie: "+str(r[0]))
    
    except Exception as error:
        print('Error: ' + repr(error))
        
def removeMovie(idMovie):
    """
        Remove the movie with idMovier.
        Parameter:
            idMovie -> id of the movie
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        removeAllUserMoviefromMovie(idMovie)     
        sql = "DELETE FROM MOVIE WHERE id = " + str(idMovie)
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is not None:
            for r in row:
                print(r)
        db1.commit()
        
    except Exception as error:
        print('Error: ' + repr(error))
        
def removeMovies(idMovies):
    """
        Remove a list of movies
        Parameter:
            idUsers -> list of id of movies
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')

        for idMovie in idMovies:    
             removeMovie(idMovie)
        db1.commit()
        
    except Exception as error:
        print('Error: ' + repr(error))
         
def insertUserMovie(idU, idM, like):
    """
        Creating OR UPDATING a UserMovie. Database needs to be initalized
        Parameters:
            idU -> id of the User
            idV -> id of the Movie
            like -> boolean. If the user like ou disliked the movie
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
            
        command = 'REPLACE into USERMOVIE values('+str(idU) +',' + str(idM) +','+ str(like) + ')'
        cursor.execute(command)
        row = cursor.fetchone()
        if row is not None:
            print(row)
        db1.commit()
        
    except Exception as error:
        print('Error: ' + repr(error))

def getLike(idU, idM):
    """
        return what the user think about a movie
        Parameters:
            idU -> id of the User
            idV -> id of the Movie
        Return:
            boolean 0 if disliked, 1 if liked. -1 if not found
            
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        
        sql = "SELECT LIKED from USERMOVIE WHERE IDUSER = "+str(idU)+" AND IDMOVIE = " + str(idM)
        cursor.execute(sql)
        row = cursor.fetchall()
        result = -1
        if row is not None:
            for r in row:
                result = r[0]
        return result
    
    except Exception as error:
        print('Error: ' + repr(error))

def showAllUsersMovies():
    """
        show all UsersMovies of the database
            
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        
        sql = "SELECT * from USERMOVIE"
        cursor.execute(sql)
        row = cursor.fetchall()
        if row is not None:
            for r in row:
                print("idUser: "+str(r[0])+", idMovie: "+str(r[1])+", Liked: "+ str(r[2]))
    
    except Exception as error:
        print('Error: ' + repr(error))
        
def getAllMoviesFromUser(idUser):
    """
        return all movies of the database that a user said its opinion
        Parameter:
            idUser -> id of the User
        Return:
            dictionnary (K:idmovie, V:Opinion)
            
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        
        sql = "SELECT IDMOVIE, LIKED from USERMOVIE WHERE IDUSER = " + str(idUser)
        cursor.execute(sql)
        row = cursor.fetchall()
        result = {}
        if row is not None:
            for r in row:
                result[r[0]] = r[1]
        return result
    
    except Exception as error:
        print('Error: ' + repr(error))
        
def getLikedMoviesFromUser(idUser,liked = 1):
    """
        return all liked movies of a user from the database. If liked = 0, return
        all disliked movies
        Parameters:
            idUser -> id of the User
            (optional) liked -> write 0 if you want disliked values
        Return:
            list of id of liked/disliked movies
            
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        
        sql = "SELECT IDMOVIE from USERMOVIE WHERE IDUSER = " + str(idUser) + " AND LIKED = " + str(liked)
        cursor.execute(sql)
        row = cursor.fetchall()
        result = []
        if row is not None:
            for r in row:
                result.append(r[0])
        return result
    
    except Exception as error:
        print('Error: ' + repr(error))
              
def getAllUsersFromMovie(idMovie):
    """
        return all users of the database that gave a opinion of the movie
        Parameter:
            idMovie -> id of the Movie
        Return:
            dictionnary (K:idUser, V:Opinion)
            
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        
        sql = "SELECT IDUSER, LIKED from USERMOVIE WHERE IDMOVIE = " + str(idMovie)
        cursor.execute(sql)
        row = cursor.fetchall()
        result = {}
        if row is not None:
            for r in row:
                result[r[0]] = r[1]
        return result
    
    except Exception as error:
        print('Error: ' + repr(error))
        
def getLikedUsersFromMovie(idMovie,liked = 1):
    """
        return all users that liked the movie from the database. If liked = 0, return
        all users that disliked the movie
        Parameters:
            idMovie -> id of the movie
            (optional) liked -> write 0 if you want disliked values
        Return:
            list of id of users
            
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        
        sql = "SELECT IDUSER from USERMOVIE WHERE IDMOVIE = " + str(idMovie) + " AND LIKED = " + str(liked)
        cursor.execute(sql)
        row = cursor.fetchall()
        result = []
        if row is not None:
            for r in row:
                result.append(r[0])
        return result
    
    except Exception as error:
        print('Error: ' + repr(error))
              

def removeUserMovie(idUser,idMovie):
    """
        Remove the USERMOVIE with idMovie and idUser.
        Parameter:
            idUser -> id of the user
            idMovie -> id of the movie
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
                
        sql = "DELETE FROM USERMOVIE WHERE IDUSER = " + str(idUser) + " AND IDMOVIE = " + str(idMovie)
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is not None:
            for r in row:
                print(r)
        db1.commit()
        
    except Exception as error:
        print('Error: ' + repr(error))
        
def removeAllUserMoviefromUser(idUser):
    """
        Remove all USERMOVIES of a user.
        Parameter:
            idUser -> id of the user
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
                
        sql = "DELETE FROM USERMOVIE WHERE IDUSER = " + str(idUser) 
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is not None:
            for r in row:
                print(r)
        db1.commit()  
        
    except Exception as error:
        print('Error: ' + repr(error))  

def removeAllUserMoviefromMovie(idMovie):
    """
        Remove all USERMOVIES of a movie.
        Parameter:
            idMovie -> id of the movie
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
                
        sql = "DELETE FROM USERMOVIE WHERE IDMOVIE = " + str(idMovie) 
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is not None:
            for r in row:
                print(r)
        db1.commit() 
        
    except Exception as error:
        print('Error: ' + repr(error))
        
def customRequest(sql):
    """
        This is a function to send a custom request to SQL.
        Warning : Some behaviors are not defined as fetchall() or commit
        function don't work with some requests
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
            
        cursor.execute(sql)
        row = cursor.fetchall()
        if row is not None:
            for r in row:
                print(r)
        db1.commit()
        
    except Exception as error:
        print('Error: ' + repr(error))

        
        