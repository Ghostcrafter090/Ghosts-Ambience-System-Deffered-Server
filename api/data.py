import modules.audio as audio
import modules.pytools as pytools
import time
import traceback
import math
import modules.logManager as log
import geopy.distance

import websocket
import threading
import json
import os
import sys

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
    lat = 0
    lon = 0
    urlBase = 'http://gsweathermore.ddns.net:226/access.php?grabopenspec=true&lat=<lat>&lon=<lon>&key='
    urlBaseNorth = 'http://gsweathermore.ddns.net:226/access.php?grabopennorth=true&lat=<lat>&lon=<lon>&key='
    urlBaseSouth = 'http://gsweathermore.ddns.net:226/access.php?grabopensouth=true&lat=<lat>&lon=<lon>&key='
    urlBaseEast = 'http://gsweathermore.ddns.net:226/access.php?grabopeneast=true&lat=<lat>&lon=<lon>&key='
    urlBaseWest = 'http://gsweathermore.ddns.net:226/access.php?grabopenwest=true&lat=<lat>&lon=<lon>&key='
    
    doManual = False
    
    urlFast = 'http://gsweathermore.ddns.net:226/access.php?key=56c15c7d00df42d8815c7d00df42d8ab'
    urlSuperFast = 'http://gsweathermore.ddns.net:226/currentdata.json'
    urlPrecip = "http://gsweathermore.ddns.net:226/access.php?key=makeitrain&grabrain=true"
    dataBaseOld = [0.0, 0.0, 15000, 0.0, 'clear', 0, 1000.0, 15.0, 50.0, 0, 0]
    dataFastOld = [0, 0, 1000.0, 15, 50, 0]
    dataSuperOld = [15, 50, 1000.0, 0, 0, 0]
    dataPrecipOld = {"data": {"main": {"particles": {"avgCount": 0.00, "currentCount": 0, "speed": 1053.7, "speedMax": 1084, "particleSpeedMin": 580}, "precipitation": {"type": {"snow": 0.0, "rain": 0.0, "hail": 0.0}, "intensity": 0.01}, "avgSensorReading": 337.81, "loopTic": 204.03, "sensorCalibratedTo": 337.44}}, "grabbed": "yes"}

def doManual(baseData):
    baseData[7] = baseData[7] + 20
    if baseData[4] == "snow":
        baseData[4] = "rain"
    return baseData

class grabber:
    def getBaseData(url):
        url = url.replace("<lat>", str(globals.lat)).replace("<lon>", str(globals.lon))
        urlNorth = globals.urlBaseNorth.replace("<lat>", str(globals.lat)).replace("<lon>", str(globals.lon))
        urlSouth = globals.urlBaseSouth.replace("<lat>", str(globals.lat)).replace("<lon>", str(globals.lon))
        urlEast = globals.urlBaseEast.replace("<lat>", str(globals.lat)).replace("<lon>", str(globals.lon))
        urlWest = globals.urlBaseWest.replace("<lat>", str(globals.lat)).replace("<lon>", str(globals.lon))
        
        try:
            print(str(pytools.clock.getDateTime()) + ' ::: Getting Base Data...')
            # url: http://api.openweathermap.org/data/2.5/weather?lat=44.7659964&lon=-63.6850686&appid=<apiKey>
            # try:
            data = pytools.net.getJsonAPI(url + status.apiKey)["data"]["main"]
            
            try:
                dataNorth = pytools.net.getJsonAPI(urlNorth + status.apiKey)["data"]["main"]
                dataSouth = pytools.net.getJsonAPI(urlSouth + status.apiKey)["data"]["main"]
                dataEast = pytools.net.getJsonAPI(urlEast + status.apiKey)["data"]["main"]
                dataWest = pytools.net.getJsonAPI(urlWest + status.apiKey)["data"]["main"]
                tempMiddle = data["main"]["temp"]
                tempNorth = dataNorth["main"]["temp"]
                tempSouth = dataSouth["main"]["temp"]
                tempEast = dataEast["main"]["temp"]
                tempWest = dataWest["main"]["temp"]
                
                cape = math.fabs(111 * (tempMiddle - tempNorth)) + math.fabs(111 * (tempMiddle - tempSouth)) + math.fabs(111 * (tempMiddle - tempEast)) + math.fabs(111 * (tempMiddle - tempWest))
            except:
                print(traceback.format_exc())
                cape = 0
            
            print("capeIndex: " + str(cape))
                
            # except:
            #     data = globals.dataBaseOld
            globals.dataBaseOld = data
            # [windspeeds, windgusts, visibility, snow, weather, modifier]
            r = 0
            print(data)
            condf = 0
            weather = 'clear'
            while r < len(data['weather']):
                print(data['weather'][r]['main'] )
                try:
                    print(data['weather'][r])
                    if data['weather'][r]['main'] == "Thunderstorm":
                        weather = 'thunder'
                        condf = 6
                    elif (data['weather'][r]['main'] == "Snow") and (condf < 5):
                        weather = 'snow'
                        condf = 5
                    elif (data['weather'][r]['main'] == "Rain") and (condf < 4):
                        weather = 'rain'
                        condf = 4
                    elif (data['weather'][r]['main'] == "Drizzle") and (condf < 3):
                        weather = 'lightrain'
                        condf = 3
                    elif (data['weather'][r]['main'] == "Mist") and (condf < 2):
                        weather = 'mist'
                        condf = 2
                    elif (data['weather'][r]['main'] == "Clouds") and (condf < 1):
                        weather = 'clouds'
                        condf = 1
                    elif (float(data['weather'][r]['id']) == 500.0) and (condf < 3):
                        weather = 'lightrain'
                        condf = 3
                except:
                    print("fuck")
                r = r + 1
            
            try:
                if grabber.lightning.currentDangerLevel > 4:
                    weather = "thunder"
            except:
                pass

            try:
                i = 0
                modifier = 0
                while i < len(data['weather']):
                    modifier = modifier + (float(data['weather'][i]['id']) % 100)
                    i = i + 1
            except:
                modifier = 0
            
            try:
                speed = float(data['wind']['speed'])
            except:
                speed = 0
            try:
                temp = float(data['main']['temp']) - 273
            except:
                temp = 0
            try:
                pressure = float(data['main']['pressure'])
            except:
                pressure = 0
            try:
                humidity = float(data['main']['humidity'])
            except:
                humidity = 0
            try:
                direction = float(data["wind"]["deg"])
            except:
                direction = 0
            try:
                gusts = float(data['wind']['gust'])
            except:
                gusts = 0
            try:
                snow = float(data['snow']['1h'])
            except:
                try:
                    snow = float(data['snow']['3h'])
                except:
                    snow = 0
            array = [speed, gusts, float(data['visibility']), snow, weather, modifier, pressure, temp, humidity, direction, cape]
            print(array)
            return array
        except:
            print(traceback.format_exc())
            return [0.0, 0.0, 15000, 0.0, 'clear', 0, 1000.0, 15.0, 50.0, 0, 0]

    def getFastData(url):
        try:
            print(str(pytools.clock.getDateTime()) + ' ::: Getting Fast Data...')
            # url: https://api.weather.com/v2/pws/observations/current?stationId=INOVASCO146&format=json&units=s&apiKey=<apiKey>
            try:
                data = pytools.net.getJsonAPI(url)['data']
            except:
                data = globals.dataFastOld
            globals.dataFastOld = data
            # [rainRate, rainTotal, pressure, temp, humidity, lightningDanger]
            rainRate = data['main']['observations'][0]['metric_si']['precipRate']
            rainTotal = data['main']['observations'][0]['metric_si']['precipTotal']
            pressure = data['main']['observations'][0]['metric_si']['pressure']
            temp = data['main']['observations'][0]['metric_si']['temp']
            humidity = data['main']['observations'][0]['humidity']
            lightning = data['lightning_danger']
            array = [float(rainRate) * 2, float(rainTotal) * 10, float(pressure), float(temp), float(humidity), int(lightning)]
            print(array)
            return array
        except:
            return False

    def getSuperFastData(url):
        try:
            data = pytools.net.getJsonAPI(url)
            out = True
        except:
            data = globals.dataSuperOld
            out = False
        globals.dataSuperOld = data
        try:
            rainRate = float(data['rainHour'])
        except:
            rainRate = 0.0
        try:
            windGusts = float(data['windPeak'])
        except:
            windGusts = 0.0
        try:
            windSpeeds = float(data['windAvg'])
        except:
            windSpeeds = 0.0
        try:
            temp = float(data['temp'])
        except:
            temp = 0.0
        try:
            humidity = float(data['humidity'])
        except:
            humidity = 0.0
        try:
            pressure = float(data['rainHour'])
        except:
            pressure = 0.0
        return [temp, humidity, pressure, rainRate, windSpeeds, windGusts, out]

    def getPrecipData(url):
        try:
            data = pytools.net.getJsonAPI(url)
        except:
            data = globals.dataPrecipOld
        try:
            snow = data["data"]["main"]["precipitation"]["type"]["snow"]
        except:
            snow = 0.0
        try:
            rain = data["data"]["main"]["precipitation"]["type"]["rain"]
        except:
            rain = 0.0
        try:
            hail = data["data"]["main"]["precipitation"]["type"]["hail"]
        except:
            hail = 0.0     
        try:
            lightLevel = data["data"]["main"]["sensorReadings"]["laserOffAmbientReading"]
        except:
            lightLevel = 0
        precipDataOld = data
        return [snow, rain, hail, lightLevel]
    
    class lightning:
        
        closestStrike = {
            "lat": 0,
            "lon": 0,
            "time": 0
        }
        
        lastUpdate = [1, 1, 1, 0, 0, 0]
        
        currentDangerLevel = 0
        
        def getDistance(x, y):
            coords_1 = (x, y)
            coords_2 = (globals.lat, globals.lon)

            return geopy.distance.geodesic(coords_1, coords_2).km
        
        def getDangerLevel(distance):
            return 6 - (distance / 10)
        
            # tests
            if distance < 10:
                return 5
            elif distance < 20:
                return 4
            elif distance < 30:
                return 3
            elif distance < 40:
                return 2
            elif distance < 50:
                return 1
            else:
                return 0
        
        def on_message(wsapp, message):
            messagea = '{"v":24,"i":{},"s":false,"x":0,"w":0,"tx":0,"tw":1,"a":6,"z":6,"b":true,"h":"","l":1,"t":1,"from_lightningmaps_org":true,"p":[51.7,-54.8,38.1,-73.1],"r":"A"}'
            messageJson = json.loads(message)
            if messageJson["time"]:
                if len(messageJson) == 1:
                    wsapp.send(messagea)
                    globals.sysTmf = [messageJson["time"], time.time()]
                    pytools.IO.saveJson(".\\webSocketTimeDelay.json", {
                        "times": globals.sysTmf
                    })
                else:
                    try:
                        if messageJson["strokes"]:
                            dateArray = pytools.clock.getDateTime()
                            datef = str(dateArray[0]) + "-" + str(dateArray[1]) + "-" + str(dateArray[2])
                            timef = str(dateArray[3]) + "." + str(dateArray[4]) + "." + str(dateArray[5])
                            if not os.path.exists(".\\blitzData\\" + datef):
                                os.system("mkdir \".\\blitzData\\" + datef + "\"")
                            if os.path.exists(".\\blitzData\\" + datef + "\\strike_" + timef + ".wstrike"):
                                jsonf = pytools.IO.getJson(".\\blitzData\\" + datef + "\\strike_" + timef + ".wstrike")
                            else:
                                jsonf = {}
                            messageTime = messageJson["time"]
                            messageJson.pop("time")
                            messageJson["sysTmf"] = globals.sysTmf
                            for strike in messageJson["strokes"]:
                                print("Lightning Strike: " + str({
                                        "lat": strike["lat"],
                                        "lon": strike["lon"],
                                        "time": strike["time"],
                                        "distance": grabber.lightning.getDistance(strike["lat"], strike["lon"])
                                    }))
                                if (grabber.lightning.getDistance(strike["lat"], strike["lon"]) < grabber.lightning.getDistance(grabber.lightning.closestStrike["lat"], grabber.lightning.closestStrike["lon"])) or ((time.time() * 1000) > (grabber.lightning.closestStrike["time"] + 600000)):
                                    grabber.lightning.closestStrike = {
                                        "lat": strike["lat"],
                                        "lon": strike["lon"],
                                        "time": time.time() * 1000
                                    }
                                    grabber.lightning.currentDangerLevel = grabber.lightning.getDangerLevel(grabber.lightning.getDistance(strike["lat"], strike["lon"]))
                                    print("Setting Lightning Danger: " + str(grabber.lightning.getDangerLevel(grabber.lightning.getDistance(strike["lat"], strike["lon"]))))
                                    pytools.IO.saveJson(".\\lightningData.json", {
                                        "dangerLevel": grabber.lightning.getDangerLevel(grabber.lightning.getDistance(strike["lat"], strike["lon"]))
                                    })
                    except:
                        print(traceback.format_exc())
            try:
                if (pytools.clock.dateArrayToUTC(grabber.lightning.lastUpdate) + 300) < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                    wsapp.close()
            except:
                wsapp.close()
                        
        def run():
            while not status.exit:
                try:
                    print("Websocket reset detected. Reconnecting...")
                    grabber.lightning.lastUpdate = pytools.clock.getDateTime()
                    wsapp = websocket.WebSocketApp("wss://live2.lightningmaps.org/", on_message=grabber.lightning.on_message)
                    wsapp.run_forever()
                except:
                    print(traceback.format_exc())
                time.sleep(1)
        
class bulk:
    def getData(oldBool: bool, oldData, bypass):
        dateArray = pytools.clock.getDateTime()
        if bypass:
            baseData = grabber.getBaseData(globals.urlBase)
            if globals.doManual:
                baseData = doManual(baseData)
            baseDataf = [baseData[0], baseData[1]]
            fastData = grabber.getFastData(globals.urlFast)
            superData = grabber.getSuperFastData(globals.urlSuperFast)
            precipData = grabber.getPrecipData(globals.urlPrecip)
            dateNewBase = dateArray[4]
            dateNewFast = dateArray[4]
            dateNewSuper = dateArray[5]
            dateNewPrecip = dateArray[5]
        else:
            baseData = oldData[0]
            baseDataf = oldData[7]
            fastData = oldData[1]
            superData = oldData[2]
            dateNewBase = oldData[4]
            dateNewFast = oldData[5]
            dateNewSuper = oldData[6]
            dateNewPrecip = oldData[8]
            precipData = oldData[9]
            if (dateArray[4] % 3) == 0:
                if oldData[4] != dateArray[4]:
                    dateNewBase = dateArray[4]
                    baseData = grabber.getBaseData(globals.urlBase)
                    if globals.doManual:
                        baseData = doManual(baseData)
                    baseDataf[0] = baseData[0]
                    baseDataf[1] = baseData[1]
            if (dateArray[4] % 1) == 0:
                if oldData[5] != dateArray[4]:
                    dateNewFast = dateArray[4]
                    fastData = grabber.getFastData(globals.urlFast)
            if (dateArray[5] % 20) == 0:
                if oldData[6] != dateArray[5]:
                    dateNewSuper = dateArray[5]
                    superData = grabber.getSuperFastData(globals.urlSuperFast)
            if (dateArray[5] % 15) == 0:
                if oldData[8] != dateArray[5]:
                    dateNewPrecip = dateArray[5]
                    precipData = grabber.getPrecipData(globals.urlPrecip)
        try:
            if superData[6]:
                baseData[6] = superData[2]
                baseData[7] = superData[0]
                baseData[8] = superData[1]
                baseData[0] = superData[4]
            else:
                if baseData[7] > superData[0]:
                    baseData[7] = superData[0]
                    if globals.doManual:
                        baseData = doManual(baseData)
                elif math.fabs(baseData[7] - superData[0]) > 5:
                    baseData[7] = superData[0]
                    if globals.doManual:
                        baseData = doManual(baseData)
                if baseDataf[0] < superData[4]:
                    baseData[0] = superData[4]
            if baseDataf[1] < superData[5]:
                baseData[1] = superData[5]
            if fastData == False:
                fastData = [0, 0, baseData[6], baseData[7], baseData[8], 0]      
                
            pIf = 0
            while pIf < len(precipData):
                if precipData[pIf] < 0:
                    precipData[pIf] = 0
                pIf = pIf + 1
                
            if precipData[0] > 0:
                h = baseData[8]
                t = baseData[7]
                w = t * math.atan(0.151977 * (h + 8.313659) ** (((1) / (2)))) + math.atan(t + h) - math.atan(h * 1.676331) + 0.00391838 * (h) ** (((3) / (2))) * math.atan(0.023101 * h) - 4.686035
                if w < 0:
                    baseData[4] = "snow"
                else:
                    if (precipData[0] + precipData[1] + precipData[2]) > 0.06:
                        baseData[4] = "rain"
                    elif (precipData[0] + precipData[1] + precipData[2]) > 0.03:
                        baseData[4] = "lightrain"
                    elif (precipData[0] + precipData[1] + precipData[2]) > 0:
                        baseData[4] = "mist"
            elif (precipData[0] + precipData[1] + precipData[2]) > 0.06:
                baseData[4] = "rain"
            elif (precipData[0] + precipData[1] + precipData[2]) > 0.03:
                baseData[4] = "lightrain"
            elif (precipData[0] + precipData[1] + precipData[2]) > 0:
                baseData[4] = "mist"
            if precipData[2] > 0.25:
                baseData[4] = "rain"
            if precipData[3] > 700:
                baseData[4] = "clear"
            elif precipData[3] > 600:
                baseData[4] = "clouds"
        except:
            pass

        outString = """set temp=""" + str(superData[0] + 273).split('.')[0] + """
    set tempc=""" + str(superData[0]).split('.')[0] + """
    set windspeed=""" + str(baseData[0]).split('.')[0] + """
    set windgust=""" + str(baseData[1]).split('.')[0] + """
    set pressure=""" + str(superData[2]).split('.')[0] + """
    set humidity=""" + str(superData[1]).split('.')[0] + """
    set weather=""" + str(baseData[4]).split('.')[0] + """
    set modifier=""" + str(baseData[5]).split('.')[0]
        dispString = """Temperature (C)      : """ + str(baseData[7]) + """C
Wind Speeds (m/s)    : """ + str(baseData[0]) + """m/s
Wind Gusts  (m/s)    : """ + str(baseData[1]) + """m/s
Pressure    (hPa)    : """ + str(superData[2]) + """hPa
Humidity    (%)      : """ + str(superData[1]) + """%
Condition   (type)   : """ + str(baseData[4]) + """
Date        (YY-M-D) : """ + str(dateArray[0]) + "-" + str(dateArray[1]) + "-" + str(dateArray[2]) + """
Time        (hh:mm)  : """ + str(dateArray[3]) + ":" + str(dateArray[4])
        pytools.IO.saveFile("..\\vars\\dispstring.cx", dispString)
        pytools.IO.saveJson("..\\vars\\data.json", {
            "data": [baseData, fastData, outString, dateNewBase, dateNewFast],
            "dateArray": dateArray
        })
        if oldBool == 1:
            pytools.IO.saveFile('cond.cmd', outString)
        return [baseData, fastData, superData, outString, dateNewBase, dateNewFast, dateNewSuper, baseDataf, dateNewPrecip, precipData]

def setCoords():
    globals.lat = pytools.IO.getJson("location.json")["coords"][0]
    globals.lon = pytools.IO.getJson("location.json")["coords"][1]

def main():
    setCoords()
    
    lightningThread = threading.Thread(target=grabber.lightning.run)
    lightningThread.start()
    
    if status.apiKey == "":
        status.apiKey = pytools.IO.getJson("access.key")["openweathermap"]
    data = bulk.getData(1, [], True)
    while not status.exit:
        data = bulk.getData(1, data, False)
        print(str(pytools.clock.getDateTime()) + ' ::: ' + str(data))
        time.sleep(0.5)
        if (pytools.clock.getDateTime()[5] % 20) == 0:
            pytools.IO.saveList("dataList.pyl", data)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True


def run():
    status.hasExited = False
    main()
    status.hasExited = True
