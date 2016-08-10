#!/bin/bash

cd ..

LAST_TAG=$(git describe --abbrev=0 --tags)
CURRENT_TAG=$(git describe --tags HEAD)

if [ "$LAST_TAG" != "$CURRENT_TAG" ]; then
    >&2 echo "warning project is not tagged properly"
fi

FILENAME="opt-$LAST_TAG.zip"
if [[ -f $FILENAME ]]; then
    echo "delete previous archive $FILENAME"
    rm $FILENAME
fi

echo "create archive"
git archive -o $FILENAME HEAD
mv $FILENAME deploy

cd deploy
echo "$FILENAME"  # so we can chain method
