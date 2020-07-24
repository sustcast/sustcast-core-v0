import importlib.util
import random
import time
import datetime as dt
import _thread
from recommender_chiron import Observer

TAG = "@CHIRON>"
observer_flag = False


def observe():

    while True:
        #Observer.importMusicsFromCsv()
        Observer.observe()
        
        cur = dt.datetime.now()
        mid_night = dt.datetime(cur.year,cur.month,cur.day,23,59,59)

        wait_time = (mid_night - cur).total_seconds()
        time.sleep(wait_time)



def initObserver():
    try:
        _thread.start_new_thread(observe, ())
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
    cut_off_constant = 10000
    for music in dataset:
        model = {
            "url": "https://www.youtube.com/watch?v="+ music["url_id"],
            "artist": music["artist"],
            "title":music["title"],
            "duration":music["duration"],
            "score": int((music["view_increased"])/cut_off_constant)
        }
        
        if(model["score"] > 0):
            score_model.append(model)
    
    selected_song = selectOne(score_model)

    return selected_song
    #print(dataset)

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
