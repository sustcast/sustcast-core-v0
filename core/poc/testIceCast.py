import requests
import json
import os

LISTEN_URL = 'http://103.84.159.230:8000/sustcastTEST.ogg'
TAG = '@ICESMASTER>'

def start_ices():
    os.system('docker-compose -f ../../ices-docker/docker-compose.yml down')
    os.system('docker-compose -f ../../ices-docker/docker-compose.yml up -d')

response = requests.get('http://103.84.159.230:8000/status-json.xsl').text  
data = json.loads(response)

server_stat = {}
if 'source' in data['icestats'].keys():
    if type(data['icestats']['source']) == dict:
        server_stat = data['icestats']['source']
        if server_stat['listenurl'] != LISTEN_URL:
            server_stat = {}

    elif type(data['icestats']['source']) == list:
        for source in data['icestats']['source']:
            if source['listenurl'] == LISTEN_URL:
                server_stat = source
                break
else:
    print(TAG, "server off")
    start_ices()

if server_stat == {}:
    print(TAG, "server off")
    start_ices()
else:
    latest_music = json.dumps(server_stat['artist'])
    print(server_stat['title'])
    print(latest_music)