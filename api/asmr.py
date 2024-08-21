import modules.pytools as pytools
import modules.logManager as log
import modules.audio as audio

import time
import random
import os

import api.wind as wind

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
    
class tools:
    def dayTimesGrabber():
            dayTimes = pytools.IO.getList('daytimes.pyl')[1]
            if dayTimes == 1:
                dayTimes = [[2022, 5, 11, 3, 45, 15], [2022, 5, 11, 4, 34, 10], [2022, 5, 11, 5, 16, 33], [2022, 5, 11, 5, 48, 29], [2022, 5, 11, 13, 10, 47], [2022, 5, 11, 20, 33, 6], [2022, 5, 11, 21, 5, 2], [2022, 5, 11, 21, 47, 25], [2022, 5, 11, 22, 36, 20]]
            return dayTimes
    
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, "", 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out

class candles:
    
    candlesAreRunning = False
    
    lastFireplaceLoop = -1
    lastWindowLoop = -1
    lastGenericLoop = -1
    
    windowFailCounter = 0
    
    fireplaceWaxRemaining = 8
    windowWaxRemaining = 8
    genericWaxRemaining = 6
    
    def playLightCandles():
        event = audio.event()
        event.register("door_enter_clock.mp3", 0, 100, 1.0, 0.0, 0, clock=True)
        event.register("door_enter_fireplace.mp3", 1, 100, 1.0, 0.0, 1)
        event.run()
        event = audio.event()
        event.register("candle_start.mp3", 1, 100, 1.0, 0.0, 0)
        event.run()
        candles.lastFireplaceLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        time.sleep(10)
        status.vars["fireplaceCandleLit"] = True
        event = audio.event()
        event.register("walk_ctw_clock.mp3", 1, 100, 1.0, 0.0, 0)
        event.register("walk_ctw_window.mp3", 2, 100, 1.0, 0.0, 1)
        event.run()
        event = audio.event()
        event.register("candle_start.mp3", 2, 100, 1.0, 0.0, 0)
        event.run()
        candles.lastWindowLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        time.sleep(10)
        status.vars["windowCandleLit"] = True
        event = audio.event()
        event.register("walk_ctw_clock.mp3", 2, 100, 1.0, 0.0, 0)
        event.register("walk_ctw_window.mp3", 7, 100, 1.0, 0.0, 1)
        event.run()
        event = audio.event()
        event.register("candle_start.mp3", 7, 100, 1.0, 0.0, 0)
        event.run()
        candles.lastGenericLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        time.sleep(10)
        status.vars["genericCandleLit"] = True
        event = audio.event()
        event.register("door_exit_clock.mp3", 0, 100, 1.0, 0.0, 0, clock=True)
        event.register("door_exit_fireplace.mp3", 7, 100, 1.0, 0.0, 0)
        event.run()
        
    def playEndCandles():
        event = audio.event()
        event.register("door_enter_clock.mp3", 0, 100, 1.0, 0.0, 0, clock=True)
        event.register("door_enter_fireplace.mp3", 1, 100, 1.0, 0.0, 1)
        event.run()
        event = audio.event()
        event.register("candle_end.mp3", 1, 100, 1.0, 0.0, 1)
        event.run()
        status.vars["fireplaceCandleLit"] = False
        candles.lastFireplaceLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        event = audio.event()
        event.register("walk_ctw_clock.mp3", 1, 100, 1.0, 0.0, 0)
        event.register("walk_ctw_window.mp3", 2, 100, 1.0, 0.0, 1)
        event.run()
        event = audio.event()
        event.register("candle_end.mp3", 2, 100, 1.0, 0.0, 1)
        event.run()
        status.vars["windowCandleLit"] = False
        candles.lastWindowLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        event = audio.event()
        event.register("walk_ctw_clock.mp3", 2, 100, 1.0, 0.0, 0)
        event.register("walk_ctw_window.mp3", 7, 100, 1.0, 0.0, 1)
        event.run()
        event = audio.event()
        event.register("candle_end.mp3", 7, 100, 1.0, 0.0, 1)
        event.run()
        status.vars["genericCandleLit"] = False
        candles.lastGenericLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        event = audio.event()
        event.register("door_exit_clock.mp3", 0, 100, 1.0, 0.0, 0, clock=True)
        event.register("door_exit_fireplace.mp3", 7, 100, 1.0, 0.0, 0)
        event.run()
        
    def playRunCandles():
        if (candles.lastFireplaceLoop + 30) < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
            if candles.fireplaceWaxRemaining > 0:
                status.vars["fireplaceCandleLit"] = True
                event = audio.event()
                event.register("candle_lit.mp3", 1, 25, 1.0, 0.0, 0)
                event.run()
                candles.lastFireplaceLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
                candles.fireplaceWaxRemaining = candles.fireplaceWaxRemaining - (0.05 * random.random())
                status.vars["lastFireplaceLoop"] =  pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
            else:
                status.vars["fireplaceCandleLit"] = False
                if random.random() < 0.01:
                    candles.relightCandle("fireplace")
                    candles.fireplaceWaxRemaining = 7 + (random.random() * 2)
                    if candles.fireplaceWaxRemaining > 0:
                        event = audio.event()
                        event.register("candle_lit.mp3", 1, 25, 1.0, 0.0, 0)
                        event.run()
                        candles.lastFireplaceLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
                        candles.fireplaceWaxRemaining = candles.fireplaceWaxRemaining - (0.05 * random.random())
                        status.vars["lastFireplaceLoop"] =  pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        
        if (candles.lastWindowLoop + 30) < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
            if (os.path.exists("nomufflewn.derp")) or (not os.path.exists("nomufflewn.derp") and ((tools.dataGrabber()[0][4] == "rain") or (tools.dataGrabber()[0][4] == "lightrain") or (tools.dataGrabber()[0][1] > (18 - wind.globals.windModif)) or (tools.dataGrabber()[0][0] > (13 - wind.globals.windModif)))):
                candles.windowFailCounter = candles.windowFailCounter - 1
                if candles.windowWaxRemaining > 0:
                    if candles.windowFailCounter < 3:
                        status.vars["windowCandleLit"] = True
                        event = audio.event()
                        event.register("candle_lit.mp3", 2, 25, 1.0, 0.0, 0)
                        event.run()
                        candles.lastWindowLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
                        candles.windowWaxRemaining = candles.windowWaxRemaining - (0.05 * random.random())
                        status.vars["lastWindowLoop"] =  pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
                else:
                    status.vars["windowCandleLit"] = False
                    if random.random() < 0.01:
                        candles.relightCandle("window")
                        candles.windowWaxRemaining = 7 + (random.random() * 2)
                        if candles.windowWaxRemaining > 0:
                            event = audio.event()
                            event.register("candle_lit.mp3", 2, 25, 1.0, 0.0, 0)
                            event.run()
                            candles.lastWindowLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
                            candles.windowWaxRemaining = candles.windowWaxRemaining - (0.05 * random.random())
                            status.vars["lastWindowLoop"] =  pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
            else:
                event = audio.event()
                event.register("candle_weather_out.mp3", 2, 100, 1.0, 0.0, 1)
                event.run()
                status.vars["windowCandleLit"] = False
                candles.windowFailCounter = candles.windowFailCounter + 1
        
        if (candles.lastGenericLoop + 30) < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
            if candles.genericWaxRemaining > 0:
                status.vars["genericCandleLit"] = True
                event = audio.event()
                event.register("candle_lit.mp3", 7, 25, 1.0, 0.0, 0)
                event.run()
                candles.lastGenericLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
                candles.genericWaxRemaining = candles.genericWaxRemaining - (0.03 * random.random())
                status.vars["lastGenericLoop"] =  pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
            else:
                status.vars["genericCandleLit"] = False
                if random.random() < 0.01:
                    candles.relightCandle("generic")
                    candles.genericWaxRemaining = 5 + (random.random() * 2)
                    if candles.genericWaxRemaining > 0:
                        event = audio.event()
                        event.register("candle_lit.mp3", 7, 25, 1.0, 0.0, 0)
                        event.run()
                        candles.lastGenericLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
                        candles.genericWaxRemaining = candles.genericWaxRemaining - (0.05 * random.random())
                        status.vars["lastGenericLoop"] =  pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
            
    def relightCandle(speaker):
        if speaker == "fireplace":
            event = audio.event()
            event.register("door_enter_clock.mp3", 0, 100, 1.0, 0.0, 0, clock=True)
            event.register("door_enter_fireplace.mp3", 1, 100, 1.0, 0.0, 1)
            event.run()
            event = audio.event()
            event.register("candle_start.mp3", 1, 100, 1.0, 0.0, 0)
            event.run()
            candles.lastFireplaceLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
            time.sleep(10)
            status.vars["fireplaceCandleLit"] = True
            event = audio.event()
            event.register("door_exit_clock.mp3", 0, 100, 1.0, 0.0, 0, clock=True)
            event.register("door_exit_fireplace.mp3", 1, 100, 1.0, 0.0, 0)
            event.run()
            
        elif speaker == "window":
            if candles.windowFailCounter < 3:
                event = audio.event()
                event.register("door_enter_clock.mp3", 0, 100, 1.0, 0.0, 0, clock=True)
                event.register("door_enter_fireplace.mp3", 2, 100, 1.0, 0.0, 1)
                event.run()
                event = audio.event()
                event.register("candle_start.mp3", 2, 100, 1.0, 0.0, 0)
                event.run()
                candles.lastWindowLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
                time.sleep(10)
                status.vars["windowCandleLit"] = True
                event = audio.event()
                event.register("door_exit_clock.mp3", 0, 100, 1.0, 0.0, 0, clock=True)
                event.register("door_exit_fireplace.mp3", 2, 100, 1.0, 0.0, 0)
                event.run()
                
        else:
            event = audio.event()
            event.register("door_enter_clock.mp3", 0, 100, 1.0, 0.0, 0, clock=True)
            event.register("door_enter_fireplace.mp3", 7, 100, 1.0, 0.0, 1)
            event.run()
            event = audio.event()
            event.register("candle_start.mp3", 7, 100, 1.0, 0.0, 0)
            event.run()
            candles.lastGenericLoop = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
            time.sleep(10)
            status.vars["genericCandleLit"] = True
            event = audio.event()
            event.register("door_exit_clock.mp3", 0, 100, 1.0, 0.0, 0, clock=True)
            event.register("door_exit_fireplace.mp3", 7, 100, 1.0, 0.0, 0)
            event.run()
    
    def run():
        currentDayTimes = tools.dayTimesGrabber()
        
        status.vars["nextCandleStart"] = currentDayTimes[6]
        status.vars["nextCandleEnd"] = currentDayTimes[3]
        
        if (pytools.clock.dateArrayToUTC(currentDayTimes[6]) < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())) or (pytools.clock.dateArrayToUTC(currentDayTimes[3]) > pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())) or (tools.dataGrabber()[0][4] == "rain") or (tools.dataGrabber()[0][4] == "lightrain") or (tools.dataGrabber()[0][4] == "snow"):
            if not candles.candlesAreRunning:
                candles.playLightCandles()
                candles.candlesAreRunning = True
                candles.playRunCandles()
            else:
                candles.playRunCandles()
        else:
            if candles.candlesAreRunning:
                candles.playEndCandles()
                candles.candlesAreRunning = False
        
        pytools.IO.saveJson("candles.json", {
            "fireplaceWaxRemaining": candles.fireplaceWaxRemaining,
            "windowWaxRemaining": candles.windowWaxRemaining,
            "genericWaxRemaining": candles.genericWaxRemaining,
        })
        
        status.vars["waxInfo"] = {
            "fireplaceWaxRemaining": candles.fireplaceWaxRemaining,
            "windowWaxRemaining": candles.windowWaxRemaining,
            "genericWaxRemaining": candles.genericWaxRemaining,
        } 

def main():
    
    candleInfo = pytools.IO.getJson("candles.json")
    try:
        candles.fireplaceWaxRemaining = candleInfo["fireplaceWaxRemaining"]
        candles.windowWaxRemaining = candleInfo["windowWaxRemaining"]
        candles.genericWaxRemaining = candleInfo["genericWaxRemaining"]
    except:
        print("Could not load candle info. Regenerating...")
    
    while not status.exit:
        candles.run()
        time.sleep(1)
        status.vars["lastLoop"] = pytools.clock.getDateTime()

def run():
    status.hasExited = False
    main()
    status.hasExited = True