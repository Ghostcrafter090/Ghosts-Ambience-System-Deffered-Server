import modules.audio as audio
import modules.pytools as pytools
import random
import math
import os
import time
import modules.logManager as log
import api.halloween_extension as h
import traceback
print = log.printLog

class status:
    apiKey = ""
    audioObj = False
    finishedLoop = False
    exit = False
    hasExited = False
    vars = {
        "lastLoop": [],
        "notHunterCoeff": 0,
        "birds": {}
    }

audioBuffer = audio.rapidFire(30)

birds = pytools.IO.getJson("birds.json")
birdTimes = pytools.IO.getJson("birdDays.json")

class tools:
    def getActivity(weights, dayTimesUTC):
        utc = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())
        curr = 0
        while curr < (len(dayTimesUTC) - 1):
            if dayTimesUTC[curr] <= utc < dayTimesUTC[curr + 1]:
                break
            curr = curr + 1
        try:
            percent = (utc - dayTimesUTC[curr]) / dayTimesUTC[curr + 1]
        except:
            percent = (utc - dayTimesUTC[curr]) / (dayTimesUTC[0] + 86400)
        
        try:
            return (weights[curr] * (1 - percent)) + (weights[curr + 1] * percent)
        except:
            if (curr + 1) >= len(weights):
                return weights[curr]
        
    def isWater(bird):
        n = ["goose", "duck", "mallard", "bufflehead", "merganser", "grouse", "gull"]
        i = 0
        while i < len(n):
            if bird.find(n[i]) != -1:
                return (random.random() * random.random() * random.random() * random.random() * random.random())
            i = i + 1
        return 1
    
    def isWoodPecker(bird):
        if ("pecker" in bird) or ("flicker" in bird) or ("sapsucker" in bird):
            return True
        return False
    
    def isRaven(bird):
        if bird.find("raven") != -1:
            return random.random() * random.random()
        else:
            return 1
        
    def isCrow(bird):
        if bird.find("crow") != -1:
            return random.random() * random.random()
        else:
            return 1
        
    def isHunter(bird):
        n = ["hawk", "eagle", "owl", "osprey", "heron", "woodpecker", "grouse", "bat"]
        for f in n:
            if bird.find(f) != -1:
                return (random.random() * random.random())
        return 1
    
    notHunterCoeff = 0
    
    def isNotHunter(bird, dayTimes):
        n = ["hawk", "eagle", "owl", "osprey", "heron", "woodpecker", "grouse", "bat"]
        out = 1
        p = True
        for f in n:
            if bird.find(f) != -1:
                p = False
        if p:
            if pytools.clock.getDateTime()[3] > 12:
                tools.notHunterCoeff = ((1000000 * tools.notHunterCoeff) + (3 * (5 - math.fabs(5 - math.fabs(((pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - (pytools.clock.dateArrayToUTC(dayTimes[0]) + 86400)) / 3600)))) + 1)) / 1000001
                if tools.notHunterCoeff > 0.1:
                    out = (random.random() * random.random()) / (tools.notHunterCoeff * 10)
            else:
                tools.notHunterCoeff = ((1000000 * tools.notHunterCoeff) + (3 * (5 - math.fabs(5 - math.fabs(((pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) - (pytools.clock.dateArrayToUTC(dayTimes[0]))) / 3600)))) + 1)) / 1000001
                if tools.notHunterCoeff > 0.1:
                    out = (random.random() * random.random()) / (tools.notHunterCoeff * 10)
            status.vars["notHunterCoeff"] = tools.notHunterCoeff
        return out
            
    def gullInc(bird, dataArray):
        if bird.find("gull") != -1:
            if dataArray[0][3] > 0:
                return (random.random() * dataArray[0][3]) + 1
            else:
                return 1
        else:
            return 1
        
    def tempDiff(bird, dataArray):
        i = 0
        f = 0
        r = 0
        dateArray = pytools.clock.getDateTime()
        hourTime = dateArray[3] + (((dateArray[4] * 60) + dateArray[5]) / 3600)
        while i < len(bird["activity"]):
            if r < bird["activity"][i]:
                r = bird["activity"][i]
                f = i
            i = i + 1
        monthPeak = 365 * (f / 12)
        tempDial = 4 * math.sin((2 * 3.14 * ((1 / 24) * hourTime)) - 21)
        currentPeak = (3 + math.fabs(dataArray[0][7] - (tempDial + ((-16 * math.sin(2 * 3.14 * ((1 / 365) * monthPeak))) + 7))))
        if currentPeak < 0.01:
            currentPeak = 0.01
        out = random.random() / (currentPeak / 3)
        if out > 3:
            out = 3
        if out < 1:
            out = 1
        return out

class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        return out
    
    def testWindow():
        out = False
        if os.path.exists(".\\nomufflewn.derp") == True:
            out = True
        return out
    
def main():
    totalBirdSounds = 0
    totalCountIndex = 0
    birds = pytools.IO.getJson("birds.json")
    for bird in birds.keys():
        status.vars["birds"][bird] = {
            "monthActivity": 0,
            "dayActivity": 0,
            "activity": 0
        }
    birdTimes = pytools.IO.getJson("birdDays.json")
    dayTimes = pytools.IO.getList("daytimes.pyl")[1]
    dayTimesUTC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    i = 0
    while i < len(dayTimes):
        dayTimesUTC[i + 1] = pytools.clock.dateArrayToUTC(dayTimes[i])
        i = i + 1
    dataArray = utils.dataGrabber()
    while not status.exit:
        if pytools.clock.getDateTime()[5] == 0:
            
            birdTimes = pytools.IO.getJson("birdDays.json")
            birds = pytools.IO.getJson("birds.json")
            dayTimes = pytools.IO.getList("daytimes.pyl")[1]
            dayTimesUTC = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            i = 0
            while i < len(dayTimes):
                dayTimesUTC[i] = pytools.clock.dateArrayToUTC(dayTimes[i])
                i = i + 1
            dataArray = utils.dataGrabber()
            dayTimesUTC = [(pytools.clock.dateArrayToUTC(dayTimes[4]) - (86400 / 2)), *(dayTimesUTC[0:5]), (pytools.clock.dateArrayToUTC(dayTimes[4]) + 3600), *(dayTimesUTC[5:]), (pytools.clock.dateArrayToUTC(dayTimes[4]) + (86400 / 2))]
        
        status.vars["totalBirdSoundCount"] = totalBirdSounds
        status.vars["maxBirdSoundCount"] = ((((12 - ((pytools.clock.getDateTime()[3] + (pytools.clock.getDateTime()[4] / 60)) - 12)) * 2) * (1 + (5 * ("owl" in bird)))) * ((100 - h.data.getHallowIndex(pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()))) / 100))
        
        for bird in sorted(birds):
            ytc = (12 * pytools.clock.getYearUTC()) / 31536000
            try:
                monthActivity = ((1 - (ytc - math.floor(ytc))) * birds[bird]["activity"][int(math.floor(ytc))] + (((ytc - math.floor(ytc))) * birds[bird]["activity"][int(math.floor(ytc + 1))]))
            except:
                monthActivity = ((1 - (ytc - math.floor(ytc))) * birds[bird]["activity"][int(math.floor(ytc))] + (((ytc - math.floor(ytc))) * birds[bird]["activity"][int(math.floor(0))]))
            dayActivity = tools.getActivity(birdTimes[bird], dayTimesUTC)
            activity = (((monthActivity * dayActivity) / 100) ** (2 - (1 - tools.isHunter(bird)))) * tools.isWater(bird) * tools.isRaven(bird) * tools.isHunter(bird) * random.random() * tools.gullInc(bird, dataArray) * tools.tempDiff(birds[bird], dataArray)
            
            if tools.isWater(bird):
                activity = activity * (- 0.60981 ** ( - 0.59078 * (dataArray[0][0] - 20.33576)) + 1.00646)
            if tools.isWoodPecker(bird):
                activity = activity * (- 0.60981 ** ( - 0.59078 * (dataArray[0][0] - 30.33576)) + 1.00646)
            elif tools.isHunter(bird):
                activity = activity * (- 0.60981 ** ( - 0.59078 * (dataArray[0][0] - 15.33576)) + 1.00646)
            elif tools.isCrow(bird):
                activity = activity * (- 0.60981 ** ( - 0.59078 * (dataArray[0][0] - 25.33576)) + 1.00646)
            elif tools.isRaven(bird):
                activity = activity * (- 0.60981 ** ( - 0.59078 * (dataArray[0][0] - 30.33576)) + 1.00646)
            else:
                activity = activity * (- 0.60981 ** ( - 0.59078 * (dataArray[0][0] - 10.33576)) + 1.00646)
            
            try:
                if os.path.exists("halloweenmode.derp"):
                    horrorIndex = float(pytools.IO.getFile("horrorindex.cx"))
                    if horrorIndex > 0:
                        if bird.find("owl") != -1:
                            horrf = (horrorIndex / 100)
                            if horrf > 1:
                                activity = activity * (horrf + 1)
                        else:
                                activity = activity / ((horrorIndex / 10) + 1)
                    elif horrorIndex < 0:
                        if bird.find("crow") == -1:
                            horrf = activity / ((math.fabs(horrorIndex) / 20) + 1)
                            if horrf > 1:
                                activity = activity / ((math.fabs(horrorIndex) / 100) + 1)
                        if bird.find("raven") == -1:
                            horrf = activity / ((math.fabs(horrorIndex) / 100) + 1)
                            if horrf > 1:
                                activity = activity / ((math.fabs(horrorIndex) / 100) + 1)
            except:
                pass
            if dayTimesUTC[6] < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                activity = activity * tools.isNotHunter(bird, dayTimes)
            if dayTimesUTC[0] < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) < dayTimesUTC[1]:
                activity = activity * tools.isNotHunter(bird, dayTimes)
            status.vars["birds"][bird]["monthActivity"] = monthActivity
            status.vars["birds"][bird]["dayActivity"] = dayActivity
            status.vars["birds"][bird]["activity"] = ((status.vars["birds"][bird]["activity"] * 100) + activity) / 101
            # print("Bird " + bird + " activity is registering at " + str(int(math.floor(activity * 100))) + "%" + " " + str(monthActivity) + " " + str(dayActivity))
            try:
                if random.random() < activity:
                    
                    if totalBirdSounds < (((((12 - ((pytools.clock.getDateTime()[3] + (pytools.clock.getDateTime()[4] / 60)) - 12)) * 2) * (1 + (5 * (tools.isHunter(bird) != 1)))) * ((100 - h.data.getHallowIndex(pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()))) / 100))) * 20:
                        # if utils.testWindow():
                        #     # audioEvent = audio.event()
                        #     audioBuffer.register(birds[bird]["sounds"][int(math.floor(random.random() * len(birds[bird]["sounds"])))], 6, (((activity / 15) * 10)) * random.random() * tools.isWater(bird) * tools.tempDiff(birds[bird], dataArray) * tools.isRaven(bird) * tools.isCrow(bird) * 16, (random.random() * 0.05) + 0.95, 0, 0)
                        #     # audioEvent.run()
                        # else:
                        
                        soundIndex = int(math.floor(random.random() * len(birds[bird]["sounds"])))
                        
                        speedModifier = 1
                        if "speed" in birds[bird]:
                            speedModifier = birds[bird]["speed"]
                            
                        volume = (((activity / 15) * 10)) * random.random() * tools.isWater(bird) * tools.isRaven(bird) * tools.tempDiff(birds[bird], dataArray) * tools.isCrow(bird) * 16 * (1 + (4 * (tools.isHunter(bird) != 1)))
                        windowVolume = volume / 16
                        
                        speed = ((random.random() * 0.05) + 0.95) * speedModifier
                        
                        if volume > 30:
                            volume = (30 * random.random())
                            windowVolume = volume / 16
                            
                        if random.random() < (1 / 10000):
                            
                            volume = volume * 10
                            if volume > 40:
                                volume = 40
                            
                            audioEvent = audio.event()
                            audioEvent.register(birds[bird]["sounds"][soundIndex], 1, 100, speed, 0, 0, lowPass=1300)
                            audioEvent.register(birds[bird]["sounds"][soundIndex], 1, 100, speed + 0.0005, 0, 0, lowPass=1300)
                            audioEvent.register(birds[bird]["sounds"][soundIndex], 1, 100, speed - 0.0005, 0, 0, lowPass=1300)
                            audioEvent.register(birds[bird]["sounds"][soundIndex], 3, volume, speed, 0, 0, lowPass=1300)
                            if tools.isWoodPecker(bird):
                                audioEvent.register("woodpecker_on_chimney.mp3", 1, 100, speed, 0, 0)
                                audioEvent.register("woodpecker_on_chimney.mp3", 3, 100, speed, 0, 0, highPass=200)
                            else:
                                audioEvent.register("bird_on_chimney.mp3", 1, 100, speed, 0, 0)
                                audioEvent.register("bird_on_chimney.mp3", 3, 100, speed, 0, 0, highPass=200)
                            audioEvent.run()
                            
                        else:
                        
                            audioEvent = audio.event()
                            audioEvent.register(birds[bird]["sounds"][soundIndex], 3, volume, speed, 0, 0)
                            audioEvent.register(birds[bird]["sounds"][soundIndex], 2, windowVolume, speed, 0, 0)
                            audioEvent.run()
                        
                        totalBirdSounds = totalBirdSounds + 1
            except:
                print(traceback.format_exc())
                print(activity)
                print(bird)
            time.sleep(0.1)
            
            totalCountIndex = totalCountIndex + 1
            
            if totalCountIndex > 100:
                totalCountIndex = 0
                totalBirdSounds = totalBirdSounds - 1
                if totalBirdSounds < 0:
                    totalBirdSounds = 0
            
            status.vars["lastLoop"] = pytools.clock.getDateTime()
def run():
    status.hasExited = False
    audioBuffer._start()
    main()
    audioBuffer._stop()
    status.hasExited = True
