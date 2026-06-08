from concurrent.futures import thread

import modules.pytools as pytools
import traceback
import time
import os
import threading
import random

class globals:
    lastGrab = -1
    lastValue = 0
    threadCounter = 0
    lastYearGrab = {}
    smoothedValue = 0
    
try:
    globals.lastYearGrab = pytools.IO.getJson(".\\working\\deathStatistics.json")["data"]
except:
    print(traceback.format_exc())
    
try:
    globals.smoothedValue = pytools.IO.getJson(".\\working\\deathRate.json")["average"]
except:
    print(traceback.format_exc())

# Grabs hourly death rate according to find a grave
def getCurrentDeathRate():
    if globals.lastGrab != pytools.clock.getDateTime()[4]:
        print("Grabbing new deathrate value...")
        try:
            numberStr = pytools.net.getTextAPI("https://www.findagrave.com/memorial/search?fulltext=&firstname=&middlename=&lastname=&birthyear=&birthyearfilter=&deathyear=" + str(pytools.clock.getDateTime()[0]) + "&deathyearfilter=&location=&locationId=&bio=&linkedToName=&plot=&memorialid=&mcid=&datefilter=1&orderby=d-&page=1#sr-300312131").split(" matching records")[0].split(" ")[-1]
            aNumber = ""
            for char in numberStr:
                if char in "0123456789-.":
                    aNumber = aNumber + char
            
            globals.lastGrab = pytools.clock.getDateTime()[4]
            globals.lastValue = float(aNumber) / 24
            
            try:
                globals.smoothedValue = pytools.IO.getJson(".\\deathRate.json")["average"]
            except:
                print(traceback.format_exc())
            if globals.lastValue > globals.smoothedValue:
                globals.smoothedValue = ((globals.smoothedValue * 180) + globals.lastValue) / 181
                
            else:
                globals.smoothedValue = ((globals.smoothedValue * 720) + globals.lastValue) / 721
            pytools.IO.saveJson(".\\deathRate.json", {
                "average": globals.smoothedValue
            })
            
        except:
            print(traceback.format_exc())
    
    return globals.smoothedValue

def getYearlyDeathsPerHour(year, doWait=False):
    if str(year) not in globals.lastYearGrab:
        globals.lastYearGrab[str(year)] = {
            "lastDay": -1,
            "lastValue": 0
        }
    
    if ((globals.lastYearGrab[str(year)]["lastDay"] != pytools.clock.getDateTime()[2]) and (pytools.clock.getDateTime()[3] > 1)) or (globals.lastYearGrab[str(year)]["lastValue"] == 0):
        try:
            def do(year):
                time.sleep(random.random() * 2)
                
                while globals.threadCounter > 1:
                    time.sleep(5)
                    
                globals.threadCounter = globals.threadCounter + 1
                
                try:
                    print("Grabbing new average deathrate value for year " + str(year) + "...")
                    
                    numberStr = pytools.net.getTextAPI("https://www.findagrave.com/memorial/search?fulltext=&firstname=&middlename=&lastname=&birthyear=&birthyearfilter=&deathyear=" + str(year) + "&deathyearfilter=&location=&locationId=&bio=&linkedToName=&plot=&memorialid=&mcid=&datefilter=&orderby=d-&page=1#sr-300312131").split(" matching records")[0].split(" ")[-1]
                    aNumber = ""
                    for char in numberStr:
                        if char in "0123456789-.":
                            aNumber = aNumber + char
                    
                    globals.lastYearGrab[str(year)]["lastValue"] = float(aNumber) / ((365 + ((year % 4) == 0)) * 24)
                    
                    if os.path.exists(".\\working"):
                        pytools.IO.saveJson(".\\working\\deathStatistics.json", {
                            "data": globals.lastYearGrab
                        })
                    else:
                        pytools.IO.saveJson(".\\deathStatistics.json", {
                            "data": globals.lastYearGrab
                        })
                except:
                    print(traceback.format_exc())
                
                globals.threadCounter = globals.threadCounter - 1
            
            
            while globals.threadCounter >= 10:
                time.sleep(1)
            
            threading.Thread(target=do, args=(year,)).start()
            globals.lastYearGrab[str(year)]["lastDay"] = pytools.clock.getDateTime()[2]
            
        except:
            print(traceback.format_exc())
        
    return globals.lastYearGrab[str(year)]["lastValue"]

def getMinDeathsPerYear(verbose=False):
    
    year = pytools.clock.getDateTime()[0] - 5
    minDeathRate = [1000000000000000000, year]
    while year >= 1900:
        deathRate = getYearlyDeathsPerHour(year, doWait=True)
        if verbose:
            print("year: " + str(year) + ", rate: " + str(round(deathRate, 4)))
        if (deathRate < minDeathRate[0]) and (round(deathRate, 4) != 0):
            minDeathRate = [deathRate, year]
        
        year = year - 1
        
    return minDeathRate

def getMaxDeathsPerYear(verbose=False):
    year = pytools.clock.getDateTime()[0] - 5
    maxDeathRate = [0, year]
    while year >= 1900:
        deathRate = getYearlyDeathsPerHour(year, doWait=True)
        if verbose:
            print("year: " + str(year) + ", rate: " + str(round(deathRate, 4)))
        if (deathRate > maxDeathRate[0]) and (round(deathRate, 4) != 0):
            maxDeathRate = [deathRate, year]
        
        year = year - 1
        
    return maxDeathRate

def getCurrentDeathIndex():
    minRate = getMinDeathsPerYear()
    maxRate = getMaxDeathsPerYear()
    
    currRate = getCurrentDeathRate()
    
    return (currRate - minRate[0]) / (maxRate[0] - minRate[0])