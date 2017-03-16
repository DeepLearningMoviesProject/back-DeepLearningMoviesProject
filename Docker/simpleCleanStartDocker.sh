#!/bin/bash
#Script permettant de supprimer toutes les choses inutiles de Docker et de lancer directement le bash pour tester votre image
./deleteAllContainers.sh #Supprime tout les containers
docker rmi $(docker images | grep "^<none>" | awk "{print $3}") #Supprime toutes les images sans tag (<none>)
docker build -t testdocker . #Build
docker create --tty --interactive --name="latest_contener"  testdocker:latest 
docker start latest_contener
docker exec -it latest_contener bash
