from youtube_search import YoutubeSearch
import requests
from bs4 import BeautifulSoup

url = "https://www.youtube.com/watch?v=OmF1AY3sO9Q"
soup = BeautifulSoup(requests.get(url).text, 'lxml')
print(soup.select_one('meta[itemprop="interactionCount"][content]')['content'])
print(soup.select_one('meta[itemprop="duration"][content]')['content'])

#{"@context":"https://schema.org","@type":"VideoObject","description":"1 Million Drop!! Here's my Official Remix of Lauv's Modern Loneliness!\n\nArtwork & Animation by my G - Santanu Hazarika (https://www.instagram.com/santanu_hazarika_art/)\n\nStream on:\nSpotify - https://tinyurl.com/ModernLonlinessRemix\nApple Music - https://tinyurl.com/ModernLonlinessRemixAM\nJioSaavn - https://tinyurl.com/ModernLonlinessRemixSVN","duration":"PT218S","embedUrl":"https://www.youtube.com/embed/OmF1AY3sO9Q?list=RDOmF1AY3sO9Q","interactionCount":"872767","name":"Lauv - Modern Loneliness (Ritviz Remix)","thumbnailUrl":["https://i.ytimg.com/vi/OmF1AY3sO9Q/maxresdefault.jpg"],"uploadDate":"2020-05-22"}
#results = YoutubeSearch('Dindūn - Chandor Tolay Dekha Hoibo', max_results=10).to_json()

#print(results)