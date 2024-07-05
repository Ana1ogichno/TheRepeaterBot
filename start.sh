#! /usr/bin/env bash

# Up infrastructure by docker-compose
#docker compose up --build -d

# Init
python3 src/scripts/initial_data.py

# Start bot
python3 main.py
