from youtube_search import YoutubeSearch
import requests
from bs4 import BeautifulSoup
import random
import json
import isodate

def getYtIdFromMusicName(music):
    r = random.randint(1, 5)

    results = json.loads(YoutubeSearch(music, max_results=r).to_json())

    return results['videos'][0]['id']

def getDuration_n_ViewsFromId(id):
    url = "https://www.youtube.com/watch?v="+id
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    
    count = soup.select_one('meta[itemprop="interactionCount"][content]')['content']
    duration = soup.select_one('meta[itemprop="duration"][content]')['content']
    seconds = isodate.parse_duration(duration).total_seconds()

    return count,str(seconds)

#print (getDuration_n_ViewsFromId(getYtIdFromMusicName('Dindūn - Chandor Tolay Dekha Hoibo')))