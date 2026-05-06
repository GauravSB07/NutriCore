#!/usr/bin/env bash
set -o errexit
set -x

echo "Installing requirements..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --verbosity 3

echo "Loading data..."
python manage.py loaddata data.json --verbosity 3

echo "Creating superuser..."
python manage.py shell << END
from django.contrib.auth.models import User
import os

username = os.environ.get("ADMIN_USERNAME")
email = os.environ.get("ADMIN_EMAIL")
password = os.environ.get("ADMIN_PASSWORD")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
END

echo "Collecting static..."
python manage.py collectstatic --noinput