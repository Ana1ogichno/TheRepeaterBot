#! /usr/bin/env bash

# Up infrastructure by docker-compose
docker compose up --build -d

# Init
python3 -m scripts.initial_data

# Start bot
python3 main.py
