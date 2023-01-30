#!/bin/bash

action=$1


prestart() {
    printf "\n-- init prestart -----------------------\n"

    # Execute migrations
    alembic upgrade head

    # Create default scopes
    python manage.py core create-default-scopes

    # Create super user
    python manage.py core create-superuser

    # Insert initial data
    python manage.py universities insert-initial-data

    printf "\n-- finish prestart -----------------------\n"
}


build_img() {
    version=$1
    [ -z "$version" ] && version=0.1 && echo "\nset defaul version 0.1\n"

    docker build --no-cache -t crissalvarezh/ubicor-api:$version .

    docker tag crissalvarezh/ubicor-api:$version crissalvarezh/ubicor-api:latest
}


if [ "$action" = "start" ]; then
    prestart

    uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 80

elif [ "$action" = "dev" ]; then
    uvicorn app.main:app --reload

elif [ "$action" = "prestart" ]; then
    prestart

elif [ "$action" = "build" ]; then
    build_img "$2"

elif [ "$action" = "publish" ]; then
    build_img "$2"

    docker push crissalvarezh/ubicor-api:$version
    docker push crissalvarezh/ubicor-api:latest

elif [ "$action" = "deploy" ]; then

  ssh -o StrictHostKeyChecking=no \
      -i ./server-key.pem ec2-user@alvarezcristian.com \
      "cd /home/ec2-user/cristian-server-projects && make reload service=ubicor-api"

fi

