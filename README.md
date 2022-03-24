## TECHNIQUES WEB - PROJET 1

Ce projet a été réalisé dans le cadre du cours Technique Web dirigé par M. Elvis Mboning, du Master Traitement Automatique des Langues de l'INALCO.

Groupe 1 : Alexandra PONOMAREVA, Lufei LIU, Elise LINCKER

# Description du projet

Le projet consiste en la mise en place d'une application Back-End pour l'entreprise DataViewer, pour répondre à l'appel à projet du gouvernement suivant : ref : 30232RD3/CO/EDU/2022, pour traiter et rendre disponible des données publiques sur la Covid-19 afin de mieux informer les populations sur l’évolution de la pandémie.

# Objectif du projet :

Cette application Back-End est développée avec la librairie Python Flask et déployée sur Heroku. Les données du client sont accessibles sur Postman.

L'application doit répondre aux critères suivants :

- L'application doit permettre aux populations de consulter les données sur la vaccination par commune.
- Ces données sont mises à jour chaque jour, par une synchronisation des données.
- Les populations peuvent contribuer à ces ressources en effectuant les actions suivantes : créer, modifier et supprimer.
- Ces opérations nécessitent une connexion préalable.
- L'application doit être sécurisée.
- L’application doit être hébergée sur un serveur local et accessible via une URL (dataviewer.api.localhost).

Nos missions en tant qu'employés de l'entreprise DataViewer sont les suivantes :

- Mettre en place un environnement de développement web pour cette application.
- Développer l’application Back-End (REST API via méthodes HTTP) avec la librairie Python Flask pour exploiter les données du client et les rendre accessibles sur un client web (Postman)
- Déployer cette application sur Heroku
- Documenter le travail

## Installation

Pour installer les dépendances :
pip install -r requirements.txt

Pour mettre à jour les dépendances :
pip freeze > requirements.txt

## Utilisation

Pour lancer l'application :
python3 app.py

URL d'accès :
