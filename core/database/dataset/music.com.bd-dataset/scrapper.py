import requests
import tempfile
from bs4 import BeautifulSoup
import time
from pydub import AudioSegment
from urllib.request import urlopen
import urllib

music_com_bd_list = [
    "http://www.music.com.bd/download/browse/A/",
    "http://www.music.com.bd/download/browse/B/",
    "http://www.music.com.bd/download/browse/C/",
    "http://www.music.com.bd/download/browse/D/",
    "http://www.music.com.bd/download/browse/E/",
    "http://www.music.com.bd/download/browse/F/",
    "http://www.music.com.bd/download/browse/G/",
    "http://www.music.com.bd/download/browse/H/",
    "http://www.music.com.bd/download/browse/I/",
    "http://www.music.com.bd/download/browse/J/",
    "http://www.music.com.bd/download/browse/K/",
    "http://www.music.com.bd/download/browse/L/",
    "http://www.music.com.bd/download/browse/M/",
    "http://www.music.com.bd/download/browse/N/",
    "http://www.music.com.bd/download/browse/O/",
    "http://www.music.com.bd/download/browse/P/",
    "http://www.music.com.bd/download/browse/Q/",
    "http://www.music.com.bd/download/browse/R/",
    "http://www.music.com.bd/download/browse/S/",
    "http://www.music.com.bd/download/browse/T/",
    "http://www.music.com.bd/download/browse/U/",
    "http://www.music.com.bd/download/browse/V/",
    "http://www.music.com.bd/download/browse/W/",
    "http://www.music.com.bd/download/browse/X/",
    "http://www.music.com.bd/download/browse/Y/",
    "http://www.music.com.bd/download/browse/Z/",
]

def debugStop():
    print("STOP")
    time.sleep(10)


def saveInText(artist,title,album,length,size,url,downloadUrl):
    f = open("data.csv","a+")

    print(artist,title,album,length,size)

    f.write(artist+','+title+','+album+','+length+','+size+','+url+','+downloadUrl)
    f.write('\n')
    f.close()


def downloadMusicFile(artist,title,album,url):
    data = urlopen(url).read()
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(data)
    AudioSegment.from_mp3(f.name).export(artist+'-'+title+'.ogg', format='ogg', tags= {'artist': artist, 'title':title, 'album':album})
    f.close()


def scrapMusic(url):
    #print(url)
    
    url = urllib.parse.quote(url,safe=':/()')
    
    musicUrl = url[6:]
    musicUrl = "http://"+musicUrl

    downloadUrl = url[28:-5]
    downloadUrl = "http://download.music.com.bd/" + downloadUrl
    
    #print(musicUrl)
    #print(downloadUrl)

    artist,title,album,length,size = getMusicInfo(musicUrl)

    saveInText(artist,title,album,length,size,musicUrl,downloadUrl)


def scrapArtist(artistUrl):
    #print(url)

    page = requests.get(artistUrl)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.findAll('a')

    for link in links:
        url = link.get('href')
        
        if(type(url) == str):
            if(url.find('.mp3.html') > -1):
                scrapMusic(url)
            elif artistUrl in url and len(artistUrl) < len(url):
                scrapArtist(url)

def startScrap(start,end):

    global music_com_bd_list

    i = start
    while i <= end:
        URL = music_com_bd_list[i]

        print(URL)

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.findAll('a')

        for link in links:
            url = link.get('href')

            if type(url) == str:
                if URL in url and len(url) > len(URL):
                    scrapArtist(url)
        i+=1

def getMusicInfo(url):
    print(url)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    infoHtml = soup.findAll("li","list-group-item")

    artist = str(infoHtml[0].a.string)
    if infoHtml[0].a.string is None:
        artist = ''
    
    title = str(infoHtml[1].a.string)
    if infoHtml[1].a.string is None:
        title = ''
    
    album = str(infoHtml[2].a.string)
    if infoHtml[2].a.string is None:
        album = ''
    
    length = str(infoHtml[3].string.split(' ')[2])

    size = str(infoHtml[4].string.split(' ')[2])
    if str(infoHtml[4].string.split(' ')[3])[0] == 'K':
        size = str(float(size)*0.001)
    
    return artist,title,album,length,size
    

startScrap(1,25)

#getMusicInfo("http://music.com.bd/download/Music/A/Ayub%20Bachchu/Best%20of%20Ayub%20Bachchu/Ayub%20Bachchu%20-%20Sukhe%20Theko%20Tumi%20(music.com.bd).mp3.html")







