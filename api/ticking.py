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
        "lastLoop": []
    }

def main():
    dateArray = pytools.clock.getDateTime()
    diaa = dateArray[4]
    diab = diaa + 30
    while diab >= 60:
        diab = diab - 60

    status.vars["tickingMinuteA"] = diaa
    status.vars["tickingMinuteB"] = diab

    while not status.exit:
        dateArray = pytools.clock.getDateTime()
        if dateArray[4] == diaa:
            audioEvent = audio.event() 
            audioEvent.register("ticking.mp3", 0, 50, 1.0, 0.0, 0, clock=False)
            audioEvent.run()
        if dateArray[4] == diab:
            audioEvent = audio.event() 
            audioEvent.register("ticking.mp3", 0, 50, 1.0, 0.0, 0, clock=False)
            audioEvent.run()
        time.sleep(60)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
        
