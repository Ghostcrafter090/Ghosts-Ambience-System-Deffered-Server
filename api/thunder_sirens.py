import modules.audio as audio
import modules.pytools as pytools
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
        "alertLevel": 2
    }

class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out

def main():
    count = 0
    alertLevel = 2
    while not status.exit:
        dataList = utils.dataGrabber()
        dateArray = pytools.clock.getDateTime()
        try:
            lightningDanger = pytools.IO.getJson("lightningData.json")["dangerLevel"]
        except:
            lightningDanger = 0
            
        status.vars["alertLevel"] = alertLevel
        
        if (dataList[1][5] > 4) or (lightningDanger > alertLevel):
            count = count + 1
            if dateArray[3] >= 22:
                volume = 20
            elif dateArray[3] <= 6:
                volume = 20
            else:
                volume = 100
            audioEvent = audio.event()
            audioEvent.registerWindow("tornado_sirens.mp3;tornado_sirens_nm.mp3", volume, 1.0, 0.0, 0)
            audioEvent.register("tornado_sirens_wall.mp3", 0, volume * 0.8, 1.0, 0.0, 0)
            audioEvent.register("tornado_sirens_wall.mp3", 1, volume * 0.8, 1.0, 0.0, 0)
            audioEvent.run()
            if count == 2:
                audioEvent = audio.event()
                audioEvent.register("radio_thunder_start.mp3", 0, 100, 1.0, 0.0, 0)
                audioEvent.run()
            time.sleep(104)
        else:
            if count > 0:
                audioEvent = audio.event()
                audioEvent.register("radio_thunder_end.mp3", 0, 100, 1.0, 0.0, 0)
                audioEvent.run()
                count = 0
        if (dateArray[2] == 1) or (dateArray[2] == 15):
            if dateArray[3] == 12:
                if dateArray[4] == 20:
                    audioEvent = audio.event()
                    audioEvent.registerWindow("tornado_sirens_test.mp3;tornado_sirens_test_nm.mp3", 100, 1.0, 0.0, 0)
                    audioEvent.register("tornado_sirens_test_wall.mp3", 0, 80, 1.0, 0.0, 0)
                    audioEvent.register("tornado_sirens_test_wall.mp3", 1, 80, 1.0, 0.0, 0)
                    audioEvent.run()
            time.sleep(55)
            
        if (lightningDanger > 2) and (lightningDanger > alertLevel):
            alertLevel = alertLevel + 1
        else:
            alertLevel = alertLevel - 1
            if lightningDanger > alertLevel:
                alertLevel = alertLevel + 1
            
        if alertLevel > 6:
            alertLevel = 6
        if alertLevel < 2.5:
            alertLevel = 2.5
        
        time.sleep(10)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
        

