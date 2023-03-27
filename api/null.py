import modules.audio as audio
import time
import modules.pytools as pytools

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": []
    }

def hello():
    time.sleep(5)
    return 0

def main():
    while not status.exit:
        hello()
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True

