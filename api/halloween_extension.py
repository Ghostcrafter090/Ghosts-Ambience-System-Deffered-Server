import modules.audio as audio
from datetime import datetime
import random
import os
import sys
import modules.pytools as pytools
import time
import threading
import math
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
        "horrorIndex": 0,
        "horrorStats": {
            "sections.ghostsChance-0": 0,
            "sections.ghostsChance-1": 0,
            "sections.ghostsChance-2": 0,
            "sections.draftChance": 0,
            "sections.breathChance": 0,
            "sections.moodChance": 0,
            "sections.knockChance": 0,
            "sections.chainChance": 0
        }
    }
    
class globals:
    run = False
    runUncanny = False
    
class data:
    sunJson = {}
    dayTimes = []
    dateArray = []
    minZ = 0
    hourZ = 0
    
    def grabWeatherData():
        try:
            dataArray = pytools.IO.getList(".\\dataList.pyl")[1]
            lightningDanger = pytools.IO.getJson("lightningData.json")["dangerLevel"]
            return [dataArray, lightningDanger]
        except:
            return False
    
    def grabSunData():
        while not status.exit:
            try:
                error = 1
                while error == 1:
                    try:
                        data.dayTimes = pytools.IO.getList("dayTimes.pyl")[1]
                        data.sunJson = {
                            "ceth": data.dayTimes[6][3],
                            "cetm": data.dayTimes[6][4],
                            "csth": data.dayTimes[2][3],
                            "cstm": data.dayTimes[2][4],
                            "cesth": data.dayTimes[5][3],
                            "cestm": data.dayTimes[5][4],
                            "neth": data.dayTimes[7][3],
                            "netm": data.dayTimes[7][4],
                            "aeth": data.dayTimes[8][3],
                            "aetm": data.dayTimes[8][4]
                        }
                        # data.sunJson = json.loads(("{\"" + getFile('data.dayTimes.cmd').replace("set ", "").replace("\n", "\", \"").replace("=", "\": \"") + "}").replace(", \"}", "}").replace(" \",", "\",").replace(" \"}", "\"}"))
                        doNull(data.sunJson['ceth'])
                        doNull(data.sunJson['cetm'])
                        doNull(data.sunJson['csth'])
                        doNull(data.sunJson['cstm'])
                        doNull(data.sunJson['cesth'])
                        doNull(data.sunJson['cestm'])
                        error = 0
                    except:
                        error = 1
            except:
                pass
            time.sleep(10)
    
    def getZ():
        error = True
        while error:
            try:
                dummy(data.sunJson['cetm'])
                error = False
            except:
                pass
        data.minZ = (int(data.sunJson['cetm']) + 30)
        data.hourZ = (int(data.sunJson['ceth']))
        if data.minZ < 0:
            data.minZ = data.minZ + 60
            data.hourZ = data.hourZ - 1
            
    # https://www.desmos.com/calculator/jertocumt3
    def getWeatherHallowModifier():
        
        dataf = data.grabWeatherData()
        
        if dataf:
            try:
                lightningModif = (1.14898 ** (0.997531 * (dataf[1] + 0.00708756)) - 0.000982331) * 2
            except:
                lightningModif = 0
            try:
                baseIndex = data.getHallowIndex(pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()), noModif=True)
                if baseIndex > 0:
                    windGustModif = (1.0382 ** (0.9993 * (dataf[0][0][1] - 1.00002)) - 0.963234) * (150 - baseIndex) ** 0.35
                else:
                    windGustModif = (1.0382 ** (0.9993 * (dataf[0][0][1] - 1.00002)) - 0.963234) * 2.5
            except:
                windGustModif = 0
            try:
                windSpeedModif = 1.0382 ** (0.9993 * (dataf[0][0][0] - 1.00002)) - 0.963234
            except:
                windSpeedModif = 0
            if windGustModif > windSpeedModif:
                windModif = windGustModif
            else:
                windModif = windSpeedModif
            weatherModif = 0
            try:
                if dataf[0][0][4] == "lightrain":
                    weatherModif = 1.5
                elif dataf[0][0][4] == "rain":
                    weatherModif = 3
                elif dataf[0][0][4] == "snow":
                    weatherModif = 3
                elif dataf[0][0][4] == "thunder":
                    weatherModif = 4.5
            except:
                pass
        else:
            return False
        
        return lightningModif + windModif + weatherModif
            
    # https://www.desmos.com/calculator/sd674thhfq
    def getHallowIndex(timeStamp, noDay=False, noModif=False):
        u = math.floor(timeStamp / (365 * 24 * 60 * 60))
        w = (timeStamp - (24 * 60 * 60) - (u * (365 * 24 * 60 * 60)) - 1)
        q = math.floor(math.floor(((u) / (4))) - (((u) / (4))) + 1) * 24 * 60 * 60
        a = 100
        b = 26265600 + q
        c = 3000000000000
        f = 30931200 + q
        g = 300000000000
        p = 3.14159265359
        h = 50
        e = 2.71828182846
        j = 16 * math.sin((((p) / (1180295.8))) * ( - (w - (((1180295.8) / (2)))) - (u * (365.25 * 24 * 60 * 60))))
        l_2 = 13 * e ** ( - (((w - 1080000) ** (2)) / (g)))
        l_3 = 13 * e ** ( - (((w - 3758400) ** (2)) / (g)))
        l_4 = 13 * e ** ( - ((((w - q) - 6177600) ** (2)) / (g)))
        l_5 = 13 * e ** ( - ((((w - q) - 8856000) ** (2)) / (g)))
        l_6 = 13 * e ** ( - ((((w - q) - 11448000) ** (2)) / (g)))
        l_7 = 13 * e ** ( - ((((w - q) - 14126400) ** (2)) / (g)))
        l_8 = 13 * e ** ( - ((((w - q) - 16718400) ** (2)) / (g)))
        l_9 = 13 * e ** ( - ((((w - q) - 19396800) ** (2)) / (g)))
        l_10 = 13 * e ** ( - ((((w - q) - 22075200) ** (2)) / (g)))
        l_11 = 13 * e ** ( - ((((w - q) - 24667200) ** (2)) / (g)))
        l_12 = 13 * e ** ( - ((((w - q) - 27345600) ** (2)) / (g)))
        l_13 = 13 * e ** ( - ((((w - q) - 29937600) ** (2)) / (g)))
        r = 29376000 + q
        s = 27302400 + q
        t = - 2 * ((a * e ** ( - (((w - r) ** (2)) / (c)))) + (h * e ** ( - (((w - r) ** (2)) / (g)))))
        z = - 2 * ((a * e ** ( - (((((w - s) ** (2)) / (c))) / (0.15)))) + (h * e ** ( - (((((w - s) ** (2)) / (g))) / (0.15)))))
        k = 18 * math.sin((((p) / (302400.0))) * ((w + 36 * 60 * 60) + (u * 365.25 * 24 * 60 * 60) - 6))
        z_1 = 16 * math.sin((((p) / (1180295.8))) * ( - (24778000.0 - (((1180295.8) / (2)))) - (u * (356.25 * 24 * 60 * 60)))) + (7 * math.sin((((p) / (302400.0))) * ((24778000.0 + 12 * 60 * 60) + (u * 365.25 * 24 * 60 * 60) - 6))) + 13
        o = - 3 * ((a * e ** ( - (((w - f) ** (2)) / (c)))) + (h * e ** ( - (((w - f) ** (2)) / (g)))))
        m = (1.11 * (((((math.fabs(z_1 )) / (2)) + 15) / (15)) ** (1) * (a * e ** ( - 0.65 * (((w - b) ** (2)) / (c))))) + (h * e ** ( - 0.65 * (((w - b) ** (2)) / (g))))) + j + k + (2 * (l_2 + l_3 + l_4 + l_5 + l_6 + l_7 + l_8 + l_9 + l_10 + l_11 + l_12 + l_13)) + o + t + z - 40
        if not noModif:
            weatherModif = data.getWeatherHallowModifier()
        else:
            weatherModif = 0
        if weatherModif:
            m = m + weatherModif
        n = - 10 * math.sin(((p) / (12 * 60 * 60)) * (w - 6 * 60 * 60))
        z_2 = ((1) / (2)) * (n * (((m) / (10))) + m)
        if noDay:
            return m
        else:
            return z_2

def dummy(var):
    pass

def getFile(path):
    error = 0
    try:
        file = open(path, "r")
        jsonData = file.read()
        file.close()
    except:
        print("Unexpected error:", sys.exc_info())
        error = 1
    if error != 0:
        jsonData = error
    return jsonData

def saveFile(path, jsonData):
    error = 0
    try:
        file = open(path, "w")
        file.write(jsonData)
        file.close()
    except:
        print("Unexpected error:", sys.exc_info())
        error = 1
    return error

def getDateTime():
    daten = datetime.now()
    data.dateArray = [1970, 1, 1, 0, 0, 0]
    data.dateArray[0] = int(str(daten).split(" ")[0].split("-")[0])
    data.dateArray[1] = int(str(daten).split(" ")[0].split("-")[1])
    data.dateArray[2] = int(str(daten).split(" ")[0].split("-")[2])
    data.dateArray[3] = int(str(daten).split(" ")[1].split(":")[0])
    data.dateArray[4] = int(str(daten).split(" ")[1].split(":")[1])
    data.dateArray[5] = int(str(daten).split(" ")[1].split(":")[2].split(".")[0])
    return data.dateArray
    
def playSound(path, speaker, volume, speed, balence, waitBool):
    if speaker == 0:
        speakern = "clock.exe"
    elif speaker == 1:
        speakern = "fireplace.exe"
    else:
        speakern = "windown.exe"
    if waitBool == 0:
        os.system('cmd.exe /c start /b "" ' + speakern + ' runaudio.vbs ' + path + ' ' + str(volume) + ' ' + str(balence) + ' ' + str(speed) + ' ' + path.split(".")[0])
        print("Playing sound " + path + " on speaker " + speakern + " with volume " + str(volume) + " with speed of " + str(speed) + " with balence of " + str(balence) + "...")
    else:
        os.system('cmd.exe /c start /b /wait "" ' + speakern + ' runaudio.vbs ' + path + ' ' + str(volume) + ' ' + str(balence) + ' ' + str(speed) + ' ' + path.split(".")[0])
        print("Playing sound " + path + " on speaker " + speakern + " with volume " + str(volume) + " with speed of " + str(speed) + " with balence of " + str(balence) + ". Waiting...")

def closetomidTest(dateArray, hour, day, minute, noA):
    if data.dateArray[3] == hour:
        if data.dateArray[2] > day:
            if data.dateArray[4] == minute:
                if noA != 1:
                    audio.playSoundAll('closetomidnight.mp3', 40, 1, 0, 0)
                    noA = 1
            else:
                noA = 0
        else:
            noA = 0
    else:
        noA = 0
    return noA
    
def doNull(val):
    return val

class mainVars:
    noA = 0
    noB = 0
    noC = 0
    noD = 0

class sections:
    ghostsChance = [0, 0, 0]
    
    def testGhosts():
        ghostsChance = [0, 0, 0]
        while not status.exit:
            if globals.run:
                try:
                    deathGhostChance = 0
                    dyingGhostChance = 0
                    ghostChance = 0
                    if data.dateArray[2] > 24:
                        if data.dateArray[3] > data.hourZ:
                                deathGhostChance = (data.dateArray[3] - (int(data.hourZ + 2))) * data.dateArray[4]
                                deathGhostChance = deathGhostChance / (32 - data.dateArray[2])
                                deathGhostChance = deathGhostChance * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 170)
                                if random.randrange(0, 37500) < (deathGhostChance / ((32 - data.dateArray[2]) / 3) + 1):
                                    ghSpeaker = 5
                                    while ghSpeaker == 5:
                                        ghSpeaker = random.randrange(0, 10)
                                    audioEvent = audio.event()
                                    speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                                    audioEvent.register('death_ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                    audioEvent.run()
                        elif data.dateArray[3] == data.hourZ:
                            if data.dateArray[4] >= data.minZ:
                                deathGhostChance = (data.dateArray[3] - (int(data.hourZ + 2))) * data.dateArray[4]
                                deathGhostChance = deathGhostChance / (32 - data.dateArray[2])
                                deathGhostChance = deathGhostChance * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 170)
                                if random.randrange(0, 37500) < (deathGhostChance / ((32 - data.dateArray[2]) / 3) + 1):
                                    ghSpeaker = 5
                                    while ghSpeaker == 5:
                                        ghSpeaker = random.randrange(0, 10)
                                    audioEvent = audio.event()
                                    speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                                    audioEvent.register('death_ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                    audioEvent.run()
                    if data.dateArray[2] > 19:
                        if data.dateArray[3] > data.hourZ:
                            dyingGhostChance = (data.dateArray[3] - (int(data.hourZ + 1))) * data.dateArray[4]
                            dyingGhostChance = dyingGhostChance / (32 - data.dateArray[2])
                            dyingGhostChance = dyingGhostChance * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 170)
                            if random.randrange(0, 37500) < (dyingGhostChance / ((32 - data.dateArray[2]) / 5) + 1):
                                ghSpeaker = 5
                                while ghSpeaker == 5:
                                    ghSpeaker = random.randrange(0, 10)
                                audioEvent = audio.event()
                                speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                                audioEvent.register('dying_ghost_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                audioEvent.run()
                        elif data.dateArray[3] == data.hourZ:
                            if data.dateArray[4] >= data.minZ:
                                dyingGhostChance = 0
                                if data.dateArray[3] < (24):
                                    dyingGhostChance = (data.dateArray[3] - (int(data.hourZ + 1))) * data.dateArray[4]
                                    dyingGhostChance = dyingGhostChance / (32 - data.dateArray[2])
                                    dyingGhostChance = dyingGhostChance * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 170)
                                if random.randrange(0, 37500) < (dyingGhostChance / ((32 - data.dateArray[2]) / 5) + 1):
                                    ghSpeaker = 5
                                    while ghSpeaker == 5:
                                        ghSpeaker = random.randrange(0, 10)
                                    audioEvent = audio.event()
                                    speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                                    audioEvent.register('dying_ghost_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                    audioEvent.run()
                    if data.dateArray[2] > 9:
                        if data.dateArray[3] > data.hourZ:
                            ghostChance = 0
                            if data.dateArray[3] < (24):
                                ghostChance = (data.dateArray[3] - (int(data.hourZ))) * data.dateArray[4]
                                ghostChance = ghostChance / (32 - data.dateArray[2])
                                ghostChance = ghostChance * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 170)
                            if random.randrange(0, 37500) < (ghostChance / ((32 - data.dateArray[2]) / 9) + 1):
                                ghSpeaker = 5
                                while ghSpeaker == 5:
                                    ghSpeaker = random.randrange(0, 10)
                                audioEvent = audio.event()
                                speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                                audioEvent.register('ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, (0.5 + random.random()) * 40, speed, 0, 0)
                                audioEvent.run()
                        elif data.dateArray[3] == data.hourZ:
                            if data.dateArray[4] >= data.minZ:
                                ghostChance = 0
                                if data.dateArray[3] < (24):
                                    ghostChance = (data.dateArray[3] - (int(data.hourZ))) * data.dateArray[4]
                                    ghostChance = ghostChance / (32 - data.dateArray[2])
                                    ghostChance = ghostChance * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 170)
                                if random.randrange(0, 37500) < (ghostChance / ((32 - data.dateArray[2]) / 9) + 1):
                                    ghSpeaker = 5
                                    while ghSpeaker == 5:
                                        ghSpeaker = random.randrange(0, 10)
                                    audioEvent = audio.event()
                                    speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                                    audioEvent.register('ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, (0.5 + random.random()) * 40, speed, 0, 0)
                                    audioEvent.run()
                    time.sleep(0.1)
                    sections.ghostsChance = [(deathGhostChance / ((32 - data.dateArray[2]) / 3) + 1), (dyingGhostChance / ((32 - data.dateArray[2]) / 5) + 1), (ghostChance / ((32 - data.dateArray[2]) / 9) + 1)]
                except:
                    pass
            wait = True
            for n in sections.ghostsChance:
                if n > 1:
                    wait = False
            if wait:
                time.sleep(1)
    
    uncannyGhostsChance = [0, 0, 0]
             
    def testGhostsUncanny():
        uncannyGhostsChance = [0, 0, 0]
        while not status.exit:
            if globals.runUncanny:
                try:
                    uncannyDeathGhostChance = 0
                    uncannyDyingGhostChance = 0
                    uncannyGhostChance = 0
                    if data.dateArray[2] > 24:
                        if data.dateArray[3] > data.hourZ:
                                uncannyDeathGhostChance = (data.dateArray[3] - (int(data.hourZ + 2))) * data.dateArray[4]
                                uncannyDeathGhostChance = uncannyDeathGhostChance / (32 - data.dateArray[2])
                                uncannyDeathGhostChance = uncannyDeathGhostChance * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 170)
                                if random.randrange(0, 37500) < (uncannyDeathGhostChance / ((32 - data.dateArray[2]) / 3) + 1):
                                    ghSpeaker = 5
                                    while ghSpeaker == 5:
                                        ghSpeaker = random.randrange(0, 10)
                                    audioEvent = audio.event()
                                    speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                                    audioEvent.register('hu_death_ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                    audioEvent.run()
                        elif data.dateArray[3] == data.hourZ:
                            if data.dateArray[4] >= data.minZ:
                                uncannyDeathGhostChance = (data.dateArray[3] - (int(data.hourZ + 2))) * data.dateArray[4]
                                uncannyDeathGhostChance = uncannyDeathGhostChance / (32 - data.dateArray[2])
                                uncannyDeathGhostChance = uncannyDeathGhostChance * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 170)
                                if random.randrange(0, 37500) < (uncannyDeathGhostChance / ((32 - data.dateArray[2]) / 3) + 1):
                                    ghSpeaker = 5
                                    while ghSpeaker == 5:
                                        ghSpeaker = random.randrange(0, 10)
                                    audioEvent = audio.event()
                                    speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                                    audioEvent.register('hu_death_ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                    audioEvent.run()
                    if data.dateArray[2] > 19:
                        if data.dateArray[3] > data.hourZ:
                            uncannyDyingGhostChance = (data.dateArray[3] - (int(data.hourZ + 1))) * data.dateArray[4]
                            uncannyDyingGhostChance = uncannyDyingGhostChance / (32 - data.dateArray[2])
                            uncannyDyingGhostChance = uncannyDyingGhostChance * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 170)
                            if random.randrange(0, 37500) < (uncannyDyingGhostChance / ((32 - data.dateArray[2]) / 5) + 1):
                                ghSpeaker = 5
                                while ghSpeaker == 5:
                                    ghSpeaker = random.randrange(0, 10)
                                audioEvent = audio.event()
                                speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                                audioEvent.register('hu_dying_ghost_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                audioEvent.run()
                        elif data.dateArray[3] == data.hourZ:
                            if data.dateArray[4] >= data.minZ:
                                uncannyDyingGhostChance = 0
                                if data.dateArray[3] < (24):
                                    uncannyDyingGhostChance = (data.dateArray[3] - (int(data.hourZ + 1))) * data.dateArray[4]
                                    uncannyDyingGhostChance = uncannyDyingGhostChance / (32 - data.dateArray[2])
                                    uncannyDyingGhostChance = uncannyDyingGhostChance * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 170)
                                if random.randrange(0, 37500) < (uncannyDyingGhostChance / ((32 - data.dateArray[2]) / 5) + 1):
                                    ghSpeaker = 5
                                    while ghSpeaker == 5:
                                        ghSpeaker = random.randrange(0, 10)
                                    audioEvent = audio.event()
                                    speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                                    audioEvent.register('hu_dying_ghost_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                    audioEvent.run()
                    if data.dateArray[2] > 9:
                        if data.dateArray[3] > data.hourZ:
                            uncannyGhostChance = 0
                            if data.dateArray[3] < (24):
                                uncannyGhostChance = (data.dateArray[3] - (int(data.hourZ))) * data.dateArray[4]
                                uncannyGhostChance = uncannyGhostChance / (32 - data.dateArray[2])
                                uncannyGhostChance = uncannyGhostChance * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 170)
                            if random.randrange(0, 37500) < (uncannyGhostChance / ((32 - data.dateArray[2]) / 9) + 1):
                                ghSpeaker = 5
                                while ghSpeaker == 5:
                                    ghSpeaker = random.randrange(0, 10)
                                audioEvent = audio.event()
                                speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                                audioEvent.register('hu_ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, (0.5 + random.random()) * 40, speed, 0, 0)
                                audioEvent.run()
                        elif data.dateArray[3] == data.hourZ:
                            if data.dateArray[4] >= data.minZ:
                                uncannyGhostChance = 0
                                if data.dateArray[3] < (24):
                                    uncannyGhostChance = (data.dateArray[3] - (int(data.hourZ))) * data.dateArray[4]
                                    uncannyGhostChance = uncannyGhostChance / (32 - data.dateArray[2])
                                    uncannyGhostChance = uncannyGhostChance * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 170)
                                if random.randrange(0, 37500) < (uncannyGhostChance / ((32 - data.dateArray[2]) / 9) + 1):
                                    ghSpeaker = 5
                                    while ghSpeaker == 5:
                                        ghSpeaker = random.randrange(0, 10)
                                    audioEvent = audio.event()
                                    speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                                    audioEvent.register('hu_ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, (0.5 + random.random()) * 40, speed, 0, 0)
                                    audioEvent.run()
                    time.sleep(0.1)
                    sections.uncannyGhostsChance = [(uncannyDeathGhostChance / ((32 - data.dateArray[2]) / 3) + 1), (uncannyDyingGhostChance / ((32 - data.dateArray[2]) / 5) + 1), (uncannyGhostChance / ((32 - data.dateArray[2]) / 9) + 1)]
                except:
                    pass
            wait = True
            for n in sections.uncannyGhostsChance:
                if n > 1:
                    wait = False
            if wait:
                time.sleep(1)

    def closeMidTestRun():
        while not status.exit:
            if globals.run:
                try:
                    mainVars.noA = closetomidTest(data.dateArray, 23, 25, 10, mainVars.noA)
                    mainVars.noB = closetomidTest(data.dateArray, 23, 20, 15, mainVars.noB)
                    mainVars.noC = closetomidTest(data.dateArray, 23, 15, 30, mainVars.noC)
                    mainVars.noD = closetomidTest(data.dateArray, 23, 10, 45, mainVars.noD)
                except:
                    pass
            time.sleep(1)
    
    draftChance = 0
    
    def runDrafts():
        while not status.exit:
            if globals.run:
                try:
                    draftChance = 0
                    if data.dateArray[3] < 24:
                        draftChance = (data.dateArray[3] - (int(data.sunJson['cesth']))) * data.dateArray[4] * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)
                    if data.dateArray[3] < (int(data.sunJson['csth'])):
                        draftChance = ((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4] * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)

                    if random.randrange(0, 25000) < draftChance:
                        ghSpeaker = 5
                        while ghSpeaker == 5:
                            ghSpeaker = random.randrange(0, 10)
                        audioEvent = audio.event()
                        speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                        audioEvent.register('draft_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, (20 * ((0.6 * random.random()) + 0.4)) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                        audioEvent.run()
                    sections.draftChance = draftChance
                    time.sleep(0.1)
                except:
                    pass
            if sections.draftChance <= 0:
                time.sleep(1)
                
    uncannyDraftChance = 0
    
    def runUncannyDrafts():
        while not status.exit:
            if globals.runUncanny:
                try:
                    uncannyDraftChance = 0
                    if data.dateArray[3] < 24:
                        uncannyDraftChance = (data.dateArray[3] - (int(data.sunJson['cesth']))) * data.dateArray[4] * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)
                    if data.dateArray[3] < (int(data.sunJson['csth'])):
                        uncannyDraftChance = ((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4] * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)

                    if random.randrange(0, 25000) < uncannyDraftChance:
                        ghSpeaker = 5
                        while ghSpeaker == 5:
                            ghSpeaker = random.randrange(0, 10)
                        audioEvent = audio.event()
                        speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                        audioEvent.register('hu_draft_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, (20 * ((0.6 * random.random()) + 0.4)) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                        audioEvent.run()
                    sections.uncannyDraftChance = uncannyDraftChance
                    time.sleep(0.1)
                except:
                    pass
            if sections.uncannyDraftChance <= 0:
                time.sleep(1)
        
    breathChance = 0
    
    def runBreaths():
        while not status.exit:
            if globals.run:
                try:
                    breathChance = 0
                    if data.dateArray[3] < (int(data.sunJson['csth'])):
                        breathChance = ((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4]
                    breathChance = (breathChance / (32 - data.dateArray[2])) * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)
                    if random.randrange(0, 25000) < breathChance:
                        ghSpeaker = 5
                        while ghSpeaker == 5:
                            ghSpeaker = random.randrange(0, 10)
                        audioEvent = audio.event()
                        speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                        audioEvent.register('h_breath_' + str(random.randrange(0, 4)) + ".mp3", ghSpeaker, 40 * ((0.6 * random.random()) + 0.4), speed, 0, 0)
                        audioEvent.run()
                    sections.breathChance = breathChance
                    time.sleep(0.1)
                except:
                    pass
            if sections.draftChance <= 0:
                time.sleep(1)
                
    uncannyBreathChance = 0
    
    def runUncannyBreaths():
        while not status.exit:
            if globals.runUncanny:
                try:
                    uncannyBreathChance = 0
                    if data.dateArray[3] < (int(data.sunJson['csth'])):
                        uncannyBreathChance = ((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4]
                    uncannyBreathChance = (uncannyBreathChance / (32 - data.dateArray[2])) * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)
                    if random.randrange(0, 25000) < uncannyBreathChance:
                        ghSpeaker = 5
                        while ghSpeaker == 5:
                            ghSpeaker = random.randrange(0, 10)
                        audioEvent = audio.event()
                        speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray)) - 492.654)) - 0.0531709)
                        audioEvent.register('hu_breath_' + str(random.randrange(0, 4)) + ".mp3", ghSpeaker, 40 * ((0.6 * random.random()) + 0.4), speed, 0, 0)
                        audioEvent.run()
                    sections.uncannyBreathChance = uncannyBreathChance
                    time.sleep(0.1)
                except:
                    pass
            if sections.draftChance <= 0:
                time.sleep(1)
                
    moodChance = [0, 0, 0, 0, 0, 0]

    def runMood():
        prevMin = -1
        while not status.exit:
            if globals.run:
                try:
                    if ((os.path.isfile('deathmode.derp') == True) and (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) > 0)) or (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) > 0):
                        if prevMin != data.dateArray[4]:
                            monthS = pytools.clock.dateArrayToUTC([data.dateArray[0], data.dateArray[1], 1, 0, 0, 0])
                            monthE = pytools.clock.dateArrayToUTC([data.dateArray[0], data.dateArray[1] + 1, 1, 0, 0, 0])
                            monthC = pytools.clock.dateArrayToUTC(data.dateArray) - monthS
                            
                            hGeneralVol = (42 * (0.5 + (monthC / (monthE - monthS))))
                            if hGeneralVol > 35:
                                hGeneralVol = 35
                            hGeneralVol = hGeneralVol * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)
                            hGeneralSpeedModifier = 0.08
                            midnight = pytools.clock.dateArrayToUTC(pytools.clock.getMidnight(data.dateArray))
                            sunset = pytools.clock.dateArrayToUTC(data.dayTimes[5])
                            civil = pytools.clock.dateArrayToUTC(data.dayTimes[2])
                            sunrise = pytools.clock.dateArrayToUTC(data.dayTimes[3])
                            current = pytools.clock.dateArrayToUTC(data.dateArray)
                            try:
                                if current > sunset:
                                    hGeneralSpeedModifier = 0.08 * (((midnight - sunset) - (midnight - current)) / (midnight - sunset))
                                elif (midnight - current) > 82800:
                                    hGeneralSpeedModifier = 0.08 * (1 - ((midnight - current - 83160) / 3600))
                                elif current < civil:
                                    hGeneralSpeedModifier = 0.1
                                elif current < sunrise:
                                    hGeneralSpeedModifier =  0.1 * (((sunrise - civil) / ((sunrise - civil + 1) - (sunrise - current))) - 1)
                                else:
                                    hGeneralSpeedModifier = 0
                            except:
                                pass
                            if hGeneralSpeedModifier > 0.4:
                                hGeneralSpeedModifier = 0.4
                            elif hGeneralSpeedModifier < 0:
                                hGeneralSpeedModifier = 0
                            hGeneralSpeedModifier = (hGeneralSpeedModifier * (monthC / (monthE - monthS))) * (1.05 - (1 + (((data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)) ** 0.1) - 1))
                            # if data.dateArray[1] != 11:
                            print("Looping h_general effect at volume " + str(hGeneralVol) + ", and speed " + str(1 - hGeneralSpeedModifier) + ".")
                            audio.playSoundAll('h_general.mp3', hGeneralVol, 1 - hGeneralSpeedModifier, 0, 0)
                            # else:
                                # audio.playSoundAll('h_general.mp3', hGeneralVol * (1 - (((data.dateArray[3] * 60 * 60) + (data.dateArray[4] * 60) + (data.dateArray[5])) / ((data.sunJson["csth"] * 60 * 60) + (data.sunJson["cstm"] * 60)))), 1 - hGeneralSpeedModifier, 0, 0)
                            prevMin = data.dateArray[4]
                        
                        moodChance = [0, 0, 0, 0, 0, 0]
                        
                        moodChance[0] = (data.dateArray[3] - (int(data.sunJson['cesth']))) * data.dateArray[4]
                        if data.dateArray[3] < (int(data.sunJson['csth'])):
                            moodChance[0] = ((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4]
                        
                        moodChance[1] = ((data.dateArray[3] - (int(data.sunJson['ceth']))) * data.dateArray[4] / 3) / (32 - data.dateArray[2])
                        if data.dateArray[3] < (int(data.sunJson['csth'])):
                            moodChance[1] = (((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4] / 3) / (32 - data.dateArray[2])
                        
                        moodChance[2] = ((data.dateArray[3] - (int(data.sunJson['neth']))) * data.dateArray[4] / 4) / (32 - data.dateArray[2])
                        if data.dateArray[3] < (int(data.sunJson['csth'])):
                            moodChance[2] = (((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4] / 4) / (32 - data.dateArray[2])
                        
                        moodChance[3] = ((data.dateArray[3] - (int(data.sunJson['aeth']))) * data.dateArray[4] / 5) / (32 - data.dateArray[2])
                        if data.dateArray[3] < (int(data.sunJson['csth'])):
                            moodChance[3] = (((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4] / 5) / (32 - data.dateArray[2])
                        
                        moodChance[4] = ((data.dateArray[3] - (int(data.sunJson['aeth']) + 1)) * data.dateArray[4]) / ((32 - data.dateArray[2]) / 2)
                        if data.dateArray[3] < (int(data.sunJson['csth'])):
                            moodChance[4] = (((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4]) / ((32 - data.dateArray[2]) / 2)
                        
                        moodChance[5] = ((data.dateArray[3] - (int(data.sunJson['aeth']) + 2)) * data.dateArray[4]) / ((32 - data.dateArray[2]) / 4)
                        if data.dateArray[3] < (int(data.sunJson['csth'])):
                            moodChance[5] = (((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4]) / ((32 - data.dateArray[2]) / 4)
                            
                        moodChanceModif = (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 150)
                        if moodChanceModif > 0.95:
                            moodChanceModif = 0.95
                        
                        i = 0
                        while i < len(moodChance):
                            moodChance[i] = moodChance[i] * moodChanceModif
                            i = i + 1
                        
                        if random.randrange(0, 25000) < moodChance[0]:
                            audio.playSoundAll('h_general_mood.mp3', hGeneralVol, 1, 0, 0)
                        if random.randrange(0, 25000) < moodChance[1]:
                            audio.playSoundAll('h_general_dark.mp3', hGeneralVol, 1, 0, 0)
                        if random.randrange(0, 25000) < moodChance[2]:
                            audio.playSoundAll('h_general_evil.mp3', hGeneralVol, 1, 0, 0)
                        if random.randrange(0, 25000) < moodChance[3]:
                            audio.playSoundAll('h_general_sinister.mp3', hGeneralVol, 1, 0, 0)
                        if random.randrange(0, 25000) < moodChance[4]:
                            audio.playSoundAll('h_general_dying.mp3', hGeneralVol, 1, 0, 0)
                        if random.randrange(0, 25000) < moodChance[5]:
                            audio.playSoundAll('h_general_death.mp3', hGeneralVol * (1 + (random.random() / 5)), 1, 0, 0)
                    sections.moodChance = moodChance
                except:
                    pass
                time.sleep(0.1)
            wait = True
            for n in sections.moodChance:
                if n > 0:
                    wait = False
            if wait:
                time.sleep(1)

    uncannyMoodChance = [0, 0, 0, 0, 0, 0]

    def runUncannyMood():
        prevMin = -1
        while not status.exit:
            if globals.runUncanny:
                try:
                    if (os.path.isfile('deathmode.derp') and (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) > 0)):
                        if prevMin != data.dateArray[4]:
                            monthS = pytools.clock.dateArrayToUTC([data.dateArray[0], data.dateArray[1], 1, 0, 0, 0])
                            monthE = pytools.clock.dateArrayToUTC([data.dateArray[0], data.dateArray[1] + 1, 1, 0, 0, 0])
                            monthC = pytools.clock.dateArrayToUTC(data.dateArray) - monthS
                            
                            hGeneralVol = (42 * (0.5 + (monthC / (monthE - monthS))))
                            if hGeneralVol > 35:
                                hGeneralVol = 35
                            hGeneralVol = hGeneralVol * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)
                            hGeneralSpeedModifier = 0.08
                            midnight = pytools.clock.dateArrayToUTC(pytools.clock.getMidnight(data.dateArray))
                            sunset = pytools.clock.dateArrayToUTC(data.dayTimes[5])
                            civil = pytools.clock.dateArrayToUTC(data.dayTimes[2])
                            sunrise = pytools.clock.dateArrayToUTC(data.dayTimes[3])
                            current = pytools.clock.dateArrayToUTC(data.dateArray)
                            try:
                                if current > sunset:
                                    hGeneralSpeedModifier = 0.08 * (((midnight - sunset) - (midnight - current)) / (midnight - sunset))
                                elif (midnight - current) > 82800:
                                    hGeneralSpeedModifier = 0.08 * (1 - ((midnight - current - 83160) / 3600))
                                elif current < civil:
                                    hGeneralSpeedModifier = 0.1
                                elif current < sunrise:
                                    hGeneralSpeedModifier =  0.1 * (((sunrise - civil) / ((sunrise - civil + 1) - (sunrise - current))) - 1)
                                else:
                                    hGeneralSpeedModifier = 0
                            except:
                                pass
                            if hGeneralSpeedModifier > 0.4:
                                hGeneralSpeedModifier = 0.4
                            elif hGeneralSpeedModifier < 0:
                                hGeneralSpeedModifier = 0
                            hGeneralSpeedModifier = (hGeneralSpeedModifier * (monthC / (monthE - monthS))) * (1.05 - (1 + ((((-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True)) / 100)) ** 0.1) - 1))
                            
                            if type(hGeneralSpeedModifier) == complex:
                                hGeneralSpeedModifier = hGeneralSpeedModifier.real
                            
                            # if data.dateArray[1] != 11:
                            print("Looping hu_general effect at volume " + str(hGeneralVol) + ", and speed " + str(1 - hGeneralSpeedModifier) + ".")
                            audio.playSoundAll('hu_general.mp3', hGeneralVol, 1 - hGeneralSpeedModifier, 0, 0)
                            # else:
                                # audio.playSoundAll('hu_general.mp3', hGeneralVol * (1 - (((data.dateArray[3] * 60 * 60) + (data.dateArray[4] * 60) + (data.dateArray[5])) / ((data.sunJson["csth"] * 60 * 60) + (data.sunJson["cstm"] * 60)))), 1 - hGeneralSpeedModifier, 0, 0)
                            prevMin = data.dateArray[4]
                        
                        uncannyMoodChance = [0, 0, 0, 0, 0, 0]
                        
                        uncannyMoodChance[0] = (data.dateArray[3] - (int(data.sunJson['cesth']))) * data.dateArray[4]
                        if data.dateArray[3] < (int(data.sunJson['csth'])):
                            uncannyMoodChance[0] = ((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4]
                        
                        uncannyMoodChance[1] = ((data.dateArray[3] - (int(data.sunJson['ceth']))) * data.dateArray[4] / 3) / (32 - data.dateArray[2])
                        if data.dateArray[3] < (int(data.sunJson['csth'])):
                            uncannyMoodChance[1] = (((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4] / 3) / (32 - data.dateArray[2])
                        
                        uncannyMoodChance[2] = ((data.dateArray[3] - (int(data.sunJson['neth']))) * data.dateArray[4] / 4) / (32 - data.dateArray[2])
                        if data.dateArray[3] < (int(data.sunJson['csth'])):
                            uncannyMoodChance[2] = (((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4] / 4) / (32 - data.dateArray[2])
                        
                        uncannyMoodChance[3] = ((data.dateArray[3] - (int(data.sunJson['aeth']))) * data.dateArray[4] / 5) / (32 - data.dateArray[2])
                        if data.dateArray[3] < (int(data.sunJson['csth'])):
                            uncannyMoodChance[3] = (((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4] / 5) / (32 - data.dateArray[2])
                        
                        uncannyMoodChance[4] = ((data.dateArray[3] - (int(data.sunJson['aeth']) + 1)) * data.dateArray[4]) / ((32 - data.dateArray[2]) / 2)
                        if data.dateArray[3] < (int(data.sunJson['csth'])):
                            uncannyMoodChance[4] = (((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4]) / ((32 - data.dateArray[2]) / 2)
                        
                        uncannyMoodChance[5] = ((data.dateArray[3] - (int(data.sunJson['aeth']) + 2)) * data.dateArray[4]) / ((32 - data.dateArray[2]) / 4)
                        if data.dateArray[3] < (int(data.sunJson['csth'])):
                            uncannyMoodChance[5] = (((int(data.sunJson['csth'])) - data.dateArray[3]) * data.dateArray[4]) / ((32 - data.dateArray[2]) / 4)
                            
                        uncannyMoodChanceModif = (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 150)
                        if uncannyMoodChanceModif > 0.95:
                            uncannyMoodChanceModif = 0.95
                        
                        i = 0
                        while i < len(uncannyMoodChance):
                            uncannyMoodChance[i] = uncannyMoodChance[i] * uncannyMoodChanceModif
                            i = i + 1
                        
                        if random.randrange(0, 25000) < uncannyMoodChance[0]:
                            audio.playSoundAll('hu_general_mood.mp3', hGeneralVol, 1, 0, 0)
                        if random.randrange(0, 25000) < uncannyMoodChance[1]:
                            audio.playSoundAll('hu_general_dark.mp3', hGeneralVol, 1, 0, 0)
                        if random.randrange(0, 25000) < uncannyMoodChance[2]:
                            audio.playSoundAll('hu_general_evil.mp3', hGeneralVol, 1, 0, 0)
                        if random.randrange(0, 25000) < uncannyMoodChance[3]:
                            audio.playSoundAll('hu_general_sinister.mp3', hGeneralVol, 1, 0, 0)
                        if random.randrange(0, 25000) < uncannyMoodChance[4]:
                            audio.playSoundAll('hu_general_dying.mp3', hGeneralVol, 1, 0, 0)
                        if random.randrange(0, 25000) < uncannyMoodChance[5]:
                            audio.playSoundAll('hu_general_death.mp3', hGeneralVol * (1 + (random.random() / 5)), 1, 0, 0)
                    sections.uncannyMoodChance = uncannyMoodChance
                except:
                    pass
                time.sleep(0.1)
            wait = True
            for n in sections.uncannyMoodChance:
                if n > 0:
                    wait = False
            if wait:
                time.sleep(1)
        
        
    knockChance = 0
        
    def runKnocks():
        while not status.exit:
            if globals.run:
                try:
                    knockChance = 0
                    if data.dateArray[3] < 24:
                        knockChance = (data.dateArray[3] - (int(data.sunJson['cesth']))) * data.dateArray[4] * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)
                    knockChance = (knockChance / (32 - data.dateArray[2])) * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)
                    if random.randrange(0, 15000) < knockChance:
                        ghSpeaker = 5
                        while ghSpeaker == 5:
                            ghSpeaker = random.randrange(0, 10)
                        audioEvent = audio.event()
                        speed = 0.96 + (random.random() / 12.5)
                        audioEvent.register('h_knock_' + str(random.randrange(0, 6)) + ".mp3", ghSpeaker, 60 * ((0.3 * random.random()) + 0.7), speed, 0, 0)
                        audioEvent.run()
                    sections.knockChance = knockChance
                except:
                    pass
                time.sleep(0.1)
            if sections.knockChance <= 0:
                time.sleep(1)
        
    chainChance = 0
    
    def runChains():
        while not status.exit:
            if globals.run:
                try:
                    chainChance = 0
                    if data.dateArray[3] < 24:
                        chainChance = (data.dateArray[3] - (int(data.sunJson['cesth']) + 2)) * data.dateArray[4] * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)
                    chainChance = (chainChance / (32 - data.dateArray[2])) * (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100)
                    if random.randrange(0, 15000) < chainChance:
                        ghSpeaker = 5
                        while ghSpeaker == 5:
                            ghSpeaker = random.randrange(0, 10)
                        audioEvent = audio.event()
                        speed = 0.96 + (random.random() / 12.5)
                        audioEvent.register('h_chains_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, 40 * ((0.2 * random.random()) + 0.8), speed, 0, 0)
                        audioEvent.run()
                    sections.chainChance = chainChance
                except:
                    pass
                time.sleep(0.1)
            if sections.chainChance <= 0:
                time.sleep(1)

def main():
    mainVars.noA = 0
    mainVars.noB = 0
    mainVars.noC = 0
    mainVars.noD = 0
    pHorr = False
    noE = 0
    noF = 0
    noG = 0
    
    calcGrabber = threading.Thread(target=data.grabSunData)
    ghostsRunner = threading.Thread(target=sections.testGhosts)
    uncannyGhostsRunner = threading.Thread(target=sections.testGhostsUncanny)
    closeToMidTester = threading.Thread(target=sections.closeMidTestRun)
    draftsRunner = threading.Thread(target=sections.runDrafts)
    uncannyDraftsRunner = threading.Thread(target=sections.runUncannyDrafts)
    breathsRunner = threading.Thread(target=sections.runBreaths)
    uncannyBreathsRunner = threading.Thread(target=sections.runUncannyBreaths)
    moodRunner = threading.Thread(target=sections.runMood)
    uncannyMoodRunner = threading.Thread(target=sections.runUncannyMood)
    knocksRunner = threading.Thread(target=sections.runKnocks)
    chainsRunner = threading.Thread(target=sections.runChains)
    
    calcGrabber.start()
    ghostsRunner.start()
    uncannyGhostsRunner.start()
    closeToMidTester.start()
    draftsRunner.start()
    uncannyDraftsRunner.start()
    breathsRunner.start()
    uncannyBreathsRunner.start()
    moodRunner.start()
    uncannyMoodRunner.start()
    knocksRunner.start()
    chainsRunner.start()

    while not status.exit:
        data.dateArray = pytools.clock.getDateTime()
        
        globals.run = (data.dateArray[1] == 10) or ((data.dateArray[1] == 11) and (data.dateArray[2] == 1) and (data.dateArray[3] < data.sunJson["csth"])) or ((data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100) > 0) or ((data.dateArray[1] == 9) and (data.dateArray[2] == 30) and (data.dateArray[3] > 11))
        
        if globals.run and (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) < 0):
            globals.run = False
            globals.runUncanny = True
        else:
            globals.runUncanny = False
            
        print(globals.run)
        
        if globals.run:
            
            data.getZ()
            
            if data.dateArray[2] > 19:
                if data.dateArray[4] == 35:
                    if noE != 1:
                        if random.random() < (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100):
                            if random.randrange(data.dateArray[3], 24) == 23:
                                rumbleNum = random.randrange(0, 2)
                                audio.playSoundAll('h_rumble_' + str(rumbleNum) + '.mp3', 40, 1, 0, 0)
                            noE = 1
                else:
                    noE = 0
            else:
                noE = 0
            
            if data.dateArray[2] > 24:
                if data.dateArray[4] == 20:
                    if noF != 1:
                        if random.random() < (data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100):
                            if random.randrange(data.dateArray[3], 24) == 23:
                                rumbleNum = random.randrange(0, 2)
                                audio.playSoundAll('h_rumble_' + str(rumbleNum) + '.mp3', 40, 1, 0, 0)
                        noF = 1
                elif data.dateArray[4] == 40:
                    if noF != 1:
                        if random.randrange(data.dateArray[3], 24) == 23:
                            rumbleNum = random.randrange(0, 2)
                            audio.playSoundAll('h_rumble_' + str(rumbleNum) + '.mp3', 40, 1, 0, 0)
                        noF = 1
                else:
                    noF = 0
            else:
                noF = 0
            
            if data.dateArray[3] == int(data.sunJson['cesth']):
                if data.dateArray[4] == int(data.sunJson['cestm']):
                    if noG != 1:
                        if (random.randint(data.dateArray[2], 31) == 31) or ((random.random() * 180) < data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True)):
                            audio.playSoundWindow('h_sunset.mp3;h_sunset.mp3', [40, 80], 1, 0, 0)
                        noG = 1
                else:
                    noG = 0
            else:
                noG = 0
        
        if globals.runUncanny:     
            if data.dateArray[2] > 19:
                if data.dateArray[4] == 35:
                    if noE != 1:
                        if random.random() < (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100):
                            if random.randrange(data.dateArray[3], 24) == 23:
                                rumbleNum = random.randrange(0, 2)
                                audio.playSoundAll('hu_rumble_' + str(rumbleNum) + '.mp3', 40, 1, 0, 0)
                            noE = 1
                else:
                    noE = 0
            else:
                noE = 0
            
            if data.dateArray[2] > 24:
                if data.dateArray[4] == 20:
                    if noF != 1:
                        if random.random() < (-data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True) / 100):
                            if random.randrange(data.dateArray[3], 24) == 23:
                                rumbleNum = random.randrange(0, 2)
                                audio.playSoundAll('hu_rumble_' + str(rumbleNum) + '.mp3', 40, 1, 0, 0)
                        noF = 1
                elif data.dateArray[4] == 40:
                    if noF != 1:
                        if random.randrange(data.dateArray[3], 24) == 23:
                            rumbleNum = random.randrange(0, 2)
                            audio.playSoundAll('hu_rumble_' + str(rumbleNum) + '.mp3', 40, 1, 0, 0)
                        noF = 1
                else:
                    noF = 0
            else:
                noF = 0
            
            if data.dateArray[3] == int(data.sunJson['cesth']):
                if data.dateArray[4] == int(data.sunJson['cestm']):
                    if noG != 1:
                        if (random.randint(data.dateArray[2], 31) == 31) or ((random.random() * 180) < -data.getHallowIndex(pytools.clock.dateArrayToUTC(data.dateArray), noDay=True)):
                            audio.playSoundWindow('hu_sunset.mp3;hu_sunset.mp3', [40, 80], 1, 0, 0)
                        noG = 1
                else:
                    noG = 0
            else:
                noG = 0
        
        if globals.run or globals.runUncanny:  
            if sections.breathChance < 0:
                sections.breathChance = 0
            horrorIndex = sections.ghostsChance[0] + sections.ghostsChance[1] + sections.ghostsChance[2] + sections.draftChance + sections.breathChance + sections.moodChance[0] + sections.moodChance[1] + sections.moodChance[2] + sections.moodChance[3] + sections.moodChance[4] + sections.moodChance[5] + sections.knockChance + sections.chainChance
                
            time.sleep(1)
            
            status.vars["horrorStats"]["sections.ghostsChance-0"] = sections.ghostsChance[0]
            status.vars["horrorStats"]["sections.ghostsChance-1"] = sections.ghostsChance[1]
            status.vars["horrorStats"]["sections.ghostsChance-2"] = sections.ghostsChance[2]
            status.vars["horrorStats"]["sections.uncannyGhostsChance-0"] = sections.uncannyGhostsChance[0]
            status.vars["horrorStats"]["sections.uncannyGhostsChance-1"] = sections.uncannyGhostsChance[1]
            status.vars["horrorStats"]["sections.uncannyGhostsChance-2"] = sections.uncannyGhostsChance[2]
            status.vars["horrorStats"]["sections.draftChance"] = sections.draftChance
            status.vars["horrorStats"]["sections.uncannyDraftChance"] = sections.uncannyDraftChance
            status.vars["horrorStats"]["sections.breathChance"] = sections.breathChance
            status.vars["horrorStats"]["sections.uncannyBreathChance"] = sections.uncannyBreathChance
            status.vars["horrorStats"]["sections.moodChance"] = sections.moodChance
            status.vars["horrorStats"]["sections.uncannyMoodChance"] = sections.uncannyMoodChance
            status.vars["horrorStats"]["sections.knockChance"] = sections.knockChance
            status.vars["horrorStats"]["sections.chainChance"] = sections.chainChance
            
            if (data.dateArray[5] % 2) == 0:
                if pHorr == False:
                    print("Current Horror Index: " + str(horrorIndex))
                    status.vars['horrorIndex'] = horrorIndex
                    saveFile('horrorindex.cx', str(horrorIndex))
                    pHorr = True
            else:
                pHorr = False
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
                        
            
            
            
            
                        
                    
                        
            
                    
                    
                
            
            
                    
