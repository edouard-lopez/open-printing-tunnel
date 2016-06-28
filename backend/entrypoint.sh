#!/bin/sh

python manage.py migrate
python manage.py loaddata groups.json
python manage.py loaddata companies.json
python manage.py collectstatic --clear --no-input

exec "$@"