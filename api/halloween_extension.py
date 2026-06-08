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
import modules.weather as weather
import pylunar
import copy
import traceback
import importlib
import modules.findagrave as findagrave

weather = importlib.reload(weather)
findagrave = importlib.reload(findagrave)

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
    
audioBuffer = audio.rapidFire(10)
    
class globals:
    run = False
    runUncanny = False
    hallowForecasted = False
    deathHistory = {}
    
try:
    deathHistory = pytools.IO.getJson(".\\working\\deathHistory.json")["data"]
except:
    print(traceback.format_exc())

def getDateTime(*args):
    return pytools.clock.getDateTime(*args)

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
                        
                        doNull(data.sunJson['ceth'])
                        doNull(data.sunJson['cetm'])
                        doNull(data.sunJson['csth'])
                        doNull(data.sunJson['cstm'])
                        doNull(data.sunJson['cesth'])
                        doNull(data.sunJson['cestm'])
                        error = 0
                    except:
                        print(traceback.format_exc())
                        error = 1
                        
            except:
                print(traceback.format_exc())
            time.sleep(10)
    
    def getZ():
        error = True
        while error:
            try:
                dummy(data.sunJson['cetm'])
                error = False
            except:
                print(traceback.format_exc())
                time.sleep(0.1)
        data.minZ = (int(data.sunJson['cetm']) + 30)
        data.hourZ = (int(data.sunJson['ceth']))
        if data.minZ < 0:
            data.minZ = data.minZ + 60
            data.hourZ = data.hourZ - 1
            
    # https://www.desmos.com/calculator/jertocumt3
    def getWeatherHallowModifier(timeStamp=pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()), weatherData=False):
        
        if type(weatherData) == list:
            dataf = [weatherData, 0]
        else:
            dataf = data.grabWeatherData()
        
        if dataf:
            try:
                lightningModif = (1.14898 ** (0.997531 * (dataf[1] + 0.00708756)) - 0.000982331) * 2
            except:
                lightningModif = 0
            try:
                baseIndex = data.getHallowIndex(timeStamp, noModif=True, noDay=True)
                if baseIndex > 0:
                    
                    if (dataf[0][0][0] / 0.74) > dataf[0][0][1]:
                        dataf[0][0][1] = dataf[0][0][0] / 0.74
                    
                    # Old: windGustModif = ((1.0382 ** (0.9993 * (dataf[0][0][1] - 1.00002)) - 0.963234) * (150 - baseIndex) ** 0.35)
                    windGustModif = (((1.0382 ** (0.9993 * (dataf[0][0][1] - 1.00002)) - 0.963234) * (150 - baseIndex) ** 0.35) ** 1.75) / 4
                    # if dataf[0][0][1] <= 30:
                    #     _betterGustModif = 0
                    # if dataf[0][0][1] > 40:
                    #     _betterGustModif = (baseIndex) + ((1.0382 ** (0.9993 * ((dataf[0][0][1] - 40) - 1.00002)) - 0.963234) * 2.5) / 0.04046123415518205
                    # else:
                    #     _betterGustModif = (baseIndex) * ((dataf[0][0][1] - 30) / 10)
                    
                    rainModif = dataf[0][1][0]
                else:
                    # Old: windGustModif = (1.0382 ** (0.9993 * (dataf[0][0][1] - 1.00002)) - 0.963234) * 2.5
                    windGustModif = (((1.0382 ** (0.9993 * (dataf[0][0][1] - 1.00002)) - 0.963234) * (150 - baseIndex) ** 0.35) ** 1.75) / 4
                    
                    # if dataf[0][0][1] <= 30:
                    #     _betterGustModif = 0
                    # if dataf[0][0][1] > 40:
                    #     _betterGustModif = (0 - baseIndex) + ((1.0382 ** (0.9993 * ((dataf[0][0][1] - 40) - 1.00002)) - 0.963234) * 2.5) / 0.04046123415518205
                    # else:
                    #     _betterGustModif = (0 - baseIndex) * ((dataf[0][0][1] - 30) / 10)
                    
                    rainModif = dataf[0][1][0] / 5
            except:
                windGustModif = 0
                rainModif = 0
            try:
                windSpeedModif = 1.0382 ** (0.9993 * (dataf[0][0][0] - 1.00002)) - 0.963234
            except:
                windSpeedModif = 0
            
            try:
                temperatureModif = ((36 * 8 ** ((( - 7 * (dataf[0][0][7] + 10.5) ** (2)) / (4898))) + 58 * 164 ** ((( - 3 * (dataf[0][0][7] + 0.4) ** (2)) / (336)))) / 100) * 10
            except:
                temperatureModif = 0
                
            try:
                dampColdModif = temperatureModif * (dataf[0][0][8] / 100)
            except:
                dampColdModif = 0
                
            try:
                visibilityModif = (1 - ((dataf[0][0][3] / 10000) ** 0.2)) * 10
            except:
                visibilityModif = 0
            try:
                if windGustModif > windSpeedModif:
                    windModif = windGustModif
                else:
                    windModif = windSpeedModif
            except:
                if type(windGustModif) == float:
                    windModif = windGustModif
                elif type(windSpeedModif) == float:
                    windModif = windSpeedModif
                else:
                    windModif = 0
            
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
                print(traceback.format_exc())
        else:
            return False
        
        try:
            currentYearToDate = findagrave.getYearlyDeathsPerHour(pytools.clock.getDateTime()[0]) * 24 * (365 + ((pytools.clock.getDateTime()[0] % 4) == 0))
            currentAverageRate = currentYearToDate / ((((pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())) - (24 * 60 * 60) - (pytools.clock.dateArrayToUTC([pytools.clock.getDateTime()[0], 1, 1, 0, 0, 0])) - 1) + 86400) / (60 * 60))

            if str(pytools.clock.getDateTime()[0:4]) in globals.deathHistory:
                currentAverageRate = globals.deathHistory[str(pytools.clock.getDateTime()[0:4])]
            
            if weatherData == False:
                currentAverageRate = findagrave.getCurrentDeathIndex()
                globals.deathHistory[str(pytools.clock.getDateTime()[0:4])] = findagrave.getCurrentDeathRate()
                try:
                    inf = 0
                    while ({"data": globals.deathHistory} != pytools.IO.getJson("deathHistory.json")) and (inf < 100):
                        if os.path.exists(".\\working"):
                            pytools.IO.saveJson(".\\working\\deathHistory.json", {"data": globals.deathHistory})
                        else:
                            pytools.IO.saveJson(".\\deathHistory.json", {"data": globals.deathHistory})
                        inf = inf + 1
                except:
                    pass
            else:
                minRate = findagrave.getMinDeathsPerYear()
                maxRate = findagrave.getMaxDeathsPerYear()
    
                currentAverageRate = (currentAverageRate - minRate[0]) / (maxRate[0] - minRate[0])
            
            deathRateModif = (currentAverageRate ** 3) * 20
        except:
            print(traceback.format_exc())
            deathRateModif = 0
            
        return lightningModif + windModif + weatherModif + rainModif + dampColdModif + visibilityModif + deathRateModif
    
    def getLunarPhase(dateArray):
        
        try:
            coords = pytools.IO.getJson(".\\location.json", doPrint=False)["coords"]
        except:
            coords = pytools.IO.getJson(".\\working\\location.json")["coords"]
        
        moonObj = pylunar.MoonInfo((coords[0], 0, 0), (coords[1], 0, 0))
        moonObj.update(tuple(dateArray))
        return (moonObj.fractional_phase() - 0.5) * 2
    
    # https://www.desmos.com/calculator/cen0vzl8q4
    # https://www.desmos.com/calculator/gxlcmcqbq5
    # https://www.desmos.com/calculator/iaxogvk6jt
    def getHallowIndex(timeStamp, noDay=False, noModif=False):
        
        fourYearFloat = timeStamp / (1461 * 24 * 60 * 60)
        
        dayOfFourYears = pytools.clock.getDayOfFourYear(pytools.clock.UTCToDateArray(timeStamp))
        
        dayOfYear = pytools.clock.getDayOfYear(pytools.clock.UTCToDateArray(timeStamp))
        
        u = pytools.clock.UTCToDateArray(timeStamp)[0]
        
        w = ((timeStamp) - (24 * 60 * 60) - (pytools.clock.dateArrayToUTC([u, 1, 1, 0, 0, 0])) - 1) + 86400
        
        q = 0
        a = 100
        b = 26265600 + q
        c = 3000000000000
        f = 30931200 + q
        g = 300000000000
        p = 3.14159265359
        h = 50
        e = 2.71828182846
        
        friday13Coeff = 50
        j = 16 * ( data.getLunarPhase(pytools.clock.UTCToDateArray(timeStamp)))
        l_2 = (11 * e ** ( - friday13Coeff * (((w - 1080000) ** (2)) / (g)))) + (4 * e ** ( - (3 * ((w - 1080000) ** (2)) / (g))))
        l_3 = (11 * e ** ( - friday13Coeff * (((w - 3758400) ** (2)) / (g)))) + (4 * e ** ( - (3 * ((w - 3758400) ** (2)) / (g))))
        l_4 = (11 * e ** ( - friday13Coeff * ((((w - q) - 6177600) ** (2)) / (g)))) + (4 * e ** ( - (3 * (((w - q) - 6177600) ** (2)) / (g))))
        l_5 = (11 * e ** ( - friday13Coeff * ((((w - q) - 8856000) ** (2)) / (g)))) + (4 * e ** ( - (3 * (((w - q) - 8856000) ** (2)) / (g))))
        l_6 = (11 * e ** ( - friday13Coeff * ((((w - q) - 11448000) ** (2)) / (g)))) + (4 * e ** ( - (3 * (((w - q) - 11448000) ** (2)) / (g))))
        l_7 = (11 * e ** ( - friday13Coeff * ((((w - q) - 14126400) ** (2)) / (g)))) + (4 * e ** ( - (3 * (((w - q) - 14126400) ** (2)) / (g))))
        l_8 = (11 * e ** ( - friday13Coeff * ((((w - q) - 16718400) ** (2)) / (g)))) + (4 * e ** ( - (3 * (((w - q) - 16718400) ** (2)) / (g))))
        l_9 = (11 * e ** ( - friday13Coeff * ((((w - q) - 19396800) ** (2)) / (g)))) + (4 * e ** ( - (3 * (((w - q) - 19396800) ** (2)) / (g))))
        l_10 = 18 * e ** ( - (friday13Coeff / 5) * (1 * (((w - q) - 22075200) ** (2)) / (g)))
        l_11 = (11 * e ** ( - friday13Coeff * ((((w - q) - 24667200) ** (2)) / (g)))) + (4 * e ** ( - (3 * (((w - q) - 24667200) ** (2)) / (g))))
        l_12 = (11 * e ** ( - friday13Coeff * ((((w - q) - 27345600) ** (2)) / (g)))) + (4 * e ** ( - (3 * (((w - q) - 27345600) ** (2)) / (g))))
        l_13 = (11 * e ** ( - friday13Coeff * ((((w - q) - 29937600) ** (2)) / (g)))) + (4 * e ** ( - (3 * (((w - q) - 29937600) ** (2)) / (g))))
        r = 29376000 + q
        s = 27302400 + q
        t = - 2 * ((a * e ** ( - (((w - r) ** (2)) / (c)))) + (h * e ** ( - (((w - r) ** (2)) / (g)))))
        z = - 2 * ((a * e ** ( - (((((w - s) ** (2)) / (c))) / (0.15)))) + (h * e ** ( - (((((w - s) ** (2)) / (g))) / (0.15)))))
        k = 20 * math.sin((((p) / (302400.0))) * ((w + 36 * 60 * 60) + pytools.clock.dateArrayToUTC([u, 1, 1, 0, 0, 0]) - 172800))
        
        # https://www.desmos.com/calculator/yhvhjm3tms
        # https://www.desmos.com/calculator/ca2x63vefa
        if j < 0:
            tCoeff = l_2 + l_3 + l_4 + l_5 + l_6 + l_7 + l_8 + l_9 + l_10 + l_11 + l_12 + l_13 + k
            j = j + ((1 - (- 10509.535 ** (0.0299375 * (tCoeff - 38.30504)) + 1.00002)) * 40)
        
        
        z_1 = 16 * math.sin((((p) / (1180295.8))) * ( - (24778000.0 - (((1180295.8) / (2)))) - (u * (356.25 * 24 * 60 * 60)))) + (7 * math.sin((((p) / (302400.0))) * ((24778000.0 + 12 * 60 * 60) + (u * 365.25 * 24 * 60 * 60) - 6))) + 13
        o = - 3 * ((a * e ** ( - (((w - f) ** (2)) / (c)))) + (h * e ** ( - (((w - f) ** (2)) / (g)))))
        m = (1.11 * (((((math.fabs(z_1 )) / (2)) + 15) / (15)) ** (1) * (a * e ** ( - 0.65 * (((w - b) ** (2)) / (c))))) + (h * e ** ( - 0.65 * (((w - b) ** (2)) / (g))))) + j + k + (2 * (l_2 + l_3 + l_4 + l_5 + l_6 + l_7 + l_8 + l_9 + l_10 + l_11 + l_12 + l_13)) + o + t + z - 40
        
        if not noModif:
            weatherModif = data.getWeatherHallowModifier()
        elif (type(noModif) == list):
            weatherModif = data.getWeatherHallowModifier(timeStamp=timeStamp, weatherData=noModif)
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
    
    def forecastHallowIndex(timeStamp, noDay=False):
        i = copy.deepcopy(timeStamp)
        indexMap = []
        while i < (timeStamp + 864000):
            if weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i)):
                indexMap.append(data.getHallowIndex(i, noDay=noDay, noModif=weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i))))
            else:
                indexMap.append(data.getHallowIndex(i, noDay=noDay, noModif=True))
            i = i + 3600
        
        return [max(indexMap), timeStamp + (indexMap.index(max(indexMap)) * 3600)]

    def getHallowForecastStart(timeStamp, noDay=False):
        i = copy.deepcopy(timeStamp)
        indexMap = []
        while i < (timeStamp + 864000):
            if weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i)):
                indexMap.append(data.getHallowIndex(i, noDay=noDay, noModif=weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i))))
            else:
                indexMap.append(data.getHallowIndex(i, noDay=noDay, noModif=True))
            
            if indexMap[-1] > 0:
                return [max(indexMap), timeStamp + (indexMap.index(max(indexMap)) * 3600)]
            
            i = i + 3600
        
        return [max(indexMap), timeStamp + (indexMap.index(max(indexMap)) * 3600)]

    def getMinutelyHallowData():
        timeStamp = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        i = timeStamp
        
        indexMap = []
        while i < (timeStamp + 3600):
            if weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i)):
                indexMap.append(data.getHallowIndex(i, noDay=False, noModif=weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i))))
            else:
                indexMap.append(data.getHallowIndex(i, noDay=False, noModif=True))
            i = i + 60
            
        return indexMap

    def getBiHourlyHallowData():
        timeStamp = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        i = timeStamp
        
        indexMap = []
        while i < (timeStamp + 864000):
            if weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i)):
                indexMap.append(data.getHallowIndex(i, noDay=True, noModif=weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i))))
            else:
                indexMap.append(data.getHallowIndex(i, noDay=True, noModif=True))
            i = i + 7200
            
        return indexMap
    
    def getCompleteHallowData(noModif=False, silent=True):
        timeStamp = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        i = timeStamp
        
        indexMap = []
        while i < (timeStamp + 7776000):
            if weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i)) and (not noModif):
                indexMap.append(data.getHallowIndex(i, noDay=True, noModif=weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i))))
            else:
                indexMap.append(data.getHallowIndex(i, noDay=True, noModif=True))
                
            if not silent:
                print("Completion: " + str(((i - timeStamp) / 7776000) * 100) + "% (" + str(indexMap[-1]) + ") " + str(pytools.clock.UTCToDateArray(i)))
            
            i = i + 3600
            
        return indexMap

    def forecastStartHallowIndex(timeStamp, noDay=False):
        i = copy.deepcopy(timeStamp)
        indexMap = []
        while i < (timeStamp + 864000):
            if weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i)):
                indexMap.append(data.getHallowIndex(i, noDay=noDay, noModif=weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i))))
            else:
                indexMap.append(data.getHallowIndex(i, noDay=noDay, noModif=True))
            i = i + 3600
        
        def _first(indexMap):
            for n in indexMap:
                if n > 0:
                    return n
        
        return [_first(indexMap), timeStamp + (indexMap.index(_first(indexMap)) * 3600)]

    def forecastUncannyIndex(timeStamp, noDay=False):
        i = copy.deepcopy(timeStamp)
        indexMap = []
        while i < (timeStamp + 864000):
            
            if pytools.clock.UTCToDateArray(i)[1] == 9:
                septUncannyRun = -((-0.517241 * pytools.clock.UTCToDateArray(i)[2]) + 0.517241)
            elif pytools.clock.UTCToDateArray(i)[1] == 10:
                septUncannyRun = 1000
            else:
                septUncannyRun = -1000
            
            if weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i)):
                
                if 0 < -data.getHallowIndex(i, noDay=noDay, noModif=weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i))) < septUncannyRun:
                    indexMap.append(-data.getHallowIndex(i, noDay=noDay, noModif=weather.forecast.getForecastAtTime(pytools.clock.UTCToDateArray(i))))
                else:
                    indexMap.append(-1000)
            else:
                if 0 < -data.getHallowIndex(i, noDay=noDay, noModif=True) < septUncannyRun:
                    indexMap.append(-data.getHallowIndex(i, noDay=noDay, noModif=True))
                else:
                    indexMap.append(-1000)
                
            i = i + 3600
            
        return [max(indexMap), timeStamp + (indexMap.index(max(indexMap)) * 3600)]

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

# def getDateTime():
#     daten = datetime.now()
#     dateArray = [1970, 1, 1, 0, 0, 0]
#     getDateTime()[0] = int(str(daten).split(" ")[0].split("-")[0])
#     getDateTime()[1] = int(str(daten).split(" ")[0].split("-")[1])
#     getDateTime()[2] = int(str(daten).split(" ")[0].split("-")[2])
#     getDateTime()[3] = int(str(daten).split(" ")[1].split(":")[0])
#     getDateTime()[4] = int(str(daten).split(" ")[1].split(":")[1])
#     getDateTime()[5] = int(str(daten).split(" ")[1].split(":")[2].split(".")[0])
#     return getDateTime()
    
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
    if getDateTime()[3] == hour:
        if getDateTime()[2] > day:
            if getDateTime()[4] == minute:
                if noA != 1:
                    threading.Thread(target=audio.playSoundAll, args=('closetomidnight.mp3', 40, 1, 0, 0,)).start()
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
        loopTime = time.monotonic()
        chanceModifier = 1
        while not status.exit:
            try:
                if globals.run:
                    try:
                        deathGhostChance = 0
                        dyingGhostChance = 0
                        ghostChance = 0
                        hasPlayed = False
                        if getDateTime()[2] > 24:
                            if getDateTime()[3] > data.hourZ:
                                    deathGhostChance = (getDateTime()[3] - (int(data.hourZ + 2))) * getDateTime()[4]
                                    deathGhostChance = deathGhostChance / (32 - getDateTime()[2])
                                    deathGhostChance = deathGhostChance * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 170)
                                    if random.randrange(0, int(45000 * chanceModifier)) < (deathGhostChance / ((32 - getDateTime()[2]) / 3) + 1):
                                        ghSpeaker = 5
                                        while ghSpeaker == 5:
                                            ghSpeaker = random.randrange(0, 10)
                                        # audioEvent = audio.event()
                                        speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                                        audioBuffer.register('death_ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                        # threading.Thread(target=audioEvent.run).start()
                                        hasPlayed = True
                            elif getDateTime()[3] == data.hourZ:
                                if getDateTime()[4] >= data.minZ:
                                    deathGhostChance = (getDateTime()[3] - (int(data.hourZ + 2))) * getDateTime()[4]
                                    deathGhostChance = deathGhostChance / (32 - getDateTime()[2])
                                    deathGhostChance = deathGhostChance * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 170)
                                    if random.randrange(0, int(45000 * chanceModifier)) < (deathGhostChance / ((32 - getDateTime()[2]) / 3) + 1):
                                        ghSpeaker = 5
                                        while ghSpeaker == 5:
                                            ghSpeaker = random.randrange(0, 10)
                                        # audioEvent = audio.event()
                                        speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                                        audioBuffer.register('death_ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                        # threading.Thread(target=audioEvent.run).start()
                                        hasPlayed = True
                        if getDateTime()[2] > 19:
                            if getDateTime()[3] > data.hourZ:
                                dyingGhostChance = (getDateTime()[3] - (int(data.hourZ + 1))) * getDateTime()[4]
                                dyingGhostChance = dyingGhostChance / (32 - getDateTime()[2])
                                dyingGhostChance = dyingGhostChance * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 170)
                                if random.randrange(0, int(45000 * chanceModifier)) < (dyingGhostChance / ((32 - getDateTime()[2]) / 5) + 1):
                                    ghSpeaker = 5
                                    while ghSpeaker == 5:
                                        ghSpeaker = random.randrange(0, 10)
                                    # audioEvent = audio.event()
                                    speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                                    audioBuffer.register('dying_ghost_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                    # threading.Thread(target=audioEvent.run).start()
                                    hasPlayed = True
                            elif getDateTime()[3] == data.hourZ:
                                if getDateTime()[4] >= data.minZ:
                                    dyingGhostChance = 0
                                    if getDateTime()[3] < (24):
                                        dyingGhostChance = (getDateTime()[3] - (int(data.hourZ + 1))) * getDateTime()[4]
                                        dyingGhostChance = dyingGhostChance / (32 - getDateTime()[2])
                                        dyingGhostChance = dyingGhostChance * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 170)
                                    if random.randrange(0, int(45000 * chanceModifier)) < (dyingGhostChance / ((32 - getDateTime()[2]) / 5) + 1):
                                        ghSpeaker = 5
                                        while ghSpeaker == 5:
                                            ghSpeaker = random.randrange(0, 10)
                                        # audioEvent = audio.event()
                                        speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                                        audioBuffer.register('dying_ghost_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                        # threading.Thread(target=audioEvent.run).start()
                                        hasPlayed = True
                        if getDateTime()[2] > 9:
                            if getDateTime()[3] > data.hourZ:
                                ghostChance = 0
                                if getDateTime()[3] < (24):
                                    ghostChance = (getDateTime()[3] - (int(data.hourZ))) * getDateTime()[4]
                                    ghostChance = ghostChance / (32 - getDateTime()[2])
                                    ghostChance = ghostChance * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 170)
                                if random.randrange(0, int(45000 * chanceModifier)) < (ghostChance / ((32 - getDateTime()[2]) / 9) + 1):
                                    ghSpeaker = 5
                                    while ghSpeaker == 5:
                                        ghSpeaker = random.randrange(0, 10)
                                    # audioEvent = audio.event()
                                    speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                                    audioBuffer.register('ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, (0.5 + random.random()) * 40, speed, 0, 0)
                                    hasPlayed = True
                                    # threading.Thread(target=audioEvent.run).start()
                            elif getDateTime()[3] == data.hourZ:
                                if getDateTime()[4] >= data.minZ:
                                    ghostChance = 0
                                    if getDateTime()[3] < (24):
                                        ghostChance = (getDateTime()[3] - (int(data.hourZ))) * getDateTime()[4]
                                        ghostChance = ghostChance / (32 - getDateTime()[2])
                                        ghostChance = ghostChance * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 170)
                                    if random.randrange(0, int(45000 * chanceModifier)) < (ghostChance / ((32 - getDateTime()[2]) / 9) + 1):
                                        ghSpeaker = 5
                                        while ghSpeaker == 5:
                                            ghSpeaker = random.randrange(0, 10)
                                        # audioEvent = audio.event()
                                        speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                                        audioBuffer.register('ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, (0.5 + random.random()) * 40, speed, 0, 0)
                                        hasPlayed = True
                                        # threading.Thread(target=audioEvent.run).start()
                        time.sleep(0.1)
                        
                        if hasPlayed:
                            time.sleep(5)
                        
                        try:
                            chanceModifier = 0.1 / (time.monotonic() - loopTime)
                            
                            if loopTime > 1:
                                loopTime = 1
                        except ZeroDivisionError:
                            chanceModifier = 1
                        loopTime = time.monotonic()
                        sections.ghostsChance = [(deathGhostChance / ((32 - getDateTime()[2]) / 3) + 1), (dyingGhostChance / ((32 - getDateTime()[2]) / 5) + 1), (ghostChance / ((32 - getDateTime()[2]) / 9) + 1)]
                    except:
                        print(traceback.format_exc())
                wait = True
                for n in sections.ghostsChance:
                    if n > 1:
                        wait = False
                if wait:
                    time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)
    
    uncannyGhostsChance = [0, 0, 0]
             
    def testGhostsUncanny():
        uncannyGhostsChance = [0, 0, 0]
        while not status.exit:
            try:
                if globals.runUncanny:
                    try:
                        uncannyDeathGhostChance = 0
                        uncannyDyingGhostChance = 0
                        uncannyGhostChance = 0
                        if getDateTime()[2] > 24:
                            if getDateTime()[3] > data.hourZ:
                                    uncannyDeathGhostChance = (getDateTime()[3] - (int(data.hourZ + 2))) * getDateTime()[4]
                                    uncannyDeathGhostChance = uncannyDeathGhostChance / (32 - getDateTime()[2])
                                    uncannyDeathGhostChance = uncannyDeathGhostChance * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 170)
                                    if random.randrange(0, 37500) < (uncannyDeathGhostChance / ((32 - getDateTime()[2]) / 3) + 1):
                                        ghSpeaker = 5
                                        while ghSpeaker == 5:
                                            ghSpeaker = random.randrange(0, 10)
                                        # audioEvent = audio.event()
                                        speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                                        audioBuffer.register('hu_death_ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                        # threading.Thread(target=audioEvent.run).start()
                            elif getDateTime()[3] == data.hourZ:
                                if getDateTime()[4] >= data.minZ:
                                    uncannyDeathGhostChance = (getDateTime()[3] - (int(data.hourZ + 2))) * getDateTime()[4]
                                    uncannyDeathGhostChance = uncannyDeathGhostChance / (32 - getDateTime()[2])
                                    uncannyDeathGhostChance = uncannyDeathGhostChance * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 170)
                                    if random.randrange(0, 37500) < (uncannyDeathGhostChance / ((32 - getDateTime()[2]) / 3) + 1):
                                        ghSpeaker = 5
                                        while ghSpeaker == 5:
                                            ghSpeaker = random.randrange(0, 10)
                                        # audioEvent = audio.event()
                                        speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                                        audioBuffer.register('hu_death_ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                        # threading.Thread(target=audioEvent.run).start()
                        if getDateTime()[2] > 19:
                            if getDateTime()[3] > data.hourZ:
                                uncannyDyingGhostChance = (getDateTime()[3] - (int(data.hourZ + 1))) * getDateTime()[4]
                                uncannyDyingGhostChance = uncannyDyingGhostChance / (32 - getDateTime()[2])
                                uncannyDyingGhostChance = uncannyDyingGhostChance * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 170)
                                if random.randrange(0, 37500) < (uncannyDyingGhostChance / ((32 - getDateTime()[2]) / 5) + 1):
                                    ghSpeaker = 5
                                    while ghSpeaker == 5:
                                        ghSpeaker = random.randrange(0, 10)
                                    # audioEvent = audio.event()
                                    speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                                    audioBuffer.register('hu_dying_ghost_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                    # threading.Thread(target=audioEvent.run).start()
                            elif getDateTime()[3] == data.hourZ:
                                if getDateTime()[4] >= data.minZ:
                                    uncannyDyingGhostChance = 0
                                    if getDateTime()[3] < (24):
                                        uncannyDyingGhostChance = (getDateTime()[3] - (int(data.hourZ + 1))) * getDateTime()[4]
                                        uncannyDyingGhostChance = uncannyDyingGhostChance / (32 - getDateTime()[2])
                                        uncannyDyingGhostChance = uncannyDyingGhostChance * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 170)
                                    if random.randrange(0, 37500) < (uncannyDyingGhostChance / ((32 - getDateTime()[2]) / 5) + 1):
                                        ghSpeaker = 5
                                        while ghSpeaker == 5:
                                            ghSpeaker = random.randrange(0, 10)
                                        # audioEvent = audio.event()
                                        speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                                        audioBuffer.register('hu_dying_ghost_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, ((0.5 + random.random()) * 40) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                                        # threading.Thread(target=audioEvent.run).start()
                        if getDateTime()[2] > 9:
                            if getDateTime()[3] > data.hourZ:
                                uncannyGhostChance = 0
                                if getDateTime()[3] < (24):
                                    uncannyGhostChance = (getDateTime()[3] - (int(data.hourZ))) * getDateTime()[4]
                                    uncannyGhostChance = uncannyGhostChance / (32 - getDateTime()[2])
                                    uncannyGhostChance = uncannyGhostChance * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 170)
                                if random.randrange(0, 37500) < (uncannyGhostChance / ((32 - getDateTime()[2]) / 9) + 1):
                                    ghSpeaker = 5
                                    while ghSpeaker == 5:
                                        ghSpeaker = random.randrange(0, 10)
                                    # udioEvent = audio.event()
                                    speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                                    audioBuffer.register('hu_ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, (0.5 + random.random()) * 40, speed, 0, 0)
                                    # threading.Thread(target=audioEvent.run).start()
                            elif getDateTime()[3] == data.hourZ:
                                if getDateTime()[4] >= data.minZ:
                                    uncannyGhostChance = 0
                                    if getDateTime()[3] < (24):
                                        uncannyGhostChance = (getDateTime()[3] - (int(data.hourZ))) * getDateTime()[4]
                                        uncannyGhostChance = uncannyGhostChance / (32 - getDateTime()[2])
                                        uncannyGhostChance = uncannyGhostChance * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 170)
                                    if random.randrange(0, 37500) < (uncannyGhostChance / ((32 - getDateTime()[2]) / 9) + 1):
                                        ghSpeaker = 5
                                        while ghSpeaker == 5:
                                            ghSpeaker = random.randrange(0, 10)
                                        # audioEvent = audio.event()
                                        speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                                        audioBuffer.register('hu_ghost_' + str(random.randrange(0, 2)) + ".mp3", ghSpeaker, (0.5 + random.random()) * 40, speed, 0, 0)
                                        # threading.Thread(target=audioEvent.run).start()
                        time.sleep(0.1)
                        sections.uncannyGhostsChance = [(uncannyDeathGhostChance / ((32 - getDateTime()[2]) / 3) + 1), (uncannyDyingGhostChance / ((32 - getDateTime()[2]) / 5) + 1), (uncannyGhostChance / ((32 - getDateTime()[2]) / 9) + 1)]
                    except:
                        print(traceback.format_exc())
                wait = True
                for n in sections.uncannyGhostsChance:
                    if n > 1:
                        wait = False
                if wait:
                    time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)

    def closeMidTestRun():
        while not status.exit:
            if globals.run:
                try:
                    mainVars.noA = closetomidTest(getDateTime(), 23, 25, 10, mainVars.noA)
                    mainVars.noB = closetomidTest(getDateTime(), 23, 20, 15, mainVars.noB)
                    mainVars.noC = closetomidTest(getDateTime(), 23, 15, 30, mainVars.noC)
                    mainVars.noD = closetomidTest(getDateTime(), 23, 10, 45, mainVars.noD)
                except:
                    print(traceback.format_exc())
            time.sleep(1)
    
    draftChance = 0
    
    def runDrafts():
        loopTime = time.monotonic()
        chanceModifier = 1
        wasRunning = 0 
        while not status.exit:
            try:
                if globals.run:
                    if (wasRunning < 1):
                        speed = ((random.random() * 0.5) - 0.25) + 0.5
                        draftNumber = str(random.randrange(0, 3))
                        audioEvent = audio.event()
                        audioEvent.register('draft_' + draftNumber + ".mp3", 0, 100 * ((1 - wasRunning) + random.random()), speed, 0, 0)
                        audioEvent.register('draft_' + draftNumber + ".mp3", 0, 25 * ((1 - wasRunning) + random.random()), speed * 0.25, 0, 0)
                        audioEvent.register('draft_' + draftNumber + ".mp3", 1, 100 * ((1 - wasRunning) + random.random()), speed, 0, 0)
                        audioEvent.register('draft_' + draftNumber + ".mp3", 1, 25 * ((1 - wasRunning) + random.random()), speed * 0.25, 0, 0)
                        audioEvent.register('draft_' + draftNumber + ".mp3", 2, 100 * ((1 - wasRunning) + random.random()), speed, 0, 0)
                        audioEvent.register('draft_' + draftNumber + ".mp3", 2, 25 * ((1 - wasRunning) + random.random()), speed * 0.25, 0, 0)
                        audioEvent.register('draft_' + draftNumber + ".mp3", 9, 50 * ((1 - wasRunning) + random.random()), speed * 0.5, 0, 0)
                        audioEvent.register('draft_' + draftNumber + ".mp3", 3, 100 * ((1 - wasRunning) + random.random()), speed * 0.25, 0, 1)
                        audioEvent.run()
                        
                        wasRunning = wasRunning + random.random()
                         
                    try:
                        draftChance = 0
                        if getDateTime()[3] < 24:
                            draftChance = (getDateTime()[3] - (int(data.sunJson['cesth']))) * getDateTime()[4] * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        if getDateTime()[3] < (int(data.sunJson['csth'])):
                            draftChance = ((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4] * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)

                        if random.randrange(0, int(25000 * chanceModifier)) < draftChance:
                            ghSpeaker = 5
                            while ghSpeaker == 5:
                                ghSpeaker = random.randrange(0, 10) 
                            # audioEvent = audio.event()
                            speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                            audioBuffer.register('draft_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, (20 * ((0.6 * random.random()) + 0.4)) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                            time.sleep(5)
                            # threading.Thread(target=audioEvent.run).start()
                        sections.draftChance = draftChance
                        time.sleep(0.1)
                        try:
                            chanceModifier = 0.1 / (time.monotonic() - loopTime)
                            
                            if loopTime > 1:
                                loopTime = 1
                        except ZeroDivisionError:
                            chanceModifier = 1
                        loopTime = time.monotonic()
                    except:
                        print(traceback.format_exc())
                
                else:
                    if (wasRunning > 0):
                        speed = (((random.random() * 0.5) - 0.25) + 0.5) * (0.5 + (random.random() * 0.5))
                        draftNumber = str(random.randrange(0, 3))
                        audioEvent = audio.event()
                        audioEvent.register('hu_draft_' + draftNumber + ".mp3", 0, 100 * (wasRunning + random.random()), speed, 0, 0)
                        audioEvent.register('hu_draft_' + draftNumber + ".mp3", 0, 25 * (wasRunning + random.random()), speed * 0.25, 0, 0)
                        audioEvent.register('hu_draft_' + draftNumber + ".mp3", 1, 100 * (wasRunning + random.random()), speed, 0, 0)
                        audioEvent.register('hu_draft_' + draftNumber + ".mp3", 1, 25 * (wasRunning + random.random()), speed * 0.25, 0, 0)
                        audioEvent.register('hu_draft_' + draftNumber + ".mp3", 2, 100 * (wasRunning + random.random()), speed, 0, 0)
                        audioEvent.register('hu_draft_' + draftNumber + ".mp3", 2, 25 * (wasRunning + random.random()), speed * 0.25, 0, 0)
                        audioEvent.register('hu_draft_' + draftNumber + ".mp3", 9, 50 * (wasRunning + random.random()), speed * 0.5, 0, 0)
                        audioEvent.register('hu_draft_' + draftNumber + ".mp3", 3, 100 * (wasRunning + random.random()), speed * 0.25, 0, 1)
                        audioEvent.run()
                        wasRunning = wasRunning - random.random()
                
                if sections.draftChance <= 0:
                    time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)
                
    uncannyDraftChance = 0
    
    def runUncannyDrafts():
        loopTime = time.monotonic()
        chanceModifier = 1
        while not status.exit:
            try:
                if globals.runUncanny:
                    try:
                        uncannyDraftChance = 0
                        if getDateTime()[3] < 24:
                            uncannyDraftChance = (getDateTime()[3] - (int(data.sunJson['cesth']))) * getDateTime()[4] * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        if getDateTime()[3] < (int(data.sunJson['csth'])):
                            uncannyDraftChance = ((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4] * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)

                        if random.randrange(0, int(25000 * chanceModifier)) < uncannyDraftChance:
                            ghSpeaker = 5
                            while ghSpeaker == 5:
                                ghSpeaker = random.randrange(0, 10)
                            # audioEvent = audio.event()
                            speed = (0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)) ** 8
                            audioBuffer.register('hu_draft_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, (20 * ((0.6 * random.random()) + 0.4)) / ((ghSpeaker == 3) + 1), speed, 0, 0)
                            time.sleep(5)
                            # threading.Thread(target=audioEvent.run).start()
                        sections.uncannyDraftChance = uncannyDraftChance
                        time.sleep(0.1)
                        try:
                            chanceModifier = 0.1 / (time.monotonic() - loopTime)
                            
                            if loopTime > 1:
                                loopTime = 1
                        except ZeroDivisionError:
                            chanceModifier = 1
                        loopTime = time.monotonic()
                    except:
                        print(traceback.format_exc())
                if sections.uncannyDraftChance <= 0:
                    time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)
        
    breathChance = 0
    
    def runBreaths():
        loopTime = time.monotonic()
        chanceModifier = 1
        while not status.exit:
            try:
                if globals.run:
                    try:
                        breathChance = 0
                        if getDateTime()[3] < (int(data.sunJson['csth'])):
                            breathChance = ((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4]
                        breathChance = (breathChance / (32 - getDateTime()[2])) * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        if random.randrange(0, int(15000 * chanceModifier)) < breathChance:
                            ghSpeaker = 5
                            while ghSpeaker == 5:
                                ghSpeaker = random.randrange(0, 10)
                            # audioEvent = audio.event()
                            speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                            audioBuffer.register('h_breath_' + str(random.randrange(0, 4)) + ".mp3", ghSpeaker, 40 * ((0.6 * random.random()) + 0.4), speed, 0, 0)
                            time.sleep(5)
                            # threading.Thread(target=audioEvent.run).start()
                        sections.breathChance = breathChance
                        
                        time.sleep(0.1)
                        try:
                            chanceModifier = 0.1 / (time.monotonic() - loopTime)
                            
                            if loopTime > 1:
                                loopTime = 1
                        except ZeroDivisionError:
                            chanceModifier = 1
                        loopTime = time.monotonic()
                    except:
                        print(traceback.format_exc())
                if sections.draftChance <= 0:
                    time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)
                
    uncannyBreathChance = 0
    
    def runUncannyBreaths():
        loopTime = time.monotonic()
        chanceModifier = 1
        while not status.exit:
            try:
                if globals.runUncanny:
                    try:
                        uncannyBreathChance = 0
                        if getDateTime()[3] < (int(data.sunJson['csth'])):
                            uncannyBreathChance = ((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4]
                        uncannyBreathChance = (uncannyBreathChance / (32 - getDateTime()[2])) * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        if random.randrange(0, int(25000 * chanceModifier)) < uncannyBreathChance:
                            ghSpeaker = 5
                            while ghSpeaker == 5:
                                ghSpeaker = random.randrange(0, 10)
                            # audioEvent = audio.event()
                            speed = 0.96 + (random.random() / 12.5) + (0.983577 ** ( - 0.400303 * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) - 492.654)) - 0.0531709)
                            audioBuffer.register('hu_breath_' + str(random.randrange(0, 4)) + ".mp3", ghSpeaker, 40 * ((0.6 * random.random()) + 0.4), speed, 0, 0)
                            time.sleep(5)
                            # threading.Thread(target=audioEvent.run).start()
                        sections.uncannyBreathChance = uncannyBreathChance
                        time.sleep(0.1)
                        try:
                            chanceModifier = 0.1 / (time.monotonic() - loopTime)
                            
                            if loopTime > 1:
                                loopTime = 1
                        except ZeroDivisionError:
                            chanceModifier = 1
                        loopTime = time.monotonic()
                    except:
                        print(traceback.format_exc())
                if sections.draftChance <= 0:
                    time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)
                
    moodChance = [0, 0, 0, 0, 0, 0]

    def runMoodWaking():
        prevMinWaking = -1
        lastHGeneralWakingSpeedModifier = 1
        while not status.exit:
            doWaking = False
            try:
                forecastIndexValues = data.forecastHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True)
                if forecastIndexValues[0] > 0:
                    doWaking = True
                    if prevMinWaking != int(getDateTime()[4] / (2 / (1.1 - lastHGeneralWakingSpeedModifier))):
                        forecastIndex = forecastIndexValues[0] ** 2
                        forecastIndex = forecastIndex * ((forecastIndexValues[1] - pytools.clock.dateArrayToUTC(getDateTime())) / 864000)
                        monthS = pytools.clock.dateArrayToUTC([getDateTime()[0], getDateTime()[1], 1, 0, 0, 0])
                        monthE = pytools.clock.dateArrayToUTC([getDateTime()[0], getDateTime()[1] + 1, 1, 0, 0, 0])
                        monthC = pytools.clock.dateArrayToUTC(getDateTime()) - monthS
                        
                        hGeneralVol = (42 * (0.5 + (monthC / (monthE - monthS))))
                        if hGeneralVol > 35:
                            hGeneralVol = 35
                        hGeneralVol = hGeneralVol * (forecastIndex / 100)
                        
                        if hGeneralVol > 30:
                            hGeneralVol = 30
                        
                        hGeneralSpeedModifier = 0.08
                        midnight = pytools.clock.dateArrayToUTC(pytools.clock.getMidnight(getDateTime()))
                        sunset = pytools.clock.dateArrayToUTC(data.dayTimes[5])
                        civil = pytools.clock.dateArrayToUTC(data.dayTimes[2])
                        sunrise = pytools.clock.dateArrayToUTC(data.dayTimes[3])
                        current = pytools.clock.dateArrayToUTC(getDateTime())
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
                            print(traceback.format_exc())
                        if hGeneralSpeedModifier > 0.4:
                            hGeneralSpeedModifier = 0.4
                        elif hGeneralSpeedModifier < 0:
                            hGeneralSpeedModifier = 0
                        hGeneralSpeedModifier = (hGeneralSpeedModifier * (monthC / (monthE - monthS))) * (1.05 - (1 + (((forecastIndex / 100)) ** 0.1) - 1))
                        
                        hGeneralSpeedModifier = hGeneralSpeedModifier + (0.1 - (((forecastIndexValues[1] - pytools.clock.dateArrayToUTC(getDateTime())) / 864000) * 0.2))
                        
                        lastHGeneralWakingSpeedModifier = hGeneralSpeedModifier
                        
                        if getDateTime()[1] != 12:
                            
                            if forecastIndexValues[1] < (pytools.clock.dateArrayToUTC(getDateTime()) + 432000):
                                globals.hallowForecasted = True
                            
                            print("Looping h_general_waking effect at volume " + str(hGeneralVol) + ", and speed " + str(1.1 - hGeneralSpeedModifier) + ". Hallow Forecast index is at: " + str(forecastIndex))
                            moodEvent = audio.event()
                            moodEvent.register('h_general_waking.mp3', 0, hGeneralVol * random.random(), 1.1 - hGeneralSpeedModifier, 0, 0)
                            moodEvent.register('h_general_waking.mp3', 1, hGeneralVol * random.random(), 1.1 - hGeneralSpeedModifier, 0, 0)
                            moodEvent.registerWindow('h_general_waking.mp3;h_general_waking.mp3', [hGeneralVol * random.random(), hGeneralVol * random.random() * 2, math.fabs(1 - hGeneralVol * random.random())], 1.1 - hGeneralSpeedModifier, 0, 0)
                            
                            a = 0.924109
                            b = 1.00121
                            c = 4.00678
                            d = 1.35062
                            
                            windSpeedModif = (-a ** (b * (data.grabWeatherData()[0][0][1] - c))) + d
                            windSpeedVolModif = ((100 - (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())))) / 100) * (0.25 + (math.fabs((getDateTime()[3] + (getDateTime()[4] / 60) + (getDateTime()[5] / 60 / 60)) - 12) / 16))
                            
                            if (random.random() * 60) < (hGeneralVol + (7.5 * windSpeedVolModif) + (7.5 * windSpeedModif)):
                                
                                if windSpeedModif > 0.2:
                                    
                                    if type((1.1 - hGeneralSpeedModifier) * windSpeedModif) != complex:
                                
                                        moodEvent.register('death_wind_mood.mp3', 0, hGeneralVol * random.random() * windSpeedModif * windSpeedVolModif, (1.1 - hGeneralSpeedModifier) * windSpeedModif, 0, 0, lowPass=500 * windSpeedModif * windSpeedVolModif)
                                        moodEvent.register('death_wind_mood.mp3', 1, hGeneralVol * random.random() * windSpeedModif * windSpeedVolModif, (1.1 - hGeneralSpeedModifier) * windSpeedModif, 0, 0, lowPass=1000 * windSpeedModif * windSpeedVolModif)
                                        moodEvent.registerWindow('death_wind_mood.mp3;death_wind_mood.mp3', [hGeneralVol * random.random() * windSpeedModif * 0.5 * windSpeedVolModif, hGeneralVol * random.random() * windSpeedModif * windSpeedVolModif, math.fabs(1 - hGeneralVol * random.random() * windSpeedModif * 0.5) * windSpeedVolModif], (1.1 - hGeneralSpeedModifier) * windSpeedModif, 0, 0)
                            
                            threading.Thread(target=moodEvent.run).start()
                        
                        prevMinWaking = int(getDateTime()[4] / (2 / (1.1 - lastHGeneralWakingSpeedModifier)))
            except:
                print(traceback.format_exc())
            
            if doWaking:
                time.sleep(1)
            else:
                time.sleep(60)

    def runMood():
        loopTime = time.monotonic()
        chanceModifier = 1
        prevMin = -1
        prevMinWaking = -1
        lastHGeneralSpeedModifier = 1
        lastHGeneralWakingSpeedModifier = 1
        lastMood = -1
        while not status.exit:
            try:
                if globals.run:

                    # print("hgeneral a1")
                    try:
                        
                        if type(lastHGeneralSpeedModifier) == complex:
                            lastHGeneralSpeedModifier = 0.08
                        
                        if ((os.path.isfile('deathmode.derp') == True) and (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) > 0)) or (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) > 0):
                            
                            # print("hgeneral a2" + str(prevMin))
                            if (prevMin != int(math.floor((getDateTime()[4] + (getDateTime()[5] / 60)) * 2) / (1.1 - lastHGeneralSpeedModifier))):
                                
                                print("hgeneral a3")
                                monthS = pytools.clock.dateArrayToUTC([getDateTime()[0], getDateTime()[1], 1, 0, 0, 0])
                                monthE = pytools.clock.dateArrayToUTC([getDateTime()[0], getDateTime()[1] + 1, 1, 0, 0, 0])
                                monthC = pytools.clock.dateArrayToUTC(getDateTime()) - monthS
                                
                                # print("hgeneral a4")
                                
                                hGeneralVol = (42 * (0.5 + (monthC / (monthE - monthS))))
                                if hGeneralVol > 35:
                                    hGeneralVol = 35                                    
                                hGeneralVol = hGeneralVol * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                                if (getDateTime()[2] == 13) or (getDateTime()[2] == 14):
                                    if datetime(getDateTime()[0], getDateTime()[1], 13).isoweekday() == 5:
                                        finalArray = [getDateTime()[0], getDateTime()[1], 15, 0, 0, 0]
                                        hGeneralVol = hGeneralVol * ((2 * (random.random() + 0.5) * (1 - (math.fabs(pytools.clock.dateArrayToUTC(finalArray) - pytools.clock.dateArrayToUTC(getDateTime()) - 86400) / 86400))) + 1)
                                hGeneralSpeedModifier = 0.08
                                
                                # print("hgeneral a5")
                                
                                midnight = pytools.clock.dateArrayToUTC(pytools.clock.getMidnight(getDateTime()))
                                sunset = pytools.clock.dateArrayToUTC(data.dayTimes[5])
                                civil = pytools.clock.dateArrayToUTC(data.dayTimes[2])
                                sunrise = pytools.clock.dateArrayToUTC(data.dayTimes[3])
                                current = pytools.clock.dateArrayToUTC(getDateTime())
                                
                                # print("hgeneral a6")
                                
                                try:
                                    if current > sunset:
                                        hGeneralSpeedModifier = ((0.08 * (((midnight - sunset) - (midnight - current)) / (midnight - sunset)) ** 0.85)) + (0.2 * (data.grabWeatherData()[0][0][12] / 200))
                                        if hGeneralSpeedModifier > 0.2:
                                            hGeneralSpeedModifier = 0.2
                                    elif current < civil:
                                        hGeneralSpeedModifier = (0.08 * ((((midnight - 86400) - (sunset - 86400)) - ((midnight - 86400) - current)) / ((midnight - 86400) - (sunset - 86400))) ** 0.85) + (0.2 * (data.grabWeatherData()[0][0][12] / 200))
                                        if hGeneralSpeedModifier > 0.2:
                                            hGeneralSpeedModifier = 0.2
                                    elif current < sunrise:
                                        hGeneralSpeedModifier =  (0.2 - (2 * (-0.2 * (((sunrise - civil) / ((sunrise - civil + 1) - (sunrise - current))) - 1)))) + (0.2 * (data.grabWeatherData()[0][0][12] / 200))
                                        if hGeneralSpeedModifier > 0.2:
                                            hGeneralSpeedModifier = 0.2
                                    else:
                                        hGeneralSpeedModifier = 0.2 * (data.grabWeatherData()[0][0][12] / 200)
                                except:
                                    print(traceback.format_exc())
                                    
                                # print("hgeneral a7")
                                
                                hGeneralSpeedModifier = (hGeneralSpeedModifier * (monthC / (monthE - monthS))) * (data.getHallowIndex(pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()), noDay=True) / 100)
                                
                                if hGeneralSpeedModifier > 0.25:
                                    hGeneralSpeedModifier = 0.25
                                elif hGeneralSpeedModifier < 0:
                                    hGeneralSpeedModifier = 0
                                
                                # print("hgeneral a8")
                                
                                lastHGeneralSpeedModifier = hGeneralSpeedModifier
                                
                                print("Looping h_general effect at volume " + str(hGeneralVol) + ", and speed " + str(1.1 - hGeneralSpeedModifier) + ".")
                                moodEvent = audio.event()
                                moodEvent.register('h_general.mp3', 0, hGeneralVol, 1.1 - hGeneralSpeedModifier, 0, 0)
                                moodEvent.register('h_general.mp3', 1, hGeneralVol, 1.1 - hGeneralSpeedModifier, 0, 0)
                                moodEvent.registerWindow('h_general.mp3;h_general.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1.1 - hGeneralSpeedModifier, 0, 0)
                                threading.Thread(target=moodEvent.run).start()
                                
                                prevMin = int(math.floor((getDateTime()[4] + (getDateTime()[5] / 60)) * 2) / (1.1 - lastHGeneralSpeedModifier))
                            
                            if (lastMood + 15) < time.time():
                                # print("hgeneral a9")
                                
                                moodChance = [0, 0, 0, 0, 0, 0]
                                
                                moodChance[0] = (getDateTime()[3] - (int(data.sunJson['cesth']))) * getDateTime()[4]
                                if getDateTime()[3] < (int(data.sunJson['csth'])):
                                    moodChance[0] = ((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4]
                                
                                moodChance[1] = ((getDateTime()[3] - (int(data.sunJson['ceth']))) * getDateTime()[4] / 3) / (32 - getDateTime()[2])
                                if getDateTime()[3] < (int(data.sunJson['csth'])):
                                    moodChance[1] = (((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4] / 3) / (32 - getDateTime()[2])
                                
                                moodChance[2] = ((getDateTime()[3] - (int(data.sunJson['neth']))) * getDateTime()[4] / 4) / (32 - getDateTime()[2])
                                if getDateTime()[3] < (int(data.sunJson['csth'])):
                                    moodChance[2] = (((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4] / 4) / (32 - getDateTime()[2])
                                
                                moodChance[3] = ((getDateTime()[3] - (int(data.sunJson['aeth']))) * getDateTime()[4] / 5) / (32 - getDateTime()[2])
                                if getDateTime()[3] < (int(data.sunJson['csth'])):
                                    moodChance[3] = (((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4] / 5) / (32 - getDateTime()[2])
                                
                                moodChance[4] = ((getDateTime()[3] - (int(data.sunJson['aeth']) + 1)) * getDateTime()[4]) / ((32 - getDateTime()[2]) / 2)
                                if getDateTime()[3] < (int(data.sunJson['csth'])):
                                    moodChance[4] = (((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4]) / ((32 - getDateTime()[2]) / 2)
                                
                                moodChance[5] = ((getDateTime()[3] - (int(data.sunJson['aeth']) + 2)) * getDateTime()[4]) / ((32 - getDateTime()[2]) / 4)
                                if getDateTime()[3] < (int(data.sunJson['csth'])):
                                    moodChance[5] = (((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4]) / ((32 - getDateTime()[2]) / 4)
                                
                                # print("hgeneral a10")
                                
                                moodChanceModif = (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 150)
                                if moodChanceModif > 0.95:
                                    moodChanceModif = 0.95
                                
                                i = 0
                                while i < len(moodChance):
                                    moodChance[i] = moodChance[i] * moodChanceModif
                                    i = i + 1
                                    
                                # print("hgeneral a11")
                                
                                if (getDateTime()[2] == 13) or (getDateTime()[2] == 14):
                                    if datetime(getDateTime()[0], getDateTime()[1], 13).isoweekday() == 5:
                                        finalArray = [getDateTime()[0], getDateTime()[1], 15, 0, 0, 0]
                                        moodChance[2] = moodChance[2] * ((1000 * (random.random() + 0.5) * (1 - (math.fabs(pytools.clock.dateArrayToUTC(finalArray) - pytools.clock.dateArrayToUTC(getDateTime()) - 86400) / 86400))) + 1)
                                        moodChance[3] = moodChance[3] * ((1000 * (random.random() + 0.5) * (1 - (math.fabs(pytools.clock.dateArrayToUTC(finalArray) - pytools.clock.dateArrayToUTC(getDateTime()) - 86400) / 86400))) + 1)
                                
                                # print("hgeneral a12")
                                
                                moodEvent = audio.event()
                                
                                if random.randrange(0, int(25000 * chanceModifier)) < moodChance[0]:
                                    moodEvent.register('h_general_mood.mp3', 0, hGeneralVol, 1, 0, 0)
                                    moodEvent.register('h_general_mood.mp3', 1, hGeneralVol, 1, 0, 0)
                                    moodEvent.registerWindow('h_general_mood.mp3;h_general_mood.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1, 0, 0)
                                    # threading.Thread(target=moodEvent.run).start()
                                    lastMood = time.time()
                                    
                                if random.randrange(0, int(25000 * chanceModifier)) < moodChance[1]:
                                    # moodEvent = audio.event()
                                    moodEvent.register('h_general_dark.mp3', 0, hGeneralVol, 1, 0, 0)
                                    moodEvent.register('h_general_dark.mp3', 1, hGeneralVol, 1, 0, 0)
                                    moodEvent.registerWindow('h_general_dark.mp3;h_general_dark.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1, 0, 0)
                                    # threading.Thread(target=moodEvent.run).start()
                                    lastMood = time.time()
                                    
                                if random.randrange(0, int(25000 * chanceModifier)) < moodChance[2]:
                                    # moodEvent = audio.event()
                                    moodEvent.register('h_general_evil.mp3', 0, hGeneralVol, 1, 0, 0)
                                    moodEvent.register('h_general_evil.mp3', 1, hGeneralVol, 1, 0, 0)
                                    moodEvent.registerWindow('h_general_evil.mp3;h_general_evil.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1, 0, 0)
                                    # threading.Thread(target=moodEvent.run).start()
                                    lastMood = time.time()
                                    
                                if random.randrange(0, int(25000 * chanceModifier)) < moodChance[3]:
                                    # moodEvent = audio.event()
                                    moodEvent.register('h_general_sinister.mp3', 0, hGeneralVol, 1, 0, 0)
                                    moodEvent.register('h_general_sinister.mp3', 1, hGeneralVol, 1, 0, 0)
                                    moodEvent.registerWindow('h_general_sinister.mp3;h_general_sinister.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1, 0, 0)
                                    # threading.Thread(target=moodEvent.run).start()
                                    lastMood = time.time()
                                    
                                if random.randrange(0, int(25000 * chanceModifier)) < moodChance[4]: 
                                    # moodEvent = audio.event()
                                    moodEvent.register('h_general_dying.mp3', 0, hGeneralVol, 1, 0, 0)
                                    moodEvent.register('h_general_dying.mp3', 1, hGeneralVol, 1, 0, 0)
                                    moodEvent.registerWindow('h_general_dying.mp3;h_general_dying.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1, 0, 0)
                                    # threading.Thread(target=moodEvent.run).start()
                                    lastMood = time.time()
                                    
                                if random.randrange(0, int(25000 * chanceModifier)) < moodChance[5]:
                                    # moodEvent = audio.event()
                                    moodEvent.register('h_general_death.mp3', 0, hGeneralVol, 1, 0, 0)
                                    moodEvent.register('h_general_death.mp3', 1, hGeneralVol, 1, 0, 0)
                                    moodEvent.registerWindow('h_general_death.mp3;h_general_death.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1, 0, 0)
                                    # threading.Thread(target=moodEvent.run).start()
                                    lastMood = time.time()
                                
                                if (lastMood + 15) >= time.time():
                                    threading.Thread(target=moodEvent.run).start()
                            
                            # print("hgeneral a13")
                            
                        sections.moodChance = moodChance
                    except:
                        print(traceback.format_exc())
                    
                    time.sleep(0.1)
                    try:
                        chanceModifier = 0.1 / (time.monotonic() - loopTime)
                        
                        if loopTime > 1:
                            loopTime = 1
                    except ZeroDivisionError:
                        chanceModifier = 1
                    loopTime = time.monotonic()
                    if chanceModifier > 1:
                        chanceModifier = 1
                else:
                    print("halloween_extension hgeneral_loop message: not_running.")
                
                wait = True
                
                for n in sections.moodChance:
                    if n > 0:
                        wait = False
                
                if wait:
                    # print("hgeneral a15")
                    time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)

    uncannyMoodChance = [0, 0, 0, 0, 0, 0]

    def runUncannyMood():
        prevMin = -1
        loopTime = time.monotonic()
        chanceModifier = 1
        prevMinWaking = -1
        lastHGeneralWakingSpeedModifier = 0
        lastHGeneralSpeedModifier = 0
        while not status.exit:
            try:
                doWaking = False
                try:
                        
                    if type(lastHGeneralSpeedModifier) == complex:
                        lastHGeneralSpeedModifier = 0.08
                    
                    forecastIndexValues = data.forecastUncannyIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True)
                    if (forecastIndexValues[0] > 0) and (8 < pytools.clock.UTCToDateArray(forecastIndexValues[1])[1] < 11):
                        doWaking = True
                        if prevMinWaking != int(getDateTime()[4] / (2 / (1.1 - lastHGeneralWakingSpeedModifier))):
                            forecastIndex = forecastIndexValues[0] ** 2
                            forecastIndex = forecastIndex * ((forecastIndexValues[1] - pytools.clock.dateArrayToUTC(getDateTime())) / 864000)
                            doWaking = True
                            monthS = pytools.clock.dateArrayToUTC([getDateTime()[0], getDateTime()[1], 1, 0, 0, 0])
                            monthE = pytools.clock.dateArrayToUTC([getDateTime()[0], getDateTime()[1] + 1, 1, 0, 0, 0])
                            monthC = pytools.clock.dateArrayToUTC(getDateTime()) - monthS
                            
                            hGeneralVol = (42 * (0.5 + (monthC / (monthE - monthS))))
                            if hGeneralVol > 35:
                                hGeneralVol = 35
                            hGeneralVol = hGeneralVol * (forecastIndex / 100)
                            
                            if hGeneralVol > 30:
                                hGeneralVol = 30
                            
                            hGeneralSpeedModifier = 0.08
                            midnight = pytools.clock.dateArrayToUTC(pytools.clock.getMidnight(getDateTime()))
                            sunset = pytools.clock.dateArrayToUTC(data.dayTimes[5])
                            civil = pytools.clock.dateArrayToUTC(data.dayTimes[2])
                            sunrise = pytools.clock.dateArrayToUTC(data.dayTimes[3])
                            current = pytools.clock.dateArrayToUTC(getDateTime())
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
                                print(traceback.format_exc())
                            if hGeneralSpeedModifier > 0.4:
                                hGeneralSpeedModifier = 0.4
                            elif hGeneralSpeedModifier < 0:
                                hGeneralSpeedModifier = 0
                            hGeneralSpeedModifier = (hGeneralSpeedModifier * (monthC / (monthE - monthS))) * (1.05 - (1 + (((forecastIndex / 100)) ** 0.1) - 1))
                            
                            hGeneralSpeedModifier = hGeneralSpeedModifier + (0.1 - (((forecastIndexValues[1] - pytools.clock.dateArrayToUTC(getDateTime())) / 864000) * 0.2))
                            
                            lastHGeneralWakingSpeedModifier = hGeneralSpeedModifier
                            
                            print("Looping hu_general_waking effect at volume " + str(hGeneralVol) + ", and speed " + str(1.1 - hGeneralSpeedModifier) + ". Uncanny Forecast index is at: " + str(forecastIndex))
                            moodEvent = audio.event()
                            moodEvent.register('hu_general_waking.mp3', 0, hGeneralVol * random.random(), 1.1 - hGeneralSpeedModifier, 0, 0)
                            moodEvent.register('hu_general_waking.mp3', 1, hGeneralVol * random.random(), 1.1 - hGeneralSpeedModifier, 0, 0)
                            moodEvent.registerWindow('hu_general_waking.mp3;hu_general_waking.mp3', [hGeneralVol * random.random(), hGeneralVol * random.random() * 2, hGeneralVol * random.random()], 1.1 - hGeneralSpeedModifier, 0, 0)
                            threading.Thread(target=moodEvent.run).start()
                            
                            prevMinWaking = int(getDateTime()[4] / (2 / (1.1 - lastHGeneralWakingSpeedModifier)))
                except:
                    print(traceback.format_exc())
                
                if globals.runUncanny:
                    print("Uncanny Mooooood looper!")
                    try:
                        if ((os.path.isfile('deathmode.derp') and (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) > 0))) or (os.path.exists("runningUncanny.derp")):
                            if prevMin != int(getDateTime()[4] / (1 - lastHGeneralSpeedModifier)):
                                monthS = pytools.clock.dateArrayToUTC([getDateTime()[0], getDateTime()[1], 1, 0, 0, 0])
                                monthE = pytools.clock.dateArrayToUTC([getDateTime()[0], getDateTime()[1] + 1, 1, 0, 0, 0])
                                monthC = pytools.clock.dateArrayToUTC(getDateTime()) - monthS
                                
                                hGeneralVol = (42 * (0.5 + (monthC / (monthE - monthS))))
                                if hGeneralVol > 35:
                                    hGeneralVol = 35
                                hGeneralVol = hGeneralVol * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                                hGeneralSpeedModifier = 0.08
                                midnight = pytools.clock.dateArrayToUTC(pytools.clock.getMidnight(getDateTime()))
                                sunset = pytools.clock.dateArrayToUTC(data.dayTimes[5])
                                civil = pytools.clock.dateArrayToUTC(data.dayTimes[2])
                                sunrise = pytools.clock.dateArrayToUTC(data.dayTimes[3])
                                current = pytools.clock.dateArrayToUTC(getDateTime())
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
                                    print(traceback.format_exc())
                                if hGeneralSpeedModifier > 0.4:
                                    hGeneralSpeedModifier = 0.4
                                elif hGeneralSpeedModifier < 0:
                                    hGeneralSpeedModifier = 0
                                hGeneralSpeedModifier = (hGeneralSpeedModifier * (monthC / (monthE - monthS))) * (1.05 - (1 + ((((-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True)) / 100)) ** 0.1) - 1))
                                
                                if type(hGeneralSpeedModifier) == complex:
                                    hGeneralSpeedModifier = hGeneralSpeedModifier.real
                                
                                lastHGeneralSpeedModifier = hGeneralSpeedModifier
                                
                                print("Looping hu_general effect at volume " + str(hGeneralVol) + ", and speed " + str(1 - hGeneralSpeedModifier) + ".")
                                moodEvent = audio.event()
                                moodEvent.register('hu_general.mp3', 0, hGeneralVol, 1 - hGeneralSpeedModifier, 0, 0)
                                moodEvent.register('hu_general.mp3', 1, hGeneralVol, 1 - hGeneralSpeedModifier, 0, 0)
                                moodEvent.registerWindow('hu_general.mp3;hu_general.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1 - hGeneralSpeedModifier, 0, 0)
                                threading.Thread(target=moodEvent.run).start()
                                
                                prevMin = int(getDateTime()[4] / (1 - lastHGeneralSpeedModifier))
                            
                            uncannyMoodChance = [0, 0, 0, 0, 0, 0]
                            
                            uncannyMoodChance[0] = (getDateTime()[3] - (int(data.sunJson['cesth']))) * getDateTime()[4]
                            if getDateTime()[3] < (int(data.sunJson['csth'])):
                                uncannyMoodChance[0] = ((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4]
                            
                            uncannyMoodChance[1] = ((getDateTime()[3] - (int(data.sunJson['ceth']))) * getDateTime()[4] / 3) / (32 - getDateTime()[2])
                            if getDateTime()[3] < (int(data.sunJson['csth'])):
                                uncannyMoodChance[1] = (((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4] / 3) / (32 - getDateTime()[2])
                            
                            uncannyMoodChance[2] = ((getDateTime()[3] - (int(data.sunJson['neth']))) * getDateTime()[4] / 4) / (32 - getDateTime()[2])
                            if getDateTime()[3] < (int(data.sunJson['csth'])):
                                uncannyMoodChance[2] = (((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4] / 4) / (32 - getDateTime()[2])
                            
                            uncannyMoodChance[3] = ((getDateTime()[3] - (int(data.sunJson['aeth']))) * getDateTime()[4] / 5) / (32 - getDateTime()[2])
                            if getDateTime()[3] < (int(data.sunJson['csth'])):
                                uncannyMoodChance[3] = (((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4] / 5) / (32 - getDateTime()[2])
                            
                            uncannyMoodChance[4] = ((getDateTime()[3] - (int(data.sunJson['aeth']) + 1)) * getDateTime()[4]) / ((32 - getDateTime()[2]) / 2)
                            if getDateTime()[3] < (int(data.sunJson['csth'])):
                                uncannyMoodChance[4] = (((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4]) / ((32 - getDateTime()[2]) / 2)
                            
                            uncannyMoodChance[5] = ((getDateTime()[3] - (int(data.sunJson['aeth']) + 2)) * getDateTime()[4]) / ((32 - getDateTime()[2]) / 4)
                            if getDateTime()[3] < (int(data.sunJson['csth'])):
                                uncannyMoodChance[5] = (((int(data.sunJson['csth'])) - getDateTime()[3]) * getDateTime()[4]) / ((32 - getDateTime()[2]) / 4)
                                
                            uncannyMoodChanceModif = (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 150)
                            if uncannyMoodChanceModif > 0.95:
                                uncannyMoodChanceModif = 0.95
                            
                            i = 0
                            while i < len(uncannyMoodChance):
                                uncannyMoodChance[i] = uncannyMoodChance[i] * uncannyMoodChanceModif
                                i = i + 1
                            
                            if random.randrange(0, int(25000 * chanceModifier)) < uncannyMoodChance[0]:
                                moodEvent = audio.event()
                                moodEvent.register('hu_general_mood.mp3', 0, hGeneralVol, 1, 0, 0)
                                moodEvent.register('hu_general_mood.mp3', 1, hGeneralVol, 1, 0, 0)
                                moodEvent.registerWindow('hu_general_mood.mp3;hu_general_mood.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1, 0, 0)
                                threading.Thread(target=moodEvent.run).start()
                                    
                            if random.randrange(0, int(25000 * chanceModifier)) < uncannyMoodChance[1]:
                                darkMoodEvent = audio.event()
                                moodEvent.register('hu_general_dark.mp3', 0, hGeneralVol, 1, 0, 0)
                                moodEvent.register('hu_general_dark.mp3', 1, hGeneralVol, 1, 0, 0)
                                moodEvent.registerWindow('hu_general_dark.mp3;hu_general_dark.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1, 0, 0)
                                threading.Thread(target=moodEvent.run).start()
                                
                            if random.randrange(0, int(25000 * chanceModifier)) < uncannyMoodChance[2]:
                                evilMoodEvent = audio.event()
                                moodEvent.register('hu_general_evil.mp3', 0, hGeneralVol, 1, 0, 0)
                                moodEvent.register('hu_general_evil.mp3', 1, hGeneralVol, 1, 0, 0)
                                moodEvent.registerWindow('hu_general_evil.mp3;hu_general_evil.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1, 0, 0)
                                threading.Thread(target=moodEvent.run).start()
                                
                            if random.randrange(0, int(25000 * chanceModifier)) < uncannyMoodChance[3]:
                                sinisterMoodEvent = audio.event()
                                moodEvent.register('hu_general_sinister.mp3', 0, hGeneralVol, 1, 0, 0)
                                moodEvent.register('hu_general_sinister.mp3', 1, hGeneralVol, 1, 0, 0)
                                moodEvent.registerWindow('hu_general_sinister.mp3;hu_general_sinister.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1, 0, 0)
                                threading.Thread(target=moodEvent.run).start()
                                
                            if random.randrange(0, int(25000 * chanceModifier)) < uncannyMoodChance[4]:
                                dyingMoodEvent = audio.event()
                                moodEvent.register('hu_general_dying.mp3', 0, hGeneralVol, 1, 0, 0)
                                moodEvent.register('hu_general_dying.mp3', 1, hGeneralVol, 1, 0, 0)
                                moodEvent.registerWindow('hu_general_dying.mp3;hu_general_dying.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1, 0, 0)
                                threading.Thread(target=moodEvent.run).start()
                                
                            if random.randrange(0, int(25000 * chanceModifier)) < uncannyMoodChance[5]:
                                deathMoodEvent = audio.event()
                                moodEvent.register('hu_general_death.mp3', 0, hGeneralVol, 1, 0, 0)
                                moodEvent.register('hu_general_death.mp3', 1, hGeneralVol, 1, 0, 0)
                                moodEvent.registerWindow('hu_general_death.mp3;hu_general_death.mp3', [hGeneralVol, hGeneralVol * 2, hGeneralVol], 1, 0, 0)
                                threading.Thread(target=moodEvent.run).start()
                                
                        sections.uncannyMoodChance = uncannyMoodChance
                    except:
                        print(traceback.format_exc())
                    time.sleep(0.1)
                    
                    try:
                        chanceModifier = 0.1 / (time.monotonic() - loopTime)
                        
                        if loopTime > 1:
                            loopTime = 1
                    except ZeroDivisionError:
                        chanceModifier = 1
                    loopTime = time.monotonic()
                wait = True
                
                for n in sections.uncannyMoodChance:
                    if n > 0:
                        wait = False
                
                if doWaking:
                    wait = False
                
                if wait:
                    time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)
        
        
    knockChance = 0
        
    def runKnocks():
        loopTime = time.monotonic()
        chanceModifier = 1
        while not status.exit:
            try:
                if globals.run:
                    try:
                        knockChance = 0
                        if getDateTime()[3] < 24:
                            knockChance = (getDateTime()[3] - (int(data.sunJson['cesth']))) * getDateTime()[4] * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        knockChance = (knockChance / (32 - getDateTime()[2])) * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        if random.randrange(0, int(37500 * chanceModifier)) < knockChance:
                            ghSpeaker = 5
                            while ghSpeaker == 5:
                                ghSpeaker = random.randrange(0, 10)
                            # audioEvent = audio.event()
                            speed = 0.96 + (random.random() / 12.5)
                            audioBuffer.register('h_knock_' + str(random.randrange(0, 6)) + ".mp3", ghSpeaker, 60 * ((0.3 * random.random()) + 0.7), speed, 0, 0)
                            time.sleep(5)
                            # threading.Thread(target=audioEvent.run).start()
                        sections.knockChance = knockChance
                    except:
                        print(traceback.format_exc())
                    try:
                        chanceModifier = 0.1 / (time.monotonic() - loopTime)
                        
                        if loopTime > 1:
                            loopTime = 1
                    except ZeroDivisionError:
                        loopTime = 1

                    loopTime = time.monotonic()
                if sections.knockChance <= 0:
                    time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)
        
    chainChance = 0
    
    def runChains():
        loopTime = time.monotonic()
        chanceModifier = 1
        while not status.exit:
            try:
                if globals.run:
                    try:
                        chainChance = 0
                        if getDateTime()[3] < 24:
                            chainChance = (getDateTime()[3] - (int(data.sunJson['cesth']) + 2)) * getDateTime()[4] * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        chainChance = (chainChance / (32 - getDateTime()[2])) * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        if random.randrange(0, int(37500 * chanceModifier)) < chainChance:
                            ghSpeaker = 5
                            while ghSpeaker == 5:
                                ghSpeaker = random.randrange(0, 10)
                            # audioEvent = audio.event()
                            speed = 0.96 + (random.random() / 12.5)
                            audioBuffer.register('h_chains_' + str(random.randrange(0, 3)) + ".mp3", ghSpeaker, 40 * ((0.2 * random.random()) + 0.8), speed, 0, 0)
                            time.sleep(5)
                            # threading.Thread(target=audioEvent.run).start()
                        sections.chainChance = chainChance
                    except:
                        print(traceback.format_exc())
                    time.sleep(0.1)
                    try:
                        chanceModifier = 0.1 / (time.monotonic() - loopTime)
                        
                        if loopTime > 1:
                            loopTime = 1
                    except ZeroDivisionError:
                        chanceModifier = 1
                    loopTime = time.monotonic()
                if sections.chainChance <= 0:
                    time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)
    
    bansheeChance = 0
        
    def runBanshee():
        loopTime = time.monotonic()
        chanceModifier = 1
        while not status.exit:
            try:
                if globals.run:
                    try:
                        bansheeChance = 0
                        if getDateTime()[3] > 12:
                            bansheeChance = (getDateTime()[3] - (int(data.sunJson['cesth']) + 1)) * getDateTime()[4] * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        else:
                            currentMinute = (getDateTime()[3] * 60) + getDateTime()[4]
                            bansheeChance = 195 * 2.7 ** ( - ((397 * (currentMinute - 180) ** (2)) / (1218816)))
                            if bansheeChance < 1:
                                bansheeChance = (1 - bansheeChance) * (getDateTime()[3] - (int(data.sunJson['cesth']) + 1)) * getDateTime()[4] * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        bansheeChance = (bansheeChance / (32 - getDateTime()[2])) * (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        if random.randrange(0, int(110000 * chanceModifier)) < bansheeChance:
                            # ghSpeaker = 5
                            # while ghSpeaker == 5:
                            #     ghSpeaker = random.randrange(0, 10)
                            # audioEvent = audio.event()
                            speed = 0.96 + (random.random() / 12.5)
                            aVolume = 80 * ((0.4 * random.random()) + 0.6)
                            audioBuffer.registerWindow('h_banshee_' + str(random.randrange(0, 2)) + ".mp3", [aVolume * 0.4, aVolume, aVolume * 0.7], speed, 0, 0)
                            time.sleep(5)
                            # threading.Thread(target=audioEvent.run).start()
                        sections.bansheeChance = bansheeChance
                    except:
                        print(traceback.format_exc())
                    time.sleep(0.1)
                    try:
                        chanceModifier = 0.1 / (time.monotonic() - loopTime)
                        
                        if loopTime > 1:
                            loopTime = 1
                    except ZeroDivisionError:
                        chanceModifier = 1
                    loopTime = time.monotonic()
                if sections.bansheeChance <= 0:
                    time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)
                
    uncannyBansheeChance = 0
        
    def runUncannyBanshee():
        loopTime = time.monotonic()
        chanceModifier = 1
        while not status.exit:
            try:
                if globals.runUncanny:
                    try:
                        bansheeChance = 0
                        if getDateTime()[3] < 24:
                            bansheeChance = (getDateTime()[3] - (int(data.sunJson['cesth']) + 1)) * getDateTime()[4] * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        bansheeChance = (bansheeChance / (32 - getDateTime()[2])) * (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100)
                        if random.randrange(0, int(55000 * chanceModifier)) < bansheeChance:
                            # ghSpeaker = 5
                            # while ghSpeaker == 5:
                            #     ghSpeaker = random.randrange(0, 10)
                            # audioEvent = audio.event()
                            speed = 0.96 + (random.random() / 12.5)
                            aVolume = 80 * ((0.4 * random.random()) + 0.6)
                            audioBuffer.registerWindow('hu_banshee_' + str(random.randrange(0, 2)) + ".mp3", [aVolume * 0.4, aVolume, aVolume * 0.7], speed, 0, 0)
                            time.sleep(5)
                            # threading.Thread(target=audioEvent.run).start()
                        sections.uncannyBansheeChance = bansheeChance
                    except:
                        print(traceback.format_exc())
                    time.sleep(0.1)
                    try:
                        chanceModifier = 0.1 / (time.monotonic() - loopTime)
                        
                        if loopTime > 1:
                            loopTime = 1
                    except ZeroDivisionError:
                        chanceModifier = 1
                    loopTime = time.monotonic()
                if sections.uncannyBansheeChance <= 0:
                    time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)

class forecastHandler:
    isRunning = False
    
    def run():
        
        forecastHandler.isRunning = True
        
        try:
            pytools.IO.saveJson("hallowForecastHourly.json", data.getMinutelyHallowData())
            pytools.IO.saveJson("hallowForecastBiHourly.json", data.getBiHourlyHallowData())
        except:
            print(traceback.format_exc())
        
        forecastHandler.isRunning = False

def main():
    mainVars.noA = 0
    mainVars.noB = 0
    mainVars.noC = 0
    mainVars.noD = 0
    pHorr = False
    noE = 0
    noF = 0
    noG = 0
    
    threadsRunning = False
    
    
    calcGrabber = threading.Thread(target=data.grabSunData)
    moodWakingRunner = threading.Thread(target=sections.runMoodWaking)
    
    calcGrabber.start()
    moodWakingRunner.start()
    doRun = False
    while not status.exit:
        
        doRun = globals.run
        
        try:
            data.dateArray = pytools.clock.getDateTime()
            
            doRun = (getDateTime()[1] == 10) or ((getDateTime()[1] == 11) and (getDateTime()[2] == 1) and (getDateTime()[3] < data.sunJson["csth"])) or ((data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100) > 0) or ((getDateTime()[1] == 9) and (getDateTime()[2] == 30) and (getDateTime()[3] > 11))
            
            if (getDateTime()[1] == 9) or (getDateTime()[1] == 10):
                septUncannyIndex = getDateTime()[2] + (getDateTime()[3] / 24) + (getDateTime()[4] / 24 / 60) + (getDateTime()[5] / 24 / 60 / 60)
                
                septUncannyRun = (-0.517241 * septUncannyIndex) + 0.517241
                septUncannyRun = septUncannyRun - (2.23806 ** (1.24394 * (septUncannyIndex - 27.2977)))
                
                if getDateTime()[1] != 9:
                    septUncannyRun = -1000
                
                if (os.path.exists("runningUncanny.derp")) and ((getDateTime()[1] < 11) or ((getDateTime()[1] == 11) and (getDateTime()[2] < 10))):
                    globals.runUncanny = True
                elif not ((getDateTime()[1] < 11) or ((getDateTime()[1] == 11) and (getDateTime()[2] < 10))):
                    globals.runUncanny = False
                
                if (doRun and (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) < 0)) or (((septUncannyRun < data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) < 0)) or (globals.runUncanny and (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) < -0.3))):
                    doRun = False
                    if not globals.runUncanny:
                        audio.command.setFlag("runningUncanny", True)
                    globals.runUncanny = True
                    
                elif (getDateTime()[1] == 9) and (septUncannyRun != -1000) and ((((septUncannyRun < data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) < 0)) or (globals.runUncanny and (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())) < -0.3)))):
                    globals.runUncanny = True
                    audio.command.setFlag("runningUncanny", True)
                
                else:
                    globals.runUncanny = False
                    audio.command.setFlag("runningUncanny", False)
            else:
                globals.runUncanny = False
                audio.command.setFlag("runningUncanny", False)
            
            globals.run = doRun
            
            if globals.run:
                
                data.getZ()
                
                if (getDateTime()[3] >= data.sunJson["cesth"]) or (getDateTime()[3] <= data.sunJson["csth"]):
                    if getDateTime()[2] > 19:
                        if getDateTime()[4] == 35:
                            if noE != 1:
                                if random.random() < (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100):
                                    if random.randrange(getDateTime()[3], 24) == 23:
                                        rumbleNum = random.randrange(0, 2)
                                        threading.Thread(target=audio.playSoundAll, args=('h_rumble_' + str(rumbleNum) + '.mp3', 40, 1, 0, 0,)).start()
                                    noE = 1
                        else:
                            noE = 0
                    else:
                        noE = 0
                
                    if getDateTime()[2] > 24:
                        if getDateTime()[4] == 20:
                            if noF != 1:
                                if random.random() < (data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100):
                                    if random.randrange(getDateTime()[3], 24) == 23:
                                        rumbleNum = random.randrange(0, 2)
                                        threading.Thread(target=audio.playSoundAll, args=('h_rumble_' + str(rumbleNum) + '.mp3', 40, 1, 0, 0,)).start()
                                noF = 1
                        elif getDateTime()[4] == 40:
                            if noF != 1:
                                if random.randrange(getDateTime()[3], 24) == 23:
                                    rumbleNum = random.randrange(0, 2)
                                    threading.Thread(target=audio.playSoundAll, args=('h_rumble_' + str(rumbleNum) + '.mp3', 40, 1, 0, 0,)).start()
                                noF = 1
                        else:
                            noF = 0
                    else:
                        noF = 0
                
                if getDateTime()[3] == int(data.sunJson['cesth']):
                    if getDateTime()[4] == int(data.sunJson['cestm']):
                        if noG != 1:
                            if (random.randint(getDateTime()[2], 31) == 31) or ((random.random() * 180) < data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True)):
                                threading.Thread(target=audio.playSoundWindow, args=('h_sunset.mp3;h_sunset.mp3', [40, 80], 1, 0, 0,)).start()
                            noG = 1
                    else:
                        noG = 0
                else:
                    noG = 0
            
            if globals.runUncanny:     
                if getDateTime()[2] > 19:
                    if getDateTime()[4] == 35:
                        if noE != 1:
                            if random.random() < (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100):
                                if random.randrange(getDateTime()[3], 24) == 23:
                                    rumbleNum = random.randrange(0, 2)
                                    threading.Thread(target=audio.playSoundAll, args=('hu_rumble_' + str(rumbleNum) + '.mp3', 40, 1, 0, 0,)).start()
                                noE = 1
                    else:
                        noE = 0
                else:
                    noE = 0
                
                if getDateTime()[2] > 24:
                    if getDateTime()[4] == 20:
                        if noF != 1:
                            if random.random() < (-data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True) / 100):
                                if random.randrange(getDateTime()[3], 24) == 23:
                                    rumbleNum = random.randrange(0, 2)
                                    threading.Thread(target=audio.playSoundAll, args=('hu_rumble_' + str(rumbleNum) + '.mp3', 40, 1, 0, 0,)).start()
                            noF = 1
                    elif getDateTime()[4] == 40:
                        if noF != 1:
                            if random.randrange(getDateTime()[3], 24) == 23:
                                rumbleNum = random.randrange(0, 2)
                                threading.Thread(target=audio.playSoundAll, args=('hu_rumble_' + str(rumbleNum) + '.mp3', 40, 1, 0, 0,)).start()
                            noF = 1
                    else:
                        noF = 0
                else:
                    noF = 0
                
                if getDateTime()[3] == int(data.sunJson['cesth']):
                    if getDateTime()[4] == int(data.sunJson['cestm']):
                        if noG != 1:
                            if (random.randint(getDateTime()[2], 31) == 31) or ((random.random() * 180) < -data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True)):
                                threading.Thread(target=audio.playSoundWindow, args=('hu_sunset.mp3;hu_sunset.mp3', [40, 100], 1, 0, 0,)).start()
                            noG = 1
                    else:
                        noG = 0
                else:
                    noG = 0
            
            hallowForecast = data.getHallowForecastStart(pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()), noDay=True)
            if globals.run or globals.runUncanny or (hallowForecast[1] < (pytools.clock.dateArrayToUTC(getDateTime()) + 432000)):
                try:
                    pytools.IO.saveFile("deathForecasted.derp", str(hallowForecast[0]))
                except:
                    print(traceback.format_exc())
            else:
                os.system("del deathForecasted.derp /f /q")
            
            if not forecastHandler.isRunning:
                threading.Thread(target=forecastHandler.run).start()
                
            pytools.IO.saveJson("hallowIndex.json", {
                "value": data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime())),
                "noDay": data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True),
                "noModif": data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noModif=True),
                "raw": data.getHallowIndex(pytools.clock.dateArrayToUTC(getDateTime()), noDay=True, noModif=True)
            })
            
            if globals.run or globals.runUncanny:
                
                if not threadsRunning:
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
                    bansheeRunner = threading.Thread(target=sections.runBanshee)
                    uncannyBansheeRunner = threading.Thread(target=sections.runUncannyBanshee)
                    
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
                    bansheeRunner.start()
                    uncannyBansheeRunner.start()
                    
                    threadsRunning = True
                
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
                status.vars["horrorStats"]["sections.bansheeChance"] = sections.bansheeChance
                status.vars["horrorStats"]["sections.uncannyBansheeChance"] = sections.uncannyBansheeChance
                
                if (getDateTime()[5] % 2) == 0:
                    if pHorr == False:
                        print("Current Horror Index: " + str(horrorIndex))
                        status.vars['horrorIndex'] = horrorIndex
                        saveFile('horrorindex.cx', str(horrorIndex))
                        pHorr = True
                else:
                    pHorr = False
            
            if (not globals.run) and (not globals.runUncanny):
                time.sleep(5)
                if not threadsRunning:
                    print("halloween_extension mainloop message: not_running.")
            
            status.vars['lastLoop'] = pytools.clock.getDateTime()
            status.finishedLoop = True
        except:
            print(traceback.format_exc())
            time.sleep(5)

def run():
    status.hasExited = False
    audioBuffer._start()
    print("$")
    main()
    audioBuffer._stop()
    status.hasExited = True