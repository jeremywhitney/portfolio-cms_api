#!/bin/bash

rm db.sqlite3
rm -rf ./portfoliocmsapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations portfoliocmsapi
python3 manage.py migrate portfoliocmsapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

