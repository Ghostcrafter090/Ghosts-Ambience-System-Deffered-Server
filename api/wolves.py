import modules.audio as audio
import json
import random
import os
import math
import modules.pytools as pytools
import threading
import time
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
        "wolvesChance": 0,
        "illumChance": 0,
        "monthn": 0,
        "wolfActivity": 0,
        "moonData": [0, 0, 0],
        "utc": 0
    }

class globals:
    daytimes = 'set csth=6 \nset cstm=17 \nset ceth=20 \nset cetm=4 \nset cesth=19 \nset cestm=35 \nset nsth=5 \nset nstm=42 \nset neth=20 \nset netm=40 \nset asth=5 \nset astm=5 \nset aeth=21 \nset aetm=16 \n'
    minn = [-1, -1]
    clouds = 0
    location = {}
    jsonData = {}
    timeTic = 0
    timeOld = 0
    key = ""
    temp = 0

class main:
    def dataGrabber():
        dataGrabbed = 0
        apiUrl = "http://gsweathermore.ddns.net:226/access.php?grabopenspec=true&lat=<lat>&lon=<lon>&key=<key>"
        globals.location = pytools.IO.getJson(".\\location.json")
        globals.key = pytools.IO.getJson(".\\access.key")["openweathermap"]
        apiUrl = apiUrl.replace("<key>", globals.key).replace("<lat>", str(globals.location["coords"][0])).replace("<lon>", str(globals.location["coords"][1]))
        while not status.exit:
            dateArray = pytools.clock.getDateTime()
            if ((dateArray[4] % 2) == 0) and (dataGrabbed != 1):
                jsonDatan = pytools.net.getJsonAPI(apiUrl)
                globals.clouds = jsonDatan["data"]["main"]['clouds']['all']
                globals.temp = float(pytools.calc.abs(float(jsonDatan["data"]['main']["main"]['temp']) - 283))
                if globals.temp < 1:
                    globals.temp = 1
                print("API Data Collected.")
                dataGrabbed = 1
            if ((dateArray[4] % 2) != 0):
                dataGrabbed = 0
            time.sleep(5)
            status.vars['lastLoop'] = pytools.clock.getDateTime()
    
    def workHandler():
        dateArray = pytools.clock.getDateTime()
        if len(str(dateArray[1])) == 1:
            monthg = "0" + str(dateArray[1])
        else:
            monthg = str(dateArray[1])
        
        if len(str(dateArray[2])) == 1:
            dayg = "0" + str(dateArray[2])
        else:
            dayg = str(dateArray[2])
        globals.location = pytools.IO.getJson(".\\location.json")
        globals.jsonData = pytools.net.getJsonAPI(("https://api.solunar.org/solunar/<lat>,<lon>," + str(dateArray[0]) + str(monthg) + str(dayg) + ",-4").replace("<lat>", str(globals.location["coords"][0])).replace("<lon>", str(globals.location["coords"][1])))
        minZ = [dateArray[4] - 1, int(dateArray[5] / 10), globals.jsonData, -1, [0, {'x': 0, 'y': 0, 'z': 0}]]
        while not status.exit:
            minZ = main.worker(minZ[0], minZ[1], minZ[2], minZ[3], minZ[4])
            status.vars['lastLoop'] = pytools.clock.getDateTime()
            status.finishedLoop = True


    def worker(minZ, minN, jsonData, ticb, currentColor):
        globals.jsonData = jsonData
        dateArray = pytools.clock.getDateTime()
        try:
            sunJson = json.loads(("{\"" + pytools.IO.getFile('daytimes.cmd').replace("set ", "").replace("\n", "\", \"").replace("=", "\": \"") + "}").replace(", \"}", "}").replace(" \",", "\",").replace(" \"}", "\"}"))
        except:
            sunJson = json.loads(("{\"" + globals.daytimes.replace("set ", "").replace("\n", "\", \"").replace("=", "\": \"") + "}").replace(", \"}", "}").replace(" \",", "\",").replace(" \"}", "\"}"))
        if minZ != dateArray[4]:
            if len(str(dateArray[1])) == 1:
                monthg = "0" + str(dateArray[1])
            else:
                monthg = str(dateArray[1])
            
            if len(str(dateArray[2])) == 1:
                dayg = "0" + str(dateArray[2])
            else:
                dayg = str(dateArray[2])
            globals.location = pytools.IO.getJson(".\\location.json")
            globals.jsonData = pytools.net.getJsonAPI(("https://api.solunar.org/solunar/<lat>,<lon>," + str(dateArray[0]) + str(monthg) + str(dayg) + ",-4").replace("<lat>", str(globals.location["coords"][0])).replace("<lon>", str(globals.location["coords"][1])))
            minZ = dateArray[4]
            print(str(dateArray) + " ::: Retreived data.")
            print(globals.jsonData)
        if ticb != dateArray[4]:
            ticb = dateArray[4]
            currentColor = pytools.color.returnSunInfo(globals.clouds)
        dayModifier = int(currentColor[1]['x']) + int(currentColor[1]['y']) + int(currentColor[1]['z'])
        utc = (dateArray[3] * 60) + (dateArray[4])
        moonRise = (int(globals.jsonData['moonRise'].split(":")[0]) * 60) + (int(globals.jsonData['moonRise'].split(":")[1]))
        try:
            moonSet = (int(globals.jsonData['moonSet'].split(":")[0]) * 60) + (int(globals.jsonData['moonSet'].split(":")[1]))
        except:
            moonSet = 0
        if moonRise < moonSet:
            pass
        else:
            if (moonRise - 1440) < moonSet:
                moonRise = moonRise - 1440
            if (moonRise) < (moonSet + 1440):
                moonSet = moonSet + 1440
        moonMid = moonRise + ((moonSet - moonRise) / 2)
        if (float(globals.jsonData['moonIllumination'])) != 0:
            illumChance = (dayModifier + 1) * (100000000 * (float(globals.jsonData['moonIllumination']))) * globals.temp * (globals.clouds + 1)
        else:
            illumChance = (dayModifier + 1) * (100000000 * 0.0001) * globals.temp * (globals.clouds + 1)
        if globals.minn[0] != dateArray[4]:
            print('illumChance = ' + str(illumChance) + '; utc = ' + str(utc) + '; moonRise = ' + str(moonRise) + '; moonSet = ' + str(moonSet) + '; moonMid = ' + str(moonMid))
            globals.minn[0] = dateArray[4]
        status.vars["illumChance"] = illumChance  
        wolfChance = 0
        status.vars["moonData"] = [moonRise, moonMid, moonSet]
        status.vars["utc"] = utc
        if moonRise < utc < moonSet:
            if dateArray[3] < 24:
                wolfChance = (dateArray[3] - (int(moonMid / 60 / 24))) * dateArray[4]
            if dateArray[3] < (int(sunJson['csth'])):
                wolfChance = ((int(moonMid / 60 / 24)) - dateArray[3]) * dateArray[4]
            monthn = 1
            
            wolfChance = math.fabs(wolfChance)
            
            # if dateArray[1] <= 5:
                # monthn = ((((dateArray[1] - 1) * 31) + dateArray[2]) / 31) ** 2.16
            # elif dateArray[1] <= 10:
                # monthn = ((10 * 31) / (((dateArray[1] - 1) * 31) + dateArray[2])) ** 5
            # else:
                # monthn = ((((dateArray[1] - 1) * 31) + dateArray[2]) / ((10 * 31))) ** 8
                
            # https://www.desmos.com/calculator/xpesswsrlf
            monthn = ((dateArray[1] - 1) + (dateArray[2] / pytools.clock.getMonthEnd(dateArray[1])))
            x = monthn
            d = 8.65649
            h = -7.88838
            f = 5.93588
            g = 6.13395
            b = -12.4395
            a = 11.2949
            e = 2.71828182846
            monthn = (((d * e ** (((h * (x - f) ** (2)) / (2 * g ** (2)))) + ((1) / (2)) * (x + b) * (a + b + 1) + 0.5) ** (0.93)) / 1.2) ** 0.8
            if globals.minn[1] != dateArray[4]:
                globals.minn[1] = dateArray[4]
                print('wolvesChance = ' + str(wolfChance) + "; monthn = " + str(monthn))
            status.vars["wolvesChance"] = wolfChance
            status.vars["monthn"] = monthn
            status.vars["wolfActivity"] = ((wolfChance) / monthn) / ((int(illumChance) / 300000) + 1)
            globals.timeTic = time.time() - globals.timeOld
            globals.timeOld = time.time()
            if minN != int(dateArray[5] / 10):
                print(str(dateArray) + " ::: " + str(illumChance) + " " + str(wolfChance / monthn))
                print("Wolf Activity: " + str(((wolfChance) / monthn) / ((int(illumChance) / 300000) + 1)))
                
                # print(globals.timeTic)
                minN = int(dateArray[5] / 10)
            try:
                if random.randrange(0, int(illumChance)) / 300000 < ((wolfChance) / monthn):
                    howlInt = str(random.randrange(0, 3))
                    volume = (30 * random.random()) + 0.5
                    audio.playSoundWindow('wolf_howl_' + howlInt + "_m.mp3;wolf_howl_" + howlInt + ".mp3;wolf_howl_" + howlInt + ".mp3", [volume, volume * 1.5, volume], 0.95 + (random.random() / 10), 0, 0)
            except:
                pass
            time.sleep(1)
        else:
            time.sleep(5)
        return [minZ, minN, jsonData, ticb, currentColor]

def run():
    status.hasExited = False
    # while pytools.sound.audioObj == False:
#         pytools.sound.audioObj = status.audioObj
    seta = threading.Thread(target=main.workHandler)
    setb = threading.Thread(target=main.dataGrabber)
    seta.start()
    setb.start()
    seta.join()
    setb.join()
    status.hasExited = True
    
    
    
