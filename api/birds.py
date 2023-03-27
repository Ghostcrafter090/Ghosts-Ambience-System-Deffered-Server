import modules.audio as audio
import modules.pytools as pytools
import random
import math
import os
import time

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
        # print((weights[curr + 1] * (1 - percent)))
        return (weights[curr] * (1 - percent)) + (weights[curr + 1] * percent)
    
    def isWater(bird):
        n = ["goose", "duck", "mallard", "bufflehead", "merganser", "grouse", "gull"]
        i = 0
        while i < len(n):
            if bird.find(n[i]) != -1:
                return (random.random() * random.random() * random.random() * random.random() * random.random())
            i = i + 1
        return 1
    
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
        n = ["hawk", "eagle", "owl", "osprey", "heron", "woodpecker", "grouse"]
        for f in n:
            if bird.find(f) != -1:
                return (random.random() * random.random())
        return 1
    
    notHunterCoeff = 0
    
    def isNotHunter(bird, dayTimes):
        n = ["hawk", "eagle", "owl", "osprey", "heron", "woodpecker", "grouse"]
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
            dayTimes = pytools.IO.getList("daytimes.pyl")[1]
            dayTimesUTC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            i = 0
            while i < len(dayTimes):
                dayTimesUTC[i + 1] = pytools.clock.dateArrayToUTC(dayTimes[i])
                i = i + 1
            dataArray = utils.dataGrabber()
        dayTimesUTC[0] = pytools.clock.dateArrayToUTC(dayTimes[4]) - (86400 / 2)
        for bird in birds:
            ytc = (12 * pytools.clock.getYearUTC()) / 31536000
            try:
                monthActivity = ((1 - (ytc - math.floor(ytc))) * birds[bird]["activity"][int(math.floor(ytc))] + (((ytc - math.floor(ytc))) * birds[bird]["activity"][int(math.floor(ytc + 1))]))
            except:
                monthActivity = ((1 - (ytc - math.floor(ytc))) * birds[bird]["activity"][int(math.floor(ytc))] + (((ytc - math.floor(ytc))) * birds[bird]["activity"][int(math.floor(0))]))
            dayActivity = tools.getActivity(birdTimes[bird], dayTimesUTC)
            activity = (((monthActivity * dayActivity) / 100) ** (2 - (1 - tools.isHunter(bird)))) * tools.isWater(bird) * tools.isRaven(bird) * tools.isHunter(bird) * random.random() * tools.gullInc(bird, dataArray) * tools.tempDiff(birds[bird], dataArray)
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
            if random.random() < activity:
                if utils.testWindow():
                    audioEvent = audio.event()
                    audioEvent.register(birds[bird]["sounds"][int(math.floor(random.random() * len(birds[bird]["sounds"])))], 6, (((activity / 15) * 10)) * random.random() * tools.isWater(bird) * tools.tempDiff(birds[bird], dataArray) * tools.isRaven(bird) * tools.isCrow(bird), 1, 0, 0)
                    audioEvent.run()
                else:
                    audioEvent = audio.event()
                    audioEvent.register(birds[bird]["sounds"][int(math.floor(random.random() * len(birds[bird]["sounds"])))], 2, (((activity / 15) * 10)) * random.random() * tools.isWater(bird) * tools.isRaven(bird) * tools.tempDiff(birds[bird], dataArray) * tools.isCrow(bird), 1, 0, 0)
                    audioEvent.register(birds[bird]["sounds"][int(math.floor(random.random() * len(birds[bird]["sounds"])))], 3, (((activity / 15) / 16) * 10) * random.random() * tools.isWater(bird) * tools.isRaven(bird) * tools.tempDiff(birds[bird], dataArray) * tools.isCrow(bird), 1, 0, 0)
                    audioEvent.run()
            time.sleep(0.1)
            status.vars["lastLoop"] = pytools.clock.getDateTime()
def run():
    status.hasExited = False
    print("fuck me")
    main()
    status.hasExited = True
