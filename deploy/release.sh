#!/usr/bin/env bash
# DESCRIPTION
#       Build backoffice front-end, frontoffice front-end and
# USAGE:
#       ./release.sh v1.5.6
#   or
#       ./release.sh

onexit(){ while caller $((n++)); do :; done; }
trap onexit EXIT

TAG="${1:-latest}"
DEFAULT_INTERFACE="${2:-ens192}"

function usage() {
    printf "Usage: ./release.sh [tag]\n\n"
}

function build_frontoffice_frontend() {
    cd ../daemon/frontend/
    yarn build
}

function build_backoffice_frontend() {
    cd ../../frontend/
    yarn build
}

function build_images() {
    cd ..
    docker-compose build
    cd daemon
    docker build \
        --pull \
        --cache-from coaxisasp/coaxisopt_daemon \
        --tag coaxisopt_daemon .
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

function build_and_push() {
    local tag="${1}"
    docker_images=(
        'coaxisopt_daemon'
        'coaxisopt_nginx'
        'coaxisopt_frontend'
        'coaxisopt_backend'
    )

    # see http://stackoverflow.com/a/4017175/802365 and http://stackoverflow.com/a/6828383/802365
    tag_images docker_images[@] "$tag"
    push_images docker_images[@] "$tag"

    tag_images docker_images[@] "latest"
    push_images docker_images[@] "latest"
}

usage
build_frontoffice_frontend
build_backoffice_frontend
build_images
build_and_push "$TAG"
printf "\nRun\n\tdeploy/send-scripts.sh\n"
printf "\nThen, on the host machine, pull new containers releases with:\n\n\tdeploy/deploy.sh\n\n"
