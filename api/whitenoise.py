import modules.audio as audio
import modules.pytools as pytools
import os
import time
import random
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
        "lastLoop": []
    }

class globals:
    windowBroken = 0
    windowOpen = 0
    windowFixUtc = 0

class utils:
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

class secs:
    def window(dataList):
        windowf = 0
        if globals.windowBroken == 1:
            windowf = 1
        if dataList[0][7] >= 12:
            if dataList[0][1] <= 15:
                if dataList[0][4] != "rain":
                    if dataList[0][4] != "lightrain":
                        if dataList[0][4] != "thunder":
                            windowf = 1
        if windowf == 1:
            if os.path.isfile("nomufflewn.derp") == False:
                if globals.windowBroken == 0:
                    audioEvent = audio.event()
                    audioEvent.register("openwindow1.mp3", 0, 100, 1.0, 0.0, 0)
                    audioEvent.register("openwindow2.mp3", 2, 100, 1.0, 0.0, 0)
                    audioEvent.run()
                pytools.IO.saveFile('nomufflewn.derp', "1")
            audio.command.setFlag("nomufflewn", True)
        else:
            if os.path.isfile("nomufflewn.derp"):
                audioEvent = audio.event()
                audioEvent.register("closewindow1.mp3", 0, 100, 1.0, 0.0, 0)
                audioEvent.register("closewindow2.mp3", 2, 100, 1.0, 0.0, 0)
                audioEvent.run()
                os.system('del nomufflewn.derp /f /s /q')
            audio.command.setFlag("nomufflewn", False)

    def windowBreakState(dataList):
        rand = 37 * ((dataList[0][1] - 19 + api.wind.globals.windModif) ** 1.55)
        print(rand)
        randf = random.random() * 32768
        print(randf)
        if dataList[0][1] > 20 - api.wind.globals.windModif:
            if randf < (rand / 3):
                if globals.windowBroken == 0:
                    audioEvent = audio.event()
                    audioEvent.register("windowsmash.mp3", 2, 50, 1.0, 0.0, 0)
                    audioEvent.register("windowsmash.mp3", 3, 50, 1.0, 0.0, 0)
                    audioEvent.run()
                    time.sleep(6)
                    globals.windowBroken = 1
                    windowFixArray = pytools.clock.getDateTime()
                    windowFixArray[2] = windowFixArray[2] + 1
                    if windowFixArray[2] > pytools.clock.getMonthEnd(windowFixArray[1]):
                        windowFixArray[2] = 1
                        windowFixArray[1] = windowFixArray[1] + 1
                        if windowFixArray[1] > 12:
                            windowFixArray[1] = 1
                            windowFixArray[0] = windowFixArray[0] + 1
                    windowFixArray[3] = 15
                    globals.windowFixUtc = pytools.clock.dateArrayToUTC(windowFixArray)
                    print(globals.windowFixUtc)
                    secs.window(dataList)
                else:
                    windowFixArray = pytools.clock.getMidnight(pytools.clock.getDateTime())
                    windowFixArray[2] = windowFixArray[2] + 1
                    windowFixArray[3] = 15
                    globals.windowFixUtc = pytools.clock.dateArrayToUTC(pytools.clock.fixDateArray(windowFixArray))
    
    def fixWindow(dataList):
        audioEvent = audio.event()
        audioEvent.register("windowrepair.mp3", 2, 100, 1.0, 0.0, 0)
        audioEvent.register("windowrepair.mp3", 3, 35, 1.0, 0.0, 0)
        audioEvent.run()
        time.sleep(510)
        globals.windowBroken = 0
        secs.window(dataList)

def main():
    typeState = [0, 0, 0, 0, 0, 0]
    
    try:
        globals.windowBroken = pytools.IO.getJson("windowState.json")["windowBroken"]
    except:
        globals.windowBroken = 0
        
    try:
        globals.windowFixUtc = pytools.IO.getJson("windowState.json")["windowFixUtc"]
    except:
        globals.windowFixUtc = 0
    
    while not status.exit:
        
        dateArray = pytools.clock.getDateTime()
        dayTimes = utils.dayTimesGrabber()
        dataList = utils.dataGrabber()

        secs.window(dataList)
        secs.windowBreakState(dataList)
        if globals.windowBroken == 1:
            print(globals.windowFixUtc)
            print(pytools.clock.dateArrayToUTC(dateArray))
            if globals.windowFixUtc < pytools.clock.dateArrayToUTC(dateArray):
                secs.fixWindow(dataList)
                
        pytools.IO.saveJson("windowState.json", {
            "windowBroken": globals.windowBroken,
            "windowFixUtc": globals.windowFixUtc,
            "windowOpen": globals.windowOpen
        })
        
        activeState = [0, 0, 0, 0, 0, 0]
        if dataList[0][7] >= 5:
            if dateArray[3] < dayTimes[2][3]:
                activeState[0] = 1
            if dateArray[3] == dayTimes[2][3]:
                if dateArray[4] < dayTimes[2][4]:
                    activeState[0] = 1
            if dateArray[3] > dayTimes[6][3]:
                activeState[0] = 1
            if dateArray[3] == dayTimes[6][3]:
                if dateArray[4] > dayTimes[6][4]:
                    activeState[0] = 1
            
            if (dateArray[3] > dayTimes[5][3]) and (dateArray[3] < dayTimes[6][3]):
                activeState[1] = 1
            if dateArray[3] == dayTimes[5][3]:
                if dateArray[4] > dayTimes[5][4]:
                    activeState[1] = 1
            if dateArray[3] == dayTimes[6][3]:
                if dateArray[4] < dayTimes[6][4]:
                    activeState[1] = 1
            
            if (dateArray[3] > dayTimes[1][3]) and (dateArray[3] < dayTimes[2][3]):
                activeState[2] = 1
            if dateArray[3] == dayTimes[1][3]:
                if dateArray[4] > dayTimes[1][4]:
                    activeState[2] = 1
            if dateArray[3] == dayTimes[2][3]:
                if dateArray[4] < dayTimes[2][4]:
                    activeState[2] = 1
            
            if (dateArray[3] > dayTimes[2][3]) and (dateArray[3] < dayTimes[7][3]):
                activeState[3] = 1
            if dateArray[3] == dayTimes[2][3]:
                if dateArray[4] > dayTimes[2][4]:
                    activeState[3] = 1
            if dateArray[3] == dayTimes[7][3]:
                if dateArray[4] < dayTimes[7][4]:
                    activeState[3] = 1
        
        if dataList[0][7] < 10:
            if dateArray[3] < dayTimes[2][3]:
                activeState[4] = 1
            if dateArray[3] == dayTimes[2][3]:
                if dateArray[4] < dayTimes[2][4]:
                    activeState[4] = 1
            if dateArray[3] > dayTimes[6][3]:
                activeState[4] = 1
            if dateArray[3] == dayTimes[6][3]:
                if dateArray[4] > dayTimes[6][4]:
                    activeState[4] = 1

            if (dateArray[3] > dayTimes[2][3]) and (dateArray[3] < dayTimes[7][3]):
                activeState[5] = 1
            if dateArray[3] == dayTimes[2][3]:
                if dateArray[4] > dayTimes[2][4]:
                    activeState[5] = 1
            if dateArray[3] == dayTimes[7][3]:
                if dateArray[4] < dayTimes[7][4]:
                    activeState[5] = 1
        
        if activeState[0] == 1:
            if typeState[0] == 0:
                typeState[0] = 1
                audio.playSoundWindow("warm_wn_night_fi.mp3;warm_wn_night_fi_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
            else:
                audio.playSoundWindow("warm_wn_night.mp3;warm_wn_night_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
        else:
            if typeState[0] == 1:
                typeState[0] = 0
                audio.playSoundWindow("warm_wn_night_fo.mp3;warm_wn_night_fo_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)

        if activeState[1] == 1:
            if typeState[1] == 0:
                typeState[1] = 1
                audio.playSoundWindow("warm_wn_evening_fi.mp3;warm_wn_evening_fi_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
            else:
                audio.playSoundWindow("warm_wn_evening.mp3;warm_wn_evening_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
        else:
            if typeState[1] == 1:
                typeState[1] = 0
                audio.playSoundWindow("warm_wn_evening_fo.mp3;warm_wn_evening_fo_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)

        if activeState[2] == 1:
            if typeState[2] == 0:
                typeState[2] = 1
                audio.playSoundWindow("warm_wn_morning_fi.mp3;warm_wn_morning_fi_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
            else:
                audio.playSoundWindow("warm_wn_morning.mp3;warm_wn_morning_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
        else:
            if typeState[2] == 1:
                typeState[2] = 0
                audio.playSoundWindow("warm_wn_morning_fo.mp3;warm_wn_morning_fo_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
        
        if activeState[3] == 1:
            if typeState[3] == 0:
                typeState[3] = 1
                audio.playSoundWindow("warm_wn_day_fi.mp3;warm_wn_day_fi_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
            else:
                audio.playSoundWindow("warm_wn_day.mp3;warm_wn_day_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
        else:
            if typeState[3] == 1:
                typeState[3] = 0
                audio.playSoundWindow("warm_wn_day_fo.mp3;warm_wn_day_fo_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
            
        if activeState[4] == 1:
            if typeState[4] == 0:
                typeState[4] = 1
                audio.playSoundWindow("cold_wn_night_fi.mp3;cold_wn_night_fi_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
            else:
                audio.playSoundWindow("cold_wn_night.mp3;cold_wn_night_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
        else:
            if typeState[4] == 1:
                typeState[4] = 0
                audio.playSoundWindow("cold_wn_night_fo.mp3;cold_wn_night_fo_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
        
        if activeState[5] == 1:
            if typeState[5] == 0:
                typeState[5] = 1
                audio.playSoundWindow("cold_wn_day_fi.mp3;cold_wn_day_fi_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
            else:
                audio.playSoundWindow("cold_wn_day.mp3;cold_wn_day_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
        else:
            if typeState[5] == 1:
                typeState[5] = 0
                audio.playSoundWindow("cold_wn_day_fo.mp3;cold_wn_day_fo_nm.mp3", [100, 100, 50], 1.0, 0.0, 0)
        
        time.sleep(194)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True


def run():
    status.hasExited = False
    main()
    status.hasExited = True

