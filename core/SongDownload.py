from utils import YoutubeUtils
from pydub import AudioSegment
from utils import Constant
import time
from shutil import copyfile
import os
import json


TAG="@SongDownload>"
def downloadOgg(music):

    if 'url' in music :
        url = music['url']

        if url.find("https://www.youtube.com/watch") != 0:
            return False


        yt_id = url.replace("https://www.youtube.com/watch?v=","")

        if os.path.isfile(Constant.default_cache_path+yt_id+".ogg"):
            
            #copyfile(Constant.default_cache_path+yt_id+".ogg",Constant.default_ogg_download_path)
            AudioSegment.from_ogg(Constant.default_cache_path+yt_id+".ogg").export(Constant.default_ogg_download_path, format='ogg',tags={'artist': json.dumps(music), 'title': music['title_show']}, parameters=["-ac", "2"])

            return True


        try:
            print(TAG,"started...")
                        
            YoutubeUtils.downloadMp3(yt_id)
            
            AudioSegment.from_mp3(Constant.default_mp3_download_path).export(Constant.default_ogg_download_path, format='ogg',tags={'artist': json.dumps(music), 'title': music['title_show']}, parameters=["-ac", "2"])
            
            copyfile(Constant.default_ogg_download_path, Constant.default_cache_path+yt_id+".ogg")

            print(TAG,"completed...")
            
            return True

        except Exception as ex:
            print(TAG,ex)
            print(TAG, "ERROR => ", music)
            return False
    
    elif 'file' in music:
        file_path = music['file']
        print("Converting")
        if(file_path.split(".")[-1]!='ogg'):
                AudioSegment.from_mp3(file_path).export(Constant.default_ogg_download_path, format='ogg',tags={'artist': json.dumps(music), 'title': music['title_show']}, parameters=["-ac", "2"])
                print("Conversion Done")
        else:
                #AudioSegment.from_ogg(file_path).export(Constant.default_ogg_download_path, format='ogg',tags={'artist': json.dumps(music), 'title': music['title_show']}, parameters=["-ac", "2"])
                
                title = music['title_show']
                new_title = title.replace(" ", "\ ")
                new_music = file_path.replace(" ", "\ ")
                os.system(f"tracktag --name {new_title} {new_music}")

                copyfile(file_path, Constant.default_ogg_download_path)
                print("ogg file copied succesfully.")

        return True

    return False

