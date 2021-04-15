#!/bin/bash

while ! inotifywait -e modify program_schedule.csv; do 
	pkill -f start.sh
	pkill -f Main.py
	bash /home/ubuntu/Workspace/sustcast-core-v0/startTest.sh &
done
