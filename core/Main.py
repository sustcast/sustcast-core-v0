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

def initThreads():
    print("just for later use")
    '''
    try:
        _thread.start_new_thread(newsFetcher, ())
    except:
        print("Error: unable to start newsFetcher thread")
    '''

def setModules():
    Scheduler.set_recommender(Chiron)
    Observer.set_modules(CsvUtils,YoutubeUtils)



setModules()
first_load = True

while True :

    current_music = Helper.findLastPlayedFile()
    
    next_music = Scheduler.shuffle()

    if first_load == True:
        prev_music = next_music
        first_load = False

    else:
        while next_music["url"].find(prev_music["url"]) >= 0:
            next_music = Scheduler.shuffle()

    next_music["yt_title"] = YoutubeUtils.getTitleFromId(next_music['url'].replace("https://www.youtube.com/watch?v=",""))
    next_music["title_show"] = Helper.ytVideoTitleFilter(next_music["yt_title"])
    print(next_music)
    
    SongDownload.downloadOgg(next_music)

    if( current_music.find("A") < 0 ):
        copyfile(Constant.default_ogg_download_path, Constant.currentA_path)
    else:
        copyfile(Constant.default_ogg_download_path, Constant.currentB_path)

    

    check = 0
    while current_music.find(Helper.findLastPlayedFile()) >= 0:
        if check == 0:
            time.sleep(prev_music['duration'] - 60)
        else:
            time.sleep(10)
        
        check = check + 1
    
    FireBaseUtil.put_artist_title(next_music)

    prev_music = next_music







    



