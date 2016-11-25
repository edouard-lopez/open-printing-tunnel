#!/bin/bash
# DESCRIPTION
#       Pull and restart latest or given tag on the machine.

echo "Usage: ./deploy.sh [DEFAULT_INTERFACE [TAG]"

DEFAULT_INTERFACE="${1:-ens192}"
TAG="${2:-latest}"

export DEFAULT_INTERFACE
export COMPOSE_HTTP_TIMEOUT=600


function pull_images() {
    docker-compose pull
    docker pull docker.akema.fr:5000/coaxis/coaxisopt_daemon:"$TAG"
}

function clean_images() {
    docker rmi "$(docker images -f "dangling=true" -q)"
}

function restart() {
    docker-compose down
    docker-compose up -d
}

pull_images
restart
clean_images
