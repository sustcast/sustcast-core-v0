import re
import json
import requests
import isodate

videoId = 'HbCUCKf6wT8' #example
def get_music_info_from_id(videoid):
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


print(get_videoDuration_viewCount(videoId))