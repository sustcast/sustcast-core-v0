from utils import YoutubeUtils
from pydub import AudioSegment
from utils import Constant

TAG="@SongDownload>"
def downloadOgg(music):

    print(TAG,"started...")

    url = music['url']
    if(url.find("https://www.youtube.com/watch") == 0):
        YoutubeUtils.downloadMp3(url.replace("https://www.youtube.com/watch?",""))

    AudioSegment.from_mp3(Constant.default_mp3_download_path).export(Constant.default_ogg_download_path, format='ogg',tags={'artist': music['artist'], 'title': music['title']})

    print(TAG,"completed...")

    
        