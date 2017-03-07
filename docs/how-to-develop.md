We are using a `docker-compose` to manage the various containers. See [how to docker](./docs/HOW-TO-DOCKER.md) for install and basics: 

    cd open-printing-tunnel-master/  # project root directory
    docker-compose build  # create the containers images 
    docker-compose up  # start project

Then you need to add a super user to the backend if none exists:

    docker exec -it coaxisopt_backend bash
    ./manage.py createsuperuser

Finally go to [http://localhost/](http://localhost/)