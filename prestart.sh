#!/bin/bash

echo "\n-- init prestart -----------------------\n"

# Execute migrations
alembic upgrade head

# Create super user
python manage.py core create-superuser

# Insert inicial data
python manage.py universities insert-initial-data

echo "\n-- finish prestart -----------------------\n"