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
    if overwrite is not None:
        sql = 'DROP DATABASE IF EXISTS' + DBName
        cursor.execute(sql)
    
    sql = 'CREATE DATABASE ' + DBName
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is not None:
        print(row)
    db1.commit()


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
    
def createUser(user):
    """
        Creating OR UPDATING user. Database needs to be initalized
        Parameter:
            user : User that will be inserted in the database
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        userId, userName, userMail, tmdbKey, pw = user.getInfo()
        command = 'REPLACE into USER values('+str(userId)+',"'+userName+'","'+userMail+'","'+tmdbKey+'","'+pw+'")'
        cursor.execute(command)
        row = cursor.fetchone()
        if row is not None:
            print(row)
        db1.commit()
        
    except Exception as error:
        print('Error: ' + repr(error))
def getUser(idUser):
    """
        Return the user with the id User. None otherwise
        Parameter:
            idUser -> id of the user
        Return: user with id idUser in the database. None otherwise
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
    except Exception as error:
        print('Error: ' + repr(error))
        
def showAllUsers():
    """
        Print all users of the database
    """
    sql = "SELECT * from USER"
    try:
        if(not init):
            raise Exception('Database need to be initialized')
        cursor.execute(sql)
        row = cursor.fetchall()
        if row is not None:
            for r in row:
                print(r) #TODO : unicode to utf8

        db1.commit()
    except Exception as error:
        print('Error: ' + repr(error))
        
def removerUser(idUser):
    """
        Remove the user with the id User. Null otherwise
        Parameter:
            idUser -> id of the user
    """
    try:
        if(not init):
            raise Exception('Database need to be initialized')
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

        
        