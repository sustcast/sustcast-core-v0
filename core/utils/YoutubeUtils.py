from youtube_search import YoutubeSearch
import requests
from bs4 import BeautifulSoup
import random
import json
import isodate
import youtube_dl
import urllib
import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

def set_modules(moduleHelper,api_key):
    global Helper
    global API_KEY
    
    Helper = moduleHelper
    API_KEY = api_key

def findSimilarity(search,yt_title):
    X = search
    Y =yt_title

    # tokenization 
    X_list = word_tokenize(X) 
    Y_list = word_tokenize(Y) 

    # sw contains the list of stopwords 
    sw = stopwords.words('english') 
    l1 =[];l2 =[] 

    # remove stop words from the string 
    X_set = {w for w in X_list if not w in sw} 
    Y_set = {w for w in Y_list if not w in sw} 

    # form a set containing keywords of both strings 
    rvector = X_set.union(Y_set) 
    for w in rvector: 
        if w in X_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0


    # cosine formula 
    for i in range(len(rvector)): 
        c+= l1[i]*l2[i] 
    
    try:
        cosine = c / float((sum(l1)*sum(l2))**0.5) 
    except:
        print("@NLTK>","search -> ", search, "yt_title -> ", yt_title)
        cosine = 0
    return cosine

def getYtIdFromMusicName(music):
    query = urllib.parse.quote(music)

    url = "https://www.youtube.com/results?search_query=" + query

    html = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    title = ""
    while len(title) == 0:
        title = Helper.ytVideoTitleFilter(getTitleFromId(video_ids[0])).lower()
    
    similarity = findSimilarity(music,title)

    if similarity >= 0.5 :
        return video_ids[0]
    else:
         return ""

def getMusicInfoFromId(videoid):
    count = 0
    endpoint = "https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part=snippet,contentDetails,statistics"
    url = endpoint.format(videoid, api_key)
    response = {}
    try:
        response = json.loads(requests.get(url).text)
    except Exception as e :
        count+=1
        print(e)
        
    dur = response["items"][0]["contentDetails"]["duration"]
    seconds = str(isodate.parse_duration(dur).total_seconds())
    viewCount = response["items"][0]["statistics"]["viewCount"]
    title = response['items'][0]['snippet']['title']

    music = {
        "id" : videoid,
        "title" : title,
        "views" : viewCount,
        "duration" : seconds
    }

    return music 


def getDuration_n_ViewsFromId(videoid):
    count = 0
    endpoint = "https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part=contentDetails,statistics"
    url = endpoint.format(videoid, API_KEY)
    response = {}
    try:
        response = json.loads(requests.get(url).text)
    except Exception as e :
        count+=1
        print(e)

    dur = response["items"][0]["contentDetails"]["duration"]
    seconds = str(isodate.parse_duration(dur).total_seconds())

    viewCount = response["items"][0]["statistics"]["viewCount"]

    return viewCount, seconds

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