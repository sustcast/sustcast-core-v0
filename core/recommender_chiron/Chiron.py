import importlib.util
import random
import time
import datetime as dt
import _thread
import math
from recommender_chiron import Observer

TAG = "@CHIRON>"
observer_flag = False

def set_modules(YTUtils,HelperMod):
    global YoutubeUtils
    global Helper

    YoutubeUtils = YTUtils
    Helper = HelperMod

def observe():

    while True:
        Observer.observe()
        
        cur = dt.datetime.now()
        mid_night = dt.datetime(cur.year,cur.month,cur.day,23,59,59)

        wait_time = 24*3600
        time.sleep(wait_time)

def music_importer():

    while True:
        Observer.importMusicsFromCsv()
        
        wait_time = 60
        time.sleep(wait_time)



def initObserver():
    try:
        _thread.start_new_thread(observe, ())
        _thread.start_new_thread(music_importer, ())
    except Exception as e:
        print(e)
        print(TAG,"observer thread init failed")
    


def recommend():
    global observer_flag

    if observer_flag != True:
        initObserver()
        observer_flag = True

    dataset = Observer.get_all_music_yt_data()

    score_model = []
    for music in dataset:
        model = {
            "url": "https://www.youtube.com/watch?v="+ music["url_id"],
            "artist": music["artist"],
            "title":music["title"],
            "duration":music["duration"],
            "yt_title":music["yt_title"],
            "score": int(math.log2(music['views']*music["view_increased"])*10000)
        }
        
        if(model["score"] > 0):
            score_model.append(model)
    
    selected_song = selectOne(score_model)
    
    final_music = setMeta(selected_song)

    return final_music
    #print(dataset)


def setMeta(music):

    if music["yt_title"] == None or len(music['yt_title']) == 0:
        music["yt_title"] = music['artist'] + " - " + music["title"]
    
    music["title_show"] = Helper.ytVideoTitleFilter(music["yt_title"])

    return music




def selectOne(population):
    max     = sum([c["score"] for c in population])
    pick    = random.uniform(0, max)
    current = 0
    for chromosome in population:
        current += chromosome["score"]
        if current > pick:
            return chromosome
            
def roulette(ls):
    i = 1
    l = len(ls)

    while i < l:
        ls[i] = ls[i] + ls[i - 1]
        i = i + 1

    r = random.randint(0, ls[l - 1] - 1)

    # print ls

    i = 0
    while i < l:
        if r < ls[i]:
            return i

        i = i + 1
