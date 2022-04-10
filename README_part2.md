# TECHNIQUES WEB - PROJET 2

Ce projet a été réalisé dans le cadre du cours Technique Web dirigé par M. Elvis Mboning, du Master Traitement Automatique des Langues de l'INALCO.

Groupe 1 : Elise LINCKER, Lufei LIU, Alexandra PONOMAREVA

## Description du projet

Le projet consiste à rendre accessible l'API Back-End développé au cours du projet 1 au moyen d'une interface web. 

## Documentation

## 1. Mise en place d'un environnement de développement

- Création d'un environnement virtuel pour le projet

  ```bash
  pip install pipenv # Installer pipenv
  cd RESTful-API # Entrer dans le dossier de travail
  pyhon3.8 -m pipenv --python 3.8 # Créer un environnement virtuel
  python3.8 -m pipenv shell # Lancer l'environnement virtuel
  pip install -r requirements.txt # Installer les dépendances
  ```

## 2. Arboresence du dossier

├── projet_techniques_web
│   ├── back (Dossier API Back-end)
│   │   └── app.py (Configuration API Back-end)
│   │   ├── data
│   │   │   └── DataViewer.db (Base de données COVID)
│   │   ├── lib
│   │   │   └── scheduler.py (module pour programmer la mise à jour des données)
│   │   │   ├── synchronisation.py (module pour la synchronisation des données)
│   │   │   ├── utils.py (module pour la création de token)
│   │   ├── models
│   │   │   └── covid.py (module création d'un objet DataCovidModel)
│   │   │   ├── db.py (module initialisation de la base de données)
│   │   │   ├── user.py (module création d'un objet User)
│   │   ├── resources
│   │   │   └── covid.py (module création des routes permettant d'ajouter, consulter, supprimer, modifier des données COVID)
│   │   │   ├── user.py (module création des routes permettant la création et la connexion des utilisateurs)
│   ├── front
│   │   ├── app.py  (Configuration API Front-end)
│   │   ├── models
│   │   │   └── api.py (module permettant de connecter le Front-end au Back-end)
│   │   ├── ressources
│   │   │   └── covid.py (module création des routes permettant d'ajouter, consulter, supprimer, modifier des données COVID)
│   │   │   ├── user.py (module création des routes permettant la création et la connexion des utilisateurs)
│   │   ├── static (style CSS)
│   │   ├── templates (modèles des pages HTML)
│   ├── start_app.py (programme permettant de lancer l'application)
│   ├── wsgi.py (programme permettant de lancer le Back-end avec Gunicorn)
│   ├── wsgi_front.py (programme permettant de lancer le Front-end avec Gunicorn)
│   ├── tests.py (tests unitaires)
│   └── requirements.txt (fichier des dépendances)

## 3. Lancement de l'application

#### Avec python

python3 start_app.py

#### Avec Gunicorn:

```bash
pip install gunicorn # installer gunicorn
gunicorn --bind dataviewer.api.localhost:5000 wsgi:dataviewerBack # lancer le Back-End sur gunicorn
gunicorn --bind dataviewer.localhost:5000 --workers 3 --timeout 120 wsgi_front:dataviewerFront # lancer le Front-End sur gunicorn
```

URL d'accès Front-End :
http://dataviewer.localhost:5000/

URL d'accès Back-End :
http://dataviewer.api.localhost:5000/



## 4. Utilisation Front-End

L'utilisateur peut s'inscrire en fournissant un nom d'utilisateur, un adresse mail et un mot de passe via url suivant:
http://dataviewer.localhost:5000/register

L'utilisateur peut se connecter avec son adresse mail et son mot de passe via url suivant :
http://dataviewer.localhost:5000/login

L'utilisateur peut se déconnecter via url suivant:
http://dataviewer.localhost:5000/logout

L'accès aux données est ouvert à tout le monde, cependant, seuls les utilisateurs connectécs sont autorisés à effectuer des actions sur ces données. Les actions autorisées sont : modification, ajout, suppression
Consultation des données : http://dataviewer.localhost:5000/covid/data
Modification d'une donnée en fournissat l'identifiant de la donnée : http://dataviewer.localhost:5000/covid/data/update
Suppression d'une donnée en fournissant l'identifiant de la donnée : http://dataviewer.localhost:5000/covid/data/delete
Création d'une donnée en fournissant toutes les informations demandées : http://dataviewer.localhost:5000/covid/data/new

## 5. Client web (postman)

Est utilisé le client web Postman. URL vers la documentation : https://documenter.getpostman.com/view/16846441/UVyn1JaA
