import modules.audio as audio
import time
import modules.pytools as pytools
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
    while not status.exit:
        event = audio.event()
        event.register("tavern_ambience_fireplace.mp3", 1, 100, 1.0, 0.0, 0)
        event.register("tavern_ambience_generic.mp3", 7, 100, 1.0, 0.0, 0)
        event.register("tavern_ambience_all.mp3", 0, 100, 1.0, 0.0, 0)
        event.register("tavern_ambience_all.mp3", 1, 100, 1.0, 0.0, 0)
        event.register("tavern_ambience_all.mp3", 2, 100, 1.0, 0.0, 0)
        event.register("tavern_ambience_all.mp3", 7, 100, 1.0, 0.0, 0)
        event.run()
        
        time.sleep(420)
        
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True

