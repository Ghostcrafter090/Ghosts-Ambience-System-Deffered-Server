import modules.audio as audio
import modules.pytools as pytools
import random
import threading
import time
import modules.logManager as log
import traceback

print = log.printLog

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": [],
        "fireplace": {
            "isLit": False,
            "fireplaceStage": "out"
        }
    }

class globals:
    fireLit = False
    woodCount = 0
    firePreped = False
    fireplaceStage = "out"
    tic = 0
    dataArray = []
    logs = 0
    hasGoneOut = False

class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out

class sounds:
    def playMatch():
        print("Lighting fireplace...")
        globals.fireplaceStage = "match"
        status.vars["fireplace"]["fireplaceStage"] = "match"
        try:
            pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
        except:
            pass
        audioEvent = audio.event()
        audioEvent.register('match_light.mp3', 5, 50, 1, -100, 0)
        audioEvent.register('match.mp3', 1, 35, 1, 0, 1)
        audioEvent.run()

    def playFire():
        print("Playing standard fire effect...")
        audioEvent = audio.event()
        audioEvent.register('fire.mp3', 1, 20, 1, 0, 0)
        audioEvent.register('fire.mp3', 5, 100, 1, -100, 0)   
        audioEvent.run()
        globals.fireplaceStage = "fire"
        status.vars["fireplace"]["fireplaceStage"] = "fire"
        try:
            pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
        except:
            pass
        
    def playFireStart():
        print("Playing standard fire_starting effect...")
        audioEvent = audio.event()
        audioEvent.register('fire_start.mp3', 1, 20, 1, 0, 0)
        audioEvent.register('fire_start.mp3', 5, 100, 1, -100, 0)
        audioEvent.run()
        globals.fireplaceStage = "fireStart"
        status.vars["fireplace"]["fireplaceStage"] = "fireStart"
        try:
            pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
        except:
            pass

    def playFireEnd():
        print("Playing standard fire_ending effect...")
        audioEvent = audio.event()
        audioEvent.register('fire_end.mp3', 1, 20, 1, 0, 0)
        audioEvent.register('fire_end.mp3', 5, 100, 1, -100, 0)
        audioEvent.run()
        globals.fireplaceStage = "fireEnd"
        status.vars["fireplace"]["fireplaceStage"] = "fireEnd"
        try:
            pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
        except:
            pass

    def playFireiLog():
        print("Playing standard fire_ilog effect...")
        audioEvent = audio.event()
        audioEvent.register('fire_ilog.mp3', 1, 20, 1, 0, 0)
        audioEvent.register('fire_ilog.mp3', 5, 100, 1, -100, 0)
        audioEvent.run()
        globals.fireplaceStage = "fireIlog"
        status.vars["fireplace"]["fireplaceStage"] = "fireIlog"
        try:
            pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
        except:
            pass
        
    def playFireoLog():
        print("Playing standard fire_olog effect...")
        audioEvent = audio.event()
        audioEvent.register('fire_olog.mp3', 1, 20, 1, 0, 0)
        audioEvent.register('fire_olog.mp3', 5, 100, 1, -100, 0)
        audioEvent.run()
        globals.fireplaceStage = "fireOlog"
        status.vars["fireplace"]["fireplaceStage"] = "fireOlog"
        try:
            pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
        except:
            pass
        
    def playGetLogs():
        audioEvent = audio.event()
        audioEvent.registerWindow("wood_chopper_wn.mp3;wood_chopper_nm.mp3", [15, 100], 1, 0, 0)
        audioEvent.register('wood_chopper_wall.mp3', 0, 15, 1, 0, 0)
        audioEvent.register('wood_chopper_wall.mp3', 1, 15, 1, 0, 1)
        audioEvent.run()
        
    def enterRoom():
        audioEvent = audio.event()
        audioEvent.register('door_enter_clock.mp3', 0, 100, 1, 0, 0)
        audioEvent.register('door_enter_fireplace.mp3', 1, 100, 1, 0, 1)
        audioEvent.run()
        
    def exitRoom(wait=True):
        audioEvent = audio.event()
        audioEvent.register('door_exit_clock.mp3', 0, 100, 1, 0, 0)
        if wait:
            audioEvent.register('door_exit_fireplace.mp3', 1, 100, 1, 0, 1)
        else:
            audioEvent.register('door_exit_fireplace.mp3', 1, 100, 1, 0, 0)
        audioEvent.run()
    
    def prepFireplace():
        globals.fireplaceStage = "firePrep"
        status.vars["fireplace"]["fireplaceStage"] = "firePrep"
        try:
            pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
        except:
            pass
        audioEvent = audio.event()
        audioEvent.register('fire_prep.mp3', 1, 100, 1, 0, 1)
        audioEvent.run()

    def loadFireplace():
        globals.fireplaceStage = "fireLoad"
        status.vars["fireplace"]["fireplaceStage"] = "fireLoad"
        try:
            pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
        except:
            pass
        audioEvent = audio.event()
        audioEvent.register('fire_load.mp3', 1, 100, 1, 0, 1)
        audioEvent.run()

    def chopTrees():
        distance = random.random()
        speed = 0.95 + (random.random() * 0.1)
        typef = str(random.randint(0, 2))
        audioEvent = audio.event()
        audioEvent.registerWindow("chop_tree_" + typef + "_wn.mp3;chop_tree_" + typef + "_nm.mp3", [25 * distance, 50 * distance], speed, 0.0, 0)
        audioEvent.register("chop_tree_" + typef + "_wall.mp3", 0, 25 * distance, speed, 0, 0)
        audioEvent.register("chop_tree_" + typef + "_wall.mp3", 1, 25 * distance, speed, 0, 1)
        audioEvent.run()
        
class handlers:
    def logManager():
        while True:
            try:
                if globals.logs < 1:
                    if globals.woodCount < 1:
                        while globals.woodCount < 100:
                            sounds.chopTrees()
                            globals.woodCount = globals.woodCount + random.randint(4, 12)
                            try:
                                pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
                            except:
                                pass
                            time.sleep(random.random() * 60)
                    while (globals.logs < 8) and (globals.woodCount >= 1):
                        sounds.playGetLogs()
                        globals.woodCount = globals.woodCount - 2
                        globals.logs = globals.logs + 4
                        try:
                            pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
                        except:
                            pass
                time.sleep(10)
            except:
                print(traceback.format_exc())
                time.sleep(10)
    
    def fireTender():
        justPreped = False
        while True:
            try:
                justLit = False
                if globals.fireLit == False:
                    if globals.dataArray[0][7] < 10:
                        justPreped = False
                        if globals.firePreped == False:
                            if globals.logs >= 1:
                                sounds.enterRoom()
                                sounds.prepFireplace()
                                globals.fireplaceStage = "out"
                                status.vars["fireplace"]["fireplaceStage"] = "out"
                                try:
                                    pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
                                except:
                                    pass
                                globals.logs = globals.logs - random.randint(3, 5)
                                globals.firePreped = True
                                justPreped = True
                    print(globals.firePreped)
                    print(globals.dataArray[0][7])
                    if globals.dataArray[0][7] < 8:
                        if globals.firePreped:
                            justLit = True
                            if justPreped == False:
                                sounds.enterRoom()
                            if globals.hasGoneOut:
                                sounds.loadFireplace()
                                globals.fireplaceStage = "out"
                                status.vars["fireplace"]["fireplaceStage"] = "out"
                                try:
                                    pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
                                except:
                                    pass
                            sounds.playMatch()
                            sounds.exitRoom(False)
                            globals.fireLit = 1
                            status.vars["fireplace"]["isLit"] = True
                    elif justPreped:
                        sounds.exitRoom()
                        justPreped = False
                if globals.fireLit == True:
                    if justLit:
                        sounds.playFireStart()
                        time.sleep(600)
                    tic = 0
                    while tic < 5:
                        sounds.playFire()
                        tic = tic + 1
                        time.sleep(194)
                    if globals.dataArray[0][7] < 10:
                        if (pytools.clock.getDateTime()[3] > 18) or (pytools.clock.getDateTime()[3] < 7):
                            sounds.playFireoLog()
                            time.sleep(7500)
                        else:
                            sounds.playFireiLog()
                            time.sleep(2100)
                        globals.logs = globals.logs - random.randint(0, 3)
                    else:
                        sounds.playFireEnd()
                        time.sleep(505)
                        globals.fireplaceStage = "out"
                        status.vars["fireplace"]["fireplaceStage"] = "out"
                        try:
                            pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
                        except:
                            pass
                        globals.hasGoneOut = True
                        globals.fireLit = False
                        status.vars["fireplace"]["isLit"] = False
                else:
                    time.sleep(10)
                if (globals.fireLit == False) and (globals.dataArray[0][7] > 12):
                    globals.firePreped = False
                    globals.hasGoneOut = False
                try:
                    pytools.IO.saveJson("fireplace.json", {"count": globals.woodCount, "fireplaceStage": globals.fireplaceStage})
                except:
                    pass
            except:
                print(traceback.format_exc())
                time.sleep(10)
def main():
    
    globals.dataArray = utils.dataGrabber()
    
    numberOfLogs = pytools.IO.getJson("fireplace.json")
    try:
        globals.woodCount = numberOfLogs["count"]
    except:
        pytools.IO.saveJson("fireplace.json", {"count": 0})
        globals.woodCount = 0
    globals.logs = globals.woodCount % 10
    
    logManager = threading.Thread(target=handlers.logManager)
    fireTender = threading.Thread(target=handlers.fireTender)
    
    logManager.start()
    fireTender.start()
    
    while not status.exit:
        globals.dataArray = utils.dataGrabber()
        time.sleep(15)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        
def run():
    status.hasExited = False
    main()
    status.hasExited = True
        
                        
