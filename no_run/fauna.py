import modules.audio as audio
import modules.pytools as pytools
import time
import random
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
        time.sleep(100)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    print("fuck")
    status.hasExited = False
    main()
    status.hasExited = True
