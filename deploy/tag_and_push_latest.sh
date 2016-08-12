#!/usr/bin/env bash

cd ..
docker-compose build
docker tag coaxisopt_daemon docker.akema.fr:5000/coaxis/coaxisopt_daemon:latest
docker tag coaxisopt_nginx docker.akema.fr:5000/coaxis/coaxisopt_nginx:latest
docker tag coaxisopt_frontend docker.akema.fr:5000/coaxis/coaxisopt_frontend:latest
docker tag coaxisopt_backend docker.akema.fr:5000/coaxis/coaxisopt_backend:latest

docker push docker.akema.fr:5000/coaxis/coaxisopt_daemon:latest
docker push docker.akema.fr:5000/coaxis/coaxisopt_nginx:latest
docker push docker.akema.fr:5000/coaxis/coaxisopt_frontend:latest
docker push docker.akema.fr:5000/coaxis/coaxisopt_backend:latest
cd deploy