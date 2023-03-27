import modules.audio as audio
import modules.pytools as pytools
import random
import time
import traceback
import os
import threading

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
    
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out

class globals:
    run = False
    tic = 0
    playBells = True
    dateArray = [2022, 1, 1, 0, 0, 0]
    dayTimes = []
    dataArray = [[2.57, 4.4217330551255625, 10000.0, 0, 'clouds', 3.0, 0.0, 18.388888888888886, 69.0], [0.0, 0.0, 1002.71, 18.0, 69.0, 0], [18.388888888888886, 69.0, 0.0, 0.0, 2.4936961399999995, 4.4217330551255625], 'set temp=291\n    set tempc=18\n    set windspeed=2\n    set windgust=4\n    set pressure=0\n    set humidity=69\n    set weather=clouds\n    set modifier=3', 8, 10, 0, [2.57, 0]]
    
class tools:
    def getOutStatus():
        out = 0
        if os.path.isfile('nomufflewn.derp') == True:
            out = 1
        return out

class calc:
    def bellCurve(base, amp, span, pos, tic):
        c = 1 / (10000 * span)
        return amp * (base ** (-c * ((tic - pos) ** 2)))

    def getDayTic(dateArray):
        if dateArray[1] == 11:
            out = (30 - dateArray[2]) + 25
        elif dateArray[1] == 12:
            out = 25 - dateArray[2]
        else:
            out = 1000
        if out < 1:
            out = 1
        daySec = 1 - (((dateArray[3] * 60 * 60) + (dateArray[4] * 60) + dateArray[5]) / 86400)
        return out + daySec
    
    def dayTic(dateArray):
        globals.tic = (dateArray[3] * 60 * 60) + (dateArray[4] * 60) + dateArray[5]
        return globals.tic
    
    def isNiceDay():
        if globals.dataArray[0][0] > 12:
            return False
        if globals.dataArray[0][1] > 15:
            return False
        if globals.dataArray[0][4] == "rain":
            return False
        if globals.dataArray[0][4] == "lightrain":
            return False
        return True
    
class sections:
    bellsChance = 0
    
    def runBells():
        while not status.exit:
            globals.dateArray = pytools.clock.getDateTime()
            globals.tic = calc.dayTic(globals.dateArray)
            if globals.run:
                try:
                    bellsChance = 0
                    bellsChance = calc.bellCurve(2, 1900, 10800, 54000, globals.tic) / (calc.getDayTic(globals.dateArray) * 1.5)
                    if random.randrange(0, 35000) < bellsChance:
                        ghSpeaker = 5
                        while ghSpeaker == 5:
                            ghSpeaker = random.randrange(0, 8)
                        if globals.playBells:
                            audioEvent = audio.event()
                            audioEvent.register('sleighbells_' + str(random.randrange(0, 5)) + ".mp3", ghSpeaker, 40, 1, 0, 0)
                            audioEvent.run()
                    sections.bellsChance = bellsChance
                    time.sleep(0.1)
                except:
                    pass
            else:
                sections.bellsChance = 0
            if sections.bellsChance <= 0:
                time.sleep(1)
    
    outsideBandChance = 0
    
    def runOutsideBand():
        while not status.exit:
            if globals.run and calc.isNiceDay():
                try:
                    outsideBandChance = 0
                    outsideBandChance = calc.bellCurve(2, 1900, 7800, 43200, globals.tic) / (calc.getDayTic(globals.dateArray) * 1.5)
                    if random.randrange(0, 35000) < outsideBandChance:
                        if int(globals.dayTimes[6][3]) > globals.dateArray[3]:
                            if int(globals.dayTimes[3][3]) < globals.dateArray[3]:
                                audioEvent = audio.event()
                                audioEvent.register("outside_band.mp3", 0, 10, 1, 0, 0)
                                audioEvent.register("outside_band.mp3", 1, 10, 1, 0, 0)
                                audioEvent.registerWindow("outside_band.mp3;outside_band_nm.mp3", 10, 1, 0, 0)
                                audioEvent.run()
                    sections.outsideBandChance = outsideBandChance
                    time.sleep(0.1)
                except:
                    pass
            else:
                sections.outsideBandChance = 0
            if sections.outsideBandChance <= 0:
                time.sleep(1)
                
    outsideBellsChance = 0
    
    def runOutsideBells():
        while not status.exit:
            if globals.run and calc.isNiceDay():
                try:
                    outsideBellsChance = 0
                    outsideBellsChance = calc.bellCurve(2, 1900, 8800, 39600, globals.tic) / (calc.getDayTic(globals.dateArray) * 1.5)
                    if random.randrange(0, 35000) < outsideBellsChance:
                        if int(globals.dayTimes[6][3]) > globals.dateArray[3]:
                            if int(globals.dayTimes[3][3]) < globals.dateArray[3]:
                                if globals.playBells:
                                    audioEvent = audio.event()
                                    audioEvent.register("outside_bells.mp3", 0, 10, 1, 0, 0)
                                    audioEvent.register("outside_bells.mp3", 1, 10, 1, 0, 0)
                                    audioEvent.registerWindow("outside_bells.mp3;outside_bells_nm.mp3", 10, 1, 0, 1)
                                    audioEvent.run()
                    sections.outsideBellsChance = outsideBellsChance
                    time.sleep(0.1)
                except:
                    pass
            else:
                sections.outsideBellsChance = 0
            if sections.outsideBellsChance <= 0:
                time.sleep(1)
                
    musicBoxChance = 0
    
    def runMusicBoxs():
        while not status.exit:
            if globals.run and (((globals.dateArray[1] == 11) and ((globals.dataArray[0][7] <= 0.5) or (globals.dataArray[0][3] != 0) or (globals.dataArray[0][4] == "snow"))) or (globals.dateArray[1] == 12)):
                try:
                    musicBoxChance = 0
                    musicBoxChance = calc.bellCurve(2, 1900, 8800, 72000, globals.tic) / (calc.getDayTic(globals.dateArray) * 1.5)
                    if random.randrange(0, 35000) < musicBoxChance:
                        ghSpeaker = 5
                        while ghSpeaker == 5:
                            ghSpeaker = random.randrange(0, 8)
                        if random.randrange(0, 2) == 1:
                            if globals.playBells:
                                audioEvent = audio.event()
                                audioEvent.register("jinglebells_mb.mp3", ghSpeaker, 5, 1, 0, 1)
                                audioEvent.run()
                        else:
                            if globals.playBells:
                                audioEvent = audio.event()
                                audioEvent.register("merrychristmas_mb.mp3", ghSpeaker, 5, 1, 0, 1)
                                audioEvent.run()
                    sections.musicBoxChance = musicBoxChance
                    time.sleep(0.1)
                except:
                    pass
            else:
                sections.musicBoxChance = 0
            if sections.musicBoxChance <= 0:
                time.sleep(1)
                
    class events:
        threeAmBells = -1
        sixPmDinner = -1
        mmcBells = -1
        santaLanding = -1
                
    def runEvents():
        while not status.exit:
            if globals.run:
                try:
                    if globals.dateArray[3] == 3:
                        if globals.dateArray[4] == 5:
                            if sections.events.threeAmBells != globals.dateArray[2]:
                                if (random.random * calc.getDayTic(globals.dateArray)) < 3:
                                    if (((globals.dateArray[1] == 11) and ((globals.dataArray[0][7] <= 0.5) or (globals.dataArray[0][3] != 0) or (globals.dataArray[0][4] == "snow"))) or (globals.dateArray[1] == 12)):
                                        audio.playSoundAll("3am_bells.mp3", 5, 1, 0, 0)
                                sections.events.threeAmBells = globals.dateArray[2]
                    if globals.dateArray[3] == 18:
                        if globals.dateArray[4] == 10:
                            if (globals.dateArray[2] != sections.events.sixPmDinner):
                                audio.playSoundAll("6pm_ch.mp3", 15, 1, 0, 0)
                                sections.events.sixPmDinner = globals.dateArray[2]
                    if globals.dateArray[3] == 21:
                        if globals.dateArray[4] == 23:
                            if (globals.dateArray[2] < 24) or (globals.dateArray[1] == 11):
                                if sections.events.mmcBells != globals.dateArray[2]:
                                    if (random.random() * calc.getDayTic(globals.dateArray)) < 5:
                                        if (calc.getDayTic(globals.dateArray) > 2) and (((globals.dateArray[1] == 11) and ((globals.dataArray[0][7] <= 0.5) or (globals.dataArray[0][3] != 0) or (globals.dataArray[0][4] == "snow"))) or (globals.dateArray[1] == 12)):
                                            globals.playBells = False
                                            time.sleep((random.random() + 0.5) * 40)
                                            audio.playSoundAll("mmcbells.mp3", 100, 1, 0, 1)
                                            time.sleep((random.random() + 0.5) * 10)
                                            globals.playBells = True
                                    sections.events.mmcBells = globals.dateArray[2]
                except:
                    print(traceback.format_exc())
            time.sleep(1)
    
    lateDayBellsChance = 0
    
    def runLateDayBells():
        while not status.exit:
            if globals.run and (((globals.dateArray[1] == 11) and ((globals.dataArray[0][7] <= 0.5) or (globals.dataArray[0][3] != 0) or (globals.dataArray[0][4] == "snow"))) or (globals.dateArray[1] == 12)):
                try:
                    lateDayBellsChance = 0
                    lateDayBellsChance = (calc.bellCurve(2, 1900, 7200, 82800, globals.tic) + calc.bellCurve(2, 1900, 7200, 25200, globals.tic)) / (calc.getDayTic(globals.dateArray) * 1.5)
                    if random.randrange(0, 35000) < lateDayBellsChance:
                        if globals.playBells:
                            audio.playSoundAll("lateday_bells.mp3", 10, 1, 0, 1)
                    sections.lateDayBellsChance = lateDayBellsChance
                    time.sleep(0.1)
                except:
                    pass
            else:
                sections.lateDayBellsChance = 0
            if sections.lateDayBellsChance <= 0:
                time.sleep(1)
                
    lateNightChoirChance = 0
    
    def runLateNightChoir():
        while not status.exit:
            if globals.run and calc.isNiceDay() and (((globals.dateArray[1] == 11) and ((globals.dataArray[0][7] <= 0.5) or (globals.dataArray[0][3] != 0) or (globals.dataArray[0][4] == "snow"))) or (globals.dateArray[1] == 12)):
                try:
                    lateNightChoirChance = 0
                    lateNightChoirChance = calc.bellCurve(2, 1900, 7200, 10800, globals.tic) / (calc.getDayTic(globals.dateArray) * 1.5)
                    if random.randrange(0, 35000) < lateNightChoirChance:
                        audio.playSoundAll("latenight_choir.mp3", 10, 1, 0, 1)
                    sections.lateNightChoirChance = lateNightChoirChance
                    time.sleep(0.1)
                except:
                    pass
            else:
                sections.lateNightChoirChance = 0
            if sections.lateNightChoirChance <= 0:
                time.sleep(1)
                
    mmcIdleChance = 0
    
    def runMmcIdle():
        while not status.exit:
            if globals.run and (((globals.dateArray[1] == 11) and ((globals.dataArray[0][7] <= 0.5) or (globals.dataArray[0][3] != 0) or (globals.dataArray[0][4] == "snow"))) or (globals.dateArray[1] == 12)):
                try:
                    mmcIdleChance = 0
                    mmcIdleChance = calc.bellCurve(2, 1900, 12600, 43200, globals.tic) / (calc.getDayTic(globals.dateArray) * 1.5)
                    if random.randrange(0, 35000) < mmcIdleChance:
                        audio.playSoundWindow("mmcidle.mp3;mmcidle.mp3", [20, 30], 1, 0, 1)
                    sections.mmcIdleChance = mmcIdleChance
                    time.sleep(0.1)
                except:
                    pass
            else:
                sections.mmcIdleChance = 0
            if sections.mmcIdleChance <= 0:
                time.sleep(1)
                
    class santa:
        landingChance = 0
        sleighPassingChance = 0
        
        class utils:
            def calcLandingChance():
                sections.santa.landingChance = ((1 + (0.02 / calc.getDayTic())) ** globals.tic) / 10
        
        def runLanding():
            while not status.exit:
                if globals.run and (((globals.dateArray[1] == 11) and ((globals.dataArray[0][7] <= 0.5) or (globals.dataArray[0][3] != 0) or (globals.dataArray[0][4] == "snow"))) or (globals.dateArray[1] == 12)):
                    try:
                        sections.santa.utils.calcLandingChance()
                        if sections.events.santaLanding != globals.dateArray[2]:
                            if random.randrange(0, 35000) < sections.santa.landingChance:
                                if globals.playBells:
                                    audioEvent = audio.event()
                                    audioEvent.register("santalanding.mp3", 0, 10, 1, 0, 0)
                                    audioEvent.register("santalanding.mp3", 1, 10, 1, 0, 0)
                                    audioEvent.registerWindow("santalanding_wn.mp3;santalanding_nm.mp3", [10, 10], 1, 0, 0)
                                    audioEvent.run()
                                sections.events.santaLanding = globals.dateArray[2]
                            time.sleep(0.1)
                        else:
                            time.sleep(1)
                    except:
                        pass
                else:
                    sections.santa.landingChance = 0
                if sections.santa.landingChance <= 0:
                    time.sleep(1)
                    
        def runPassing():
            while not status.exit:
                if globals.run and (((globals.dateArray[1] == 11) and ((globals.dataArray[0][7] <= 0.5) or (globals.dataArray[0][3] != 0) or (globals.dataArray[0][4] == "snow"))) or (globals.dateArray[1] == 12)):
                    try:
                        sections.santa.sleighPassingChance = calc.bellCurve(2, 1900, 3600, 10800, globals.tic) / (calc.getDayTic(globals.dateArray) * 1.5)
                        if sections.events.santaLanding != globals.dateArray[2]:
                            if random.randrange(0, 35000) < sections.santa.sleighPassingChance:
                                if globals.playBells:
                                    audioEvent = audio.event()
                                    audioEvent.register("sleigh_passing.mp3", 0, 10, 1, 0, 0)
                                    audioEvent.register("sleigh_passing.mp3", 1, 10, 1, 0, 0)
                                    audioEvent.registerWindow("sleigh_passing_wn.mp3;sleigh_passing_nm.mp3", [10, 10], 1, 0, 1)
                                    audioEvent.run()
                            time.sleep(0.1)
                        else:
                            time.sleep(1)
                    except:
                        pass
                else:
                    sections.santa.sleighPassingChance = 0
                if sections.santa.sleighPassingChance <= 0:
                    time.sleep(1)

def main():
    globals.dateArray = pytools.clock.getDateTime()
    globals.dayTimes = utils.dayTimesGrabber()
    globals.dataArray = utils.dataGrabber()
    
    bellsRunner = threading.Thread(target=sections.runBells)
    outsideBandRunner = threading.Thread(target=sections.runOutsideBand)
    outsideBellsRunner = threading.Thread(target=sections.runOutsideBells)
    musicBoxsRunner = threading.Thread(target=sections.runMusicBoxs)
    eventsRunner = threading.Thread(target=sections.runEvents)
    lateDayBellsRunner = threading.Thread(target=sections.runLateDayBells)
    lateNightChoirRunner = threading.Thread(target=sections.runLateNightChoir)
    mccIdleRunner = threading.Thread(target=sections.runMmcIdle)
    santaLandingRunner = threading.Thread(target=sections.santa.runLanding)
    santaPassingRunner = threading.Thread(target=sections.santa.runPassing)
    
    bellsRunner.start()
    outsideBandRunner.start()
    outsideBellsRunner.start()
    musicBoxsRunner.start()
    eventsRunner.start()
    lateDayBellsRunner.start()
    lateNightChoirRunner.start()
    mccIdleRunner.start()
    santaLandingRunner.start()
    santaPassingRunner.start()
    
    ticOld = -1
    
    while not status.exit:
        globals.dateArray = pytools.clock.getDateTime()
        globals.dayTimes = utils.dayTimesGrabber()
        globals.tic = calc.dayTic(globals.dateArray)
        if ((globals.dateArray[1] == 11) and (globals.dateArray[2] > 11)) or (globals.dateArray[1] == 12):
            globals.run = True
        else:
            globals.run = False
        globals.dataArray = utils.dataGrabber()
        if globals.tic != ticOld:
            ticOld = globals.tic
            heavenIndex = sections.bellsChance + sections.outsideBandChance + sections.outsideBellsChance + sections.musicBoxChance + sections.lateNightChoirChance + sections.lateDayBellsChance + sections.mmcIdleChance + sections.santa.landingChance + sections.santa.sleighPassingChance
            print("Heaven Index: " + str(heavenIndex) + "Hi")
            status.vars['heavenIndex'] = heavenIndex
            status.vars["heavenStats"] = {
                "bellsChance": sections.bellsChance,
                "outsideBandChance": sections.outsideBandChance,
                "outsideBellsChance": sections.outsideBellsChance,
                "musicBoxChance": sections.musicBoxChance,
                "lateNightChoirChance": sections.lateNightChoirChance,
                "lateDayBellsChance": sections.lateDayBellsChance,
                "mmcIdleChance": sections.mmcIdleChance,
                "santa": {
                    "landingChance": sections.santa.landingChance,
                    "sleighPassingChance": sections.santa.sleighPassingChance
                }
            }
            status.vars["eventConds"] = {
                "threeAmBells": sections.events.threeAmBells,
                "sixPmDinner": sections.events.sixPmDinner,
                "mmcBells": sections.events.mmcBells,
                "santaLanding": sections.events.santaLanding
            }
            pytools.IO.saveFile('heavenindex.cx', str(heavenIndex))
        if globals.run:
            time.sleep(1)
        else:
            time.sleep(10)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True
            
def run():
    status.hasExited = False
    main()
    status.hasExited = True
            
                
    
                
    
                
    
