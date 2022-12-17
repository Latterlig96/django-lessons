#!/bin/bash


# Section 1- Bash options
set -o errexit  
set -o nounset

# Section 3- Idempotent Django commands  
python manage.py collectstatic --noinput  
python manage.py makemigrations  
python manage.py migrate

gunicorn --reload --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS} --worker-class eventlet --log-level INFO --access-logfile "-" --error-logfile "-" ${DJANGO_WSGI_GATEWAY}
