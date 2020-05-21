#!/bin/bash
cd ices-docker
docker-compose up -d
cd ..

cd core/
source venv/bin/activate
python main.py
cd ..

cd ices-docker
docker-compose down

