#!/usr/bin/env bash
# DESCRIPTION
#       Build backoffice front-end, frontoffice front-end and
# USAGE:
#       ./release.sh v1.5.6
#   or
#       ./release.sh

TAG="${1:-latest}"
DEFAULT_INTERFACE="${2:-ens192}"

function usage() {
    printf "Usage: ./release.sh [tag]\n\n"
}

function build_vps_frontend() {
    cd ../daemon/frontend/
    npm run build
}

function build_backoffice_frontend() {
    cd ../../frontend/
    npm run build
}

function build_and_push() {
    local tag="${1}"

    cd ../deploy/
    ./build_and_push.sh "$tag"
    ./build_and_push.sh
    ./send-scripts.sh
}

function deploy_on_remote() {
    local interface="${1}"
    local tag="${2}"

    ssh \
        -p 2222 \
        coaxis@optbox-forward \
        bash -c "/home/coaxis/coaxisopt/deploy.sh "${interface}" "${tag}""
}

usage
build_vps_frontend
build_backoffice_frontend
build_and_push "$TAG"
#deploy_on_remote "${DEFAULT_INTERFACE}" "${TAG}""