import modules.audio as audio
import modules.pytools as pytools
import time
import os
import traceback
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
    
    deathSection = ""
    
    def getSection():
        dateArray = pytools.clock.getDateTime()
        dayTimes = pytools.IO.getList(".\\daytimes.pyl", False)[1]
        phases = ["Daylight Phase", "Uncanny Phase", "Dark Phase", "Evil Phase", "Sinister Phase", "Dying Phase P1", "Dying Phase P2", "Dying Phase P3", "Dying Phase P4", "Death Phase", "Necro Phase", "Reserect Phase", "Safe Phase"]
        if pytools.clock.dateArrayToUTC(dateArray) < pytools.clock.dateArrayToUTC(dayTimes[5]):
            return phases[0]
        else:
            if dateArray[3] > 12:
                if dateArray[3] < 22:
                    try:
                        if pytools.IO.getJson("..\\vars\\pluginVarsJson\\deathmode_keys.json", False)["death_wind"]["state"] == 0:
                            return phases[1]
                        else:
                            try:
                                if pytools.IO.getJson("..\\vars\\pluginVarsJson\\deathmode_keys.json", False)["monsters"]["state"] == 0:
                                    return phases[2]
                                else:
                                    try:
                                        if pytools.IO.getJson("..\\vars\\pluginVarsJson\\deathmode_keys.json", False)["ghosts"]["state"] == 0:
                                            return phases[3]
                                        else:
                                            return phases[4]
                                    except:
                                        return phases[3]
                            except:
                                return phases[2]
                    except:
                        return phases[1]
                elif dateArray[3] == 22:
                    if dateArray[4] < 15:
                        return phases[5]
                    if dateArray[4] < 30:
                        return phases[6]
                    if dateArray[4] < 45:
                        return phases[7]
                    if dateArray[4] >= 45:
                        return phases[8]
                elif dateArray[3] == 23:
                    return phases[9]
            elif dateArray[3] < (dayTimes[2][3] - 1):
                return phases[10]
            elif dateArray[3] == (dayTimes[2][3] - 1):
                return phases[11]
            else:
                return phases[12]

def playDeath(typef=1):
    if os.path.isfile("halloweenmode.derp"):
        if typef == 1:
            audio.playSoundWindow("dnwbella.mp3;dnwbella.mp3", [20, 75, 50], 1.0, 0, 1)
        elif typef != 0:
            audio.playSoundWindow("dnwbell" + str(typef) + ".mp3;dnwbell" + str(typef) + ".mp3", [20, 75, 50], 1.0, 0, 1)
        
def playDnwbell():
    if not (globals.getSection() == globals.deathSection):
        globals.deathSection = globals.getSection()
        bellCount = {
            "Daylight Phase": 0,
            "Uncanny Phase": 2,
            "Dark Phase": 4,
            "Evil Phase": 6,
            "Sinister Phase": 8,
            "Dying Phase P1": 9,
            "Dying Phase P2": 10,
            "Dying Phase P3": 11,
            "Dying Phase P4": 12,
            "Death Phase": 13,
            "Necro Phase": 3,
            "Reserect Phase": 2,
            "Safe Phase": 1
        }
        
        playDeath(typef=bellCount[globals.deathSection])
        
def getWeekDayOfMonthNumber(dateArray):
    day = 1
    i = 0
    while day <= pytools.clock.getMonthEnd(dateArray[1]):
        if pytools.clock.getDayOfWeek(dateArray=[dateArray[0], dateArray[1], day, 0, 0, 0]) == pytools.clock.getDayOfWeek(dateArray):
            i = i + 1
        if day == dateArray[2]:
            return i
        day = day + 1
    return 1

def main():
    while not status.exit:
        weekDay = pytools.clock.getDayOfWeek()
        dateArray = pytools.clock.getDateTime()
        if dateArray[3] == 9:
            if dateArray[4] == 5:
                audio.playSoundWindow("cb1.mp3;cb1.mp3", [10, 75, 50], 1.0, 0, 1)
                playDeath()
        if dateArray[3] == 14:
            if dateArray[4] == 5:
                audio.playSoundWindow("cb4.mp3;cb4.mp3", [10, 75, 50], 1.0, 0, 1)
                playDeath()
        if dateArray[3] == 18:
            if dateArray[4] == 5:
                audio.playSoundWindow("cb5.mp3;cb5.mp3", [10, 75, 50], 1.0, 0, 1)
                playDeath()
        if (weekDay == 0) or ((dateArray[1] == 10) and (getWeekDayOfMonthNumber(dateArray) == 2) and (weekDay == 1)) or ((dateArray[1] == 11) and (dateArray[2] == 11)) or ((dateArray[1] == 7) and (dateArray[2] == 1))  or ((dateArray[1] == 10) and (dateArray[2] == 31)) or ((dateArray[1] == 10) and (dateArray[2] == 13)) or ((dateArray[1] == 12) and (dateArray[2] == 24)) or ((dateArray[1] == 12) and (dateArray[2] == 25)):
            if dateArray[3] == 10:
                if dateArray[4] == 35:
                    audio.playSoundWindow("cb2.mp3;cb3.mp3", [10, 75, 50], 1.0, 0, 1)
                    playDeath()
            if dateArray[3] == 11:
                if dateArray[4] == 50:
                    audio.playSoundWindow("cb2.mp3;cb3.mp3", [10, 75, 50], 1.0, 0, 1)
                    playDeath()
        
        playDnwbell()
        
        time.sleep(60)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
