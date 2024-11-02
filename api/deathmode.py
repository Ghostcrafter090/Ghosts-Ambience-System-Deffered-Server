import modules.audio as audio
import modules.pytools as pytools
import random
import time
import os
import math
import modules.logManager as log
import api.halloween_extension as hallow
import threading

print = log.printLog

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": [],
        "whisperIndex": 0,
        "hallowedWolfIndex": 0,
        "ghosts": {},
        "monsters": {},
        "death_wind": {}
    }

class globals:
    class deathWind:
       state = 0
       run = 0
       nextPlay = 0
    class monsters:
        state = 0
        run = 0
        nextPlay = 0
    class ghosts:
        state = 0
        run = 0
        nextPlay = 0
    whispers = 0
    whisperSub = 0

class utils:
    def dayTimesGrabber():
        dayTimes = pytools.IO.getList('daytimes.pyl')[1]
        if dayTimes == 1:
            dayTimes = [[2022, 5, 11, 3, 45, 15], [2022, 5, 11, 4, 34, 10], [2022, 5, 11, 5, 16, 33], [2022, 5, 11, 5, 48, 29], [2022, 5, 11, 13, 10, 47], [2022, 5, 11, 20, 33, 6], [2022, 5, 11, 21, 5, 2], [2022, 5, 11, 21, 47, 25], [2022, 5, 11, 22, 36, 20]]
        return dayTimes
    
    def getHallowIndex(timeStamp, noDay=False):
        # u = math.floor(timeStamp / (365 * 24 * 60 * 60))
        
        fourYearFloat = timeStamp / (1461 * 24 * 60 * 60)
        
        dayOfFourYears = pytools.clock.getDayOfFourYear(pytools.clock.UTCToDateArray(timeStamp))
        
        dayOfYear = pytools.clock.getDayOfYear(pytools.clock.UTCToDateArray(timeStamp))
        
        u = pytools.clock.UTCToDateArray(timeStamp)[0]
        
        print(u)
        
        # w = (timeStamp - (24 * 60 * 60) - (u * (365 * 24 * 60 * 60)) - 1)
        
        w = ((timeStamp) - (24 * 60 * 60) - (pytools.clock.dateArrayToUTC([u, 1, 1, 0, 0, 0])) - 1) + 86400
        
        print(w)
        print(dayOfYear)
        
        # q = math.floor(math.floor(((u) / (4))) - (((u) / (4))) + 1) * 24 * 60 * 60
        q = 0
        a = 100
        b = 26265600 + q
        c = 3000000000000
        f = 30931200 + q
        g = 300000000000
        p = 3.14159265359
        h = 50
        e = 2.71828182846
        # j = 16 * math.sin((((p) / (1180295.8))) * ( - (w - (((1180295.8) / (2)))) - (u * (365.25 * 24 * 60 * 60))))
        j = 16 * ( - hallow.data.getLunarPhase(pytools.clock.UTCToDateArray(timeStamp)))
        l_2 = 15 * e ** ( - (3 * ((w - 1080000) ** (2)) / (g)))
        l_3 = 15 * e ** ( - (3 * ((w - 3758400) ** (2)) / (g)))
        l_4 = 15 * e ** ( - (3 * (((w - q) - 6177600) ** (2)) / (g)))
        l_5 = 15 * e ** ( - (3 * (((w - q) - 8856000) ** (2)) / (g)))
        l_6 = 15 * e ** ( - (3 * (((w - q) - 11448000) ** (2)) / (g)))
        l_7 = 15 * e ** ( - (3 * (((w - q) - 14126400) ** (2)) / (g)))
        l_8 = 15 * e ** ( - (3 * (((w - q) - 16718400) ** (2)) / (g)))
        l_9 = 15 * e ** ( - (3 * (((w - q) - 19396800) ** (2)) / (g)))
        l_10 = 18 * e ** ( - (1 * (((w - q) - 22075200) ** (2)) / (g)))
        l_11 = 15 * e ** ( - (3 * (((w - q) - 24667200) ** (2)) / (g)))
        l_12 = 15 * e ** ( - (3 * (((w - q) - 27345600) ** (2)) / (g)))
        l_13 = 15 * e ** ( - (3 * (((w - q) - 29937600) ** (2)) / (g)))
        r = 29376000 + q
        s = 27302400 + q
        t = - 2 * ((a * e ** ( - (((w - r) ** (2)) / (c)))) + (h * e ** ( - (((w - r) ** (2)) / (g)))))
        z = - 2 * ((a * e ** ( - (((((w - s) ** (2)) / (c))) / (0.15)))) + (h * e ** ( - (((((w - s) ** (2)) / (g))) / (0.15)))))
        # k = 18 * math.sin((((p) / (302400.0))) * ((w + 36 * 60 * 60) + (u * 365.25 * 24 * 60 * 60) - 6))
        k = 20 * math.sin((((p) / (302400.0))) * ((w + 36 * 60 * 60) + pytools.clock.dateArrayToUTC([u, 1, 1, 0, 0, 0]) - 172800))
        z_1 = 16 * math.sin((((p) / (1180295.8))) * ( - (24778000.0 - (((1180295.8) / (2)))) - (u * (356.25 * 24 * 60 * 60)))) + (7 * math.sin((((p) / (302400.0))) * ((24778000.0 + 12 * 60 * 60) + (u * 365.25 * 24 * 60 * 60) - 6))) + 13
        o = - 3 * ((a * e ** ( - (((w - f) ** (2)) / (c)))) + (h * e ** ( - (((w - f) ** (2)) / (g)))))
        m = (1.11 * (((((math.fabs(z_1 )) / (2)) + 15) / (15)) ** (1) * (a * e ** ( - 0.65 * (((w - b) ** (2)) / (c))))) + (h * e ** ( - 0.65 * (((w - b) ** (2)) / (g))))) + j + k + (2 * (l_2 + l_3 + l_4 + l_5 + l_6 + l_7 + l_8 + l_9 + l_10 + l_11 + l_12 + l_13)) + o + t + z - 40
        weatherModif = hallow.data.getWeatherHallowModifier()
        if weatherModif:
            m = m + weatherModif
        n = - 10 * math.sin(((p) / (12 * 60 * 60)) * (w - 6 * 60 * 60))
        z_2 = ((1) / (2)) * (n * (((m) / (10))) + m)
        if noDay:
            return m
        else:
            return z_2

class background:

    class whispers:
        # https://www.desmos.com/calculator/b2jdnzqx67
        def calc(dateArray, dayTimes):
            try:
                timef = dateArray
                timef[2] = dateArray[2] - 1
                start = pytools.clock.dateArrayToUTC(pytools.clock.getMidnight(timef))
                midnight = pytools.clock.dateArrayToUTC(pytools.clock.getMidnight(dateArray))
                current = pytools.clock.dateArrayToUTC(dateArray)
                x = 86400 + (current - start)
                g = 86400 - (86400 - (pytools.clock.dateArrayToUTC(dayTimes[5]) - midnight))
                while g > 86400:
                    g = g - 86400
                while x > 86400:
                    x = x - 86400
                
                e = 2.71828182846
                a = 10
                f = 0.000000004
                k = 120
                r = 0.0008
                j = 0.000000002
                n = a * (e ** (-f * ((x - 86000) ** 2)))
                l = k * (e ** ((-3) * r * ((x - g - 100) ** 1.12)))
                try:
                    pass
                    #l = math.fabs(float(l))
                except:
                    pass
                    #l = math.fabs(float(l.real))
                l = (2.5 * k) * (1 / ((2 * 3.14) ** 0.5) * (e ** (-1 * (((x - g - 100) ** 2) / (20 * k)))))
                s = 5 * (e ** (-j * ((x - g - 5400) ** 2)))
                m = 0.5 * a * (e ** (-2 * f * ((x - 86000 - 3600) ** 2)))
                d = 6 * a * (e ** (-150 * f * ((x - 86400) ** 2)))
                o = -1024 ** (x - 86400)
                h = 6 * a * (e ** (-15000 * f * ((x - 86400) ** 2)))
                if dateArray[1] == 10:
                    l = l / ((31 / dateArray[2]) ** 7)
                    d = d / ((31 / dateArray[2]) ** 16)
                    h = h / ((31 / dateArray[2]) ** 92)
                else:
                    l = l / 3
                    d = d / ((31 / 25) ** 16)
                    h = h / ((31 / 25) ** 92)
                out = n + l + s + m + d + o + h
                if out < 0:
                    out = 0
            except:
                out = 0
                
            print('Current whisper chance: ' + str(out))
            status.vars['whisperIndex'] = out
            return out

        def run(dateArray, dayTimes):
            whisperChance = background.whispers.calc(dateArray, dayTimes)
            # if whisperChance < 100:
                # whisperChance = ((whisperChance * (utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray) / 10)) + utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray)))) / ((utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray)) / 10) + 1)
            if random.randint(0, 100) < whisperChance:
                min = int(math.floor(25 + (whisperChance / 4)))
                max = int(math.floor(60 + (whisperChance / 2.5)))
                if min < 0:
                    min = 0
                if min > 100:
                    min = 100
                if max < 0:
                    max = 0
                if max > 100:
                    max = 100
                    
                def getTicType():
                    if pytools.clock.getDateTime()[3] < 22:
                        return 2
                    return 15
                if globals.whisperSub < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                    globals.whisperSub = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + getTicType()
                    globals.whispers = globals.whispers - 1
                if globals.whispers < 0:
                    globals.whispers = 0
                globals.whispers = 0
                if globals.whispers < 10:
                    globals.whispers = globals.whispers + 1
                    audioEvent = audio.event()
                    i = 0
                    while i < (int((random.random() * whisperChance / 20)) + 1):
                        ghSpeaker = 5
                        while ghSpeaker == 5:
                            ghSpeaker = random.randint(0, 10)
                        audioEvent.register("whispering.mp3", ghSpeaker, random.randint(min, max), (random.random() / 3) + 0.6 + 0.15, 0, 0, keepLoaded=True)
                        i = i + 1
                    threading.Thread(target=audioEvent.run).start()
                
    def death_wind(dateArray, dayTimes):
        startf = dayTimes[5]
        startf[4] = startf[4] + 11
        if startf[4] > 60:
            startf[4] = startf[4] - 60
            startf[3] = startf[3] + 1
        endf = dayTimes[2]
        endf[4] = endf[4] - 11
        if endf[4] < 0:
            endf[4] = endf[4] + 60
            endf[3] = endf[3] - 1
        if dateArray[3] > 12:
            endf[2] = endf[2] + 1
            if endf[2] > pytools.clock.getMonthEnd(endf[1]):
                endf[1] = endf[1] + 1
                if endf[1] > 12:
                    endf[1] = 1
                    endf[0] = endf[0] + 1
        else:
            startf[2] = startf[2] - 1
            if startf[2] < 1:
                startf[1] = startf[1] - 1
                if startf[1] < 1:
                    startf[1] = 12
                    startf[0] = startf[0] - 1
        start = pytools.clock.dateArrayToUTC(startf)
        current = pytools.clock.dateArrayToUTC(dateArray)
        end = pytools.clock.dateArrayToUTC(endf)
        print(dateArray)
        print([startf, dateArray, endf])
        print([start, current, end])
        if (start < current) and (current < end):
            globals.deathWind.run = 1
            if globals.deathWind.state != 1:
                globals.deathWind.state = 1
                globals.deathWind.nextPlay = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + 500
                audio.playSoundWindow("death_wind_fi.mp3;death_wind_fi.mp3", [10, 40, 20], 1.0, 0.0, 0)
            if globals.deathWind.state == 1:
                if globals.deathWind.nextPlay < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                    globals.deathWind.nextPlay = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + 194
                    audio.playSoundWindow("death_wind.mp3;death_wind.mp3", [10, 40, 20], 1.0, 0.0, 0)
        status.vars["death_wind"]["nextPlay"] = globals.deathWind.nextPlay
        status.vars["death_wind"]["state"] = globals.deathWind.state

    def monsters(dateArray, dayTimes):
        dayTimes = utils.dayTimesGrabber()
        startf = dayTimes[5]
        startf[4] = startf[4] + 26
        if startf[4] > 60:
            startf[4] = startf[4] - 60
            startf[3] = startf[3] + 1
        endf = dayTimes[2]
        endf[4] = endf[4] - 26
        if endf[4] < 0:
            endf[4] = endf[4] + 60
            endf[3] = endf[3] - 1
        if dateArray[3] > 12:
            endf[2] = endf[2] + 1
            if endf[2] > pytools.clock.getMonthEnd(endf[1]):
                endf[1] = endf[1] + 1
                if endf[1] > 12:
                    endf[1] = 1
                    endf[0] = endf[0] + 1
        else:
            startf[2] = startf[2] - 1
            if startf[2] < 1:
                startf[1] = startf[1] - 1
                if startf[1] < 1:
                    startf[1] = 12
                    startf[0] = startf[0] - 1
        start = pytools.clock.dateArrayToUTC(startf)
        current = pytools.clock.dateArrayToUTC(dateArray)
        end = pytools.clock.dateArrayToUTC(endf)
        print("Monsters: " + str(start) + " ;;; " + str(current))
        midnight = pytools.clock.dateArrayToUTC(pytools.clock.getMidnight(dateArray))
        dis = midnight - start
        dayMod = ((((current - midnight) + 86400) / ((start - midnight) + 86400)) ** 16)
        if dayMod > 1:
            dayMod = 1
        wolfChance = ((20 * (2.71828182846 ** -(((((current - midnight) * 0.00016) * (dis / 10854)) ** 2)))) / 2) * dayMod
        if dateArray[1] == 10:
            wolfChance = wolfChance / ((31 / dateArray[2]) ** 4)
        if random.randrange(0, 100) < wolfChance:
            howlNumber = str(random.randrange(0, 3))
            audio.playSoundWindow('wolf_howl_' + howlNumber + '_m.mp3;wolf_howl_' + howlNumber + ".mp3", [40, 40, 25], 1, 0, 0)
        status.vars['hallowedWolfIndex'] = wolfChance
        if (start < current) and (current < end):
            globals.monsters.run = 1
            if globals.monsters.state == 0:
                globals.monsters.state = 1
                globals.monsters.nextPlay = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + 500
                audio.playSoundWindow("monsters_fi.mp3;monsters_fi.mp3", [20, 30, 25], 1.0, 0.0, 0)
            if globals.monsters.state == 1:
                if globals.monsters.nextPlay < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                    globals.monsters.nextPlay = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + 194
                    audio.playSoundWindow("monsters.mp3;monsters.mp3", [20, 30, 25], 1.0, 0.0, 0)
        status.vars["monsters"]["nextPlay"] = globals.monsters.nextPlay
        status.vars["monsters"]["state"] = globals.monsters.state
    
    def ghosts(dateArray, dayTimes):
        startf = dayTimes[6]
        current = pytools.clock.dateArrayToUTC(dateArray)
        endf = dayTimes[1]
        if dateArray[3] > 12:
            endf[2] = endf[2] + 1
            if endf[2] > pytools.clock.getMonthEnd(endf[1]):
                endf[1] = endf[1] + 1
                if endf[1] > 12:
                    endf[1] = 1
                    endf[0] = endf[0] + 1
        else:
            startf[2] = startf[2] - 1
            if startf[2] < 1:
                startf[1] = startf[1] - 1
                if startf[1] < 1:
                    startf[1] = 12
                    startf[0] = startf[0] - 1
        end = pytools.clock.dateArrayToUTC(endf)
        start = pytools.clock.dateArrayToUTC(dayTimes[6])
        if (start < current) and (current < end):
            globals.ghosts.run = 1
            if globals.ghosts.state == 0:
                globals.ghosts.state = 1
                globals.ghosts.nextPlay = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + 500
                audio.playSoundWindow("ghosts_fi.mp3;ghosts_fi.mp3", [20, 40, 35], 1.0, 0.0, 0)
            if globals.ghosts.state == 1:
                if globals.ghosts.nextPlay < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                    globals.ghosts.nextPlay = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + 194
                    audio.playSoundWindow("ghosts.mp3;ghosts.mp3", [20, 40, 35], 1.0, 0.0, 0)
        status.vars["ghosts"]["nextPlay"] = globals.ghosts.nextPlay
        status.vars["ghosts"]["state"] = globals.ghosts.state
    
    def end():
        if globals.ghosts.run == 0:
            if globals.ghosts.nextPlay < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                if globals.ghosts.state == 1:
                    globals.ghosts.state = 0
                    audio.playSoundWindow("ghosts_fo.mp3;ghosts_fo.mp3", [10, 50, 35], 1.0, 0.0, 0)
        if globals.monsters.run == 0:
            if globals.monsters.nextPlay < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                if globals.monsters.state == 1:
                    globals.monsters.state = 0
                    audio.playSoundWindow("monsters_fo.mp3;monsters_fo.mp3", [10, 30, 25], 1.0, 0.0, 0)
        if globals.deathWind.run == 0:
            if globals.deathWind.nextPlay < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                if globals.deathWind.state == 1:
                        globals.deathWind.state = 0
                        audio.playSoundWindow("death_wind_fo.mp3;death_wind_fo.mp3", [10, 40, 20], 1.0, 0.0, 0)
def main():
    while not status.exit:
        dateArray = pytools.clock.getDateTime()
        dayTimes = utils.dayTimesGrabber()
        dayOfWeek = pytools.clock.getDayOfWeek()
        globals.deathWind.run = 0
        globals.monsters.run = 0
        globals.ghosts.run = 0
        wait = 600
        
        if dateArray[1] < 12:
            if dateArray[2] == 13:
                if dayOfWeek == 5:
                    if dateArray[3] > 11:
                        background.whispers.run(dateArray, dayTimes)
                        wait = 1
                        dateArray = pytools.clock.getDateTime()
                        if (utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray), noDay=True) >= 8):
                            background.death_wind(dateArray, dayTimes)
                        if (9 <= dateArray[1] <= 11) or (utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray), noDay=True) >= 18):
                            background.monsters(dateArray, dayTimes)
                            dateArray = pytools.clock.getDateTime()
                        elif (dateArray[3] > 22) or (utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray), noDay=True) >= 18):
                            background.monsters(dateArray, dayTimes)
                            dateArray = pytools.clock.getDateTime()
            elif dateArray[2] == 14:
                if dayOfWeek == 6:
                    if dateArray[3] < 12:
                        background.whispers.run(dateArray, dayTimes)
                        wait = 1
                        dateArray = pytools.clock.getDateTime()
                        if (utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray), noDay=True) >= 8):
                            background.death_wind(dateArray, dayTimes)
                        if (9 <= dateArray[1] <= 11) or (utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray), noDay=True) >= 18):
                            background.monsters(dateArray, dayTimes)
                            dateArray = pytools.clock.getDateTime()
        
        if ((dateArray[1] == 10) and (((dateArray[2] == 1) and (dateArray[3] > 12)) or (dateArray[2] > 1))) or ((dateArray[1] == 11) and (dateArray[2] == 1) and (dateArray[3] < 12)):
            background.whispers.run(dateArray, dayTimes)
            wait = 1
            dateArray = pytools.clock.getDateTime()
            dayDecimal = ((dateArray[3] * 60 * 60) + (dateArray[4] * 60) + dateArray[5]) / 86400
            if (dateArray[2] >= 29) or ((dateArray[1] == 11) and (dateArray[2] <= 1)) or ((utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray)) > (90 + (25 * (13 / (dateArray[2] + dayDecimal)))))):
                background.death_wind(dateArray, dayTimes)
                dateArray = pytools.clock.getDateTime()
            if (dateArray[2] >= 30) or ((dateArray[1] == 11) and (dateArray[2] <= 1)) or ((utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray)) > (90 + (40 * (19 / (dateArray[2] + dayDecimal)))))):
                background.monsters(dateArray, dayTimes)
                dateArray = pytools.clock.getDateTime()
            if (dateArray[2] == 31) or ((dateArray[1] == 11) and (dateArray[2] <= 1)) or (utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray)) > (90 + (55 * (24 / (dateArray[2] + dayDecimal))))):
                background.ghosts(dateArray, dayTimes)
                dateArray = pytools.clock.getDateTime()
        
        elif utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray)) > 0:
            background.whispers.run(dateArray, dayTimes)
            wait = 1
            dateArray = pytools.clock.getDateTime()
            dayDecimal = ((dateArray[3] * 60 * 60) + (dateArray[4] * 60) + dateArray[5]) / 86400
            if (utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray)) > (90 + (25 * (13 / (dateArray[2] + dayDecimal))))):
                background.death_wind(dateArray, dayTimes)
                dateArray = pytools.clock.getDateTime()
            if (utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray)) > (90 + (40 * (19 / (dateArray[2] + dayDecimal))))):
                background.monsters(dateArray, dayTimes)
                dateArray = pytools.clock.getDateTime()
            if (utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray)) > (90 + (55 * (24 / (dateArray[2] + dayDecimal))))):
                background.ghosts(dateArray, dayTimes)
                dateArray = pytools.clock.getDateTime()
        
        elif ((dateArray[1] == 9) and (dateArray[2] == 30) and (dateArray[3] > 11)):
            background.whispers.run(dateArray, dayTimes)
            wait = 1
            dateArray = pytools.clock.getDateTime()
            
        background.end()
        time.sleep(wait)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
            



