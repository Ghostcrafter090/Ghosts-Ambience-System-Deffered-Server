import modules.audio as audio
import json
import random
import os
import modules.pytools as pytools
import threading
import time

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": [],
        "wolvesChance": 0
    }

class globals:
    daytimes = 'set csth=6 \nset cstm=17 \nset ceth=20 \nset cetm=4 \nset cesth=19 \nset cestm=35 \nset nsth=5 \nset nstm=42 \nset neth=20 \nset netm=40 \nset asth=5 \nset astm=5 \nset aeth=21 \nset aetm=16 \n'
    minn = [-1, -1]
    clouds = 0
    temp = 0

class main:
    def dataGrabber():
        dataGrabbed = 0
        apiUrl = "http://api.openweathermap.org/data/2.5/weather?lat=44.8348826&lon=-63.5976494&appid=7472c08c3eb790cd771033cbbac56066"
        while not status.exit:
            dateArray = pytools.clock.getDateTime()
            if ((dateArray[4] % 5) == 0) and (dataGrabbed != 1):
                jsonDatan = pytools.net.getJsonAPI(apiUrl)
                globals.clouds = jsonDatan['clouds']['all']
                globals.temp = float(pytools.calc.abs(float(jsonDatan['main']['temp']) - 283))
                if globals.temp < 1:
                    globals.temp = 1
                print("API Data Collected.")
                dataGrabbed = 1
            if ((dateArray[4] % 5) != 0):
                dataGrabbed = 0
            time.sleep(5)
            status.vars['lastLoop'] = pytools.clock.getDateTime()
    
    def workHandler():
        dateArray = pytools.clock.getDateTime()
        jsonData = pytools.net.getJsonAPI("https://api.solunar.org/solunar/44.82,-63.62," + str(dateArray[0]) + str(dateArray[1]) + str(dateArray[2]) + ",-4")
        minZ = [dateArray[4] - 1, int(dateArray[5] / 10), jsonData, -1, [0, {'x': 0, 'y': 0, 'z': 0}]]
        while not status.exit:
            minZ = main.worker(minZ[0], minZ[1], minZ[2], minZ[3], minZ[4])
            status.vars['lastLoop'] = pytools.clock.getDateTime()
            status.finishedLoop = True


    def worker(minZ, minN, jsonData, ticb, currentColor):
        dateArray = pytools.clock.getDateTime()
        try:
            sunJson = json.loads(("{\"" + pytools.IO.getFile('daytimes.cmd').replace("set ", "").replace("\n", "\", \"").replace("=", "\": \"") + "}").replace(", \"}", "}").replace(" \",", "\",").replace(" \"}", "\"}"))
        except:
            sunJson = json.loads(("{\"" + globals.daytimes.replace("set ", "").replace("\n", "\", \"").replace("=", "\": \"") + "}").replace(", \"}", "}").replace(" \",", "\",").replace(" \"}", "\"}"))
        if minZ != dateArray[4]:
            jsonData = pytools.net.getJsonAPI("https://api.solunar.org/solunar/44.82,-63.62," + str(dateArray[0]) + str(dateArray[1]) + str(dateArray[2]) + ",-4")
            minZ = dateArray[4]
            print(str(dateArray) + " ::: Retreived data.")
            print(jsonData)
        if ticb != dateArray[4]:
            ticb = dateArray[4]
            currentColor = pytools.color.returnSunInfo(globals.clouds)
        dayModifier = int(currentColor[1]['x']) + int(currentColor[1]['y']) + int(currentColor[1]['z'])
        utc = (dateArray[3] * 60) + (dateArray[4])
        moonRise = (int(jsonData['moonRise'].split(":")[0]) * 60) + (int(jsonData['moonRise'].split(":")[1]))
        try:
            moonSet = (int(jsonData['moonSet'].split(":")[0]) * 60) + (int(jsonData['moonSet'].split(":")[1]))
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
        if (float(jsonData['moonIllumination'])) != 0:
            illumChance = (dayModifier + 1) * (100000000 * (float(jsonData['moonIllumination']))) * globals.temp * (globals.clouds + 1)
        else:
            illumChance = (dayModifier + 1) * (100000000 * 0.0001) * globals.temp * (globals.clouds + 1)
        if globals.minn[0] != dateArray[4]:
            print('illumChance = ' + str(illumChance) + '; utc = ' + str(utc) + '; moonRise = ' + str(moonRise) + '; moonSet = ' + str(moonSet) + '; moonMid = ' + str(moonMid))
            globals.minn[0] = dateArray[4]
        wolfChance = 0
        if moonRise < utc < moonSet:
            if dateArray[3] < 24:
                wolfChance = (dateArray[3] - (int(moonMid / 60 / 24))) * dateArray[4]
            if dateArray[3] < (int(sunJson['csth'])):
                wolfChance = ((int(moonMid / 60 / 24)) - dateArray[3]) * dateArray[4]
            monthn = 1
            if dateArray[1] <= 5:
                monthn = ((((dateArray[1] - 1) * 31) + dateArray[2]) / 31) ** 2.16
            elif dateArray[1] <= 10:
                monthn = ((10 * 31) / (((dateArray[1] - 1) * 31) + dateArray[2])) ** 5
            else:
                monthn = ((((dateArray[1] - 1) * 31) + dateArray[2]) / ((10 * 31))) ** 8
            if globals.minn[1] != dateArray[4]:
                globals.minn[1] = dateArray[4]
                print('wolfChance = ' + str(wolfChance) + "; monthn = " + str(monthn))
            if minN != int(dateArray[5] / 10):
                print(str(dateArray) + " ::: " + str(illumChance) + " " + str(wolfChance / monthn))
                minN = int(dateArray[5] / 10)
            try:
                if random.randrange(0, int(illumChance)) < (wolfChance / monthn):
                    if os.path.isfile('.\\nomufflewn.derp') == True:
                        audioEvent = audio.event()
                        audioEvent.register('wolf_howl_' + str(random.randrange(0, 3)) + ".mp3", 4, 40, 1, 0, 0)
                        audioEvent.run()
                    else:
                        audioEvent = audio.event()
                        audioEvent.register('wolf_howl_' + str(random.randrange(0, 3)) + "_m.mp3", 2, 40, 1, 0, 0)
                        audioEvent.register('wolf_howl_' + str(random.randrange(0, 3)) + ".mp3", 3, 40, 1, 0, 0)
                        audioEvent.run()
            except:
                pass
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
    
    
    
