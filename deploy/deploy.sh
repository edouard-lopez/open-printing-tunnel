#!/bin/bash

echo "Usage: ./deploy.sh [DEFAULT_INTERFACE]"

DEFAULT_INTERFACE="${1:-ens192}"

export DEFAULT_INTERFACE

export COMPOSE_HTTP_TIMEOUT=600

# pull new images
docker-compose pull
docker pull docker.akema.fr:5000/coaxis/coaxisopt_daemon:latest

# restart container
docker-compose down
docker-compose up -d
docker rmi $(docker images -f "dangling=true" -q)
