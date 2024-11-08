import modules.pytools as pytools
import modules.audio as audio
import random
import math
import threading
import time
import traceback
import modules.logManager as log
import api.halloween_extension as hallow
import os

print = log.printLog

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": [],
        "storms": {
            "active": {
                
            },
            "stormChance": 0,
            "stormSpawnMinute": 1,
            "canSpawnMoreStorms": True
        }
    }

class globals:
    coords = [45.680600, -62.720807]
    dataArray = []

class utils:
    def dataGrabber():
        out = pytools.IO.getList('.\\dataList.pyl')[1]
        if out == 1:
            out = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        return out

    def dayTimesGrabber():
        dayTimes = pytools.IO.getList('daytimes.pyl')[1]
        if dayTimes == 1:
            dayTimes = [[2022, 5, 11, 3, 45, 15], [2022, 5, 11, 4, 34, 10], [2022, 5, 11, 5, 16, 33], [2022, 5, 11, 5, 48, 29], [2022, 5, 11, 13, 10, 47], [2022, 5, 11, 20, 33, 6], [2022, 5, 11, 21, 5, 2], [2022, 5, 11, 21, 47, 25], [2022, 5, 11, 22, 36, 20]]
        return dayTimes
    
    def getHallowIndex(timeStamp):
        # u = math.floor(timeStamp / (365 * 24 * 60 * 60))
        
        fourYearFloat = timeStamp / (1461 * 24 * 60 * 60)
        
        dayOfFourYears = pytools.clock.getDayOfFourYear(pytools.clock.UTCToDateArray(timeStamp))
        
        dayOfYear = pytools.clock.getDayOfYear(pytools.clock.UTCToDateArray(timeStamp))
        
        u = pytools.clock.UTCToDateArray(timeStamp)[0]
        
        print(u)
        
        # w = (timeStamp - (24 * 60 * 60) - (u * (365 * 24 * 60 * 60)) - 1)
        
        w = ((timeStamp) - (24 * 60 * 60) - (pytools.clock.dateArrayToUTC([u, 1, 1, 0, 0, 0])) - 1) + 86400
        
        print(w)
        print(dayOfYear)
        
        # q = math.floor(math.floor(((u) / (4))) - (((u) / (4))) + 1) * 24 * 60 * 60
        q = 0
        a = 100
        b = 26265600 + q
        c = 3000000000000
        f = 30931200 + q
        g = 300000000000
        p = 3.14159265359
        h = 50
        e = 2.71828182846
        # j = 16 * math.sin((((p) / (1180295.8))) * ( - (w - (((1180295.8) / (2)))) - (u * (365.25 * 24 * 60 * 60))))
        j = 16 * ( - hallow.data.getLunarPhase(pytools.clock.UTCToDateArray(timeStamp)))
        l_2 = 15 * e ** ( - (3 * ((w - 1080000) ** (2)) / (g)))
        l_3 = 15 * e ** ( - (3 * ((w - 3758400) ** (2)) / (g)))
        l_4 = 15 * e ** ( - (3 * (((w - q) - 6177600) ** (2)) / (g)))
        l_5 = 15 * e ** ( - (3 * (((w - q) - 8856000) ** (2)) / (g)))
        l_6 = 15 * e ** ( - (3 * (((w - q) - 11448000) ** (2)) / (g)))
        l_7 = 15 * e ** ( - (3 * (((w - q) - 14126400) ** (2)) / (g)))
        l_8 = 15 * e ** ( - (3 * (((w - q) - 16718400) ** (2)) / (g)))
        l_9 = 15 * e ** ( - (3 * (((w - q) - 19396800) ** (2)) / (g)))
        l_10 = 18 * e ** ( - (1 * (((w - q) - 22075200) ** (2)) / (g)))
        l_11 = 15 * e ** ( - (3 * (((w - q) - 24667200) ** (2)) / (g)))
        l_12 = 15 * e ** ( - (3 * (((w - q) - 27345600) ** (2)) / (g)))
        l_13 = 15 * e ** ( - (3 * (((w - q) - 29937600) ** (2)) / (g)))
        r = 29376000 + q
        s = 27302400 + q
        t = - 2 * ((a * e ** ( - (((w - r) ** (2)) / (c)))) + (h * e ** ( - (((w - r) ** (2)) / (g)))))
        z = - 2 * ((a * e ** ( - (((((w - s) ** (2)) / (c))) / (0.15)))) + (h * e ** ( - (((((w - s) ** (2)) / (g))) / (0.15)))))
        # k = 18 * math.sin((((p) / (302400.0))) * ((w + 36 * 60 * 60) + (u * 365.25 * 24 * 60 * 60) - 6))
        k = 20 * math.sin((((p) / (302400.0))) * ((w + 36 * 60 * 60) + pytools.clock.dateArrayToUTC([u, 1, 1, 0, 0, 0]) - 172800))
        z_1 = 16 * math.sin((((p) / (1180295.8))) * ( - (24778000.0 - (((1180295.8) / (2)))) - (u * (356.25 * 24 * 60 * 60)))) + (7 * math.sin((((p) / (302400.0))) * ((24778000.0 + 12 * 60 * 60) + (u * 365.25 * 24 * 60 * 60) - 6))) + 13
        o = - 3 * ((a * e ** ( - (((w - f) ** (2)) / (c)))) + (h * e ** ( - (((w - f) ** (2)) / (g)))))
        m = (1.11 * (((((math.fabs(z_1 )) / (2)) + 15) / (15)) ** (1) * (a * e ** ( - 0.65 * (((w - b) ** (2)) / (c))))) + (h * e ** ( - 0.65 * (((w - b) ** (2)) / (g))))) + j + k + (2 * (l_2 + l_3 + l_4 + l_5 + l_6 + l_7 + l_8 + l_9 + l_10 + l_11 + l_12 + l_13)) + o + t + z - 40
        weatherModif = hallow.data.getWeatherHallowModifier()
        if weatherModif:
            m = m + weatherModif
        n = - 10 * math.sin(((p) / (12 * 60 * 60)) * (w - 6 * 60 * 60))
        z_2 = ((1) / (2)) * (n * (((m) / (10))) + m)
        return z_2

class storm:
    def __init__(self, cape):
        self.x = 50 - (random.random() * 100)
        self.y = 50 - (random.random() * 100)
        
        if (pytools.clock.getDateTime()[3] > 12) and (pytools.clock.getDateTime()[1] == 10) and (pytools.clock.getDateTime()[2] == 31):
            self.x = 15 * (random.random() - 0.5) * 2
            self.y = 15 * (random.random() - 0.5) * 2
        
        self.vx = 0
        self.vy = 0
        self.stage = 0
        self.cape = cape
        self.strength = 0
        
        self.uuid = random.random()
        
        self.radius = (3 * random.random()) + 0.5
        self.electricalPower = 0
        
        self.notDone = True
        
    def reInitThread(self):
        return threading.Thread(target=self.handler)
        
    def getDistance(self, x, y, randRadius=False):
        if randRadius:
            dis = (((math.fabs(x) ** 2) + (math.fabs(y) ** 2)) ** 0.5) - (self.radius - ((self.radius * 2) * random.random()))
        else:
            dis =  (((math.fabs(x) ** 2) + (math.fabs(y) ** 2)) ** 0.5) - self.radius
        
        if dis < 0.0001:
            dis = 0.0001
        
        return dis
    
    def getLowPass(self, x, y, distance=False):
        
        # https://www.desmos.com/calculator/hu9xpexy30
        
        if distance == False:
            distance = (((math.fabs(x) ** 2) + (math.fabs(y) ** 2)) ** 0.5) - (self.radius - ((self.radius * 2) * random.random()))
            
        if distance < 0.0001:
            distance = 0.0001
        
        a = 0.0798498
        b = 0.145595
        c = 3.91724
        d = 44.6798
        f = 1.01056
        g = -1.52756
        h = -499.998
        j = -117.812
        return (a ** (b * distance - c) + d) + (f ** (g * distance - h) + j)
    
    def getFlashVolume(self, x, y, distance=False):
        
        # https://www.desmos.com/calculator/fli6pnjq4l
        
        if distance == False:
            distance = (((math.fabs(x) ** 2) + (math.fabs(y) ** 2)) ** 0.5) - (self.radius - ((self.radius * 2) * random.random()))
            
        if distance < 0.1:
            distance = 0.1
        
        # a = 2.1064 * (10 ** 17)
        # b = 39.8951
        # c = 29.4434
        # d = -8.36855

        # return a ** ( - 0.0001 * b * (distance - c)) + d
        
        # https://www.desmos.com/calculator/zqlrjk377n
        return 10525451083000 ** ( - 0.00399851 * (distance - 43.3264)) + 0.999944
    
    def setVelocity(self):
        pi = 3.14159265359
        direction = globals.dataArray[0][9]
        speed = globals.dataArray[0][0]
        gusts = globals.dataArray[0][1] * random.random()
        velocity = speed + gusts
        self.vx = (velocity * math.sin(direction / (pi / 180))) / 1000
        self.vy = (velocity * math.cos(direction / (pi / 180))) / 1000
        
    def lightning(self):
        dis = self.getDistance(self.x, self.y, randRadius=True)
        if dis < 0.0001:
            dis = 0.0001
        num = str(random.randint(0, 14))
        volume = self.getFlashVolume(self.x, self.y, dis)
        lowPass = self.getLowPass(self.x, self.y, dis)
        speed = 1.04 - (random.random() * 0.08)
        if lowPass > 0:
            if volume > 0:
                audioEvent = audio.event()
                audioEvent.register("lightning_" + num + ".mp3", 5, volume, speed, 100, 0)
                audioEvent.run()
            time.sleep(math.fabs((dis * 1000) / 343))
            audio.playSoundAll("thunder_" + num + ".mp3", 75 + (volume / 4), speed, 0.0, 0, lowPass=lowPass)
    
    def handler(self):
        exitCount = 0
        while self.notDone and (exitCount < 1000) and not status.exit:
            try:
                self.setVelocity()
                self.x = self.x + self.vx
                self.y = self.y + self.vy
                self.electricalPower = self.electricalPower + (((self.strength / (500 / self.radius)) * random.random()) / 6)
                if self.electricalPower > 100:
                    sound = threading.Thread(target=self.lightning)
                    sound.start()
                    self.electricalPower = 0
                if self.stage == 0:
                    self.radius = self.radius + ((((self.strength / 100) / 1.3) - ((self.strength / 100) * random.random())) / 1000)
                    self.strength = self.strength + (self.cape / 1000) * random.random()
                    if self.strength > self.cape:
                        self.stage = 1
                        self.endStorm = pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()) + self.cape
                elif self.stage == 1:
                    self.radius = self.radius + ((((self.strength / 100) / 2) - ((self.strength / 100) * random.random())) / 1000)
                    self.strength = self.strength + (((self.cape / 1000) / 2) - ((self.cape / 1000) * random.random()))
                    if self.endStorm < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                        self.stage = 2
                else:
                    self.radius = self.radius + ((((self.strength / 100) / 3) - ((self.strength / 100) * random.random())) / 1000)
                    self.strength = self.strength - (self.cape / 1000) * random.random()
                    if self.strength < 0:
                        self.notDone = False
                if self.radius > 25:
                    self.radius = 25
                if self.radius < 0.1:
                    self.notDone = False
                try:
                    lightningDistance = pytools.IO.getJson("lightningData.json")["dangerLevel"]
                    
                    if self.getDistance(self.x, self.y) > ((-lightningDistance) + 25):
                        self.notDone = False
                except:
                    pass
                    
                print("Storm with uuid " + str(self.uuid) + " info: {x: " + str(self.x) + ", y: " + str(self.y) + ", stage: " + str(self.stage) + ", strength: " + str(self.strength) + ", electricalPower: " + str(self.electricalPower) + ", radius: " + str(self.radius) + ", distance: " + str(self.getDistance(self.x, self.y)) + "}")
                status.vars["storms"]["active"][self.uuid] = {
                    "x": self.x,
                    "y": self.y,
                    "vx": self.vx,
                    "vy": self.vy,
                    "stage": self.stage,
                    "capeIndex": self.cape,
                    "strength": self.strength,
                    "radius": self.radius,
                    "electricalPower": self.electricalPower,
                    "distance": self.getDistance(self.x, self.y) 
                }
                exitCount = 0
            except:
                print(traceback.format_exc())
                exitCount = exitCount + 1
            time.sleep(1)
        try:
            status.vars["storms"]["active"].pop(self.uuid)
        except:
            pass
        # storms.stormList.pop(self)
        storms.popList.append(self)
        # pytools.IO.saveList(".\\thunderStorms.pyl", storms.stormList)
        
class storms:
    stormList = []
    popList = []
    
    def start():
        storms.stormList.append(storm(globals.dataArray[0][10]))
        storms.stormList[-1].reInitThread().start()
        pytools.IO.saveList(".\\thunderStorms.pyl", storms.stormList)
        
    def grab():
        try:
            stormList = pytools.IO.getList(".\\thunderStorms.pyl")[1]
            try:
                if len(stormList) != 0:
                    storms.stormList = stormList
                    for thunderStorm in storms.stormList:
                        try:
                            thunderStorm.reInitThread().start()
                        except:
                            pass
            except:
                print(traceback.format_exc())
        except:
            print(traceback.format_exc())
            pytools.IO.saveList(".\\thunderStorms.pyl", storms.stormList)

def main():
    dataTic = -1
    spawnTic = pytools.clock.getDateTime()[4] - 1
    spawnRandom = pytools.clock.getDateTime()[4]
    if spawnRandom >= 60:
        spawnRandom = spawnRandom - 60
    globals.dataArray = utils.dataGrabber()
    if utils.getHallowIndex(pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())) > 0:
        globals.dataArray[0][10] = globals.dataArray[0][10] + (hallow.data.getHallowIndex(pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())) * 18)
    else:
        globals.dataArray[0][10] = globals.dataArray[0][10] + (hallow.data.getHallowIndex(pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())) / 2)
    if not os.path.exists(".\\deleteStorms.derp"):
        storms.grab()
    if storms.stormList == []:
        storms.start()
        
    while not status.exit:
        if dataTic != pytools.clock.getDateTime()[4]:
            dataTic = pytools.clock.getDateTime()[4]
            globals.dataArray = utils.dataGrabber()
            try:
                if utils.getHallowIndex(pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())) > 0:
                    globals.dataArray[0][10] = globals.dataArray[0][10] + (((hallow.data.getHallowIndex(pytools.clock.dateArrayToUTC(pytools.clock.getDateTime())) ** 0.16) - 1) * 2200)
            except:
                print(traceback.format_exc())
                
        try:
            lightningDanger = pytools.IO.getJson("lightningData.json")["dangerLevel"]
            if lightningDanger < -8.7:
                lightningDanger = -8.7
        except:
            lightningDanger = -8.7
        
        def powDecimal(n, d):
            if n < 0:
                return -(abs(n) ** d)
            else:
                return abs(n) ** d
        
        # https://www.desmos.com/calculator/hlkgdy60ii
        # https://www.desmos.com/calculator/fu1lww6yqy
        
        stormChance = (5.69235 ** (0.00398561 * (globals.dataArray[0][10] + (420 * (1.41604 * (powDecimal((lightningDanger + 3), 1/3)) + 2.53986))) - 1.59424)) ** 0.66
        if globals.dataArray[0][4] == "thunder":
            stormChance = stormChance + 100
        status.vars["storms"]["stormChance"] = stormChance
        status.vars["storms"]["stormCount"] = len(status.vars["storms"]["active"])
        status.vars['storms']["stormSpawnMinute"] = spawnRandom
        if (spawnTic != pytools.clock.getDateTime()[4]) and (pytools.clock.getDateTime()[4] == spawnRandom):
            spawnTic = pytools.clock.getDateTime()[4]
            spawnRandom = random.randint(1, 9) + pytools.clock.getDateTime()[4]
            if spawnRandom > 59:
                spawnRandom = spawnRandom - 60
            if (random.random() * 100) < stormChance:
                if len(status.vars["storms"]["active"]) < 3:
                    status.vars["storms"]["canSpawnMoreStorms"] = True
                    storms.start()
                else:
                    status.vars["storms"]["canSpawnMoreStorms"] = False
        time.sleep(1)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        nStart = storms.popList
        changed = False
        for n in nStart:
            try:
                storms.stormList.remove(n)
            except:
                pass
            try:
                storms.popList.remove(n)
            except:
                pass
            
            changed = True
        if changed:
            pytools.IO.saveList(".\\thunderStorms.pyl", storms.stormList)
            
def run():
    status.hasExited = False
    main()
    status.hasExited = True
                
            
            
        
            
    
        
        
        