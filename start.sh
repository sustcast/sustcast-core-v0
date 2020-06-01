#!/bin/bash
cd ices-docker
docker-compose up -d
cd ..

cd core/
source venv/bin/activate
python Main.py
cd ..

cd ices-docker
docker-compose down

