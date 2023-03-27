import modules.audio as audio
import modules.pytools as pytools
import os
import time
import math

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
    def dayTimesGrabber():
        dayTimes = pytools.IO.getList('daytimes.pyl')[1]
        if dayTimes == 1:
            dayTimes = [[2022, 5, 11, 3, 45, 15], [2022, 5, 11, 4, 34, 10], [2022, 5, 11, 5, 16, 33], [2022, 5, 11, 5, 48, 29], [2022, 5, 11, 13, 10, 47], [2022, 5, 11, 20, 33, 6], [2022, 5, 11, 21, 5, 2], [2022, 5, 11, 21, 47, 25], [2022, 5, 11, 22, 36, 20]]
        return dayTimes
    
    def getHallowIndex(timeStamp):
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
        n = - 10 * math.sin(((p) / (12 * 60 * 60)) * (w - 6 * 60 * 60))
        z_2 = ((1) / (2)) * (n * (((m) / (10))) + m)
        return z_2

def main():
    while not status.exit:
        dateArray = pytools.clock.getDateTime()
        dayTimes = utils.dayTimesGrabber()
        cestj = dayTimes[5][3] - 1
        halloweenMode = False
        if utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray)) > 0:
            if os.path.isfile("halloweenmode.derp") == False:
                pytools.IO.saveFile('halloweenmode.derp', "1")
        if (dateArray[1] == 10) or ((dateArray[1] == 11) and (dateArray[2] == 1) and (dateArray[3] < 12)):
            halloweenMode = True
            if os.path.isfile("deathmode.derp") == False:
                pytools.IO.saveFile('deathmode.derp', "1")
        elif dateArray[1] == 11:
            if dateArray[2] == 1:
                if dateArray[3] < 12:
                    halloweenMode = True
                    if os.path.isfile("deathmode.derp") == False:
                        pytools.IO.saveFile('deathmode.derp', "1")
        if halloweenMode or (utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray)) > 0):
            if dateArray[3] == dayTimes[5][3]:
                if dateArray[4] == dayTimes[5][4]:
                    audio.playSoundAll("darkrumble.mp3", ((100 / ((((((32 - dateArray[2]) * 24 * 60) + ((24 - dateArray[3]) * 60) + (60 - dateArray[4])) / (24 * 60)) / 6) + (1 - 0.17372685185185185))) + utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray))) / 2, 1.0, 0.0, 0)
                    time.sleep(60)
            if dateArray[3] == cestj:
                if dateArray[4] == dayTimes[5][4]:
                    audio.playSoundAll("darkrumble.mp3", ((100 / ((((((32 - dateArray[2]) * 24 * 60) + ((24 - dateArray[3]) * 60) + (60 - dateArray[4])) / (24 * 60)) / 6) + (1 - 0.17372685185185185))) + utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray))) / 2, 1.0, 0.0, 0)
                    time.sleep(60)
            if dateArray[3] == dayTimes[6][3]:
                if dateArray[4] == dayTimes[6][4]:
                    audio.playSoundAll("darkrumble.mp3", ((100 / ((((((32 - dateArray[2]) * 24 * 60) + ((24 - dateArray[3]) * 60) + (60 - dateArray[4])) / (24 * 60)) / 6) + (1 - 0.17372685185185185))) + utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray))) / 2, 1.0, 0.0, 0)
                    time.sleep(60)
            if dateArray[3] == dayTimes[7][3]:
                if dateArray[4] == dayTimes[7][4]:
                    audio.playSoundAll("darkrumble.mp3", ((100 / ((((((32 - dateArray[2]) * 24 * 60) + ((24 - dateArray[3]) * 60) + (60 - dateArray[4])) / (24 * 60)) / 6) + (1 - 0.17372685185185185))) + utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray))) / 2, 1.0, 0.0, 0)
                    time.sleep(60)
            if dateArray[3] == dayTimes[8][3]:
                if dateArray[4] == dayTimes[8][4]:
                    audio.playSoundAll("darkrumble.mp3", ((100 / ((((((32 - dateArray[2]) * 24 * 60) + ((24 - dateArray[3]) * 60) + (60 - dateArray[4])) / (24 * 60)) / 6) + (1 - 0.17372685185185185))) + utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray))) / 2, 1.0, 0.0, 0)
                    time.sleep(60)
            if dateArray[2] == 31:
                if dateArray[3] == 23:
                    if dateArray[4] == 45:
                        audio.playSoundAll("midnightonhalloween.mp3", 100, 1.0, 0.0, 0)
                        time.sleep(60)
            if dateArray[1] == 10:
                if dateArray[2] >= 25:
                    if dateArray[3] == 11:
                        if dateArray[4] == 11:
                            audio.playSoundWindow("draculasrevenge.mp3;draculasrevenge.mp3", [50, 100], 1.0, 0.0, 0)
                            time.sleep(60)
            if (dateArray[1] == 10) or ((dateArray[1] == 11) and (dateArray[2] == 1)):
                if dateArray[2] >= 20:
                    if dateArray[3] == 3:
                        if dateArray[4] == 11:
                            audio.playSoundWindow("comelittlechildren.mp3;comelittlechildren.mp3", [50, 100], 1.0, 0.0, 0)               
        else:
            time.sleep(55)
        if halloweenMode == False:
            os.system('del .\\deathmode.derp /f /s /q')
            
        if utils.getHallowIndex(pytools.clock.dateArrayToUTC(dateArray)) < 0:
            os.system('del .\\halloweenmode.derp /f /s /q')
        
        time.sleep(5)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True


