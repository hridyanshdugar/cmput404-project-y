#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py spectacular --file schema.yml   
python3 manage.py migrate
python3 manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:9000 backend.wsgi:application --env SCRIPT_NAME=/api
