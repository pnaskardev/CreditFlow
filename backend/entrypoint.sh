#!/bin/ash

echo "Apply database migrations"
python manage.py migrate 

# Execute the command passed as arguments
exec "$@"
