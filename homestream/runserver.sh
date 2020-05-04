#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for database to start up."
    while ! nc -z $SQL_HOST $SQL_PORT; do
        echo "waiting for db"
        sleep 0.2
    done
    echo "Database started."
fi

python manage.py flush --no-input
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --no-input --clear
python manage.py createtestusers

# If the container has no entrypoint, it's the command: from docker-compose.yml.
# Any arguments after the image name in a docker run command, or the CMD from 
# the Dockerfile. If it does have an entrypoint 
# (entrypoint:, docker run --entrypoint ..., ENTRYPOINT), it's the entrypoint, 
# which gets passed the command as arguments.
exec "$@"