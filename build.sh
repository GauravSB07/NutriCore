#!/usr/bin/env bash
set -o errexit
set -x

echo "Installing requirements..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --verbosity 3

echo "Checking files..."
ls -la

echo "Loading data..."
python manage.py loaddata data.json --verbosity 3

echo "Collecting static..."
python manage.py collectstatic --noinput

echo "BUILD FINISHED"