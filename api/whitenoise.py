import modules.audio as audio
import modules.pytools as pytools
import os
import time
import random
import api.wind
import modules.logManager as log
import modules.weather as weather
import threading
import copy

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
    windowBroken = [False, False, False, False, False, False, False, False, False]
    windowOpen = [False, False, False, False, False, False, False, False, False]
    windowBoarded = [False, False, False, False, False, False, False, False, False]
    windowFixUtc = 0
    preparedForHurricane = False
    

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
    
    def isHighWindEventForecasted():
        startStamp = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        i = startStamp
        while i < (startStamp + 432000):
            try:
                if weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i))[0][1] > 27:
                    return True
            except:
                pass
            
            i = i + 3600
        
        return False
    
    def getWindAccumulation():
        startStamp = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        i = startStamp
        maxStamp = 0
        maximumGusts = 0
        while i < (startStamp + 864000):
            try:
                predictedDataArray = weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i))
                if predictedDataArray[0][1] > maximumGusts:
                    maximumGusts = predictedDataArray[0][1]
                    maxStamp = i
            except:
                pass
            
            i = i + 3600
        
        return [maximumGusts, pytools.clock.UTCToDateArray(maxStamp)]

def playWindowChange(windowIsOpen, waitDelay, windowIndex):
    timeToWait = waitDelay - time.time()
    
    if timeToWait > 0:
        time.sleep(timeToWait)
    
    if windowIsOpen:
        audioEvent = audio.event()
        audioEvent.register("openwindow1.mp3", 0, 100, 1.0, 0.0, 0)
        audioEvent.register("openwindow2.mp3", 2, 100, 1.0, 0.0, 0)
        audioEvent.run()
        
    else:
        audioEvent = audio.event()
        audioEvent.register("closewindow1.mp3", 0, 100, 1.0, 0.0, 0)
        audioEvent.register("closewindow2.mp3", 2, 100, 1.0, 0.0, 0)
        audioEvent.run()
        
    globals.windowOpen[windowIndex] = windowIsOpen
    
    def _fixBoolList(listf):
        out = []
        for x in listf:
            out.append(not not x)
        
        return out
    
    audio.command.setFlag("nomufflewn", sum(_fixBoolList(globals.windowOpen)) / len(globals.windowOpen))
    status.vars["percentageOfWindowsOpen"] = sum(_fixBoolList(globals.windowOpen)) / len(globals.windowOpen)
    
    pytools.IO.saveJson("windowState.json", {
        "windowBroken": globals.windowBroken,
        "windowFixUtc": globals.windowFixUtc,
        "windowOpen": globals.windowOpen,
        "windowBoarded": globals.windowBoarded,
        "preparedForHurricane": globals.preparedForHurricane
    })
    
    status.vars["windowState"] = {
        "windowBroken": globals.windowBroken,
        "windowFixUtc": globals.windowFixUtc,
        "windowOpen": globals.windowOpen,
        "windowBoarded": globals.windowBoarded,
        "preparedForHurricane": globals.preparedForHurricane
    }

class secs:
    
    lastOpenTime = time.time()
    
    def window(dataList):
        
        n = random.random()
        currentWaitTime = 0
        windowIndex = 0
        while windowIndex < len(globals.windowOpen):
        
            windowIsOpen = 0
            if globals.windowBroken[windowIndex] == 1:
                windowIsOpen = 1
            
            if dataList[0][7] >= 12:
                if dataList[0][1] <= 14:
                    if dataList[0][4] != "rain":
                        if dataList[0][4] != "lightrain":
                            if dataList[0][4] != "thunder":
                                windowIsOpen = 1
                                
            if globals.windowBoarded[windowIndex]:
                windowIsOpen = 0

            windowChanged = 0
            if (windowIsOpen == 1):
                if not globals.windowOpen[windowIndex]:
                    if globals.windowBroken[windowIndex] == 0:
                        windowChanged = True
                        globals.windowOpen[windowIndex] = 2
                    if not windowChanged:
                        globals.windowOpen[windowIndex] = True
            else:
                if globals.windowOpen[windowIndex] and not (globals.windowOpen[windowIndex] == 2):
                    if not globals.windowBoarded[windowIndex]:
                        windowChanged = True
                        globals.windowOpen[windowIndex] = 2
                    if not windowChanged:
                        globals.windowOpen[windowIndex] = False
            
            if windowChanged:
                if secs.lastOpenTime > time.time():
                    secs.lastOpenTime = secs.lastOpenTime + 20
                else:
                    secs.lastOpenTime = time.time() + 20
                
                threading.Thread(target=playWindowChange, args=(windowIsOpen, copy.deepcopy(secs.lastOpenTime), windowIndex,)).start()
            else:
                def _fixBoolList(listf):
                    out = []
                    for x in listf:
                        out.append(not not x)
                    
                    return out
                
                audio.command.setFlag("nomufflewn", sum(_fixBoolList(globals.windowOpen)) / len(globals.windowOpen))
                status.vars["percentageOfWindowsOpen"] = sum(_fixBoolList(globals.windowOpen)) / len(globals.windowOpen)
                
            
            windowIndex = windowIndex + 1

    def windowBreakState(dataList):
        rand = 37 * ((dataList[0][1] - 19 + api.wind.globals.windModif) ** 1.55)
        print(rand)
        randf = random.random() * 32768
        print(randf)
        if dataList[0][1] > 20 - api.wind.globals.windModif:
            if randf < (rand / 9):
                
                windowIndex = random.randint(0, 8)
                while globals.windowBroken[windowIndex] and (not all(globals.windowBroken)):
                    windowIndex = random.randint(0, 8)
                
                if globals.windowBroken[windowIndex] == 0:
                    
                    if not globals.windowBoarded[windowIndex]:
                        audioEvent = audio.event()
                        audioEvent.register("windowsmash.mp3", 2, 50, 1.0, 0.0, 0)
                        audioEvent.register("windowsmash.mp3", 3, 50, 1.0, 0.0, 0)
                        audioEvent.run()
                        time.sleep(6)
                        globals.windowBroken[windowIndex] = 1
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
                    else:
                        audioEvent = audio.event()
                        audioEvent.registerWindow("windowsmash_plywood_inside.mp3;windowsmash_plywood_outside.mp3;windowsmash_plywood_outside.mp3", [100, 50, 1], 0.97 + (random.random() * 0.06), 0.0, 0)
                        audioEvent.run()
                        time.sleep(47)
                        globals.windowBoarded[windowIndex] = False
                    secs.window(dataList)
                else:
                    windowFixArray = pytools.clock.getMidnight(pytools.clock.getDateTime())
                    windowFixArray[2] = windowFixArray[2] + 1
                    windowFixArray[3] = 15
                    globals.windowFixUtc = pytools.clock.dateArrayToUTC(pytools.clock.fixDateArray(windowFixArray))
    
    def windowUnboardState(dataList, windowIndex):
        rand = 37 * ((dataList[0][1] - 19 + api.wind.globals.windModif) ** 1.55)
        print(rand)
        randf = random.random() * 32768
        print(randf)
        if dataList[0][1] > 20 - api.wind.globals.windModif:
            if (randf / 4) < (rand / 3):
                if globals.windowBoarded[windowIndex]:
                    audioEvent = audio.event()
                    audioEvent.registerWindow("plywood_falling.mp3;plywood_falling.mp3;plywood_falling.mp3", [100, 10, 1], 0.97 + (random.random() * 0.06), 0.0, 0)
                    audioEvent.run()
                    time.sleep(6)
                    globals.windowBoarded[windowIndex] = False
                    secs.window(dataList)
    
    fixWindowIndex = 0
    
    def fixWindow(dataList):
        if secs.fixWindowIndex > 8:
            secs.fixWindowIndex = 0
            
        hasFixed = False
        
        while (not hasFixed) and (secs.fixWindowIndex <= 8):
            if globals.windowBroken[secs.fixWindowIndex]:
                if globals.windowBoarded[secs.fixWindowIndex]:
                    audioEvent = audio.event()
                    audioEvent.registerWindow("plywood_falling.mp3;plywood_falling.mp3;plywood_falling.mp3", [100, 10, 1], 0.97 + (random.random() * 0.06), 0.0, 0)
                    audioEvent.run()
                    time.sleep(6)
                    globals.windowBoarded[secs.fixWindowIndex] = False
                hasFixed = True
                audioEvent = audio.event()
                audioEvent.registerWindow("windowrepair.mp3;windowrepair.mp3;windowrepair.mp3", [10, 100, 5], 0.97 + (random.random() * 0.06), 0.0, 0)
                audioEvent.run()
                time.sleep(510)
                globals.windowBroken[secs.fixWindowIndex] = 0
                secs.window(dataList)
            
            secs.fixWindowIndex = secs.fixWindowIndex + 1
        
    def boardWindow(dataList, windowIndex):
        audioEvent = audio.event()
        audioEvent.registerWindow("boarding_windows_inside.mp3;boarding_windows_outside.mp3;boarding_windows_outside.mp3", [100, 75, 5], 0.97 + (random.random() * 0.06), 0.0, 0)
        audioEvent.run()
        time.sleep(4)
        globals.windowBoarded[windowIndex] = True
        secs.window(dataList)

def main():
    typeState = [0, 0, 0, 0, 0, 0]
    
    try:
        globals.windowOpen = pytools.IO.getJson("windowState.json")["windowOpen"]
    except:
        globals.windowOpen = [False, False, False, False, False, False, False, False, False]
    
    try:
        globals.windowBroken = pytools.IO.getJson("windowState.json")["windowBroken"]
    except:
        globals.windowBroken = [False, False, False, False, False, False, False, False, False]
        
    try:
        globals.windowFixUtc = pytools.IO.getJson("windowState.json")["windowFixUtc"]
    except:
        globals.windowFixUtc = 0
        
    try:
        globals.windowBoarded = pytools.IO.getJson("windowState.json")["windowBoarded"]
    except:
        globals.windowBoarded = [False, False, False, False, False, False, False, False, False]
        
    try:
        globals.preparedForHurricane = pytools.IO.getJson("windowState.json")["preparedForHurricane"]
    except:
        globals.preparedForHurricane = False
    
    while not status.exit:
        
        dateArray = pytools.clock.getDateTime()
        dayTimes = utils.dayTimesGrabber()
        dataList = utils.dataGrabber()

        secs.window(dataList)
        secs.windowBreakState(dataList)
        if any(globals.windowBroken) == 1:
            print(globals.windowFixUtc)
            print(pytools.clock.dateArrayToUTC(dateArray))
            if globals.windowFixUtc < pytools.clock.dateArrayToUTC(dateArray):
                secs.fixWindow(dataList)
            elif os.path.exists(".\\fixwindow.derp"):
                secs.fixWindow(dataList)
                os.system("del .\\fixwindow.derp /f /q")
            elif os.path.exists(".\\boardwindow.derp"):
                windowIndex = random.randint(0, 8)
                n = 0
                while ((globals.windowBoarded[windowIndex] or (not globals.windowBroken[windowIndex])) and (not all(globals.windowBoarded))) and (n < 300):
                    windowIndex = random.randint(0, 8)
                    n = n + 1
                    
                if not ((globals.windowBoarded[windowIndex] or (not globals.windowBroken[windowIndex])) and (not all(globals.windowBoarded))):
                    secs.boardWindow(dataList, windowIndex)
                    os.system("del .\\boardwindow.derp /f /q")
            elif 5 < dateArray[3] <= 23:
                if dataList[0][1] >= (36 - api.wind.globals.windModif):
                    installBoardChance = (1 + (0.085 - ((((dataList[0][1] - (35 - api.wind.globals.windModif)))) ** 0.04))) ** 1.1
                    if type(installBoardChance) == complex:
                        installBoardChance = 0
                else:
                    installBoardChance = ((0.34 - (((((dataList[0][1] - 1) - (35 - api.wind.globals.windModif)))) * 0.04)) / 4) ** 1.1
                
                n = 0
                if random.random() < installBoardChance:
                    windowIndex = random.randint(0, 8)
                    while ((globals.windowBoarded[windowIndex] or (not globals.windowBroken[windowIndex])) and (not all(globals.windowBoarded))) and (n < 300):
                        windowIndex = random.randint(0, 8)
                        n = n + 1
                    if not ((globals.windowBoarded[windowIndex] or (not globals.windowBroken[windowIndex])) and (not all(globals.windowBoarded))):
                        secs.boardWindow(dataList, windowIndex)
                    
        if any(globals.windowBoarded):
            
            windowIndex = random.randint(0, 8)
            while (not globals.windowBoarded[windowIndex]) and any(globals.windowBoarded):
                windowIndex = random.randint(0, 8)
            
            secs.windowUnboardState(dataList, windowIndex)
                    
        if weather.forecast.getHurricaneData(getClosest=True, isInForecast=True) or utils.isHighWindEventForecasted():
            if dateArray[3] > 6:
                if not globals.preparedForHurricane:
                    windowIndex = 0
                    while windowIndex < len(globals.windowBoarded):
                        if not globals.windowBoarded[windowIndex]:
                            secs.boardWindow(dataList, 0)
                            if windowIndex < (len(globals.windowBoarded) - 1):
                                time.sleep(60)
                        
                        windowIndex = windowIndex + 1
                    
                    globals.preparedForHurricane = True
        else:
            if globals.preparedForHurricane and (dataList[0][1] < (20 - api.wind.globals.windModif)):
                if dateArray[3] > 6:
                    windowIndex = 0
                    while windowIndex < len(globals.windowBoarded):
                        if globals.windowBoarded[windowIndex] and (not globals.windowBroken[windowIndex]):
                            audioEvent = audio.event()
                            audioEvent.registerWindow("plywood_falling.mp3;plywood_falling.mp3;plywood_falling.mp3", [100, 10, 1], 0.97 + (random.random() * 0.06), 0.0, 0)
                            audioEvent.run()
                            globals.windowBoarded[windowIndex] = False
                            secs.window(dataList)
                            if windowIndex < (len(globals.windowBoarded) - 1):
                                time.sleep(30)
                                
                        windowIndex = windowIndex + 1
                    
                    globals.preparedForHurricane = False
                
                
        pytools.IO.saveJson("windowState.json", {
            "windowBroken": globals.windowBroken,
            "windowFixUtc": globals.windowFixUtc,
            "windowOpen": globals.windowOpen,
            "windowBoarded": globals.windowBoarded,
            "preparedForHurricane": globals.preparedForHurricane
        })
        
        status.vars["windowState"] = {
            "windowBroken": globals.windowBroken,
            "windowFixUtc": globals.windowFixUtc,
            "windowOpen": globals.windowOpen,
            "windowBoarded": globals.windowBoarded,
            "preparedForHurricane": globals.preparedForHurricane
        }
        
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

