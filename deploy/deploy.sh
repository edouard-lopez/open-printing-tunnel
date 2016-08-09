#!/bin/bash

if (( $# != 1))
then
  echo "Usage: source deploy.sh opt-vX.X.X.zip"
  return 1
fi

BACKUP_DIR="old.opt"
if [ -d "$BACKUP_DIR" ]
then
    rm -rf "$BACKUP_DIR"
fi

SRC="opt"
mv $SRC $BACKUP_DIR

ARCHIVE="$1"
unzip $ARCHIVE -d $SRC

cd $SRC
export COMPOSE_HTTP_TIMEOUT=600
docker-compose -f docker-compose.yml -f docker-compose.prod.yml rm -f
docker-compose -f docker-compose.yml -f docker-compose.prod.yml pull
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

mkdir -p sources
mv $ARCHIVE sources


cd daemon
docker build -t coaxisopt_daemon .
docker rmi $(docker images -f "dangling=true" -q)
cd ..

cd ..