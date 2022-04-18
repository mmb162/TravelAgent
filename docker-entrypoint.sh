#!/bin/bash

sleep 4
python3 manage.py collectstatic --noinput # default to yes
python3 manage.py migrate
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver 0.0.0.0:8000

