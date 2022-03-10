#!/bin/bash

set -e

echo "${0}: running migrations."
python manage.py makemigrations --merge
python manage.py migrate --noinput

echo "${0}: collecting statics."
python manage.py collectstatic --noinput

echo "${0}: Dumping data into tables in DB created."
python manage.py loaddata updated_db_data.json

cp -rv static/* static_shared/

echo "${0}: Running server..."
python manage.py runserver 0.0.0.0:8000