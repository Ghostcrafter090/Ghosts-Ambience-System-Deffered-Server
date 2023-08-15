import modules.audio as audio
import modules.pytools as pytools
import time
import random
import modules.logManager as log

print = log.printLog

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": []
    }
    
class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out

def playMusic():
    mp3 = 'ch_music_' + str(random.randint(0, 1)) + ".mp3"
    audio.playSoundWindow(mp3 + ";" + mp3, 50, 1.0, 0, 1)

def music(dateArray, dataArray=False):
    if dataArray:
        if dataArray[0][7] > 0.5:
            if dataArray[0][3] == 0:
                if dataArray[0][4] != "snow":
                    return
    if dateArray[3] > 9:
        if dateArray[3] < 16:
            if (11 < dateArray[3] < 12) == False:
                if (dateArray[4] < 10) == False:
                    if dateArray[4] < 40:
                        playMusic()

def main():
    while not status.exit:
        dataArray = utils.dataGrabber()
        dateArray = pytools.clock.getDateTime()
        if dateArray[1] == 11:
            if dateArray[2] > 11:
                music(dateArray, dataArray)
        if dateArray[1] == 12:
            music(dateArray)
        time.sleep(194)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
