from youtube_search import YoutubeSearch
import requests
from bs4 import BeautifulSoup
import random
import json
import isodate
import youtube_dl

def getYtIdFromMusicName(music):
    r = random.randint(1, 5)

    results = json.loads(YoutubeSearch(music, max_results=r).to_json())

    try:
        return results['videos'][0]['id'][:11]
    except:
        return ""

def getDuration_n_ViewsFromId(id):
    url = "https://www.youtube.com/watch?v="+id
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    
    try:
        count = soup.select_one('meta[itemprop="interactionCount"][content]')['content']
        duration = soup.select_one('meta[itemprop="duration"][content]')['content']
        seconds = isodate.parse_duration(duration).total_seconds()
        
        return count,str(seconds)
    
    except :
        return "",""

def getTitleFromId(id):
    url = "https://www.youtube.com/watch?v="+id
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    
    try:
        title = soup.select_one('meta[itemprop="name"][content]')['content']

        return title
    
    except :
        return ""


def downloadMp3(id):

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl' : "temp/download.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['http://www.youtube.com/watch?v='+id])


#print (getDuration_n_ViewsFromId(getYtIdFromMusicName('Dindūn - Chandor Tolay Dekha Hoibo')))