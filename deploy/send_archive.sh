#!/bin/bash

if (( $# != 1 ))
then
  echo "Usage: source send_archive.sh opt-vX.X.X.zip"
  return 1
fi

FILENAME="$1"
echo "send archive on the server"
scp -P 2222 $FILENAME coaxis@192.168.2.231:/home/coaxis
scp -P 2222 deploy.sh coaxis@192.168.2.231:/home/coaxis
rm $FILENAME
