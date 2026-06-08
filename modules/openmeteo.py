import modules.pytools as pytools

from datetime import datetime
import meteostat
import time
import random
import numpy
import copy
import pandas

class util:
    def getDoubleDigitString(number):
        strf = str(int(number))
        if len(strf) == 1:
            strf = "0" + strf
        
        return strf
    
    averageCache = {
            "temp": {},
            "rhum": {},
            "prcp": {},
            "snwd": {},
            "wdir": {},
            "wspd": {},
            "wpgt": {},
            "pres": {},
            "tsun": {},
            "cldc": {},
            "coco": {}
        }
    
    def jsonify(d):
        """Recursively converts all numpy.uint8 values in a dictionary to int."""
        new_dict = {}
        for k, v in d.items():
            if isinstance(v, numpy.uint8):
                new_dict[k] = int(v)
            if type(v) not in (dict, list, int, float, str):
                new_dict[k] = 0
            elif isinstance(v, dict):
                new_dict[k] = util.jsonify(v) # Recurse for nested dicts
            else:
                new_dict[k] = v
        return new_dict
    
    def getAverageData(dateArray):

        averageCache = pytools.IO.getJson("averageWeatherCache.json")
        
        if type(averageCache) == int:
            if util.averageCache == {}:
                averageCache = {}
            else:
                averageCache = util.averageCache
        
        util.averageCacge = averageCache
        
        # 1. Set location (e.g., London)
        lat = 45.680597
        lon = -62.720815
        location = meteostat.Point(lat, lon)
        stations = meteostat.stations.nearby(location)

        oldCache = copy.deepcopy(util.averageCache)

        hasModified = False
        if not str([*dateArray[0:4], 0, 0]) in util.averageCache["temp"]:
            hasModified = True
            
            
            print("Grabbing data...")
            print(str([*dateArray[0:4], 0, 0]))
            
            aNewDateArray = pytools.clock.UTCToDateArray(pytools.clock.dateArrayToUTC([dateArray[0], dateArray[1] + 1, dateArray[2], dateArray[3], dateArray[4], dateArray[5]]))

            data = True
            year = dateArray[0]
            
            while (type(data) != type(None)) and (year > (dateArray[0] - 5)):
                
                

                # 2. Set time period
                start = datetime(year, dateArray[1], dateArray[2], dateArray[3])
                end = datetime(year, aNewDateArray[1], aNewDateArray[2], aNewDateArray[3])

                # 3. Get hourly data
                data = meteostat.hourly(stations, start, end)
                
                if type(data) != type(None):
                    
                    data = data.fetch()
                    
                    try:
                        for timestamp in list(data.temp.keys()):
                            stampArray = pytools.clock.utcFormatToArray(str(timestamp[1]), "- :+")
                            if str(stampArray) not in util.averageCache["temp"]:
                                util.averageCache["temp"][str(stampArray)] = {}
                            util.averageCache["temp"][str(stampArray)][str(timestamp[0])] = data.temp[timestamp[0]][timestamp[1]]
                            
                        for timestamp in list(data.rhum.keys()):
                            stampArray = pytools.clock.utcFormatToArray(str(timestamp[1]), "- :+")
                            if str(stampArray) not in util.averageCache["rhum"]:
                                util.averageCache["rhum"][str(stampArray)] = {}
                            util.averageCache["rhum"][str(stampArray)][str(timestamp[0])] = data.rhum[timestamp[0]][timestamp[1]]
                        
                        for timestamp in list(data.prcp.keys()):
                            stampArray = pytools.clock.utcFormatToArray(str(timestamp[1]), "- :+")
                            if str(stampArray) not in util.averageCache["prcp"]:
                                util.averageCache["prcp"][str(stampArray)] = {}
                            util.averageCache["prcp"][str(stampArray)][str(timestamp[0])] = data.prcp[timestamp[0]][timestamp[1]]
                        
                        for timestamp in list(data.snwd.keys()):
                            stampArray = pytools.clock.utcFormatToArray(str(timestamp[1]), "- :+")
                            if str(stampArray) not in util.averageCache["snwd"]:
                                util.averageCache["snwd"][str(stampArray)] = {}
                            util.averageCache["snwd"][str(stampArray)][str(timestamp[0])] = data.snwd[timestamp[0]][timestamp[1]]
                        
                        for timestamp in list(data.wdir.keys()):
                            stampArray = pytools.clock.utcFormatToArray(str(timestamp[1]), "- :+")
                            if str(stampArray) not in util.averageCache["wdir"]:
                                util.averageCache["wdir"][str(stampArray)] = {}
                            util.averageCache["wdir"][str(stampArray)][str(timestamp[0])] = data.wdir[timestamp[0]][timestamp[1]]
                        
                        for timestamp in list(data.wspd.keys()):
                            stampArray = pytools.clock.utcFormatToArray(str(timestamp[1]), "- :+")
                            if str(stampArray) not in util.averageCache["wspd"]:
                                util.averageCache["wspd"][str(stampArray)] = {}
                            util.averageCache["wspd"][str(stampArray)][str(timestamp[0])] = data.wspd[timestamp[0]][timestamp[1]]
                        
                        for timestamp in list(data.wpgt.keys()):
                            stampArray = pytools.clock.utcFormatToArray(str(timestamp[1]), "- :+")
                            if str(stampArray) not in util.averageCache["wpgt"]:
                                util.averageCache["wpgt"][str(stampArray)] = {}
                            util.averageCache["wpgt"][str(stampArray)][str(timestamp[0])] = data.wpgt[timestamp[0]][timestamp[1]]
                        
                        for timestamp in list(data.pres.keys()):
                            stampArray = pytools.clock.utcFormatToArray(str(timestamp[1]), "- :+")
                            if str(stampArray) not in util.averageCache["pres"]:
                                util.averageCache["pres"][str(stampArray)] = {}
                            util.averageCache["pres"][str(stampArray)][str(timestamp[0])] = data.pres[timestamp[0]][timestamp[1]]
                        
                        for timestamp in list(data.tsun.keys()):
                            stampArray = pytools.clock.utcFormatToArray(str(timestamp[1]), "- :+")
                            if str(stampArray) not in util.averageCache["tsun"]:
                                util.averageCache["tsun"][str(stampArray)] = {}
                            util.averageCache["tsun"][str(stampArray)][str(timestamp[0])] = data.tsun[timestamp[0]][timestamp[1]]
                        
                        for timestamp in list(data.cldc.keys()):
                            stampArray = pytools.clock.utcFormatToArray(str(timestamp[1]), "- :+")
                            if str(stampArray) not in util.averageCache["cldc"]:
                                util.averageCache["cldc"][str(stampArray)] = {}
                            util.averageCache["cldc"][str(stampArray)][str(timestamp[0])] = data.cldc[timestamp[0]][timestamp[1]]
                        
                        for timestamp in list(data.coco.keys()):
                            stampArray = pytools.clock.utcFormatToArray(str(timestamp[1]), "- :+")
                            if str(stampArray) not in util.averageCache["coco"]:
                                util.averageCache["coco"][str(stampArray)] = {}
                            util.averageCache["coco"][str(stampArray)][str(timestamp[0])] = data.coco[timestamp[0]][timestamp[1]]
                    except:
                        data = None
                    
                year = year - 1
        
        outArray = {}
        
        year = dateArray[0]
        while year > (dateArray[0] - 5):
            for field in util.averageCache:
                
                if field not in outArray:
                    outArray[field] = []
                
                if str([year, *dateArray[1:4], 0, 0]) in util.averageCache[field]:
                    for station in util.averageCache[field][str([year, *dateArray[1:4], 0, 0])]:
                        try:
                            outArray[field].append(float(util.averageCache[field][str([year, *dateArray[1:4], 0, 0])][station]))
                        except:
                            pass
            year = year - 1
        
        endArray = {}
        
        for field in outArray:
            try:
                endArray[field] = float(sum(outArray[field]) / len(outArray[field]))
            except:
                endArray[field] = 0
                
        if hasModified:
            while pytools.IO.getJson("averageWeatherCache.json") != util.jsonify(util.averageCache):
                print("Saving average cache...")
                pytools.IO.saveJson("averageWeatherCache.json", util.jsonify(util.averageCache))
                time.sleep(random.random())
                
        return endArray
                
        # return outArray

def getBestModel(data):
    
    dict = {
        "windPeak": "wind_gusts_10m",
        "windAvg": "wind_speed_10m",
        "temp": "temperature_2m",
        "humidity": "relative_humidity_2m",
        "direction": "wind_direction_10m",
        "pressure": "surface_pressure"
    }
    
    dateArray = pytools.clock.getDateTime()
    timeStampString = util.getDoubleDigitString(dateArray[0]) + "-" + util.getDoubleDigitString(dateArray[1]) + "-" + util.getDoubleDigitString(dateArray[2]) + "T" + util.getDoubleDigitString(dateArray[3] + (dateArray[4] / 60)) + ":00"

    checkIndex = data["hourly"]["time"].index(timeStampString)
    
    for data in data["hourly"]:
        if data["hourly"] != data["time"]:
            pass
        
def swapRowsAndColumns(data):
    
    data = data["data"]["main"]
    
    dateArray = pytools.clock.getDateTime()
    timeStampString = util.getDoubleDigitString(dateArray[0]) + "-" + util.getDoubleDigitString(dateArray[1]) + "-" + util.getDoubleDigitString(dateArray[2]) + "T" + util.getDoubleDigitString(dateArray[3] + (dateArray[4] / 60)) + ":00"
    nextTimeStampString = util.getDoubleDigitString(dateArray[0]) + "-" + util.getDoubleDigitString(dateArray[1]) + "-" + util.getDoubleDigitString(dateArray[2]) + "T" + util.getDoubleDigitString((dateArray[3] + (dateArray[4] / 60) + 1) - (24 * (int(dateArray[3] + (dateArray[4] / 60) + 1) >= 24))) + ":00"
    
    currentData = {}
    nextData = {}
    outData = {}
    for field in data["hourly"]:
        if field != "time":
            i = 0
            while i < len(data["hourly"][field]):
                
                if data["hourly"]["time"][i] not in outData:
                    outData[data["hourly"]["time"][i]] = {}
                
                outData[data["hourly"]["time"][i]][field.replace("_icon_global", "")] = data["hourly"][field][i]
                if data["hourly"]["time"][i] == timeStampString:
                    currentData[field.replace("_icon_global", "")] = data["hourly"][field][i]
                if data["hourly"]["time"][i] == nextTimeStampString:
                    nextData[field.replace("_icon_global", "")] = data["hourly"][field][i]
                    
                i = i + 1
    
    return {
        "mostRecentReading": currentData,
        "nextReading": nextData,
        "timeline": outData
    }
    
def convertToSoilData(_data):
    listf = []
    for point in sorted(list(_data["timeline"].keys())):
        listf.append(_data["timeline"][point])
        listf[-1]["time"] = pytools.clock.getUstStampFromDateArray(pytools.clock.utcFormatToArray(point + ":00"))
        
    _data["timeline"] = listf
    
    return _data
        
        
                    
            