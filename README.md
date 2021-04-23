# sustcast-core-v0
Just Another Radio Streaming Service


## required:
docker
docker-compose
ffmpeg
python3
virtualenv
pip
inotify-tools
audiotools

## steps:
prerequisite install
firebase.json file in core/
venv in core
create ices.log in ices-docker/log
create ices.xml in ices-docker/data
create chiron.db in database/dataset/chiron-dataset/
copy test1.ogg,test2.ogg from core/example_music/ to ices-docker/music and rename them currentA.ogg and currentB.ogg
run ices-docker to check everything ok -> docker-compose -f ices-docker/docker-compose.yml up -d

If ices-docker doesn't work as intended, View ices-docker/ices.log

## on startup:
gnome-terminal --working-directory=/home/sustcast/sustcast-core-v0/ -e "./start.sh"



#nltk
1. Open terminal(Linux).
2. sudo pip3 install nltk
3. python3
4. import nltk
5. nltk.download('all')
