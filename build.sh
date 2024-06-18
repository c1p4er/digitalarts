#!/usr/bin/env bash

set -o errexit # exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-output

python manage.py migrate