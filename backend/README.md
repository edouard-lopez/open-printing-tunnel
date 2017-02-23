## Development setup

Refer to the [main project documetation for a quick introduction to virtualenv](../README.md) in Python.

### Database

* Create local database and apply migrations

        python3.5 ./manage.py migrate

* Create a super-user:

        python3.5 ./manage.py createsuperuser

* Run the tests:

        cd backend/
        export DEFAULT_INTERFACE=${interface:=wlp4s0}
        python3.5 ./manage.py test

* Run development server:

        python3.5 ./manage.py runserver
        
* Open browser and reach either http://127.0.0.1:8000/api/ or http://127.0.0.1:8000/admin/ 
 (as the `/` is managed by the [nginx](https://github.com/Coaxis-ASP/opt-nginx) and the [frontend](https://github.com/Coaxis-ASP/opt-frontend) components). 