#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate   
gunicorn --bind 0.0.0.0:9000 backend.wsgi:application --env SCRIPT_NAME=/api
