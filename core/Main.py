import time
from scheduler import Scheduler
from utils import Constant
from utils import Helper
from utils import YoutubeUtils
from recommender_chiron import Chiron
from recommender_chiron import Observer
from utils import CsvUtils
import SongDownload
from shutil import copyfile
from firebase import FireBaseUtil
import logging
import requests
import json
import os
import traceback
import _thread

logging.basicConfig(filename='sustcast_error.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

'''
scheduling
number of listner update
'''

ENV_PATH = 'ENV/env.json'
LISTEN_URL = ''
FIREBASE_DB_URL = ''
YOUTUBE_API_KEY = ''
FIRBASE_CREDENTIAL_PATH = 'ENV/firebase.json'

TAG = '@MASTER>'

def load_environement_variables():
    global LISTEN_URL
    global FIREBASE_DB_URL
    global YOUTUBE_API_KEY

    f = open(ENV_PATH,) 
    env = json.load(f) 
    f.close()   

    LISTEN_URL = env['icecast_urls'][0]
    YOUTUBE_API_KEY = env['youtube_api_key']
    FIREBASE_DB_URL = env['firebase_database_url']


def initThreads():
    print(TAG, "WORKERS INITIALIZING")
    try:
        _thread.start_new_thread(run_emergency_programs, ())
    except:
        print("Error: unable to start newsFetcher thread")
    

def run_emergency_programs():
    global BLOCK_ICECAST_WATCHER

    path = "content/emergency_program"

    time.sleep(60)
    print(TAG, "EMERGENCY PROGRAM WATCHER")

    while(True):    
        elements = os.listdir(path)

        for element in elements:
            if element.find(".mp3") >= 0:

                print(TAG," --- emergency program --- ")
                
                instant_program = {
                    "title_show" : element.replace(".mp3",""),
                    "file" : path+'/'+element
                }

                SongDownload.downloadOgg(instant_program)

                current_music_file = Helper.findLastPlayedFile()
                if( current_music_file.find("A") < 0 ):
                    copyfile(Constant.default_ogg_download_path, Constant.currentA_path)
                else:
                    copyfile(Constant.default_ogg_download_path, Constant.currentB_path)

                os.remove(path+'/'+element)

                skip_to_next_track()

        time.sleep(60)

            

def setModules():
    Chiron.set_modules(YoutubeUtils,Helper)
    Scheduler.set_recommender(Chiron)
    Scheduler.set_modules(Helper,CsvUtils)
    Observer.set_modules(CsvUtils,YoutubeUtils)
    YoutubeUtils.set_modules(Helper,YOUTUBE_API_KEY)
    FireBaseUtil.initialize(FIREBASE_DB_URL,FIRBASE_CREDENTIAL_PATH)

def skip_to_next_track():
    os.system('docker exec -it ices_sustcast kill -SIGHUP 1')


def start_ices():
    os.system('docker-compose -f ../ices-docker/docker-compose.yml down')
    os.system('docker-compose -f ../ices-docker/docker-compose.yml up -d')
    
    time.sleep(10)

def getTitleFromIceCast():
    global BLOCK_ICECAST_WATCHER

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
        getTitleFromIceCast()

    if server_stat == {}:
        print(TAG, "server off")
        start_ices()
        getTitleFromIceCast()
    
    else:
        return server_stat['title']
        


def setTitleInFirebase(title):
    data = {
        'title_show':title
    }

    FireBaseUtil.put_artist_title(data)


first_load = True
next_music = {}
prev_music = {}

def main():

    global next_music
    global prev_music
    global first_load

    current_title = getTitleFromIceCast()
    setTitleInFirebase(current_title)
    
    current_music_file = Helper.findLastPlayedFile()

    next_music = Scheduler.shuffle()

    if first_load == True:
        prev_music = next_music
        first_load = False

    else:
        while next_music["title_show"].find(prev_music["title_show"]) >= 0:
            next_music = Scheduler.shuffle()

    while SongDownload.downloadOgg(next_music) == False:
        next_music = Scheduler.shuffle()
    
    print(next_music)
    
    
    if( current_music_file.find("A") < 0 ):
        copyfile(Constant.default_ogg_download_path, Constant.currentA_path)
    else:
        copyfile(Constant.default_ogg_download_path, Constant.currentB_path)

    server_title = getTitleFromIceCast()
    while current_title.find(server_title) >= 0 and len(server_title) == len(current_title) and current_music_file.find(Helper.findLastPlayedFile()) == 0:
        time.sleep(5)
        server_title = getTitleFromIceCast()
        
    prev_music = next_music



if __name__ == '__main__':
    
    load_environement_variables()
    setModules()
    initThreads()
    while True:
        try: 
            main()
        except Exception as err :
            traceback.print_exc()
            logger.error(err)
