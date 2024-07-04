#! /usr/bin/env bash

# Up infrastructure by docker-compose
docker compose up --build -d

# Init
python3 ./scripts/initial_data.py
