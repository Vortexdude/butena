#! /usr/bin/env bash

# Let the DB start
#python3 app/pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python3 app/server.py
