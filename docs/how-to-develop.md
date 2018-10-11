### Back-office

We are using a `docker-compose` to manage the various containers. See [how to docker](./docs/HOW-TO-DOCKER.md) for install and basics: 

    make first-run

:information_source:: You will be asked to create a super user.

Create the `coaxisopt_daemon` container so we can use it as template:

        cd daemon
        docker build -t coaxisopt_daemon .

After having create a `client` we will need to create a `daemon`

> ![creation d'un deamon de test](./screenshots/creation-d'un-deamon-de-test.png)

Finally **go to [http://localhost/](http://localhost/)**

### Front-office

    cd daemon/
    ./help-me.mk build dev

To locate where is the `daemon` container on the network:

    make where-is-front-office --silent
