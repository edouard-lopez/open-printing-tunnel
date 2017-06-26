#!/usr/bin/env bash
# DESCRIPTION
#       Build docker images, tag them and push to registry
# USAGE:
#       ./build_and_push.sh v1.5.6
#   or
#       ./build_and_push.sh

onexit(){ while caller $((n++)); do :; done; }
trap onexit EXIT

TAG="${1:-latest}"

function usage() {
    printf "Usage: ./build_and_push.sh [tag]\n\n"
}

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
    tag="$2"

    for image in "${images[@]}"; do
        docker tag "$image" coaxisasp/"$image":"$tag"
    done
}

# Push all tagged images
function push_images() {
    declare -a images=("${!1}")
    tag="$2"

    for image in "${images[@]}"; do
        docker push coaxisasp/"$image":"$tag"
    done
}


docker_images=(
    'coaxisopt_daemon'
    'coaxisopt_nginx'
    'coaxisopt_frontend'
    'coaxisopt_backend'
)

usage
build_images
# see http://stackoverflow.com/a/4017175/802365 and http://stackoverflow.com/a/6828383/802365
tag_images docker_images[@] "$TAG"
push_images docker_images[@] "$TAG"
