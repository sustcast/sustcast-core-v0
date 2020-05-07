import subprocess

filename = '../../ices-docker/log/ices.log'
lineCheck = -4
lineCheckIncre = 1

def findLastPlayedFile():
    global filename
    global lineCheck
    global lineCheckIncre

    line = subprocess.check_output(['tail', str(lineCheck), filename]).split('\n')
    for ln in reversed(line):
        #print(ln)
        if ln.find("INFO playlist-builtin/playlist_read Currently playing \"/music/current.ogg\"") > 0:
            print("current")
            return
        elif ln.find("INFO playlist-builtin/playlist_read Currently playing \"/music/buffer.ogg\"") > 0:
            print("buffer")
            return

    lineCheck -= lineCheckIncre
    findLastPlayedFile()
    

findLastPlayedFile()
print("done")