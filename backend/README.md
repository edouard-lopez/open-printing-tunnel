
## Features

* liste des sites (basé sur les fichiers de conf) et leur état (en couleur) ;
* ajout / suppression de site-tunnel ;
* liste des imps par site (basé sur les fichiers de conf) ;
* ajout / suppression d'imprimante par site-tunnel ;
* la mise en forme et le style graphique pour ces pages sera réduite au minimum ;
* le code sera ouvert et documenté. ;
* l'ensemble devra être packagé pour une mise en place facile.

## Development setup

### Requirement

* Python `3.5` ;
* (`Pip` should be [available](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip)).

### Installation

* [Create a Python virtual environement](https://docs.python.org/3.5/library/venv.html#creating-virtual-environments) ;

        cd backend/
        python3.5 -m venv .env
    
* [activate the virtual env](https://packaging.python.org/en/latest/installing/#creating-virtual-environments)

        source .env/bin/activate
        
* install project's requirements:
    
        python3.5 -m pip install -r requirements.txt
        
* Create local database and apply migrations

        python3.5 ./manage.py migrate

* Create a super-user:

        python3.5 ./manage.py createsuperuser
        
* Run development server:

        python3.5 ./manage.py runserver
        
* Open browser in http://127.0.0.1:8000/.