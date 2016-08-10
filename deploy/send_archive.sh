#!/bin/bash

if (( $# < 1 )); then
  >&2 echo "Usage: source send_archive.sh opt-vX.X.X.zip [hostname]"
  exit 1
fi

FILENAME="$1"
SERVER_IP="${2:-192.168.2.231}"
echo "send archive on the server"
scp -P 2222 $FILENAME coaxis@"$SERVER_IP":/home/coaxis
scp -P 2222 deploy.sh coaxis@"$SERVER_IP":/home/coaxis
rm $FILENAME
