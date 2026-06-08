import traceback
import concurrent.futures
import threading
import json

import urllib.parse

from scipy.signal import butter, sosfilt

import modules.pytools as pytools
import modules.logManager as logman

print = logman.printLog

import random
import os
import time

executor = concurrent.futures.ThreadPoolExecutor(max_workers=30)

class audioThreadObj:
    def __init__(self, target=pytools.dummy, args=()):
        self.args = args
        self.func = target
        
    def start(self):
        self._instance = executor.submit(self.func, *self.args)
    
    def join(self):
        return self._instance.result()

doMuteOnTrue = True
doMuteOnFalse = False

if not os.path.exists(".\\logs"):
    os.system("mkdir \".\\logs\"")
    
if not os.path.exists(".\\logs\\errors"):
    os.system("mkdir \".\\logs\\errors\"")

class log:
    
    data = []
    hasLogged = False
    dateString = ""
    timeString = ""
    
    def crash(*strff, typef="errors", forceFile=False):
        for strf in strff:    
            print(str(strf))
            
            if (not log.hasLogged) and (not forceFile):
                if not (len(log.data) < 50):
                    log.data.pop(0)
                log.data.append([pytools.clock.getDateTime(), str(strf), str(traceback.format_stack())])
                if ("Traceback" in str(strf)) or ("Error" in str(strf)) or ("error" in str(strf)) or ("Failed" in str(strf)) or ("failed" in str(strf)) or ("Unable" in str(strf)) or ("unable" in str(strf)) or ("WARNING" in str(strf)) or ("Warning" in str(strf)) or ("warning" in str(strf)):
                    dateArray = pytools.clock.getDateTime()
                    if log.dateString == "":
                        log.dateString = str(dateArray[0]) + "-" + str(dateArray[1]) + "-" + str(dateArray[2])
                        log.timeString =  str(dateArray[3]) + "."  + str(dateArray[4]) + "."  + str(dateArray[5]) + "_" + str(time.time() * 100000).split(".")[0]
                    if not os.path.exists(".\\logs\\" + typef + "\\" + log.dateString):
                        os.system("mkdir \".\\logs\\" + typef + "\\" + log.dateString + "\"")
                    for data in log.data:
                        dateArray = data[0]
                        message = str(data[1])
                        callStack = str(data[2])
                        pytools.IO.appendFile(".\\logs\\" + typef + "\\" + log.dateString + "\\event_" + log.timeString + ".log", "\n" + str(dateArray) + " :;: " + message + " :;: " + callStack.replace("\n", "    \\n\t"))
                    log.hasLogged = True
            else:
                dateArray = pytools.clock.getDateTime()
                if not forceFile:
                    pytools.IO.appendFile(".\\logs\\" + typef + "\\" + log.dateString + "\\event_" + log.timeString + ".log", "\n" + str(dateArray) + " :;: " + str(strf) + " :;: " + str(traceback.format_stack()).replace("\n", "    \\n\t"))
                else:
                    pytools.IO.appendFile(".\\logs\\" + typef + "\\event_" + log.dateString + ".log", "\n" + str(dateArray) + " :;: " + str(strf) + " :;: " + str(traceback.format_stack()).replace("\n", "    \\n\t"))

    def audio(strf):
        dateArray = pytools.clock.getDateTime()
        dateString = str(dateArray[0]) + "-" + str(dateArray[1]) + "-" + str(dateArray[2])
        print(str(dateArray) + " ::: " + str(strf))
        if not os.path.exists("..\\working"):
            if not os.path.exists(".\\logs\\audio"):
                os.system("mkdir \".\\logs\\audio\"")
            pytools.IO.appendFile(".\\logs\\audio\\event_" + dateString + ".log", "\n" + str(dateArray) + " :;: " + str(strf))
        else:
            if not os.path.exists("..\\logs\\audio"):
                os.system("mkdir \"..\\logs\\audio\"")
            pytools.IO.appendFile("..\\logs\\audio\\event_" + dateString + ".log", "\n" + str(dateArray) + " :;: " + str(strf))

def printDebug(strf):
    print(strf)

from mutagen.mp3 import MP3
from mutagen.wave import WAVE

# Sound Events
# syncEvents = {
#     "events": [
#         {
#             "path": "",
#             "volume": 0,
#             "speed": 1.0,
#             "channel": "clock",
#             "effects": [
#                 {
#                     "type": "<type>", # lowpass, highpass, remeberbypass
#                     <highpass, lowpass> "freqency": <float>
#                     <highpass, lowpass> "db": <float>
#                 }
#             ],
#             "mute_options": {
#                  "flag_name": "<flagname>" # states the name of the flag
#                  "do_mute": <bool> # states whether the flag being present causes mute or unmutes 0=normal, 1=reverse
#                  "fade": <bool> # do a hard cut or fade the next chunks in and out
#             }
#         },
#     ],
#     "wait": <bool>
# }

class obj:
    activeSounds = {}

testEvent = {
    "events": [
        {
            "path": ".\\sound\\assets\\dnwbella.mp3",
            "volume": 10,
            "speed": 1.3,
            "channel": "fireplace",
            "effects": [
                 {
                     "type": "lowpass",
                     "freqency": 1000,
                     "db": 20
                }
            ]
        },
        {
            "path": ".\\sound\\assets\\dnwbella.mp3",
            "volume": 10,
            "speed": 1.3,
            "channel": "clock",
            "effects": [
                 {
                     "type": "lowpass",
                     "freqency": 1000,
                     "db": 20
                }
            ]
        },
        {
            "path": ".\\sound\\assets\\dnwbella.mp3",
            "volume": 10,
            "speed": 1.3,
            "channel": "window",
            "effects": [
                 {
                     "type": "lowpass",
                     "freqency": 1000,
                     "db": 20
                }
            ]
        },
    ],
    "wait": True
}

class globals:
    bufferSize = 8
    chunkSize = 256
    speakers = {}
    maxCount = 100
    close = False

class tools:
    def testWeights(randomInt, soundsf):
        try:
            percent = 1 - (soundsf[hosts.listf[randomInt]]["current"] / soundsf[hosts.listf[randomInt]]["max"])
            if percent > 1:
                percent = 1
            i = 0
            disparety = 0
            while i < len(hosts.listf):
                try:
                    if i != randomInt:
                        otherPercent = 1 - (soundsf[hosts.listf[i]]["current"] / soundsf[hosts.listf[i]]["max"])
                        if otherPercent > 1:
                            otherPercent = 1
                        if otherPercent < 0:
                            otherPercent = 0
                        disparety = disparety + (percent - otherPercent)
                except:
                    pass
                i = i + 1
            a = 1.87611
            b = 9.35926
            c = 9.35486
            d = -0.00277778
            chance = a ** (b * (percent + disparety) - c) + d
            return chance
        except:
            return 0
        
    def getRandomInt(soundsf):
        try:
            while True:
                try:
                    hosts.listf = pytools.IO.getJson(".\\hosts.json")["hosts"]
                    break
                except:
                    pass
            
            try:
                hosts.listf.remove("0.0.0.0")
            except:
                print("0.0.0.0 is not in list!")
            
            i = 0
            hostWeights = []
            while i < len(hosts.listf):
                hostWeights.append([tools.testWeights(i, soundsf), i])
                i = i + 1
            def key(iter):
                return iter[0]
            maxf = max(hostWeights, key=key)
            hostWeights = sorted(hostWeights, key=key)
            if maxf[0] > 0:
                i = 0
                while i < len(hosts.listf):
                    hostWeights[i][0] = hostWeights[i][0] / maxf[0]
                    i = i + 1
            else:
                return False
            randFloat = random.random()
            i = 0
            while i < len(hosts.listf):
                print(randFloat, hostWeights[i][0])
                if randFloat < hostWeights[i][0]:
                    if tools.ping(hosts.listf[hostWeights[i][1]]):
                        if not os.path.exists(".\\host-" + hosts.listf[hostWeights[i][1]] + ".bl"):
                            if hostWeights[i][1] != "0.0.0.0":
                                return hostWeights[i][1]
                            else:
                                return -1
                        else:
                            return -1
                i = i + 1
            return -1
        except:
            print(traceback.format_exc())
            return -1
    
    def ping(host):
        import subprocess
        return "Lost = 0" in subprocess.getoutput("ping " + host + " -n 1 -w 1")

class report:
    count = 0
    
    def clean():
        
        report.count = True
        
        try:
            for aUuid in list(obj.activeSounds.keys()):
                try:
                    if (pytools.clock.dateArrayToUTC(obj.activeSounds[aUuid][2]) + obj.activeSounds[aUuid][3]) < pytools.clock.dateArrayToUTC(pytools.clock.getDateTime()):
                        os.system("del \"" + "..\\vars\\pluginSounds\\" + str(aUuid) + ".cx" + "\" /f /s /q")
                        try:
                            obj.activeSounds.pop(aUuid)
                        except:
                            print("Could not pop uuid from activeSounds list.")
                    else:
                        if not os.path.exists("..\\vars\\pluginSounds"):
                            os.system("mkdir \"..\\vars\\pluginSounds\"")
                        pytools.IO.saveFile("..\\vars\\pluginSounds\\" + str(aUuid) + ".cx", str(obj.activeSounds[aUuid][0]) + ";" + str(obj.activeSounds[aUuid][1]) + ";" + str(pytools.clock.dateArrayToUTC(obj.activeSounds[aUuid][2])) + ";" + str(obj.activeSounds[aUuid][3]) + ";" + str(obj.activeSounds[aUuid][4]) + ";" + str(obj.activeSounds[aUuid][5]) + ";" + str(obj.activeSounds[aUuid][6]))
                except KeyError:
                    pass
                except:
                    print(traceback.format_exc())
        except:
            print(traceback.format_exc())
            
        report.count = False

class reportSound:
    def __init__(self, uuid):
        self.uuid = uuid
        
    def run(self):
        
        return
        
        report.count = report.count + 1
        
        try:
            if not os.path.exists("..\\vars\\pluginSounds"):
                os.system("mkdir \"..\\vars\\pluginSounds\"")
            pytools.IO.saveFile("..\\vars\\pluginSounds\\" + str(self.uuid) + ".cx", str(obj.activeSounds[self.uuid][0]) + ";" + str(obj.activeSounds[self.uuid][1]) + ";" + str(pytools.clock.dateArrayToUTC(obj.activeSounds[self.uuid][2])) + ";" + str(obj.activeSounds[self.uuid][3]) + ";" + str(obj.activeSounds[self.uuid][4]) + ";" + str(obj.activeSounds[self.uuid][5]) + ";" + str(obj.activeSounds[self.uuid][6]))
            
            try:
                print("report waiting for " + str(obj.activeSounds[self.uuid][3]) + " seconds...")
                time.sleep(obj.activeSounds[self.uuid][3])
            except:
                print(traceback.format_exc())
            os.system("del \"" + "..\\vars\\pluginSounds\\" + str(self.uuid) + ".cx" + "\" /f /s /q")
            try:
                obj.activeSounds.pop(self.uuid)
            except:
                print("Could not pop uuid from activeSounds list.")
        except:
            print(traceback.format_exc())
        
        report.count = report.count - 1
 
class playSoundWindow:
    def __init__(self, path, volume, speed, balence, wait, remember=False, lowPass=False, highPass=False, play=True, sendFile=False, startDelay=0):
        self.path = path
        self.volume = volume
        self.speed = speed
        self.balence = balence
        self.wait = wait
        self.remember = remember
        self.startDelay = startDelay
        self.lowPass = lowPass
        self.highPass = highPass
        self.run(play=play, sendFile=sendFile)
        
    eventData = {}
    
    def getVolume(self, intf):
        if str(self.volume)[0] == "[":
            if intf == 2:
                if len(self.volume) == 3:
                    return self.volume[intf]
                else:
                    return self.volume[1]
            return self.volume[intf]
        else:
            return self.volume
    
    def run(self, play=True, sendFile=False):
        startms = time.time()
        effects = []
        if self.lowPass:
            effects.append({
                "type": "lowpass",
                "frequency": self.lowPass,
                "db": 24
            })
        if self.highPass:
            effects.append({
                "type": "highpass",
                "frequency": self.highPass,
                "db": 24
            })
        if self.remember:
            effects.append({
                "type": "rememberbypass",
            })
        
        if self.path.split(";")[0] != self.path:
            eventData = {
                "events": [
                    {
                        "path": ".\\working\\sound\\assets\\" + self.path.split(";")[0],
                        "volume": self.getVolume(0),
                        "speed": self.speed,
                        "balence": self.balence,
                        "channel": "window",
                        "effects": effects,
                        "mute_options": {
                            "flag_name": "nomufflewn",
                            "do_mute": doMuteOnTrue,
                            "fade": True
                        },
                        "start_delay": self.startDelay
                    },
                    {
                        "path": ".\\working\\sound\\assets\\" + self.path.split(";")[1],
                        "volume": self.getVolume(1),
                        "speed": self.speed,
                        "balence": self.balence,
                        "channel": "window",
                        "effects": effects,
                        "mute_options": {
                            "flag_name": "nomufflewn",
                            "do_mute": doMuteOnFalse,
                            "fade": True
                        },
                        "start_delay": self.startDelay
                    },
                    {
                        "path": ".\\working\\sound\\assets\\" + self.path.split(";")[1],
                        "volume": self.getVolume(1),
                        "speed": self.speed,
                        "balence": self.balence,
                        "channel": "outside",
                        "effects": effects,
                        "start_delay": self.startDelay
                    }
                ],
                "wait": self.wait,
                "rememberanceBypass": self.remember
            }
            
            if len(self.path.split(";")) > 2:
                eventData["events"].append({
                    "path": ".\\working\\sound\\assets\\" + self.path.split(";")[2],
                    "volume": self.getVolume(2),
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "porch",
                    "effects": effects,
                    "start_delay": self.startDelay
                })
            else:
                eventData["events"].append({
                    "path": ".\\working\\sound\\assets\\" + self.path.split(";")[1],
                    "volume": self.getVolume(2),
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "porch",
                    "effects": effects,
                    "start_delay": self.startDelay
                })
            
            uuid = random.random()
            while uuid in obj.activeSounds:
                uuid = random.random()
            if self.path.split(";")[1].find(".mp3") != -1:
                duration = float(MP3(".\\sound\\assets\\" + self.path.split(";")[1]).info.length) / self.speed
            else:
                duration = float(WAVE(".\\sound\\assets\\" + self.path.split(";")[1]).info.length) / self.speed
            obj.activeSounds[uuid] = [self.path.split(";")[1].split("\\")[-1], "outside", pytools.clock.getDateTime(), duration, self.getVolume(1), self.speed, self.wait]
            soundReportObj = reportSound(uuid)
            # audioThreadObj(target=soundReportObj.run).start()
            uuid = random.random()
            while uuid in obj.activeSounds:
                uuid = random.random()
            if self.path.split(";")[0].find(".mp3") != -1:
                duration = float(MP3(".\\sound\\assets\\" + self.path.split(";")[0]).info.length) / self.speed
            else:
                duration = float(WAVE(".\\sound\\assets\\" + self.path.split(";")[0]).info.length) / self.speed
            obj.activeSounds[uuid] = [self.path.split(";")[0].split("\\")[-1], "window", pytools.clock.getDateTime(), duration, self.getVolume(0), self.speed, self.wait]
            soundReportObj = reportSound(uuid)
            # audioThreadObj(target=soundReportObj.run).start()
        else:
            eventData = {
                "events": [
                    {
                        "path": ".\\working\\sound\\assets\\" + self.path,
                        "volume": self.getVolume(0),
                        "speed": self.speed,
                        "balence": self.balence,
                        "channel": "window",
                        "effects": effects,
                        "mute_options": {
                            "flag_name": "nomufflewn",
                            "do_mute": doMuteOnTrue,
                            "fade": True
                        },
                        "start_delay": self.startDelay
                    },
                    {
                        "path": ".\\working\\sound\\assets\\" + self.path,
                        "volume": self.getVolume(1),
                        "speed": self.speed,
                        "balence": self.balence,
                        "channel": "window",
                        "effects": effects,
                        "mute_options": {
                            "flag_name": "nomufflewn",
                            "do_mute": doMuteOnFalse,
                            "fade": True
                        },
                        "start_delay": self.startDelay
                    },
                    {
                        "path": ".\\working\\sound\\assets\\" + self.path,
                        "volume": self.getVolume(1),
                        "speed": self.speed,
                        "balence": self.balence,
                        "channel": "outside",
                        "effects": effects,
                        "start_delay": self.startDelay
                    },
                    {
                        "path": ".\\working\\sound\\assets\\" + self.path,
                        "volume": self.getVolume(2),
                        "speed": self.speed,
                        "balence": self.balence,
                        "channel": "porch",
                        "effects": effects,
                        "start_delay": self.startDelay
                    }
                ],
                "wait": self.wait,
                "rememberanceBypass": self.remember
            }
            uuid = random.random()
            while uuid in obj.activeSounds:
                uuid = random.random()
            if self.path.find(".mp3") != -1:
                duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
            else:
                duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
            obj.activeSounds[uuid] = [self.path.split("\\")[-1], "outside", pytools.clock.getDateTime(), duration, self.getVolume(1), self.speed, self.wait]
            soundReportObj = reportSound(uuid)
            # audioThreadObj(target=soundReportObj.run).start()
            uuid = random.random()
            while uuid in obj.activeSounds:
                uuid = random.random()
            if self.path.find(".mp3") != -1:
                duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
            else:
                duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
            obj.activeSounds[uuid] = [self.path.split("\\")[-1], "window", pytools.clock.getDateTime(), duration, self.getVolume(0), self.speed, self.wait]
            soundReportObj = reportSound(uuid)
            # audioThreadObj(target=soundReportObj.run).start()
        self.eventData = eventData
        if play:
            
            played = False
            
            startms = time.time()
                
            def grabHostData():
                try:
                    hostList = pytools.IO.getJson(".\\hosts.json")["hosts"]
                    if "0.0.0.0" in hostList:
                        hostList.remove("0.0.0.0")
                        
                    hosts.listf = hostList
                except:
                    print("Could not grab hosts list.")
                
                try:
                    hostData = pytools.IO.getJson(".\\hostData.json")
                    if "0.0.0.0" in hostList:
                        hostData.pop("0.0.0.0")
                        
                    hosts.soundsf = hostData
                except:
                    print("Could not grab hosts list.")
            
            grabHostData()        
            
            try:
                def getHostToSendTo():
                    
                    if (type(hosts.listf) == bool) or (hosts.listf == []) or (random.random() < 0.5):
                        return pytools.IO.getJson("..\\serverSettings.json")["ip"]
                    
                    randomInt = -1
                    
                    doContinue = True
                    
                    while doContinue:
                        try:
                            randomInt = tools.getRandomInt(hosts.soundsf)
                            
                            if randomInt >= len(hosts.listf):
                                randomInt = -1
                                grabHostData()
                            else:
                                
                                if hosts.listf[randomInt] == pytools.IO.getJson("..\\serverSettings.json")["ip"]:
                                    return pytools.IO.getJson("..\\serverSettings.json")["ip"]
                                
                                if hosts.listf[randomInt] in hosts.soundsf:
                                    if (randomInt != -1) and (not os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl")) and (not os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl")) and (hosts.soundsf[hosts.listf[randomInt]]["play"] == True) and (os.path.exists(".\\host-" + hosts.listf[randomInt] + ".se")) and (os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".se")):
                                        if tools.ping(hosts.listf[randomInt]):
                                            break
                                else:
                                    randomInt = -1
                                    grabHostData()
                                time.sleep(random.random())
                                print("No hosts connected. Waiting for connection...")

                            doContinue = (randomInt == -1) or (os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl")) or (os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl")) or (hosts.soundsf[hosts.listf[randomInt]]["play"] == False) or (os.path.exists(".\\host-" + hosts.listf[randomInt] + ".se")) or (os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".se"))
                        
                        except:
                            doContinue = True
                            print(traceback.format_exc())
                            
                            
                            
                    return randomInt
                
                randomInt = getHostToSendTo()
                if type(randomInt) == str:
                    hosts.listf = [randomInt]
                    randomInt = 0
                
                def getPort(host):
                    if host == pytools.IO.getJson("..\\serverSettings.json")["ip"]:
                        return 5597
                    return 4507
                
                try:
                    if not sendFile:
                        def runSound(randomInt):
                            try:
                                hasFired = False
                                errorCount = 0
                                while (not hasFired) and (errorCount < 100):
                                    try:
                                        pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":" + str(getPort(hosts.listf[randomInt])) + "?json=" + urllib.parse.quote(json.dumps({
                                            "command": "fireEvent",
                                            "data": pytools.cipher.base64_encode(json.dumps(self.eventData))
                                        })), timeout=10)
                                        hasFired = True
                                    except:
                                        import traceback
                                        print(traceback.format_exc())
                                        errorCount = errorCount + 1
                                        if errorCount > 1000:
                                            log.audio("Failed audio event.")
                                            log.audio(str(self.eventData))
                                            log.audio(traceback.format_exc())
                                            log.crash("Failed audio event.")
                                            log.crash(str(self.eventData))
                                            log.crash(traceback.format_exc())
                                        else:
                                            log.audio("Failed to send audio event. Trying again...")
                                        grabHostData()
                                        randomInt = getHostToSendTo()
                                        if type(randomInt) == str:
                                            hosts.listf = [randomInt]
                                            randomInt = 0
                                        print("Trying again on host " + hosts.listf[randomInt] + "...")
                                    time.sleep(0.1)
                            except:
                                
                                atraceback = traceback.format_exc()
                                print(atraceback)
                                
                                log.audio("Failed audio event.")
                                log.audio(str(self.eventData))
                                log.audio(atraceback)
                                log.crash("Failed audio event.")
                                log.crash(str(self.eventData))
                                log.crash(atraceback)
                            try:
                                endms = time.time()
                                log.audio("RandomIndex: " + str(randomInt))
                                pytools.IO.appendFile("fire_times.cxl", "\n" + str(hosts.listf[randomInt]) + ", " + str(endms - startms) + ", " + str(self.eventData))
                            except:
                                log.audio(traceback.format_exc())
                        audioThreadObj(target=runSound, args=(randomInt,)).start()
                        played = True
                        for sound in self.eventData["events"]:
                            dateArray = pytools.clock.getDateTime()
                            
                            logError = True
                            while logError:
                                try:
                                    log.audio("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                                    logError = False
                                except:
                                    pass
                    else:
                        def runSound(randomInt):
                            try:
                                print(self.eventData["events"][0]["path"])
                                hasFired = False
                                errorCount = 0
                                while (not hasFired) and (errorCount < 100):
                                    try:
                                        pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":" + str(getPort(hosts.listf[randomInt])) + "?json=" + urllib.parse.quote(json.dumps({
                                            "command": "fireEvent",
                                            "data": pytools.cipher.base64_encode(json.dumps(self.eventData)),
                                            "fileData": {
                                                "data" : pytools.cipher.base64_encode(pytools.IO.getBytes(self.eventData["events"][0]["path"].replace(".\\working\\", ".\\")), isBytes=True),
                                                "fileName": self.eventData["events"][0]["path"].split("\\")[-1]
                                            }
                                        })), timeout=10)
                                        hasFired = True
                                    except:
                                        print(traceback.format_exc())
                                        errorCount = errorCount + 1
                                        if errorCount > 1000:
                                            log.audio("Failed audio event.")
                                            log.audio(str(self.eventData))
                                            log.audio(traceback.format_exc())
                                            log.crash("Failed audio event.")
                                            log.crash(str(self.eventData))
                                            log.crash(traceback.format_exc())
                                        else:
                                            log.audio("Failed to send audio event. Trying again...")
                                        grabHostData()
                                        randomInt = getHostToSendTo()
                                        if type(randomInt) == str:
                                            hosts.listf = [randomInt]
                                            randomInt = 0
                                        print("Trying again on host " + hosts.listf[randomInt] + "...")
                                    time.sleep(0.1)
                            except:
                                log.audio("Failed audio event.")
                                log.audio(str(self.eventData))
                                log.audio(traceback.format_exc())
                                log.crash("Failed audio event.")
                                log.crash(str(self.eventData))
                                log.crash(traceback.format_exc())
                            try:
                                endms = time.time()
                                pytools.IO.appendFile("fire_times.cxl", "\n" + str(hosts.listf[randomInt]) + ", " + str(endms - startms) + ", " + str(self.eventData))
                            except:
                                print(traceback.format_exc())
                        audioThreadObj(target=runSound, args=(randomInt,)).start()
                        played = True
                        for sound in self.eventData["events"]:
                            dateArray = pytools.clock.getDateTime()
                            
                            logError = True
                            while logError:
                                try:
                                    log.audio("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                                    logError = False
                                except:
                                    pass
                            # print("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                except:
                    print(traceback.format_exc())
            except:
                log.audio("Failed to send audio event. Trying again...")
                log.audio(str(self.eventData))
                log.audio(traceback.format_exc())
                log.crash("Failed to send audio event. Trying again...")
                log.crash(str(self.eventData))
                log.crash(traceback.format_exc())
            time.sleep(1)
            if self.eventData["wait"]:
                time.sleep(duration)
            if played != True:
                log.audio("Failed audio event.")
                log.audio(str(self.eventData))
                
        if not report.count:
            audioThreadObj(target=report.clean).start()

class playSoundAll:
    def __init__(self, path, volume, speed, balence, wait, remember=False, lowPass=False, highPass=False, sendFile=False, startDelay=0, play=True):
        self.path = path
        self.volume = volume
        self.speed = speed
        self.balence = balence
        self.wait = wait
        self.remember = remember
        self.lowPass = lowPass
        self.highPass = highPass
        self.startDelay = startDelay
        
        self.run(sendFile=sendFile, play=play)
    
    def run(self, sendFile=False, play=True):
        startms = time.time()
        effects = []
        if self.lowPass:
            effects.append({
                "type": "lowpass",
                "frequency": self.lowPass,
                "db": 24
            })
        if self.highPass:
            effects.append({
                "type": "highpass",
                "frequency": self.highPass,
                "db": 24
            })
        if self.remember:
            effects.append({
                "type": "rememberbypass",
            })
        
        self.eventData = {
            "events": [
                {
                    "path": ".\\working\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "clock",
                    "effects": effects,
                    "start_delay": self.startDelay
                },
                {
                    "path": ".\\working\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "generic",
                    "effects": effects,
                    "start_delay": self.startDelay
                },
                {
                    "path": ".\\working\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "fireplace",
                    "effects": effects,
                    "start_delay": self.startDelay
                },
                {
                    "path": ".\\working\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "window",
                    "effects": effects,
                    "start_delay": self.startDelay
                },
                {
                    "path": ".\\working\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "outside",
                    "effects": effects,
                    "start_delay": self.startDelay
                },
                {
                    "path": ".\\working\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "porch",
                    "effects": effects,
                    "start_delay": self.startDelay
                },
            ],
            "wait": self.wait,
            "rememberanceBypass": self.remember
        }
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [self.path.split("\\")[-1], "clock", pytools.clock.getDateTime(), duration, self.volume, self.speed, self.wait]
        soundReportObj = reportSound(uuid)
        # audioThreadObj(target=soundReportObj.run).start()
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [self.path.split("\\")[-1], "generic", pytools.clock.getDateTime(), duration, self.volume, self.speed, self.wait]
        soundReportObj = reportSound(uuid)
        # audioThreadObj(target=soundReportObj.run).start()
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [self.path.split("\\")[-1], "fireplace", pytools.clock.getDateTime(), duration, self.volume, self.speed, self.wait]
        soundReportObj = reportSound(uuid)
        # audioThreadObj(target=soundReportObj.run).start()
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [self.path.split("\\")[-1], "windown", pytools.clock.getDateTime(), duration, self.volume, self.speed, self.wait]
        soundReportObj = reportSound(uuid)
        # audioThreadObj(target=soundReportObj.run).start()
        
        
        startms = time.time()
        
        if play:
        
            played = False
                
            def grabHostData():
                
                try:
                    hostList = pytools.IO.getJson(".\\hosts.json")["hosts"]
                    if "0.0.0.0" in hostList:
                        hostList.remove("0.0.0.0")
                        
                    hosts.listf = hostList
                except:
                    print("Could not grab hosts list.")
                
                try:
                    hostData = pytools.IO.getJson(".\\hostData.json")
                    if "0.0.0.0" in hostList:
                        hostData.pop("0.0.0.0")
                        
                    hosts.soundsf = hostData
                except:
                    print("Could not grab hosts list.")
            
            grabHostData()        
            
            try:
                def getHostToSendTo():
                    
                    if (type(hosts.listf) == bool) or (hosts.listf == []) or (random.random() < 0.5):
                        return pytools.IO.getJson("..\\serverSettings.json")["ip"]
                    
                    randomInt = -1
                    while (randomInt == -1) or (os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl")) or (os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl")) or (hosts.soundsf[hosts.listf[randomInt]]["play"] == False) or (os.path.exists(".\\host-" + hosts.listf[randomInt] + ".se")) or (os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".se")):
                        randomInt = tools.getRandomInt(hosts.soundsf)
                        if hosts.listf[randomInt] in hosts.soundsf:
                            if (randomInt != -1) and (not os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl")) and (not os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl")) and (hosts.soundsf[hosts.listf[randomInt]]["play"] == True) and (os.path.exists(".\\host-" + hosts.listf[randomInt] + ".se")) and (os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".se")):
                                if tools.ping(hosts.listf[randomInt]):
                                    break
                        else:
                            randomInt = -1
                            grabHostData()
                        time.sleep(random.random())
                        print("No hosts connected. Waiting for connection...")
                    return randomInt
                
                randomInt = getHostToSendTo()
                if type(randomInt) == str:
                    hosts.listf = [randomInt]
                    randomInt = 0
                    
                def getPort(host):
                    if host == pytools.IO.getJson("..\\serverSettings.json")["ip"]:
                        return 5597
                    return 4507
                
                try:
                    if not sendFile:
                        def runSound(randomInt):
                            try:
                                hasFired = False
                                errorCount = 0
                                while (not hasFired) and (errorCount < 100):
                                    try:
                                        pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":" + str(getPort(hosts.listf[randomInt])) + "?json=" + urllib.parse.quote(json.dumps({
                                            "command": "fireEvent",
                                            "data": pytools.cipher.base64_encode(json.dumps(self.eventData))
                                        })), timeout=10)
                                        hasFired = True
                                    except:
                                        import traceback
                                        print(traceback.format_exc())
                                        errorCount = errorCount + 1
                                        if errorCount > 1000:
                                            log.audio("Failed audio event.")
                                            log.audio(str(self.eventData))
                                            log.audio(traceback.format_exc())
                                            log.crash("Failed audio event.")
                                            log.crash(str(self.eventData))
                                            log.crash(traceback.format_exc())
                                        else:
                                            log.audio("Failed to send audio event. Trying again...")
                                        grabHostData()
                                        randomInt = getHostToSendTo()
                                        if type(randomInt) == str:
                                            hosts.listf = [randomInt]
                                            randomInt = 0
                                        print("Trying again on host " + hosts.listf[randomInt] + "...")
                                    time.sleep(0.1)
                            except:
                                log.audio("Failed audio event.")
                                log.audio(str(self.eventData))
                                log.audio(traceback.format_exc())
                                log.crash("Failed audio event.")
                                log.crash(str(self.eventData))
                                log.crash(traceback.format_exc())
                            try:
                                endms = time.time()
                                pytools.IO.appendFile("fire_times.cxl", "\n" + str(hosts.listf[randomInt]) + ", " + str(endms - startms) + ", " + str(self.eventData))
                            except:
                                print(traceback.format_exc())
                        audioThreadObj(target=runSound, args=(randomInt,)).start()
                        played = True
                        for sound in self.eventData["events"]:
                            dateArray = pytools.clock.getDateTime()
                            
                            logError = True
                            while logError:
                                try:
                                    log.audio("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                                    logError = False
                                except:
                                    pass
                            # print("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                    else:
                        def runSound(randomInt):
                            try:
                                print(self.eventData["events"][0]["path"])
                                hasFired = False
                                errorCount = 0
                                while (not hasFired) and (errorCount < 1000):
                                    try:
                                        pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":" + str(getPort(hosts.listf[randomInt])) + "?json=" + urllib.parse.quote(json.dumps({
                                            "command": "fireEvent",
                                            "data": pytools.cipher.base64_encode(json.dumps(self.eventData)),
                                            "fileData": {
                                                "data" : pytools.cipher.base64_encode(pytools.IO.getBytes(self.eventData["events"][0]["path"].replace(".\\working\\", ".\\")), isBytes=True),
                                                "fileName": self.eventData["events"][0]["path"].split("\\")[-1]
                                            }
                                        })), timeout=10)
                                        hasFired = True
                                    except:
                                        import traceback
                                        print(traceback.format_exc())
                                        errorCount = errorCount + 1
                                        if errorCount > 100:
                                            log.audio("Failed audio event.")
                                            log.audio(str(self.eventData))
                                            log.audio(traceback.format_exc())
                                            log.crash("Failed audio event.")
                                            log.crash(str(self.eventData))
                                            log.crash(traceback.format_exc())
                                        else:
                                            log.audio("Failed to send audio event. Trying again...")
                                        grabHostData()
                                        randomInt = getHostToSendTo()
                                        if type(randomInt) == str:
                                            hosts.listf = [randomInt]
                                            randomInt = 0
                                        print("Trying again on host " + hosts.listf[randomInt] + "...")
                                    time.sleep(0.1)
                            except:
                                log.audio("Failed audio event.")
                                log.audio(str(self.eventData))
                                log.audio(traceback.format_exc())
                                log.crash("Failed audio event.")
                                log.crash(str(self.eventData))
                                log.crash(traceback.format_exc())
                            try:
                                endms = time.time()
                                pytools.IO.appendFile("fire_times.cxl", "\n" + str(hosts.listf[randomInt]) + ", " + str(endms - startms) + ", " + str(self.eventData))
                            except:
                                print(traceback.format_exc())
                        audioThreadObj(target=runSound, args=(randomInt,)).start()
                        played = True
                        for sound in self.eventData["events"]:
                            dateArray = pytools.clock.getDateTime()
                            
                            logError = True
                            while logError:
                                try:
                                    log.audio("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                                    logError = False
                                except:
                                    pass
                            # print("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                except:
                    print(traceback.format_exc())
            except:
                log.audio("Failed to send audio event. Trying again...")
                log.audio(str(self.eventData))
                log.audio(traceback.format_exc())
                log.crash("Failed to send audio event. Trying again...")
                log.crash(str(self.eventData))
                log.crash(traceback.format_exc())
            time.sleep(1)
            if self.eventData["wait"]:
                time.sleep(duration)
            if played != True:
                log.audio("Failed audio event.")
                log.audio(str(self.eventData))
                
        if not report.count:
            audioThreadObj(target=report.clean).start()
                
class event:
    def __init__(self):
        self.eventData = {
            "events": [],
            "wait": False,
            "rememberanceBypass": False
        }
    
    eventData = {
        "events": [],
        "wait": False,
        "rememberanceBypass": False
    }
    
    def registerWindow(self, path, volume, speed, balence, wait, remember=False, lowPass=False, highPass=False, startDelay=0, forceWait=False):
        _event = playSoundWindow(path, volume, speed, balence, wait, remember=remember, lowPass=lowPass, highPass=highPass, play=False, startDelay=startDelay)
        self.eventData["events"].extend(_event.eventData["events"])
        durations = [0]
        
            
        if _event.eventData["events"][0]["path"].split("\\")[-1].find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + _event.eventData["events"][0]["path"].split("\\")[-1]).info.length) / speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + _event.eventData["events"][0]["path"].split("\\")[-1]).info.length) / speed
        
        durations.append(duration)
        
        uuid = random.random()
        obj.activeSounds[uuid] = [_event.eventData["events"][0]["path"].split("\\")[-1], "window", pytools.clock.getDateTime(), duration, _event.eventData["events"][0]["volume"], _event.eventData["events"][0]["speed"], wait]
        soundReportObj = reportSound(uuid)
        # audioThreadObj(target=soundReportObj.run).start()
        
        uuid = random.random()
        obj.activeSounds[uuid] = [_event.eventData["events"][1]["path"].split("\\")[-1], "outside", pytools.clock.getDateTime(), duration, _event.eventData["events"][0]["volume"], _event.eventData["events"][0]["speed"], wait]
        soundReportObj = reportSound(uuid)
        # audioThreadObj(target=soundReportObj.run).start()
        
        if forceWait and max(durations):
            time.sleep(max(durations))
        
        try:
            return max(durations)
        except:
            return 0
        
    def registerAll(self, path, volume, speed, balence, wait, remember=False, lowPass=False, highPass=False, startDelay=0, forceWait=False):
        _event = playSoundAll(path, volume, speed, balence, wait, remember=remember, lowPass=lowPass, highPass=highPass, play=False, startDelay=startDelay)
        self.eventData["events"].extend(_event.eventData["events"])
        durations = [0]
        
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
            
        durations.append(duration)
        
        obj.activeSounds[uuid] = [_event.eventData["events"][0]["path"].split("\\")[-1], "clock", pytools.clock.getDateTime(), duration, _event.eventData["events"][0]["volume"], _event.eventData["events"][0]["speed"], _event.eventData["wait"]]
        soundReportObj = reportSound(uuid)
        # audioThreadObj(target=soundReportObj.run).start()
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [_event.eventData["events"][0]["path"].split("\\")[-1], "outside", pytools.clock.getDateTime(), duration, _event.eventData["events"][0]["volume"], _event.eventData["events"][0]["speed"], _event.eventData["wait"]]
        soundReportObj = reportSound(uuid)
        # audioThreadObj(target=soundReportObj.run).start()
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [_event.eventData["events"][0]["path"].split("\\")[-1], "fireplace", pytools.clock.getDateTime(), duration, _event.eventData["events"][0]["volume"], _event.eventData["events"][0]["speed"], _event.eventData["wait"]]
        soundReportObj = reportSound(uuid)
        # audioThreadObj(target=soundReportObj.run).start()
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [_event.eventData["events"][0]["path"].split("\\")[-1], "window", pytools.clock.getDateTime(), duration, _event.eventData["events"][0]["volume"], _event.eventData["events"][0]["speed"], _event.eventData["wait"]]
        soundReportObj = reportSound(uuid)
        # audioThreadObj(target=soundReportObj.run).start()
        
        if forceWait and max(durations):
            time.sleep(max(durations))
            
        return max(durations)
        
        
    def register(self, path, speaker, volume, speed, balence, wait, clock=True, remember=False, lowPass=False, highPass=False, keepLoaded=False, muteFlag=False, defaultMuteState=False, muteFade=False, startDelay=0, forceWait=False):
        
        printDebug(path + ", " + str(volume))
        
        if wait:
            self.eventData["wait"] = True
            
        effects = []
        if lowPass:
            effects.append({
                "type": "lowpass",
                "frequency": lowPass,
                "db": 24
            })
        if highPass:
            effects.append({
                "type": "highpass",
                "frequency": highPass,
                "db": 24
            })
        
        rememberanceBypass = False
        if remember:
            effects.append({
                "type": "rememberbypass",
            })
            self.eventData["rememberanceBypass"] = True
        
        if speaker == 0:
            if clock:
                speakern = ["clock", "generic"]
            else:
                speakern = ["clock"]
        elif speaker == 1:
            speakern = ["fireplace"]
        elif speaker == 2:
            speakern = ["window"]
        elif speaker == 3:
            speakern = ["outside"]
        elif speaker == 5:
            speakern = ["light"]
        elif speaker == 7:
            speakern = ["generic"]
        elif speaker == 8:
            speakern = ["window", "outside", "porch"]
        elif speaker == 9:
            speakern = ["porch"]
        else:
            speakern = ["generic"]
        
        waitDuration = 0
        
        if type(volume) == complex:
            volume = 0
        
        if type(speed) == complex:
            return 1
        
        for channel in speakern:
            self.eventData["events"].append({
                "path": ".\\working\\sound\\assets\\" + path,
                "volume": volume,
                "speed": speed,
                "channel": channel,
                "balence": balence,
                "effects": effects,
                "start_delay": startDelay
            })
            
            if muteFlag !=False:
                self.eventData["events"][-1]["mute_options"] = {}
                self.eventData["events"][-1]["mute_options"]["flag_name"] = muteFlag
                self.eventData["events"][-1]["mute_options"]["do_mute"] = defaultMuteState
                self.eventData["events"][-1]["mute_options"]["fade"] = muteFade
            
            uuid = random.random()
            while uuid in obj.activeSounds:
                uuid = random.random()
            if path.find(".mp3") != -1:
                duration = float(MP3(".\\sound\\assets\\" + path).info.length) / speed
            else:
                duration = float(WAVE(".\\sound\\assets\\" + path).info.length) / speed
            
            waitDuration = duration
            
            try:
                if self.duration < duration:
                    self.duration = duration
            except:
                self.duration = duration
            obj.activeSounds[uuid] = [path.split("\\")[-1], channel, pytools.clock.getDateTime(), duration, volume, speed, wait]
            soundReportObj = reportSound(uuid)
            # audioThreadObj(target=soundReportObj.run).start()
            
        if forceWait:
            time.sleep(waitDuration)
            
        return waitDuration
    
    def run(self, spawnChild=True, sendFile=False, largeFile=False):
        played = False
        startms = time.time()
        
        def grabHostData():
            
            try:
                hostList = pytools.IO.getJson(".\\hosts.json")["hosts"]
                if "0.0.0.0" in hostList:
                    hostList.remove("0.0.0.0")
                    
                hosts.listf = hostList
            except:
                print("Could not grab hosts list.")
            
            try:
                hostData = pytools.IO.getJson(".\\hostData.json")
                if "0.0.0.0" in hostList:
                    hostData.pop("0.0.0.0")
                    
                hosts.soundsf = hostData
            except:
                print("Could not grab hosts list.")
        
        grabHostData()        
        
        try:
            def getHostToSendTo():
                
                if (type(hosts.listf) == bool) or (hosts.listf == []) or (random.random() < 0.5):
                    return pytools.IO.getJson("..\\serverSettings.json")["ip"]
                
                randomInt = -1
                while (randomInt == -1) or (randomInt not in hosts.listf) or (os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl")) or (os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl")) or (hosts.soundsf[hosts.listf[randomInt]]["play"] == False) or (os.path.exists(".\\host-" + hosts.listf[randomInt] + ".se")) or (os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".se")):
                    randomInt = tools.getRandomInt(hosts.soundsf)
                    if hosts.listf[randomInt] in hosts.soundsf:
                        print("a1")
                        try:
                            if (randomInt != -1) and (not os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl")) and (not os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl")) and (hosts.soundsf[hosts.listf[randomInt]]["play"] == True) and (not os.path.exists(".\\host-" + hosts.listf[randomInt] + ".se")) and (not os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".se")):
                                print("a2")
                                if tools.ping(hosts.listf[randomInt]):
                                    print("a3")
                                    break
                        except KeyError:
                            print("key error. (" + str(randomInt) + ")")
                            try:
                                print("key error. (" + str(hosts.listf[randomInt]) + ")")
                            except:
                                print("key error. (listf)")
                        except TypeError:
                            print("type error. (" + str(randomInt) + ")")
                            try:
                                print("type error. (" + str(hosts.listf[randomInt]) + ")")
                            except:
                                print("type error. (listf)")
                            
                    
                    randomInt = -1
                    grabHostData()

                    time.sleep(random.random())
                    print("No hosts connected. Waiting for connection...")
                return randomInt
            
            randomInt = getHostToSendTo()
            if type(randomInt) == str:
                hosts.listf = [randomInt]
                randomInt = 0
            
            def getPort(host):
                if host == pytools.IO.getJson("..\\serverSettings.json")["ip"]:
                    return 5597
                return 4507
            
            if sendFile and largeFile:
                fileBytes = pytools.IO.getBytes(self.eventData["events"][0]["path"].replace(".\\working\\", ".\\"))
                bytesI = 0
                isFirstSend = True
                while (bytesI * 1000) < len(fileBytes):
                    hasSentBytes = False
                    errorCount = 0
                    while (not hasSentBytes) and (errorCount < 100):
                        try:
                            pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":" + str(getPort(hosts.listf[randomInt])) + "?json=" + urllib.parse.quote(json.dumps({
                                "command": "sendAudioData",
                                "data": {
                                    "fileName": self.eventData["events"][0]["path"],
                                    "fileData": pytools.cipher.base64_encode(fileBytes[bytesI * 1000:(bytesI + 1) * 1000], isBytes=True),
                                    "isFirstSend": isFirstSend
                                }
                            })), timeout=10)
                            isFirstSend = False
                            hasSentBytes = True
                        except:
                            import traceback
                            print(traceback.format_exc())
                            errorCount = errorCount + 1
                            if errorCount > 100:
                                log.audio("Failed audio event.")
                                log.audio(str(self.eventData))
                                log.audio(traceback.format_exc())
                                log.crash("Failed audio event.")
                                log.crash(str(self.eventData))
                                log.crash(traceback.format_exc())
                            else:
                                log.audio("Failed to send audio event. Trying again...")
                            grabHostData()
                            randomInt = getHostToSendTo()
                            if type(randomInt) == str:
                                hosts.listf = [randomInt]
                                randomInt = 0
                    bytesI = bytesI + 1
                
                sendFile = False
            
            try:
                if not sendFile:
                    def runSound(randomInt):
                        try:
                            hasFired = False
                            errorCount = 0
                            while (not hasFired) and (errorCount < 1000):
                                try:
                                    pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":" + str(getPort(hosts.listf[randomInt])) + "?json=" + urllib.parse.quote(json.dumps({
                                        "command": "fireEvent",
                                        "data": pytools.cipher.base64_encode(json.dumps(self.eventData))
                                    })), timeout=10)
                                    hasFired = True
                                except:
                                    import traceback
                                    _trace = traceback.format_exc()
                                    print(_trace)
                                    errorCount = errorCount + 1
                                    if errorCount > 1000:
                                        uuid = random.randint(0, 11111111111)
                                        log.audio(str(uuid) + ": Failed audio event.")
                                        log.audio(str(uuid) + ": " + str(self.eventData))
                                        log.audio(str(uuid) + ": " + _trace)
                                        log.crash(str(uuid) + ": Failed audio event.")
                                        log.crash(str(uuid) + ": " + str(self.eventData))
                                        log.crash(str(uuid) + ": " + _trace)
                                    else:
                                        log.audio("Failed to send audio event. Trying again...")
                                    grabHostData()
                                    randomInt = getHostToSendTo()
                                    if type(randomInt) == str:
                                        hosts.listf = [randomInt]
                                        randomInt = 0
                                    print("Trying again on host " + hosts.listf[randomInt] + "...")
                                time.sleep(0.1)
                        except:
                            log.audio("Failed audio event.")
                            log.audio(str(self.eventData))
                            log.audio(traceback.format_exc())
                            log.crash("Failed audio event.")
                            log.crash(str(self.eventData))
                            log.crash(traceback.format_exc())
                        try:
                            endms = time.time()
                            pytools.IO.appendFile("fire_times.cxl", "\n" + str(hosts.listf[randomInt]) + ", " + str(endms - startms) + ", " + str(self.eventData))
                        except:
                            import traceback
                            print(traceback.format_exc())
                    audioThreadObj(target=runSound, args=(randomInt,)).start()
                    played = True
                    for sound in self.eventData["events"]:
                        dateArray = pytools.clock.getDateTime()
                        
                        logError = True
                        while logError:
                            try:
                                log.audio("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                                logError = False
                            except:
                                pass
                else:
                    def runSound(randomInt):
                        try:
                            print(self.eventData["events"][0]["path"])
                            hasFired = False
                            errorCount = 0
                            while (not hasFired) and (errorCount < 1000):
                                try:
                                    pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":" + str(getPort(hosts.listf[randomInt])) + "?json=" + urllib.parse.quote(json.dumps({
                                        "command": "fireEvent",
                                        "data": pytools.cipher.base64_encode(json.dumps(self.eventData)),
                                        "fileData": {
                                            "data" : pytools.cipher.base64_encode(pytools.IO.getBytes(self.eventData["events"][0]["path"].replace(".\\working\\", ".\\")), isBytes=True),
                                            "fileName": self.eventData["events"][0]["path"].split("\\")[-1]
                                        }
                                    })), timeout=10)
                                    hasFired = True
                                except:
                                    print(traceback.format_exc())
                                    errorCount = errorCount + 1
                                    if errorCount > 1000:
                                        log.audio("Failed audio event.")
                                        log.audio(str(self.eventData))
                                        log.audio(traceback.format_exc())
                                        log.crash("Failed audio event.")
                                        log.crash(str(self.eventData))
                                        log.crash(traceback.format_exc())
                                    else:
                                        log.audio("Failed to send audio event. Trying again...")
                                    grabHostData()
                                    randomInt = getHostToSendTo()
                                    if type(randomInt) == str:
                                        hosts.listf.append(randomInt)
                                        randomInt = 0
                                    print("Trying again on host " + hosts.listf[randomInt] + "...")
                                time.sleep(0.1)
                        except:
                            log.audio("Failed audio event.")
                            log.audio(str(self.eventData))
                            log.audio(traceback.format_exc())
                            log.crash("Failed audio event.")
                            log.crash(str(self.eventData))
                            log.crash(traceback.format_exc())
                        try:
                            endms = time.time()
                            pytools.IO.appendFile("fire_times.cxl", "\n" + str(hosts.listf[randomInt]) + ", " + str(endms - startms) + ", " + str(self.eventData))
                        except:
                            import traceback
                            print(traceback.format_exc())
                    audioThreadObj(target=runSound, args=(randomInt,)).start()
                    played = True
                    for sound in self.eventData["events"]:
                        dateArray = pytools.clock.getDateTime()
                        
                        logError = True
                        while logError:
                            try:
                                log.audio("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                                logError = False
                            except:
                                pass
            except:
                print(traceback.format_exc())

        except:
            log.audio("Failed to send audio event. Trying again...")
            log.audio(str(self.eventData))
            import traceback
            log.audio(traceback.format_exc())
            log.crash("Failed to send audio event. Trying again...")
            log.crash(str(self.eventData))
            log.crash(traceback.format_exc())
        time.sleep(1)
        if self.eventData["wait"]:
            time.sleep(self.duration)
        if played != True:
            log.audio("Failed audio event.")
            log.audio(str(self.eventData))
        
        if not report.count:
            audioThreadObj(target=report.clean).start()
            


class command:
    def sendStop(target=False):
        do = True
        loc = False
        try:
            import os
            if os.path.exists(".\\hostData.json"):
                hostsDataFile = pytools.IO.getJson(".\\hostData.json")
                loc = True
            else:
                hostsDataFile = pytools.IO.getJson(".\\working\\hostData.json")
        except:
            try:
                hostsDataFile = pytools.IO.getJson(".\\working\\hostData.json")
            except:
                try:
                    hostsDataFile = pytools.IO.getJson(".\\hostData.json")
                    loc = True
                except:
                    do = False
        if do:
            try:
                for host in pytools.IO.getJson("hosts.json")["hosts"]:
                    if (target == host) or not target:
                        pytools.net.getJsonAPI("http://" + host + ":4507?json=" + urllib.parse.quote(json.dumps({
                            "command": "killEvents"
                        })))
                        hostsDataFile.pop(host)
                if loc:
                    pytools.IO.saveJson(".\\hostData.json", hostsDataFile)
                else:
                    pytools.IO.saveJson(".\\working\\hostData.json", hostsDataFile)
            except:
                print(traceback.format_exc())
                
    def setFlag(flagName, boolf, target=False, timeout=10):
        do = True
        loc = False
        try:
            if os.path.exists(".\\working\\hostData.json"):
                hostsDataFile = pytools.IO.getJson(".\\working\\hostData.json")
            else:
                hostsDataFile = pytools.IO.getJson(".\\hostData.json")
        except:
            try:
                hostsDataFile = pytools.IO.getJson(".\\hostData.json")
                loc = True
            except:
                do = False
        if do:
            try:
                for host in pytools.IO.getJson("hosts.json")["hosts"]:
                    if (target == host) or not target:
                        print("Setting flag " + flagName + " on host " + host + " to " + str(boolf) + '...')
                        try:
                            pytools.net.getJsonAPI("http://" + host + ":4507?json=" + urllib.parse.quote(json.dumps({
                                "command": "setFlag",
                                "data": {
                                    "flagName": flagName,
                                    "bool": boolf
                                }
                            })), timeout=timeout)
                            if not target:
                                if boolf:
                                    pytools.IO.saveFile(".\\" + flagName + ".derp", str(boolf))
                                else:
                                    os.system("del \".\\" + flagName + ".derp\" /f /q")
                            print("Flag Set.")
                        except:
                            print("Error. Flag could not be set.")
                        try:
                            hostsDataFile.pop(host)
                        except:
                            pass
                # if os.path.exists(".\\hostData.json"):
                    # pytools.IO.saveJson(".\\hostData.json", hostsDataFile)
                # else:
                    # pytools.IO.saveJson(".\\working\\hostData.json", hostsDataFile)
            except:
                print(traceback.format_exc())

def intenseSleep(i):
    x = time.perf_counter() + i
    while time.perf_counter() < x:
        pass


"""class __event:
        def __init__(self, majorSelf, _index):
            self.uuid = _index
            self.majorSelf = majorSelf
            self.forceWait = False
        
        def register(self, *args, keepLoaded=False):
            waitDelay = self.majorSelf._complexEvents[self.uuid].register(*args, keepLoaded=keepLoaded)
            if args[5]:
                self.forceWait = waitDelay
            
        def registerWindow(self, *args, keepLoaded=False):
            waitDelay = self.majorSelf._complexEvents[self.uuid].registerWindow(*args)
            if args[4]:
                self.forceWait = waitDelay
        
        def registerAll(self, *args, keepLoaded=False):
            waitDelay = self.majorSelf._complexEvents[self.uuid].registerAll(*args)
            if args[4]:
                self.forceWait = waitDelay
        
        def run(self):
            _current = time.monotonic()
            for ___event in self.majorSelf._complexEvents[self.uuid].eventData["events"]:
                if "start_delay" in ___event: 
                    ___event["start_delay"] = ___event["start_delay"] + ((self.majorSelf._time + self.majorSelf.delay) - _current)
                else:
                    ___event["start_delay"] = ((self.majorSelf._time + self.majorSelf.delay) - _current)
                
                self.majorSelf._event.eventData["events"].append(___event)
            
            self.majorSelf._events = self.majorSelf._events + 1
            self.majorSelf._complexEvents.pop(self.uuid)
            
            if self.forceWait:
                try:
                    time.sleep(self.forceWait)
                except:
                    print(traceback.format_exc())"""

class rapidFire:
    def __init__(self, delay, noLimit=False):
        self.delay = delay
        self._events = 0
        self._complexEvents = {}
        self.exitf = False
        self.noLimit = noLimit
        self.manuallyFired = False
        self._time = time.monotonic()
        
        self._event = event()
    
    # {"events":[{'path': '.\\working\\sound\\assets\\whirr_st.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 59.71899999998277}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 55.60999999998603}, {'path': '.\\working\\sound\\assets\\hcs.wav', 'volume': 20, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 54.875}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 53.90700000000652}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 52.17200000002049}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 50.48499999998603}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 48.79700000002049}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 47.07900000002701}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 45.39100000000326}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 43.64100000000326}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 41.95400000002701}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 40.26600000000326}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 38.625}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 36.89100000000326}, {'path': '.\\working\\sound\\assets\\whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 35.20400000002701}, {'path': '.\\working\\sound\\assets\\whirr_ed.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 33.43800000002375}, {'path': '.\\working\\sound\\assets\\gong_whirr_st.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 33.51600000000326}, {'path': '.\\working\\sound\\assets\\gong_whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 29.32900000002701}, {'path': '.\\working\\sound\\assets\\gong_5.mp3', 'volume': 20, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 28.76600000000326}, {'path': '.\\working\\sound\\assets\\gong_whirr_cont.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 26.32900000002701}, {'path': '.\\working\\sound\\assets\\gong_whirr_ed.mp3', 'volume': 50, 'speed': 1.0, 'channel': 'clock', 'balence': 0.0, 'effects': [], 'start_delay': 24.60999999998603}]}
    
    def _handler(self):
        print("handler starting...")
        self._time = time.monotonic()
        
        while not self.exitf:
            try:
                _i = 0
                while ((_i < 30) and (self.noLimit or (len(self._event.eventData["events"]) < 7))) and (not self.manuallyFired) and (not self.exitf):
                    time.sleep(self.delay / 30)
                    _i = _i + 1
                    
                if not self.manuallyFired:
                    if self._events > 0:
                        print("Event Count: " + str(len(self._event.eventData["events"])))
                        audioThreadObj(target=self._event.run).start()
                        self._event = event()
                        self._events = 0
                
                    self._time = time.monotonic()
            
                self.manuallyFired = False
            except:
                print(traceback.format_exc())
                time.sleep(1)
            
    def manualFire(self):
        if self._events > 0:
            print("Event Count: " + str(len(self._event.eventData["events"])))
            audioThreadObj(target=self._event.run).start()
            self._event = event()
            self._events = 0
        
        self._time = time.monotonic()
        self.manuallyFired = True
                
    # def event(self):
    #     uuid = random.random()
    #     self._complexEvents[uuid] = event()
    #     return self.__event(self, uuid)
    
    def register(self, *args, startDelay=0, keepLoaded=False, clock=False):
        self._events = self._events + 1
        self._event.register(*args, startDelay=(self.delay - ((self._time + self.delay) - time.monotonic()) + startDelay), forceWait=args[5], keepLoaded=keepLoaded, clock=clock)
        
        if not report.count:
            audioThreadObj(target=report.clean).start()
        
    def playSoundAll(self, *args, startDelay=0, keepLoaded=False):
        self._events = self._events + 1
        self._event.registerAll(*args, startDelay=(self.delay - ((self._time + self.delay) - time.monotonic()) + startDelay), forceWait=args[4])

        if not report.count:
            audioThreadObj(target=report.clean).start()
        
    def registerAll(self, *args, startDelay=0, keepLoaded=False):
        self.playSoundAll(*args, startDelay=startDelay, keepLoaded=keepLoaded)

        if not report.count:
            audioThreadObj(target=report.clean).start()
        
    def playSoundWindow(self, *args, startDelay=0, keepLoaded=False):
        self._events = self._events + 1
        self._event.registerWindow(*args, startDelay=(self.delay - ((self._time + self.delay) - time.monotonic()) + startDelay), forceWait=args[4])

        if not report.count:
            audioThreadObj(target=report.clean).start()
        
    def registerWindow(self, *args, startDelay=0, keepLoaded=False):
        self.playSoundWindow(*args, startDelay=startDelay, keepLoaded=keepLoaded)
        
        if not report.count:
            audioThreadObj(target=report.clean).start()
        
    def registerCombine(self, __event):
        
        _curr = time.monotonic()
        
        for ___event in __event.eventData["events"]:
            if "start_delay" in ___event:
                ___event["start_delay"] = ___event["start_delay"] + (self.delay - ((self._time + self.delay) - _curr))
            else:
                ___event["start_delay"] = (self.delay - ((self._time + self.delay) - _curr))

            self._event.eventData["events"].append(___event)
        
        self._events = self._events + 1
        
        if not report.count:
            audioThreadObj(target=report.clean).start()
        
    def _start(self):
        self.exitf = False
        self._thread = threading.Thread(target=self._handler)
        self._thread.start()
        
    def _stop(self):
        self.exitf = True
        self._thread.join()

class hosts:
    listf = False
    soundsf = {
        
    }
    
try:
    hosts.listf = pytools.IO.getJson("hosts.json")["hosts"]
except:
    hosts.listf = []
    pytools.IO.saveJson(".\\hosts.json", {
        "hosts": []
    })
    pytools.IO.saveJson(".\\working\\hosts.json", {
        "hosts": []
    })
