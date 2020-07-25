import subprocess
import re

# helper functions


def retTimeHour():
    localtime = time.asctime(time.localtime(time.time()))
    hour = 0
    hour = int(localtime[11]+localtime[12])
    return hour


def replaceLine(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()
    # replace_line('stats.txt', 0, 'Mage')


def getStringFromFile(path):

    s = open(path)
    msg = ''
    flg = 0

    for m in s:
        if flg == 0:
            msg = msg+m.strip()
            flg = 1
        else:
            msg = msg+"\n"+m.strip()

    return msg


def writeFile(string, path):
    file = open(path, 'w')
    file.write(string)
    file.close


def selectElementRandmom(ls):
    l = len(ls)
    r = random.randint(0, l-1)
    ret = ls[r]

    return ret


def findLastPlayedFile():

    filename = '../ices-docker/log/ices.log'
    lineCheck = -50
    lineCheckIncre = 1

    line = subprocess.check_output(['tail', str(lineCheck), filename]).decode("utf-8").split('\n')
    # print(reversed(line))
    for ln in reversed(line):
        # print(ln)
        if ln.find("INFO playlist-builtin/playlist_read Currently playing \"/music/currentA.ogg\"") > 0:
            return "currentA.ogg"

        elif ln.find("INFO playlist-builtin/playlist_read Currently playing \"/music/currentB.ogg\"") > 0:
            return "currentB.ogg"

    findLastPlayedFile()


def ytVideoTitleFilter(title):

    title = title.lower()

    title = re.sub("[\(\[].*?[\)\]]", "", title)

    title = title.replace("  ", " ")

    title = title.strip()
    title = title.title()
    return title

#print (ytVideoTitleFilter('Given Up (Official Video HQ) - Linkin Park (asdoijasoidjo)'))
