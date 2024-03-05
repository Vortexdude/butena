#! /usr/bin/env bash

# export the app directory
export PYTHONPATH=$PWD

# Run migrations
alembic upgrade head

# Create initial data in DB
python3 app/server.py
