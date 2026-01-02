#!/bin/bash

set -o errexit

set -o pipefail

set -o nounset

python manage.py migrate --no-input
python manage.py collectstatic --no-input
exec python manage.py runserver 0.0.0.0:8000

#exec gunicorn config.wsgi:application \
 #    --bind 0.0.0.0:8000 \
 #    --workers 3 \
 #    --timeout 120 \
 #    --log-level info