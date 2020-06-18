import importlib.util
import time
import random
import sqlite3
from sqlite3 import Error

# spec = importlib.util.spec_from_file_location("CsvUtils", "../utils/CsvUtils.py")
# CsvUtils = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(CsvUtils)

music_list_csv_path = "database/dataset/chiron-dataset/music_list.csv"
music_view_csv_path = "database/dataset/chiron-dataset/music_views.csv"
chiron_db_path = "database/dataset/chiron-dataset/chiron.db"

TAG = "@OBSERVER>"

def set_modules(moduleCsv,moduleYT):
    global CsvUtils
    global YoutubeUtils

    CsvUtils = moduleCsv
    YoutubeUtils = moduleYT



def get_db_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn



def is_music_inserted(music):
    conn = get_db_connection(chiron_db_path)
    
    sql = 'SELECT title,artist FROM songs WHERE title="'+music["title"].lower().replace('"','\'')+'" AND artist="'+ music["artist"].lower().replace('"','\'')+'"'
    
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        if(len(rows) > 0):
            return True
        else:
            return False
            
    except Exception as e:
        print(e)
        print(TAG,"ERROR in is_music_inserted")
        print(sql)
    
    conn.close()



def is_music_id_in_yt_data(id):
    conn = get_db_connection(chiron_db_path)

    sql = 'SELECT id FROM yt_data WHERE song_id='+str(id)
    
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        if(len(rows) > 0):
            return True
        else:
            return False
            
    except Exception as e:
        print(e)
        print(TAG,"ERROR in is_music_id_in_yt_data")
        print(sql)
    
    conn.close()


def get_all_music():
    conn = get_db_connection(chiron_db_path)
    
    sql = 'SELECT artist,title FROM songs'
    
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()

    return rows



def get_all_music_yt_data():
    conn = get_db_connection(chiron_db_path)
    
    sql = 'SELECT artist,title,url_id,duration,views,view_increased FROM yt_data join songs ON yt_data.song_id = songs.id;'
    
    cur = conn.cursor()
    cur.execute(sql)

    ret = []

    for row in cur.fetchall():
        music = {
            "artist":row[0],
            "title":row[1],
            "url_id":row[2],
            "duration":row[3],
            "views":row[4],
            "view_increased":row[5]
        }
        ret.append(music)
    
    conn.close()

    return ret


def get_music_url_id(music):
    conn = get_db_connection(chiron_db_path)
    
    sql = 'SELECT url_id FROM yt_data WHERE song_id in (SELECT id FROM songs WHERE artist="'+ music['artist'] +'" AND title="'+ music['title']+'")'
    
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()

    if len(rows) > 0:
        return rows[0][0]
    else:
        return ""


def get_music_id(music):
    conn = get_db_connection(chiron_db_path)
    
    sql = 'SELECT id FROM songs WHERE artist="'+ music['artist'] +'" AND title="'+ music['title']+'"'
    
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()

    if len(rows) > 0:
        return rows[0][0]
    else:
        return ""



def get_music_views(url_id):
    conn = get_db_connection(chiron_db_path)
    
    sql = 'SELECT views FROM yt_data WHERE url_id="'+url_id+'"'
    
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()

    if len(rows) > 0:
        return rows[0][0]
    else:
        return -1


def insert_music(music):
    conn = get_db_connection(chiron_db_path)

    sql = 'INSERT INTO songs(title,artist) VALUES("'+music["title"].lower().replace('"','\'')+'","'+ music["artist"].lower().replace('"','\'')+'")'
    
    cur = conn.cursor()
    cur.execute(sql)
    
    conn.commit()
    conn.close()


def insert_music_yt_data(music,update):
    conn = get_db_connection(chiron_db_path)

    if(update):
        sql = 'UPDATE yt_data SET views = '+music["views"]+', duration = '+music["duration"]+', view_increased = '+music["view_increased"]+' WHERE song_id='+str(music["song_id"])
    
    else:
        sql = 'INSERT INTO yt_data(song_id,views,duration,url_id,view_increased) VALUES('+str(music["song_id"])+','+music["views"]+','+music["duration"]+',"'+ music["url_id"]+'",'+ music["view_increased"]+')'
    
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()

    except sqlite3.IntegrityError as ex1:
        conn.close()
        delete_music(music["song_id"])

    except Exception as ex2:
        print(ex2)
        print(TAG,"error in insert_yt_data")
        print(sql)
        conn.close()


def delete_music(id):
    if is_music_id_in_yt_data(id):
        connA = get_db_connection(chiron_db_path)
        sql = "DELETE FROM yt_data WHERE song_id="+str(id)
        
        try:
            cur = connA.cursor()
            cur.execute(sql)
            connA.commit()
            connA.close()
        
        except Exception as ex1:
            print(ex1)
            print(TAG,"error delete_music")
            print(sql)
            connA.close()

    connB = get_db_connection(chiron_db_path)
    sql = "DELETE FROM songs WHERE id="+str(id)
    
    try:
        cur = connB.cursor()
        cur.execute(sql)
        connB.commit()
        connB.close() 

    except Exception as ex2:
        print(ex2)
        print(TAG,"error delete_music")
        print(sql)
        connB.close() 


def importMusicsFromCsv():
     music_list = CsvUtils.readDataFromCsv(music_list_csv_path)

     for music in music_list:
         if(is_music_inserted(music) == False):
             insert_music(music)


def observe():

# TODO observe a song based on the last-time it was observed. 
# TODO make a DB cleaning conditions for removing non-trendy songs. view_increased = 0 -> views < 1 million

    print(TAG,"started...")

    music_list = get_all_music()

    for item in music_list:
        music = {
            "artist":item[0],
            "title":item[1]
        }

        data_exists_flg = False
        
        url_id = get_music_url_id(music)

        if len(url_id) > 0:
            data_exists_flg = True
           
           ###
            continue

        ###
        print(TAG,"check1")

        retry = 5
        while len(url_id) == 0 and retry > 0:
            try:
                url_id = YoutubeUtils.getYtIdFromMusicName(music['artist'] + " - " + music["title"])
                retry = retry - 1
                
            except Exception as e:
                print(e)
                print(TAG,"error in crawling....will wait for 60s")
                time.sleep(60)

        if retry == 0:
            delete_music(get_music_id(music))
            print(TAG,"did not found in yt",music)
            continue

###
        print(TAG,"check2")
        
        yt_views = ""
        yt_duration = ""
        retry = 5 
        while len(yt_views) == 0 and len(yt_duration) == 0 and retry > 0:
            try:
                yt_views, yt_duration = YoutubeUtils.getDuration_n_ViewsFromId(url_id)
                retry = retry - 1

            except Exception as e:
                print(e)
                print(TAG,"error in crawling....will wait for some time")
                time.sleep(60)

        if retry == 0:
            delete_music(get_music_id(music))
            print(TAG,url_id+"is not available in yt",music)
            continue
###
        print(TAG,"check3")
        
        prev_views = get_music_views(url_id)
        if  prev_views >= 0:
            yt_view_increase = str(int(yt_views) - prev_views )
        else:
            yt_view_increase = str(0)
        
        music["url_id"] = url_id
        music["views"] = yt_views
        music["duration"] = yt_duration
        music["song_id"] = get_music_id(music)
        music["view_increased"] = yt_view_increase

        ##
        print(TAG,music)
        insert_music_yt_data(music,data_exists_flg)

    print(TAG,"completed...")


#piimportMusicsFromCsv()

#observe()

