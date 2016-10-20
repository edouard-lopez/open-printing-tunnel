#!/usr/bin/env bash
# USAGE:
#       ./release.sh v1.5.6
#   or
#       ./release.sh

TAG="${1:-latest}"
DEFAULT_INTERFACE="${2:-ens192}"

cd ../daemon/frontend/ ;
npm run build

cd ../../deploy/ ;
./tag_and_push.sh "$TAG"
./send_archive.sh

ssh -p 2222 coaxis@192.168.2.246 coaxisopt/deploy.sh $DEFAULT_INTERFACE "$TAG"
