import modules.audio as audio
import modules.pytools as pytools
import time
import math
import api.wind
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
    
class tools:
    def getDayMin(dateArray):
        return (dateArray[3] * 60) + (dateArray[4])

class util:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out

def main():
    while not status.exit:
        try:
            dataArray = util.dataGrabber()
        except:
            dataArray = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        dateArray = pytools.clock.getDateTime()
        if (dateArray[1] < 12) and (dateArray[1] > 8):
            if ((dateArray[1] == 9) and (dateArray[2] >= 15)) or ((dateArray[1] == 10) and (dateArray[2] <= 15)):
                if dateArray[1] == 9:
                    volume = 100 * (math.fabs(1440 / (((30 * 24 * 60) - ((dateArray[2] * 24 * 60) + tools.getDayMin(dateArray))) + 1)) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                else:
                    volume = 100 * (math.fabs(1440 / ((((dateArray[2] - 1) * 24 * 60) + tools.getDayMin(dateArray)))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                
                audio.playSoundWindow("leaves_early_m.mp3;leaves_early.mp3", [volume, volume, volume / 3], 1.0, 0.0, 0)
            if (dateArray[1] == 10) and (dateArray[2] < 25):
                if dateArray[2] <= 12:
                    volume = 100 * (math.fabs(1440 / (((12 * 24 * 60) - ((dateArray[2] * 24 * 60) + tools.getDayMin(dateArray))) + 1)) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                else:
                    volume = 100 * (math.fabs(1440 / ((((dateArray[2] - 1) * 24 * 60) - (12 * 24 * 60) + tools.getDayMin(dateArray)))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                audio.playSoundWindow("leaves_mid_m.mp3;leaves_mid.mp3", [volume, volume, volume / 3], 1.0, 0.0, 0)
            if (dateArray[1] == 10) and ((dateArray[2] >= 10) and (dateArray[2] <= 30)):
                if dateArray[2] <= 20:
                    volume = 100 * (math.fabs(1440 / (((20 * 24 * 60) - (dateArray[2] * 24 * 60) + tools.getDayMin(dateArray)) + 1)) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                else:
                    volume = 100 * (math.fabs(1440 / ((dateArray[2] * 24 * 60) - (20 * 24 * 60) + tools.getDayMin(dateArray))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                audio.playSoundWindow("leaves_late_m.mp3;leaves_late.mp3", [volume, volume, volume / 3], 1.0, 0.0, 0)
            if ((dateArray[1] == 10) and (dateArray[2] >= 20)) or ((dateArray[1] == 11) and (dateArray[2] <= 5)):
                if dateArray[1] == 10:
                    if dateArray[2] <= 28:
                        volume = 100 * (math.fabs(1440 / ((28 * 24 * 60) - (dateArray[2] * 24 * 60) + tools.getDayMin(dateArray) + 1)) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                    else:
                        volume = 100 * (math.fabs(1440 / ((((dateArray[2] - 1) * 24 * 60) - (28 * 24 * 60) + tools.getDayMin(dateArray)))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                else:
                    volume = 100 * (math.fabs(1440 / ((((dateArray[1] - 1) * 24 * 60) + (3 * 24 * 60) + tools.getDayMin(dateArray)))) ** 0.5) * (0.9 + (dataArray[0][1] / ((20 - api.wind.globals.windModif) * 4)))
                audio.playSoundWindow("leaves_end_m.mp3;leaves_end.mp3", [volume, volume, volume / 3], 1.0, 0.0, 0)
            time.sleep(194)
        else:
            time.sleep(600)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
