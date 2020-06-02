
# rj profiles
alphaMeow = ["en", "Octavia Meow"]
betaMeow = ["en-au", "Persephone Meow"]
gammaMeow = ["en-us", "Genesis Meow"]
deltaMeow = ["en-uk", "Aurora Meow"]
RJ = [alphaMeow, betaMeow, gammaMeow, deltaMeow]

def prepareRjBufferMp3(speech, rj):
    os.system("gtts-cli '" + speech + "' -l '" +
              rj[0]+"' -o "+bufferPath+"rjTemp.mp3")
    os.system("sox "+bufferPath+"rjTemp.mp3 -C 128 -r 44100 " +
              bufferPath+"rjTemp1.mp3")
    os.system("sox "+bufferPath+"silence5.mp3 -C 128 -r 44100 " +
              bufferPath+"silence55.mp3")
    os.system("sox "+bufferPath+"silence55.mp3 " +
              bufferPath+"rjTemp1.mp3 "+bufferPath+"rj.mp3")

    mp3 = MP3File(bufferPath+'rj.mp3')
    mp3.set_version(VERSION_2)
    mp3.song = 'RJ'
    mp3.artist = rj[1]
    mp3.save()

    currentGenre = "RJ"
    currentLyric = ""


def setRjBuffer(filePath):
    rj = getRandomRj()

    if len(filePath) < 1:
        speech = 'You are listening to '+streamName + \
            '. '+streamDescription + '. I am RJ '+rj[1]+'.'
        prepareRjBufferMp3(speech, rj)

    else:
        mp3 = MP3File(filePath)
        mp3.set_version(VERSION_2)
        if filePath.find('music/') > -1:
            speech = 'You are listening to '+streamName+'. I am RJ ' + \
                rj[1]+'. Now, You will listen to ' + \
                mp3.song+' by ' + mp3.artist+'.'
            #print(speech)
            prepareRjBufferMp3(speech, rj)
        elif filePath.find('news/news.mp3') > -1:
            speech = "Hello listeners, Its RJ "+rj[1]+". You are listening to "+streamName+". Now you will listen to the latest bulletin from BBC World Service."
            prepareRjBufferMp3(speech, rj)
		
        elif filePath.find('request/') > -1:
            speech = 'Hello listeners, Its RJ '+rj[1]+ \
                 '. You are listening to '+streamName+'. We just recieved a song request from ' + \
                 filePath.replace(requestPath,'').replace('.mp3','') + ' with love. Now you will listen to ' + \
                 mp3.song+' by ' + mp3.artist+'.'
            prepareRjBufferMp3(speech, rj)