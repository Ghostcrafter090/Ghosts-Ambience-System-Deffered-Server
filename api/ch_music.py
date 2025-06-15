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
    
    musicLenthDict = [25, 43, 34, 16, 31, 31, 37, 27]
    
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out
    
    def dayTimesGrabber():
        dayTimes = pytools.IO.getList('daytimes.pyl')[1]
        if dayTimes == 1:
            dayTimes = [[2022, 5, 11, 3, 45, 15], [2022, 5, 11, 4, 34, 10], [2022, 5, 11, 5, 16, 33], [2022, 5, 11, 5, 48, 29], [2022, 5, 11, 13, 10, 47], [2022, 5, 11, 20, 33, 6], [2022, 5, 11, 21, 5, 2], [2022, 5, 11, 21, 47, 25], [2022, 5, 11, 22, 36, 20]]
        return dayTimes
    
def getMusicLength(index):
    if index >= len(utils.musicLenthDict):
        return 30
    else:
        return utils.musicLenthDict[index]

def playMusic(outside=True, maxLength=1000):
    print("Playing christmas music...")
    musicIndex = random.randint(0, 7)
    i = 0
    while (getMusicLength(musicIndex) > maxLength) and (i < 28):
        musicIndex = random.randint(0, 7)
        i = i + 1
    
    if i >= 28:
        print("Could not find short enough mix.")
        return
    
    mp3 = 'ch_music_' + str(musicIndex) + ".mp3"
    pytools.IO.saveFile(".\\ch_music_playing.derp", "")
    if outside:
        audio.playSoundWindow(mp3 + ";" + mp3, [65, 35, 65], 1.0, 0, 1)
    else:
        event = audio.event()
        event.register(mp3, 2, 50, 1.0, 0, 1)
        event.register(mp3, 9, 50, 1.0, 0, 1)
        event.run()
    os.system("del \".\\ch_music_playing.derp\" /f /q")

def music(dateArray, dataArray=False):
    
    dayTimes = utils.dayTimesGrabber()
    
    if os.path.exists(".\\forceChMusic.derp"):
        playMusic()
    
    onTemp = 1.05317 ** (0.999529 * (dateArray[2] + 8.71512)) - 2.4229
    
    if dataArray:
        if dataArray[0][7] > onTemp:
            if dataArray[0][3] == 0:
                if dataArray[0][4] != "snow":
                    return
        elif dataArray[0][4] == "rain":
            return
        elif dataArray[0][4] == "lightrain":
            return
        elif dataArray[0][4] == "mist":
            return
    
    if dateArray[3] > 8:
        if dateArray[3] < 20:
            if (11 < dateArray[3] < 12) == False:
                if (dateArray[4] < 12) == False:
                    if not ((dateArray[2] == 24) and (dateArray[3] != 16) and (dateArray[3] != 17) and (dateArray[3] != 18) and (dateArray[3] != 22)):
                        if not ((dateArray[1] == 12) and (dateArray[2] > 12) and (dateArray[3] == dayTimes[5][3]) and (pytools.clock.dateArrayToUTC(dateArray) < (pytools.clock.dateArrayToUTC(dayTimes[5]) + 240))):
                            if dateArray[4] < 25:
                                if not ((dateArray[2] == 24) and ((dateArray[3] == 16) or (dateArray[3] == 17) or (dateArray[3] == 18) or (dateArray[3] == 22))):
                                    playMusic()
                            else:
                                if not ((dateArray[2] == 24) and ((dateArray[3] == 16) or (dateArray[3] == 17) or (dateArray[3] == 18) or (dateArray[3] == 22))):
                                    playMusic(maxLength=60 - dateArray[4])
        
        elif dateArray[3] < 22:
            if not ((dateArray[1] == 12) and ((dateArray[2] == 24) or (dateArray[2] == 25))):
                if (dateArray[4] < 12) == False:
                    if not ((dateArray[1] == 12) and (dateArray[2] > 12) and (dateArray[3] == dayTimes[5][3]) and (pytools.clock.dateArrayToUTC(dateArray) < (pytools.clock.dateArrayToUTC(dayTimes[5]) + 240))):
                        if dateArray[4] < 25:
                            if not ((dateArray[2] == 24) and ((dateArray[3] == 16) or (dateArray[3] == 17) or (dateArray[3] == 18) or (dateArray[3] == 22))):
                                playMusic(outside=False)
                        else:
                            if not ((dateArray[2] == 24) and ((dateArray[3] == 16) or (dateArray[3] == 17) or (dateArray[3] == 18) or (dateArray[3] == 22))):
                                playMusic(outside=False, maxLength=60 - dateArray[4])

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
