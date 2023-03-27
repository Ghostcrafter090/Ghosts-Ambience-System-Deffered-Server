import modules.audio as audio
import modules.pytools as pytools
import os
import time

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
        # if os.path.exists("server.derp"):
        time.sleep(1)
        status.finishedLoop = True
        status.vars["lastLoop"] = pytools.clock.getDateTime()

def run():
    status.hasExited = False
    main()
    status.hasExited = True
