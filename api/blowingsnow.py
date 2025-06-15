import modules.audio as audioMain
import modules.pytools as pytools
import random
import os
import time
import api.wind
import modules.logManager as log

print = log.printLog

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
    speed = 1

class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, "", 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out
    
    def testWindow():
        out = False
        if os.path.exists(".\\nomufflewn.derp") == True:
            out = True
        return out

def audio(dataList, depth):
    volume = (((2500 / 30) * dataList[0][1] + api.wind.globals.windModif) / 100) + 25 + depth
    try:
        volume = volume + dataList[9][0]
    except:
        pass
    print(volume)
    volume = volume + (dataList[9][0] * 100)
    print(volume)
    if dataList[0][4].find("snow") != -1:
        volume = volume * 2
        
    volume = volume ** 0.9
    
    speed = 10509.7103 ** (0.0407629 * (dataList[0][1] - 8.14921)) + 0.054068
    if speed > 1:
        speed = 0.180815 ** ( - 0.0480556 * (dataList[0][1] - 38.9698)) + 0.921555
        
    if speed < 0.4:
        speed = 0.4
    
    if speed < 1:
        volume = volume * (speed ** 2)
    
    status.vars["volume"] = volume
    status.vars["speed"] = speed
    
    if volume > 100:
        volume = 100
        
    if speed < 1:
        slowSpeed = speed * 2
        normalVolume = volume * ((0.6 - (1 - speed)) * 1.666666666666666666666)
        slowVolume = volume * (1 - ((0.6 - (1 - speed)) * 1.666666666666666666666))
        clickVolume = 0
    else:
        slowSpeed = speed * 2
        normalVolume = volume
        clickVolume = volume * (speed - 1)
        slowVolume = 0
    
    status.vars["slowVolume"] = slowVolume
    status.vars["normalVolume"] = normalVolume
    status.vars["clickVolume"] = clickVolume
    
    status.vars["slowSpeed"] = slowSpeed
         
    # audioMain.playSoundWindow("snowonwindow.mp3;snowwindow.mp3", [volume, volume], 1, 0, 0)
    event = audioMain.event()
    event.registerWindow("snowonwindow_slow.mp3;snowwindow_slow.mp3", [slowVolume, slowVolume], slowSpeed, 0, 0)
    event.registerWindow("snowonwindow.mp3;snowwindow.mp3", [normalVolume, normalVolume - clickVolume], speed, 0, 0)
    event.registerWindow("snowonwindow_click.mp3;snowwindow.mp3", [clickVolume, clickVolume], speed, 0, 0)
    event.run()
    
    globals.speed = speed
    # if utils.testWindow():
    #     print("Blowing snow with window open...")
    #     if volume > 100:
    #         volume = 100
    #     audioEvent = audioMain.event()
    #     audioEvent.register('snowwindow.mp3', 6, volume, 1, 0, 0)
    #     audioEvent.run()
    # else:
    #     print("Blowing snow with window closed...")
    #     if volume > 100:
    #         volume = 100
    #     audioEvent = audioMain.event()
    #     audioEvent.register('snowonwindow.mp3', 2, volume, 1, 0, 0)
    #     audioEvent.register('snowwindow.mp3', 3, volume, 1, 0, 0)
    #     audioEvent.register('snowwindow.mp3', 9, volume, 1, 0, 0)
    #     audioEvent.run()

def main():
    while not status.exit:
        n = True
        try:
            data = pytools.net.getTextAPI('https://www.snow-forecast.com/resorts/Ski-Wentworth/6day/bot')
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
        time.sleep(194 / globals.speed)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True

