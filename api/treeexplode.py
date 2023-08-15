import modules.audio as audio
import modules.pytools as pytools
import random
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
        "explodingTreeIndex": 0
    }

class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out

def main():
    while not status.exit:
        dataList = utils.dataGrabber()
        if (dataList[0][7] <= -2) or ((dataList[0][7] <= 3) and (dataList[0][4] == "snow")):
            waitTimeMax = 3092.86 * 0.915726 ** ( - 0.881507 * (dataList[0][7] - 0.997517)) - 12.1414
            waitTimeMin = 0.54 * 3092.86 * 0.915726 ** ( - 0.881507 * (dataList[0][7] - 0.997517)) - 12.1414
            
            waitTime = (random.random() * (waitTimeMax - waitTimeMin)) + waitTimeMin
            
            # https://www.desmos.com/calculator/hxumgrqsk0
            maxDistance_0 = ((3092.86 * 0.795726 ** ( - 0.881507 * (dataList[0][7] - 0.997517)) - 12.1414) / (5)) + 300
            maxDistance_1 =  - ((3092.86 * 0.9915726 ** (0.881507 * (dataList[0][7] - 0.997517)) - 12.1414 - 3000) / (5)) + 50
            distance = random.random() * (maxDistance_0 + maxDistance_1)
            
            # https://www.desmos.com/calculator/rwarkwwp6i
            lowPass = 1.0151 ** ( - (distance - 660))
            
            print("Exploding Tree Wait Time And Distance: " + str(waitTime) + "s, " + str(distance) + "m")
            status.vars['explodingTreeIndex'] = waitTime
            time.sleep(waitTime)
            randb = -1
            countb = 0
            while (randb <= 10) and (countb < 10):
                waitTimeMax = (3092.86 * 0.915726 ** ( - 0.881507 * (dataList[0][7] - 0.997517)) - 12.1414) / 10
                audio.playSoundWindow("treecr1.mp3;treecr1.mp3", [50, 100, 75], 1.0, 0.0, 1, lowPass=[lowPass, lowPass * 3])
                countb = countb + 1
            treeNum = random.randint(1, 4)
            audio.playSoundWindow("treeex" + str(treeNum) + ".mp3;treeex" + str(treeNum) + ".mp3", [50, 100, 75], 1.0, 0.0, 1, lowPass=[lowPass, lowPass * 3])
        else:
            time.sleep(60)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
            
