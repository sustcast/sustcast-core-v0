#!/bin/bash
pkill -f start.sh
pkill -f Main.py
pkill -f file_checker.sh
docker-compose -f ices-docker/docker-compose.yml down