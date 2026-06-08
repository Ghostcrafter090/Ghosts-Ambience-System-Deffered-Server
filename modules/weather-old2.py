import modules.pytools as pytools
import math
import time
import random

class globals:
    conditionCodes = {
        200: ["thunder", 0, 100, 10, 1, 50, 0],
        201: ["thunder", 0, 100, 50, 5, 75, 0],
        202: ["thunder", 0, 100, 100, 10, 100, 0],
        210: ["thunder", 0, 100, 0, 0, 25, 0],
        211: ["thunder", 0, 100, 5, 1, 50, 0],
        212: ["thunder", 0, 100, 10, 2, 75, 0],
        221: ["thunder", 50, 50, 5, 1, 15, 0],
        230: ["thunder", 0, 100, 5, 0, 25, 0],
        231: ["thunder", 0, 100, 20, 0, 50, 0],
        232: ["thunder", 0, 100, 40, 1, 100, 0],
        
        300: ["mist", 0, 100, 5, 0, 0, 0],
        301: ["mist", 0, 100, 10, 0, 0, 0],
        302: ["mist", 0, 100, 15, 0, 0, 0],
        310: ["mist", 0, 100, 7, 0, 0, 0],
        311: ["mist", 0, 100, 14, 0, 0, 0],
        312: ["mist", 0, 100, 21, 0, 0, 0],
        313: ["mist", 0, 100, 9, 0, 0, 0],
        314: ["mist", 0, 100, 18, 0, 0, 0],
        321: ["mist", 0, 100, 13, 0, 0, 0],
        
        500: ["lightrain", 0, 100, 40, 0, 0, 0],
        501: ["lightrain", 0, 100, 60, 0, 0, 0],
        502: ["lightrain", 0, 100, 80, 0, 0, 0],
        503: ["lightrain", 0, 100, 90, 0, 0, 0],
        504: ["lightrain", 0, 100, 100, 0, 0, 0],
        511: ["lightrain", 0, 100, 50, 45, 0, 5],
        520: ["lightrain", 0, 100, 30, 1, 0, 0],
        521: ["lightrain", 0, 100, 50, 2, 0, 0],
        522: ["lightrain", 0, 100, 70, 3, 0, 0],
        531: ["lightrain", 50, 50, 20, 0, 0, 0],
        
        600: ["snow", 0, 100, 0, 0, 0, 35],
        601: ["snow", 0, 100, 0, 0, 0, 65],
        602: ["snow", 0, 100, 0, 0, 0, 100],
        611: ["snow", 0, 100, 15, 5, 0, 15],
        612: ["snow", 0, 100, 5, 1, 0, 10],
        613: ["snow", 0, 100, 25, 10, 0, 35],
        615: ["snow", 0, 100, 25, 0, 0, 25],
        616: ["snow", 0, 100, 50, 0, 0, 50],
        620: ["snow", 0, 100, 0, 0, 0, 25],
        621: ["snow", 0, 100, 0, 0, 0, 50],
        622: ["snow", 0, 100, 0, 0, 0, 75],
        
        701: ["mist", 0, 100, 5, 0, 0, 0],
        711: ["clouds", 0, 100, 0, 0, 0, 0],
        721: ["clouds", 25, 75, 0, 0, 0, 0],
        731: ["clouds", 50, 50, 0, 0, 0, 0],
        741: ["clouds", 0, 100, 1, 0, 0, 0],
        751: ["clouds", 75, 25, 0, 0, 0, 0],
        761: ["clear", 85, 15, 0, 0, 0, 0],
        762: ["clear", 95, 5, 0, 0, 0, 0],
        771: ["clouds", 50, 50, 3, 0, 0, 0],
        781: ["thunder", 0, 100, 100, 100, 100, 0],
        
        800: ["clear", 100, 0, 0, 0, 0, 0],
        801: ["clouds", 75, 25, 0, 0, 0, 0],
        802: ["clouds", 50, 50, 0, 0, 0, 0],
        803: ["clouds", 25, 75, 0, 0, 0, 0],
        804: ["clouds", 0, 100, 0, 0, 0, 0]
    }
    
    lastHurricaneDataGrab = 0
    hurricaneData = {}
    forecastData = {}

class forecast:
    class tools:
        def openPointToDataSet(dataPoint):
            if "wind" in dataPoint:
                if "speed" in dataPoint["wind"]:
                    windSpeed = dataPoint["wind"]["speed"]
                else:
                    windSpeed = 0
                
                if "gust" in dataPoint["wind"]:
                    windGusts = dataPoint["wind"]["gust"]
                else:
                    windGusts = 0
                    
                if "deg" in dataPoint["wind"]:
                    windDirection = dataPoint["wind"]["deg"]
                else:
                    windDirection = 0
            else:
                windSpeed = 0
                windGusts = 0
                windDirection = 0
                    
            if ("rain" in dataPoint) and ("3h" in dataPoint["rain"]):
                rain = dataPoint["rain"]["3h"]
            else:
                rain = 0
            
            try:
                temp = float(dataPoint['main']['temp']) - 273
            except:
                temp = 0
            try:
                pressure = float(dataPoint['main']['pressure'])
            except:
                pressure = 0
            try:
                humidity = float(dataPoint['main']['humidity'])
            except:
                humidity = 0
            try:
                direction = float(dataPoint["wind"]["deg"])
            except:
                direction = 0
            try:
                gusts = float(dataPoint['wind']['gust'])
            except:
                gusts = 0
            try:
                snow = float(dataPoint['snow']['1h'])
            except:
                try:
                    snow = float(dataPoint['snow']['3h'])
                except:
                    snow = 0
            
            try:
                visibility = float(dataPoint["visibility"])
            except:
                visibility = 10000
                
            condf = 0
            weather = 'clear'
            
            actualConditions = [[0, 0, 0, 0, 0, 0], 0]
            r = 0
            while r < len(dataPoint['weather']):
                
                weather = globals.conditionCodes[dataPoint['weather'][r]['id']][0]
                if sum(globals.conditionCodes[dataPoint['weather'][r]['id']][1:]) > condf:
                    condf = sum(globals.conditionCodes[dataPoint['weather'][r]['id']][1:])
                    weather = globals.conditionCodes[dataPoint['weather'][r]['id']][0]
                
                actualConditions[0][0] = actualConditions[0][0] + globals.conditionCodes[dataPoint['weather'][r]['id']][1]
                actualConditions[0][1] = actualConditions[0][1] + globals.conditionCodes[dataPoint['weather'][r]['id']][2]
                actualConditions[0][2] = actualConditions[0][2] + globals.conditionCodes[dataPoint['weather'][r]['id']][3]
                actualConditions[0][3] = actualConditions[0][3] + globals.conditionCodes[dataPoint['weather'][r]['id']][4]
                actualConditions[0][4] = actualConditions[0][4] + globals.conditionCodes[dataPoint['weather'][r]['id']][5]
                actualConditions[0][5] = actualConditions[0][5] + globals.conditionCodes[dataPoint['weather'][r]['id']][6]
                
                actualConditions[1] = actualConditions[1] + 1
                r = r + 1
            
            actualConditions[0][0] = actualConditions[0][0] / actualConditions[1]
            actualConditions[0][1] = actualConditions[0][1] / actualConditions[1]
            actualConditions[0][2] = actualConditions[0][2] / actualConditions[1]
            actualConditions[0][3] = actualConditions[0][3] / actualConditions[1]
            actualConditions[0][4] = actualConditions[0][4] / actualConditions[1]
            actualConditions[0][5] = actualConditions[0][5] / actualConditions[1]

            try:
                i = 0
                modifier = 0
                while i < len(dataPoint['weather']):
                    modifier = modifier + (float(dataPoint['weather'][i]['id']) % 100)
                    i = i + 1
            except:
                modifier = 0
            
            return [[windSpeed * 1.4711018711018712, windGusts * 1.4711018711018712, visibility, snow, weather, modifier, pressure, temp, humidity, direction, 0, actualConditions], [rain * 2, rain * 10, pressure, temp, humidity, 0], [temp, humidity, pressure, rain, windSpeed, windGusts, True], "", [], [], [], [], [], [0, 0, 0, 0], pytools.clock.utcFormatToArray(dataPoint["dt_txt"], seperators="- :+")]
        
        def parse(location=""):
            try:
                if location == "":
                    forecastData = pytools.IO.getJson("forecastData.json")["data"]["main"]
                else:
                    forecastData = pytools.IO.getJson(location + "ForecastData.json")["data"]["main"]
                forecastList = [pytools.IO.getList("dataList.pyl")[1]]
                try:
                    forecastList[0].append(pytools.clock.getDateTime())
                except:
                    forecastList = [[[0, 0, 10000, 0, "clear", 0, 1000, 15, 50, 0, 0, [0, 0, 0, 0, 0, 0]], [0, 0, 1000, 15, 50, 0], [15, 50, 1000, 0, 0, 0, True], "", [], [], [], [], [], [0, 0, 0, 0], pytools.clock.getDateTime()]]
                for dataPoint in forecastData["list"]:
                    
                    ambDataPoint = forecast.tools.openPointToDataSet(dataPoint)
                    forecastList.append(ambDataPoint)
            except:
                forecastList = [[[0, 0, 10000, 0, "clear", 0, 1000, 15, 50, 0, 0, [0, 0, 0, 0, 0, 0]], [0, 0, 1000, 15, 50, 0], [15, 50, 1000, 0, 0, 0, True], "", [], [], [], [], [], [0, 0, 0, 0], pytools.clock.getDateTime()]]
            return forecastList
        
    def getForecastAtTime(dateArray, location=""):
        timeStamp = pytools.clock.dateArrayToUTC(dateArray)
        
        forecastSet = forecast.tools.parse(location=location)
        
        afterData = False
        beforeData = False
        i = 0
        while i < len(forecastSet):
            isBeforeNext = False
            isAfterPrevious = False
            if i < (len(forecastSet) - 1):
                if pytools.clock.dateArrayToUTC(forecastSet[i + 1][-1]) >= timeStamp:
                    isBeforeNext = True
            if pytools.clock.dateArrayToUTC(forecastSet[i][-1]) <= timeStamp:
                isAfterPrevious = True
            
            if isBeforeNext:
                afterData = forecastSet[i + 1]
            
            if isAfterPrevious:
                beforeData = forecastSet[i]
            
            if isAfterPrevious and isBeforeNext:
                i = len(forecastSet)
        
            i = i + 1
        
        def _len(_item):
            try:
                return len(_item)
            except:
                return False
        
        print("2: " + str(list(map(_len, beforeData))[0:2] == list(map(_len, afterData))[0:2]))
        print("1: " + str(((type(afterData) == list) and (type(beforeData) == list))))
        print("3: " + str(list(map(_len, beforeData))[-2:] == list(map(_len, afterData))[-2:]))
        
        print("afterData: " + str(list(map(_len, afterData))[0:2]))
        print("beforeData: " + str(list(map(_len, beforeData))[0:2]))
        
        if ((type(afterData) == list) and (type(beforeData) == list)) and (list(map(_len, beforeData))[0:2] == list(map(_len, afterData))[0:2]) and (list(map(_len, beforeData))[-2:] == list(map(_len, afterData))[-2:]):
            oldTimeStamp = pytools.clock.dateArrayToUTC(beforeData[-1])
            newTimeStamp = pytools.clock.dateArrayToUTC(afterData[-1])
            
            timeDistance = newTimeStamp - oldTimeStamp
            percentAfter = (timeStamp - oldTimeStamp) / timeDistance
            percentBefore = 1 - percentAfter
            
            def _parseList(beforeList, afterList):
                i = 0
                outList = beforeList
                if len(beforeList) == len(afterList):
                    while i < len(beforeList):
                        if (type(beforeList[i]) == type(afterList[i])) and ((type(beforeList[i]) == float) or (type(beforeList[i]) == int)):
                            outList[i] = (percentBefore * float(beforeList[i])) + (percentAfter * float(afterList[i]))
                        elif (type(beforeList[i]) == type(afterList[i])) and (type(beforeList[i]) == list):
                            outList[i] = _parseList(beforeList[i], afterList[i])
                        i = i + 1

                return outList

            return _parseList(beforeData, afterData)
                
        else:
            print("ficl")
            return False
            
    def getHurricaneData(getClosest=False, isInForecast=True):
        contenders = []
        try:
            
            if (globals.lastHurricaneDataGrab + 240) < time.time():
                globals.hurricaneData = pytools.net.getJsonAPI("https://api.weather.com/v2/tropical/currentposition?apiKey=e1f10a1e78da46f5b10a1e78da96f525&source=default&basin=all&language=en-US&units=m&nautical=true&format=json")
                globals.forecastData = pytools.net.getJsonAPI("https://api.weather.com/v2/tropical/projectedpath?apiKey=e1f10a1e78da46f5b10a1e78da96f525&source=default&basin=all&language=en-US&units=m&nautical=true&format=json")
                globals.lastHurricaneDataGrab = time.time()
            
            hurricaneData = globals.hurricaneData
            forecastData = globals.forecastData
            for hurricane in hurricaneData["advisoryinfo"]:
                added = False
                if (38 < hurricane["currentposition"]["lat"] < 50) or getClosest:
                    if (-72 < hurricane["currentposition"]["lon"] < -53) or getClosest:
                        contenders.append([hurricane["storm_name"], hurricane["issue_dt_tm"], ((hurricane["currentposition"]["wind_gust"]) / 3600) * 1000, hurricane, False])
                        added = True
                
                if isInForecast:
                    if not added:
                        for hurricaneForecast in forecastData["advisoryinfo"]:
                            if hurricaneForecast["storm_name"] == hurricane["storm_name"]:
                                for pathObject in hurricaneForecast["projectedpath"]:
                                    if ((pathObject["wind_gust"] / 3600) * 1000) > 19.5:
                                        if (42 < pathObject["latitude"] < 48):
                                            if (-69 < pathObject["longitude"] < -57):
                                                if not added:
                                                    contenders.append([hurricane["storm_name"], hurricane["issue_dt_tm"], ((hurricane["currentposition"]["wind_gust"]) / 3600) * 1000, hurricane, True])
                                                    added = True
        except:
            pass
        
        try:
            hurrList = []
            for hurricane in contenders:
                dateArrayIssue = [int(hurricane[1].split("T")[0].split("-")[0]), int(hurricane[1].split("T")[0].split("-")[1]), int(hurricane[1].split("T")[0].split("-")[2]), 0, 0, 0]
                dateUTCIssue = pytools.clock.dateArrayToUTC(dateArrayIssue)
                if (dateUTCIssue + 129600) >= pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                    if hurricane[2] > 19.5:
                        hurrList.append([hurricane[0], hurricane[2], hurricane[3], hurricane[4]])
        except:
            pass
        
        hurricaneName = False
        
        if not getClosest:
            try:
                
                def sortHurricanesKey(n):
                    return n[1]
                
                sortedHurricanes = sorted(hurrList, key=sortHurricanesKey, reverse=True)
                
                hurricaneName = sortedHurricanes[0]
            except:
                pass
        else:
            try:
                
                def getDistance(x, y, radius=0, randomRadius=False):
                    
                    locationData = pytools.IO.getJson("location.json")["coords"]
                    
                    x = (x - locationData[0]) * 111.1
                    y = (y * (111.320 * math.cos(x))) - (locationData[1] * (111.320 * math.cos(locationData[0])))
                    
                    if randomRadius:
                        dis = (((math.fabs(x) ** 2) + (math.fabs(y) ** 2)) ** 0.5) - (radius - ((radius * 2) * random.random()))
                    else:
                        dis =  (((math.fabs(x) ** 2) + (math.fabs(y) ** 2)) ** 0.5) - radius
                    
                    if dis < 0.0001:
                        dis = 0.0001
                    
                    return dis
                
                def sortHurricanesKey(n):
                    
                    try:
                        nesw = n[2]["currentposition"]["wind_radii"]["NE"] + n[2]["currentposition"]["wind_radii"]["SW"]
                        nwse = n[2]["currentposition"]["wind_radii"]["NW"] + n[2]["currentposition"]["wind_radii"]["SE"]
                    
                        if nesw > nwse:
                            radius = nesw * 7
                        else:
                            radius = nwse * 7
                    
                    except:
                        radius = 0
                    
                    return getDistance(n[2]["currentposition"]["lat"], n[2]["currentposition"]["lon"], radius=radius)
                
                sortedHurricanes = sorted(hurrList, key=sortHurricanesKey)
                
                hurricaneName = sortedHurricanes[0]
            except:
                pass
        
        return hurricaneName            
                
                