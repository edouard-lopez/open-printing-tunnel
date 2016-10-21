#!/bin/bash

echo "Usage: ./send_archive.sh [USER@HOSTNAME] [SSH_PORT]"

cd ..

HOST="${1:-coaxis@optbox-forward}"
SSH_PORT="${2:-2222}"

ssh -p $SSH_PORT $HOST 'mkdir -p ~/coaxisopt'
scp -P $SSH_PORT docker-compose.prod.yml "$HOST":~/
scp -P $SSH_PORT deploy/deploy.sh "$HOST":~/coaxisopt
ssh -p $SSH_PORT $HOST 'mv docker-compose.prod.yml ~/coaxisopt/docker-compose.yml'

cd deploy
