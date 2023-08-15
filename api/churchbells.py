import modules.audio as audio
import modules.pytools as pytools
import time
import os
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

def playDeath():
    if os.path.isfile("halloweenmode.derp"):
        audio.playSoundWindow("dnwbella.mp3;dnwbella.mp3", [20, 100], 1.0, 0, 1)

def main():
    while not status.exit:
        weekDay = pytools.clock.getDayOfWeek()
        dateArray = pytools.clock.getDateTime()
        if dateArray[3] == 9:
            if dateArray[4] == 5:
                audio.playSoundWindow("cb1.mp3;cb1.mp3", [10, 100], 1.0, 0, 1)
                playDeath()
        if dateArray[3] == 14:
            if dateArray[4] == 5:
                audio.playSoundWindow("cb4.mp3;cb4.mp3", [10, 100], 1.0, 0, 1)
                playDeath()
        if dateArray[3] == 18:
            if dateArray[4] == 5:
                audio.playSoundWindow("cb5.mp3;cb5.mp3", [10, 100], 1.0, 0, 1)
                playDeath()
        if weekDay == 0:
            if dateArray[3] == 10:
                if dateArray[4] == 35:
                    audio.playSoundWindow("cb2.mp3;cb3.mp3", [10, 100], 1.0, 0, 1)
                    playDeath()
            if dateArray[3] == 11:
                if dateArray[4] == 50:
                    audio.playSoundWindow("cb2.mp3;cb3.mp3", [10, 100], 1.0, 0, 1)
                    playDeath()
        time.sleep(60)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
