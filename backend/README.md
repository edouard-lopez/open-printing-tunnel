
## Features

* liste des sites (basé sur les fichiers de conf) et leur état (en couleur) ;
* ajout / suppression de site-tunnel ;
* liste des imps par site (basé sur les fichiers de conf) ;
* ajout / suppression d'imprimante par site-tunnel ;
* la mise en forme et le style graphique pour ces pages sera réduite au minimum ;
* le code sera ouvert et documenté. ;
* l'ensemble devra être packagé pour une mise en place facile.

## Development setup

Refer to the [main project documetation for a quick introduction to virtualenv](../README.md) in Python.

### Database

* Create local database and apply migrations

        python3.5 ./manage.py migrate

* Create a super-user:

        python3.5 ./manage.py createsuperuser

* Run the tests:

        python3.5 ./manage.py test

* Run development server:

        python3.5 ./manage.py runserver
        
* Open browser and reach either http://127.0.0.1:8000/api/ or http://127.0.0.1:8000/admin/ 
 (as the `/` is managed by the [nginx](https://github.com/Coaxis-ASP/opt-nginx) and the [frontend](https://github.com/Coaxis-ASP/opt-frontend) components). 