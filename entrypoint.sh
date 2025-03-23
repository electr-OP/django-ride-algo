#!/bin/bash
if [ "$DB" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "Database started"
fi

echo "Collect static files"
python manage.py collectstatic --noinput
echo ====================================

echo "Creating Migrations..."
python manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Starting Server..."
daphne -b 0.0.0.0 -p 8060 ridesharing.asgi:application
exec "$@"