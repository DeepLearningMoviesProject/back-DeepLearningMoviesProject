#MySQL Server

##Installation
To run MySQL server make sure that it has already been installed, if not run this command to install it:
```
sudo apt-get update
sudo apt-get install mysql-server
```

(Optional) Now to configure mysql and set default options, run the included security script:
```
sudo mysql_secure_installation
```


##Testing
MySQL should have started running automatically. To test this, check its status:
```
service mysql status
```

If MySQL isn't running, you can start it with  ```sudo service mysql start```.

Now, you can connect to MySQL as root user with ``` mysql -u root -p```, finally you will prompted to type your password to enter in the database.

##Creation of the database
To create the database needed for the project, make sure you are in same same directory as create_database.sql, connect into MySQL (see above) and source the previous file: ``` source creation_database.sql ```

