#! /usr/bin/env bash

# Let the DB start
python /usr/src/app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /usr/src/app/initial_data.py