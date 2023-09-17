#!/bin/ash

echo "Apply database makemigrations"
python manage.py makemigrations 

echo "Apply database migrations"
python manage.py migrate 

# Execute the command passed as arguments
exec "$@"
