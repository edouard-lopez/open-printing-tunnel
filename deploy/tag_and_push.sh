#!/usr/bin/env bash
onexit(){ while caller $((n++)); do :; done; }
trap onexit EXIT
#set -x  # debug

function build_images() {
    cd ..
    docker-compose build
    cd daemon
    docker build -t coaxisopt_daemon .
    cd ..
}

# Tag all images
function tag_images() {
    declare -a images=("${!1}")
    declare -a tags=("${!2}")

    for image in ${images[@]}; do
        for tag in ${tags[@]}; do

            docker tag "$image" docker.akema.fr:5000/coaxis/"$image":"$tag"
        done
    done
}

# Push all tagged images
function push_images() {
    declare -a images=("${!1}")
    declare -a tags=("${!2}")

    for image in ${images[@]}; do
        for tag in ${tags[@]}; do
            docker push docker.akema.fr:5000/coaxis/"$image":"$tag"
        done
    done
}


docker_images=(
    'coaxisopt_daemon'
    'coaxisopt_nginx'
    'coaxisopt_frontend'
    'coaxisopt_backend'
)
docker_tags=(
    'latest'
    "$1"
)
build_images
# see http://stackoverflow.com/a/4017175/802365 and http://stackoverflow.com/a/6828383/802365
tag_images docker_images[@] docker_tags[@]
push_images docker_images[@] docker_tags[@]
