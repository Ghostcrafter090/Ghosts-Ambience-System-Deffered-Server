import modules.audio as audio
import modules.pytools as pytools
import time
import api.wind
import modules.logManager as log
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
        "peepersTempModifier": 0,
        "peepersHumidModifier": 0,
        "peepersRainModifier": 0,
        "peepersWindModifier": 0,
        "peepersIndex": 0,
        "peeperCount": 0
    }
    
def fireWindowEvent(*args):
    aThread = threading.Thread(target=audio.playSoundWindow, args=(*args,))
    aThread.start()
    time.sleep(1)
    
class globals:
    peeperInfo = pytools.IO.getJson("peepers.json")

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

def main():
    pn0 = 0
    pn1 = 0
    pn2 = 0
    pn3 = 0
    pn4 = 0
    
    if str(globals.peeperInfo) != "{":
        globals.peeperInfo = {
            "count": 0
        }
    
    while not status.exit:
        
        dateArray = pytools.clock.getDateTime()
        dataList = utils.dataGrabber()
        dayTimes = utils.dayTimesGrabber()
        
        if dataList[0][7] > 0:
            globals.peeperInfo["count"] = globals.peeperInfo["count"] + (((1.14737 ** (1.00133 * (dataList[0][7] - 7.91614)) - 0.280201) * 480) * 2)
        else:
            globals.peeperInfo["count"] = globals.peeperInfo["count"] - ((1.14737 ** (1.00133 * (-(dataList[0][7] + 4) - 7.91614)) - 0.280201) * 480)
            
        if globals.peeperInfo["count"] > 200000:
            globals.peeperInfo["count"] = 200000
            
        peepersMax = -1

        if dateArray[1] == 3:
            peepersMax = 1
            if dateArray[2] < 15:
                peepersMax = 0
        if dateArray[1] == 4:
            peepersMax = 2
            if dateArray[2] < 15:
                peepersMax = 1
        elif dateArray[1] == 5:
            peepersMax = 4
            if dateArray[3] < 15:
                peepersMax = 3
        
        if dateArray[1] == 6:
            peepersMax = 4
        elif dateArray[1] == 7:
            peepersMax = 3
        elif dateArray[1] == 8:
            peepersMax = 2
        elif dateArray[1] == 9:
            peepersMax = 1
        elif dateArray[1] == 10:
            peepersMax = 0
        
        if dataList[0][7] > 0:
            tempSub = 4 - (6 * 2.718 ** (( - (((dataList[0][7] - 7) ** (2)) / (3 + dataList[0][7]))) * 0.177) - 1)
        else:
            tempSub = 5
        windSub = dataList[0][1] - 23 + api.wind.globals.windModif
        humidSub = -1 * ((((dataList[0][8] * 10) - 380) / 100) - 1)
        
        if tempSub > 5:
            tempSub = 5
        if windSub < 0:
            windSub = 0
        elif windSub > 5:
            windSub = 5
        if humidSub < 0:
            humidSub = 0 + (humidSub / 3)
        elif humidSub > 5:
            humidSub = 5

        rainSub = 0
        if dataList[0][4] == "lightrain":
            rainSub = 1
        elif dataList[0][4] == "rain":
            rainSub = 2
        elif dataList[0][4] == "snow":
            rainSub = -2

        print("Peepers Temp Modifier     = -" + str(tempSub))
        print("Peepers Wind Modifier     = -" + str(windSub))
        print("Peepers Humidity Modifier = -" + str(humidSub))
        print("Peepers Rain Modifier     = " + str(rainSub))

        peepersMax = peepersMax - tempSub - windSub - humidSub + rainSub
        
        if (globals.peeperInfo["count"] / 2000) < (peepersMax - 1):
            peepersMax = (globals.peeperInfo["count"] / 2000)

        print("Peepers Index             = " + str(peepersMax))

        status.vars['peepersTempModifier'] = tempSub
        status.vars['peepersHumidModifier'] = humidSub
        status.vars['peepersRainModifier'] = rainSub
        status.vars['peepersWindModifier'] = windSub
        status.vars['peepersIndex'] = peepersMax
    
        pep0 = pytools.clock.dateArrayToUTC(pytools.clock.fixDateArray([dateArray[0], dateArray[1], dateArray[2], dayTimes[5][3] - 2, dayTimes[5][4] + 30, 0]))
        pep1 = pytools.clock.dateArrayToUTC(pytools.clock.fixDateArray([dateArray[0], dateArray[1], dateArray[2], dayTimes[5][3], dayTimes[5][4], 0]))
        pep2 = pytools.clock.dateArrayToUTC(pytools.clock.fixDateArray([dateArray[0], dateArray[1], dateArray[2], dayTimes[5][3], dayTimes[5][4] + ((((dayTimes[6][3] - dayTimes[5][3]) * 60) + (dayTimes[6][3] - dayTimes[5][3])) / 2), 0]))
        pep3 = pytools.clock.dateArrayToUTC(pytools.clock.fixDateArray([dateArray[0], dateArray[1], dateArray[2], dayTimes[6][3], dayTimes[6][4], 0]))
        pep4 = pytools.clock.dateArrayToUTC(pytools.clock.fixDateArray([dateArray[0], dateArray[1], dateArray[2], dayTimes[6][3], dayTimes[6][4] + ((((dayTimes[6][3] - dayTimes[7][3]) * 60) + (dayTimes[6][3] - dayTimes[7][3])) / 2), 0]))
        
        psp0 = pytools.clock.dateArrayToUTC(pytools.clock.fixDateArray([dateArray[0], dateArray[1], dateArray[2], dayTimes[2][3] + 2, dayTimes[2][4] - 30, 0]))
        psp1 = pytools.clock.dateArrayToUTC(pytools.clock.fixDateArray([dateArray[0], dateArray[1], dateArray[2], dayTimes[2][3], dayTimes[2][4], 0]))
        psp2 = pytools.clock.dateArrayToUTC(pytools.clock.fixDateArray([dateArray[0], dateArray[1], dateArray[2], dayTimes[2][3], dayTimes[2][4] + ((((dayTimes[2][3] - dayTimes[1][3]) * 60) + (dayTimes[2][3] - dayTimes[1][3])) / 2), 0]))
        psp3 = pytools.clock.dateArrayToUTC(pytools.clock.fixDateArray([dateArray[0], dateArray[1], dateArray[2], dayTimes[1][3], dayTimes[1][4], 0]))
        psp4 = pytools.clock.dateArrayToUTC(pytools.clock.fixDateArray([dateArray[0], dateArray[1], dateArray[2], dayTimes[1][3], dayTimes[1][4] + ((((dayTimes[1][3] - dayTimes[2][3]) * 60) + (dayTimes[1][3] - dayTimes[2][3])) / 2), 0]))

        utc = pytools.clock.dateArrayToUTC(dateArray)
        
        pf0 = 0
        if (psp0 > utc) or (utc > pep0):
            if peepersMax >= 0:
                pf0 = 1
                if pn0 == 0:
                    pn0 = 1
                    fireWindowEvent("m_peepers_0_fi.mp3;peepers_0_fi.mp3", [25, 100, 65], 1.0, 0.0, 0)
                elif pn0 == 1:
                    fireWindowEvent("m_peepers_0.mp3;peepers_0.mp3", [25, 100, 65], 1.0, 0.0, 0)
        if pf0 == 0:
            if pn0 == 1:
                pn0 = 0
                fireWindowEvent("m_peepers_0_fo.mp3;peepers_0_fo.mp3", [25, 100, 65], 1.0, 0.0, 0)

        pf1 = 0
        if (psp1 > utc) or (utc > pep1):
            if peepersMax >= 1:
                pf1 = 1
                if pn1 == 0:
                    pn1 = 1
                    fireWindowEvent("m_peepers_1_fi.mp3;peepers_1_fi.mp3", [25, 100, 65], 1.0, 0.0, 0)
                elif pn1 == 1:
                    fireWindowEvent("m_peepers_1.mp3;peepers_1.mp3", [25, 100, 65], 1.0, 0.0, 0)
        if pf1 == 0:
            if pn1 == 1:
                pn1 = 0
                fireWindowEvent("m_peepers_1_fo.mp3;peepers_0_fo.mp3", [25, 100, 65], 1.0, 0.0, 0)

        pf2 = 0
        if (psp2 > utc) or (utc > pep2):
            if peepersMax >= 2:
                pf2 = 1
                if pn2 == 0:
                    pn2 = 1
                    fireWindowEvent("m_peepers_2_fi.mp3;peepers_2_fi.mp3", [25, 100, 65], 1.0, 0.0, 0)
                elif pn2 == 1:
                    fireWindowEvent("m_peepers_2.mp3;peepers_2.mp3", [25, 100, 65], 1.0, 0.0, 0)
        if pf2 == 0:
            if pn2 == 1:
                pn2 = 0
                fireWindowEvent("m_peepers_2_fo.mp3;peepers_2_fo.mp3", [25, 100, 65], 1.0, 0.0, 0)

        pf3 = 0
        if (psp3 > utc) or (utc > pep3):
            if peepersMax >= 3:
                pf3 = 1
                if pn3 == 0:
                    pn3 = 1
                    fireWindowEvent("m_peepers_3_fi.mp3;peepers_3_fi.mp3", [25, 100, 65], 1.0, 0.0, 0)
                elif pn3 == 1:
                    fireWindowEvent("m_peepers_3.mp3;peepers_3.mp3", [25, 100, 65], 1.0, 0.0, 0)
        if pf3 == 0:
            if pn3 == 1:
                pn3 = 0
                fireWindowEvent("m_peepers_3_fo.mp3;peepers_3_fo.mp3", [25, 100, 65], 1.0, 0.0, 0)

        pf4 = 0
        if (psp4 > utc) or (utc > pep4):
            if peepersMax >= 4:
                pf4 = 1
                if pn4 == 0:
                    pn4 = 1
                    fireWindowEvent("m_peepers_4_fi.mp3;peepers_4_fi.mp3", [25, 100, 65], 1.0, 0.0, 0)
                elif pn4 == 1:
                    fireWindowEvent("m_peepers_4.mp3;peepers_4.mp3", [25, 100, 65], 1.0, 0.0, 0)
        if pf4 == 0:
            if pn4 == 1:
                pn4 = 0
                fireWindowEvent("m_peepers_4_fo.mp3;peepers_4_fo.mp3", [25, 100, 65], 1.0, 0.0, 0)

        pytools.IO.saveJson("peepers.json", globals.peeperInfo)
        status.vars["peeperCount"] = globals.peeperInfo["count"]

        time.sleep(480)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True
        
def run():
    status.hasExited = False
    main()
    status.hasExited = True
