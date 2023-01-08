# P12

Projet 12 : Créez une API sécurisée RESTful en utilisant Django REST

Ce projet a pour but de créer une API (EpicEvents) permettant aux utilisateurs autorisés de gérer l'application, d'accéder à l'ensemble des modèles et de vérifier la configuration de la base de données.
Les trois applications exploiteront les points de terminaison d'API qui serviront les données.

# Processus
## Framework : Django REST
Ce projet utilise le framework Django REST pour crée l'application Web.

Pour plus de détails sur le fonctionnement de cette API, se référer à sa documentation[https://documenter.getpostman.com/view/23795852/2s8Z75Spmu] (Postman).

# Utilisation

## Création de l'environnement virtuel

Pour la mise en palce de l'environnement virtuel :

## Sur Windows :
Dans le Windows Powershell il faudra cloner le git.
### Récupération du projet

    $ git clone https://github.com/erikia/P12.git

### Activer l'environnement virtuel
    $ cd P10 
    $ python -m venv env 
    $ ~env\scripts\activate
    
### Installer les modules
    $ pip install -r requirements.txt

### Executer le programme
Dans le répertoire qui contient manage.py dans le terminal, exécutez le programme:

    $ python manage.py migrate
    $ manage.py runserver

Puis ouvrez votre navigateur et allez sur la page suivante : http://127.0.0.1:8000/
    
----------------------------------------------
## Sur MacOS ou Linux :
Dans le terminal, il faudra cloner le git.
### Récupération du projet

    $ git clone https://github.com/erikia/P12.git

### Activer l'environnement virtuel
    $ cd P10
    $ python3 -m venv env 
    $ source env/bin/activate
    
### Installer les modules
    $ pip install -r requirements.txt

### Executer le programme
Dans le répertoire qui contient manage.py dans le terminal, exécutez le programme:

    $ python manage.py migrate
    $ manage.py runserver

Puis ouvrez votre navigateur et allez sur la page suivante : http://127.0.0.1:8000/
