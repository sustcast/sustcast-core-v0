from utils import YoutubeUtils
from pydub import AudioSegment
from utils import Constant
import time
from shutil import copyfile
import os

TAG="@SongDownload>"
def downloadOgg(music):

    url = music['url']
    if(url.find("https://www.youtube.com/watch") == 0):
        yt_id = url.replace("https://www.youtube.com/watch?v=","")

        if os.path.isfile(Constant.default_cache_path+yt_id+".ogg"):
            copyfile(Constant.default_cache_path+yt_id+".ogg",Constant.default_ogg_download_path)
            return True


        try:
            print(TAG,"started...")
                        
            YoutubeUtils.downloadMp3(yt_id)
            
            AudioSegment.from_mp3(Constant.default_mp3_download_path).export(Constant.default_ogg_download_path, format='ogg',tags={'artist': music['artist'], 'title': music['title']})
            
            copyfile(Constant.default_ogg_download_path, Constant.default_cache_path+yt_id+".ogg")

            print(TAG,"completed...")
            
            return True

        except Exception as ex:
            print(TAG,ex)
            print(TAG, "ERROR => ", music)
            return False

    return False

    
        