#!/bin/bash
echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Starting Server..."

uwsgi --ini uwsgi.ini