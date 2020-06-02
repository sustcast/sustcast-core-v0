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
