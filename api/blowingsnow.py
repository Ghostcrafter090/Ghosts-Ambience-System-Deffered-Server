import modules.audio as audioMain
import modules.pytools as pytools
import random
import os
import time

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": [],
        "blowingSnowChance": 0
    }
    
class globals:
    dataOld = ""

class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out
    
    def testWindow():
        out = False
        if os.path.exists(".\\nomufflewn.derp") == True:
            out = True
        return out

def audio(dataList, depth):
    volume = (((2500 / 30) * dataList[0][1]) / 100) + 25 + depth
    print(volume)
    volume = volume + (dataList[9][0] * 100)
    print(volume)
    if dataList[0][4].find("snow") != -1:
        volume = volume * 2
    if utils.testWindow():
        print("Blowing snow with window open...")
        if volume > 100:
            volume = 100
        audioEvent = audioMain.event()
        audioEvent.register('snowwindow.mp3', 6, volume, 1, 0, 0)
        audioEvent.run()
    else:
        print("Blowing snow with window closed...")
        if volume > 100:
            volume = 100
        audioEvent = audioMain.event()
        audioEvent.register('snowonwindow.mp3', 2, volume, 1, 0, 0)
        audioEvent.register('snowwindow.mp3', 3, volume, 1, 0, 0)
        audioEvent.run()
def main():
    while not status.exit:
        n = True
        try:
            data = pytools.net.getTextAPI('https://www.snow-forecast.com/resorts/Ski-Martock/6day/bot')
        except:
            data = globals.dataOld
            n = False
        globals.dataOld = data
        if n:
            try:
                depth = float(data.split("Fresh snowfall depth:")[1].split(" ")[1])
            except:
                depth = 0
            try:
                dataList = utils.dataGrabber()
            except:
                dataList = [[3.49, 7.79, 10000.0, 0, 'clouds', 4.0, 1027.0, 7.360000000000014, 99.0], [0, 0, 1027.0, 7.360000000000014, 99.0], 'set temp=280\n    set tempc=7\n    set windspeed=3\n    set windgust=7\n    set pressure=1027\n    set humidity=99\n    set weather=clouds\n    set modifier=4', 7]
            if dataList[0][7] < 5:
                chance = (5 - (dataList[0][7])) * (5 - (dataList[0][7])) * (5 - (dataList[0][7])) * (5 - (dataList[0][7])) * (float(depth) + 1)
            else:
                chance = 0
            status.vars['blowingSnowChance'] = chance
            print("Blowing Snow Chance: " + str(chance))
            if dataList[0][4].find("snow") != -1:
                audio(dataList, depth)
            if (random.random() * 32768) <= chance:
                audio(dataList, depth)
        time.sleep(194)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True

