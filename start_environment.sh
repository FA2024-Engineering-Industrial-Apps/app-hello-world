#!/bin/bash

# This scripts starts the example environment by starting all docker containers in detached mode.
docker compose -f src/mqtt_broker_mosquitto/docker-compose.yml up -d
docker compose -f src/node_red/docker-compose.yml up -d
docker compose -f src/my_edge_app/docker-compose.yml up -d

docker ps