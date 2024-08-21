import modules.audio as audio
import modules.pytools as pytools
import time
import random
import modules.logManager as log
import os

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

def playMusic(outside=True):
    mp3 = 'ch_music_' + str(random.randint(0, 7)) + ".mp3"
    pytools.IO.saveFile(".\\ch_music_playing.derp", "")
    if outside:
        audio.playSoundWindow(mp3 + ";" + mp3, [50, 8, 20], 1.0, 0, 1)
    else:
        event = audio.event()
        event.register(mp3, 2, 50, 1.0, 0, 1)
        event.register(mp3, 9, 8, 1.0, 0, 1)
        event.run()
    os.system("del \".\\ch_music_playing.derp\" /f /q")

def music(dateArray, dataArray=False):
    if dataArray:
        if dataArray[0][7] > 0.5:
            if dataArray[0][3] == 0:
                if dataArray[0][4] != "snow":
                    return
    if dateArray[3] > 9:
        if dateArray[3] < 16:
            if (11 < dateArray[3] < 12) == False:
                if (dateArray[4] < 12) == False:
                    if not ((dateArray[2] == 24) and (dateArray[3] != 16) and (dateArray[3] != 17) and (dateArray[3] != 18) and (dateArray[3] != 22)):
                        if dateArray[4] < 25:
                            playMusic()
        if dateArray[3] < 21:
            if not ((dateArray[1] == 12) and ((dateArray[2] == 24) or (dateArray[2] == 25))):
                if (dateArray[4] < 12) == False:
                    if dateArray[4] < 25:
                        if not ((dateArray[2] == 24) and (dateArray[3] != 16) and (dateArray[3] != 17) and (dateArray[3] != 18) and (dateArray[3] != 22)):
                                playMusic(outside=False)

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
