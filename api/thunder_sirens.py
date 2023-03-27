import modules.audio as audio
import modules.pytools as pytools
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

class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out

def main():
    count = 0
    while not status.exit:
        dataList = utils.dataGrabber()
        dateArray = pytools.clock.getDateTime()
        if (dataList[1][5] > 4) or (dataList[0][4] == "thunder"):
            count = count + 1
            audio.playSoundAll("tornado_sirens.mp3", 100, 1.0, 0.0, 0)
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
                    audio.playSoundAll("tornado_sirens_test.mp3", 100, 1.0, 0.0, 0)
                    time.sleep(55)
        time.sleep(10)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
        

