import tempfile
from pydub import AudioSegment


AudioSegment.from_mp3('test.mp3').export('result.ogg', format='ogg',tags={'artist': 'Various artists', 'title':'Onk kop','album': 'Best of 2011', 'comments': 'This album is awesome!'})
