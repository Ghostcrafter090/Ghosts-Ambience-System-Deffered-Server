import modules.audio as audio
import modules.pytools as pytools
import random
import time

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": [],
        "trickOrTreatIndex": 0
    }

def main():
    while not status.exit:
        dateArray = pytools.clock.getDateTime()
        dayTimes = pytools.IO.getList("dayTimes.pyl")[1]
        if pytools.clock.dateArrayToUTC([dateArray[0], dateArray[1], dateArray[2], dayTimes[5][3] - 4, dayTimes[5][4], dayTimes[5][5]]) < pytools.clock.dateArrayToUTC(dateArray):
            if dateArray[1] == 10:
                if dateArray[2] >= 20:
                    randf1 = 32768
                    randf2 = randf1 * 1000
                    randf3 = randf2 / 372
                    randf4 = randf3 * dateArray[3]
                    randf4 = (randf4 / 100) / ((32 - dateArray[2]) ** 2)
                    status.vars['trickOrTreatIndex'] = randf4
                    print("trickOrTreatIndex: " + str(randf4))
                    if (32768 * random.random()) < randf4:
                        audioEvent = audio.event()
                        audioEvent.register('doorbell.mp3', 0, 40, 1.0, 0.0, 0)
                        audioEvent.run()
                        time.sleep(10)
                        audioEvent = audio.event()
                        audioEvent.register('distanttrt' + str(random.randint(1, 5)) + ".mp3", 0, 100, 1.0, 0.0, 0)
                        audioEvent.run()
        time.sleep(300)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
