#!/usr/bin/env bash
# USAGE:
#       ./release.sh v1.5.6
#   or
#       ./release.sh

TAG="${1:-latest}"
DEFAULT_INTERFACE="${2:-ens192}"

cd ../
cd daemon/frontend/ ;
npm run build

cd ../../
cd frontend/ ;
npm run build

cd ../deploy/ ;
./tag_and_push.sh "$TAG"
./send_archive.sh

ssh -p 2222 coaxis@optbox-forward /home/coaxis/coaxisopt/deploy.sh $DEFAULT_INTERFACE "$TAG"
