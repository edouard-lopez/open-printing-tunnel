#!/bin/bash
echo "Usage: ./deploy.sh [TAG [DEFAULT_INTERFACE]]"

DEFAULT_INTERFACE="${2:-ens192}"
export DEFAULT_INTERFACE
export COMPOSE_HTTP_TIMEOUT=600

docker_tags=(
    'latest'
    "$1"
)

function pull_images() {
    declare -a tags=("${!1}")

    docker-compose pull
    for tag in ${tags[@]}; do
        docker pull docker.akema.fr:5000/coaxis/coaxisopt_daemon:"$tag"
    done
}

function clean_images() {
    docker rmi $(docker images -f "dangling=true" -q)
}

function restart() {
    docker-compose down
    docker-compose up -d
}

# see http://stackoverflow.com/a/4017175/802365 and http://stackoverflow.com/a/6828383/802365
pull_images docker_tags[@]
restart
clean_images