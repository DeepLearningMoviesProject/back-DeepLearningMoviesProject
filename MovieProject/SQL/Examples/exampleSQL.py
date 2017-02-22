#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:34:48 2017

@author: edwin
"""

from MovieProject.SQL.API.apiSQL import * #API pour communiquer avec la BDD
from MovieProject.SQL.API.User import * #Cette classe permet de stocker les informations d'un utilisateur de la BDD

try:
    
#PREMIERE FOIS: On crée une base de données
    createDB("bdd","w+") #On crée la base de données "bdd". On peut ajouter un attribut "w+"
                    # pour signaler si on overwrite la BDD "bdd" si elle existe déjà
                    #Si on ne veut pas overwrite: createDB("bdd")
                    
#A CHAQUE FOIS: Charger les données dans la BDD.
    loadDB("bdd","../Ressources/bdd.sql") #On charge dans "bdd" le fichier "bdd.sql"

#On peut maintenant utiliser notre BDD (vierge actuellement)

#SIMULATION RECUPERATION DONNEES UTILISATEURS DEPUIS LE FRONT-END
#On a récupéré les données d'un utilisateur ainsi que sa liste de films (id,avis) qu'il a noté
    elsa = User(1,"Elsa Navarro","bonjour@gmail.com","456sdsl","motdepasse")
#Note : Il faut ranger les avis d'un utilisateur dans un dictionnaire avec
# pour clé l'id du film et en valeur si il l'a aimé ou non (0 pour non, 1 pour oui)
    avisElsa = {20:1,10:0,12:0,15:1,22:1}
    
#On l'ajoute dans la BDD sans vérifier que les films sont dans la BDD ou non
    insertUser(elsa,avisElsa)

#Un deuxième et un troisième utilisateurs sont enregistrés, ceux-çi n'ont pas noté de films
    edwin = User(2,"Edwin Niogret","blabla@hotmail.com","dsd412tmdb","pw")
    julian = User(3,"Julian Hattinguais","python@live.com","dsd412tmdb","monmotdepasse")

#On les ajoute à la BDD
    insertUser(edwin)
    insertUser(julian)
    
#Elsa n'est pas content et veut changer son mot de passe et son nom
    elsa = User(1,"Elsa Dunand","bonjour@gmail.com","456sdsl","viveleweb")
    elsaId, elsaName, elsaMail, tmdbKey, pw = elsa.getInfo() #On récupère ses infos
    
#On update la BDD
#Note: On précise ce qu'on veut update, seul l'id est obligatoire et non modifiable     
    updateUser(elsaId, userName = elsaName, userPassword = pw) 
#DECONSEILLE : Si on veut update l'id, il faut supprimer l'utilisateur et on le refait (mais on perdra tout ses goûts (Table USERMOVIE) !!!)

#Récupérons la liste des utilisateurs de la BDD.
    result = getAllUsers()
    print("Methode : getAllUsers()")
    for u in result: #Affichage de tout les utilisateurs
        u.showInfo() 
    print("") 
       
#Si on ne veut pas les récupérer mais juste les afficher en console: On utilise:
    print("Methode : showAllUsers()")
    showAllUsers()
    print("")
    
#Elsa  a mis à jour sa liste de films notés, elle a enlevé sa note au film "20",
#Elle a changé d'avis sur le film 10 et 12 et elle a ajouté un avis sur le film 24
    avisElsa2 = {10:1,12:1,24:0}
    deletedMovie = 20
    
#Pour les modifications (sauf la suppression), il suffit d'envoyer les modifications à la BDD
    updateMoviesForUser(elsaId, avisElsa2)
    
#Pour la supression, il faut manuellement supprimer le film de ses goûts
    removeUserMovie(elsaId, deletedMovie)
    
#Maintenant regardons la liste des films que Elsa a noté
    result = getAllMoviesFromUser(elsaId) #Retourne un dictionnaire (K:id, V:avis(0 ou 1))
    print("Avis d'Elsa")
    keys = result.keys()
    for k in keys:
        print("IdFilm : " + str(k) + " Avis : " + str(result[k]))
    print("")
        
#Ajout de quelques données
    updateMoviesForUser(edwin.userId, {10:0,12:1,25:0,28:0})
    updateMoviesForUser(julian.userId, {10:1,12:0,25:1})
 
#Regardons l'avis de Julian sur le film 25
    result = getLike(julian.userId, 25)
    print("Avis de Julian sur le film 25: " + str(result))
    print("")
    
#Regardons qui a noté le film 10 et leurs avis
    result = getAllUsersFromMovie(10)
    print ("Avis sur le film 10")
    keys = result.keys()
    for k in keys:
        print("Utilisateur : " + str(k) +  " Avis : " + str(result[k]))
    print("")  
    
#Regardons qui a aimé le film 12
    result = getLikedUsersFromMovie(12)
    print("Utilisateurs ayant aimé le film 12")
    for r in result:
        print ("Utilisateur " + str(r))
    print("")
    
#Regardons qui n'a pas aimé le film 12
#Note: Il suffit d'ajouter la variable "liked = 0" pour récuper les films non aimés
    result = getLikedUsersFromMovie(12,0)
    print("Utilisateurs n'ayant pas aimé le film 12")
    for r in result:
        print ("Utilisateur " + str(r))
    print("")
    
#Finallement Elsa veut se supprimer, il suffit de faire:
#Note: Tout les liens avec ses films sont automatiquement supprimés
    removeUser(elsaId) 

#Affichons la liste des utilisateurs
    print("Methode : showAllUsers()")
    showAllUsers()
    print("")

#Récupérons la liste des films de la BDD
    result = getAllMovies()
    print("Liste des films de la bdd")
    for r in result:
        print ("Film " + str(r))
    print("")   
     
#Si on veut juste les afficher sans les récupérer:
    print("Methode : showAllMovies()")
    showAllMovies()
    
#Fin du programme, il faut maintenant sauvegarder la BDD.
    saveDB("bdd", "../Ressources/newbdd.sql")
    
except Exception as error:
    print('Error: ' + repr(error))        