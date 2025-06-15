from traceback import format_exc as traceback_format_exc, format_stack as traceback_format_stack
    
import traceback

import urllib.parse

from scipy.signal import butter, sosfilt
    
from math import log as math_log, fabs as math_fabs, floor as math_floor
class math:
    log = math_log
    fabs = math_fabs
    floor = math_floor
    
from os.path import exists as os_path_exists
from os import system as os_system, getcwd as os_getcwd
class os:
    system = os_system
    getcwd = os_getcwd
    class path:
        exists = os_path_exists
        
from time import time as time_time, sleep as time_sleep
class time:
    time = time_time
    sleep = time_sleep
    
from random import random as random_random, randint as random_randint
class random:
    random = random_random
    randint = random_randint
    
from gtts import gTTS as gtts_gTTS
class gtts:
    gTTS = gtts_gTTS
    
from subprocess import getoutput as subprocess_getoutput
class subprocess:
    getoutput = subprocess_getoutput

try:
    from modules.pytools import IO as pytools_IO, clock as pytools_clock, cipher as pytools_cipher, net as pytools_net
except:
    from pytools import IO as pytools_IO, clock as pytools_clock, cipher as pytools_cipher, net as pytools_net
class pytools:
    IO = pytools_IO
    clock = pytools_clock
    cipher = pytools_cipher
    net = pytools_net
    
from json import dumps as json_dumps, loads as json_loads
class json:
    dumps = json_dumps
    loads = json_loads
    
from sys import argv as sys_argv
class sys:
    argv = sys_argv

from threading import Thread as threading_Thread
class threading:
    Thread = threading_Thread
    

from sounddevice import query_devices as sd_query_devices
class sd:
    query_devices = sd_query_devices

from pyaudio import PyAudio

from pydub import AudioSegment as pydub_AudioSegment
from pydub.utils import make_chunks as pydub_utils_make_chunks

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

class pydub:
    AudioSegment = pydub_AudioSegment
    class utils:
        make_chunks = pydub_utils_make_chunks

from mutagen.mp3 import MP3
from mutagen.wave import WAVE

del traceback_format_exc
del math_log, math_fabs, math_floor
del os_path_exists, os_system, os_getcwd
del time_time, time_sleep
del random_random, random_randint
del gtts_gTTS
del subprocess_getoutput
del pytools_IO, pytools_clock, pytools_cipher, pytools_net
del json_dumps, json_loads
del sys_argv
del threading_Thread
del sd_query_devices
del pydub_AudioSegment, pydub_utils_make_chunks

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
        
class reportSound:
    def __init__(self, uuid):
        self.uuid = uuid
        
    def run(self):
        if not os.path.exists("..\\vars\\pluginSounds"):
            os.system("mkdir \"..\\vars\\pluginSounds\"")
        pytools.IO.saveFile("..\\vars\\pluginSounds\\" + str(self.uuid) + ".cx", str(obj.activeSounds[self.uuid][0]) + ";" + str(obj.activeSounds[self.uuid][1]) + ";" + str(pytools.clock.dateArrayToUTC(obj.activeSounds[self.uuid][2]) + obj.activeSounds[self.uuid][3]))
        time.sleep(obj.activeSounds[self.uuid][3])
        os.system("del \"" + "..\\vars\\pluginSounds\\" + str(self.uuid) + ".cx" + "\" /f /s /q")
        try:
            obj.activeSounds.pop(self.uuid)
        except:
            print("Could not pop uuid from activeSounds list.")
 
class playSoundWindow:
    def __init__(self, path, volume, speed, balence, wait, remember=False, lowPass=False, highPass=False, play=True, sendFile=False):
        self.path = path
        self.volume = volume
        self.speed = speed
        self.balence = balence
        self.wait = wait
        self.remember = remember
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
                        }
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
                        }
                    },
                    {
                        "path": ".\\working\\sound\\assets\\" + self.path.split(";")[1],
                        "volume": self.getVolume(1),
                        "speed": self.speed,
                        "balence": self.balence,
                        "channel": "outside",
                        "effects": effects
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
                    "effects": effects
                })
            else:
                eventData["events"].append({
                    "path": ".\\working\\sound\\assets\\" + self.path.split(";")[1],
                    "volume": self.getVolume(2),
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "porch",
                    "effects": effects
                })
            
            uuid = random.random()
            while uuid in obj.activeSounds:
                uuid = random.random()
            if self.path.split(";")[1].find(".mp3") != -1:
                duration = float(MP3(".\\sound\\assets\\" + self.path.split(";")[1]).info.length) / self.speed
            else:
                duration = float(WAVE(".\\sound\\assets\\" + self.path.split(";")[1]).info.length) / self.speed
            obj.activeSounds[uuid] = [self.path.split(";")[1].split("\\")[-1], "outside", pytools.clock.getDateTime(), duration]
            soundReportObj = reportSound(uuid)
            threading.Thread(target=soundReportObj.run).start()
            uuid = random.random()
            while uuid in obj.activeSounds:
                uuid = random.random()
            if self.path.split(";")[0].find(".mp3") != -1:
                duration = float(MP3(".\\sound\\assets\\" + self.path.split(";")[0]).info.length) / self.speed
            else:
                duration = float(WAVE(".\\sound\\assets\\" + self.path.split(";")[0]).info.length) / self.speed
            obj.activeSounds[uuid] = [self.path.split(";")[0].split("\\")[-1], "window", pytools.clock.getDateTime(), duration]
            soundReportObj = reportSound(uuid)
            threading.Thread(target=soundReportObj.run).start()
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
                        }
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
                        }
                    },
                    {
                        "path": ".\\working\\sound\\assets\\" + self.path,
                        "volume": self.getVolume(1),
                        "speed": self.speed,
                        "balence": self.balence,
                        "channel": "outside",
                        "effects": effects
                    },
                    {
                        "path": ".\\working\\sound\\assets\\" + self.path,
                        "volume": self.getVolume(2),
                        "speed": self.speed,
                        "balence": self.balence,
                        "channel": "porch",
                        "effects": effects
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
            obj.activeSounds[uuid] = [self.path.split("\\")[-1], "outside", pytools.clock.getDateTime(), duration]
            soundReportObj = reportSound(uuid)
            threading.Thread(target=soundReportObj.run).start()
            uuid = random.random()
            while uuid in obj.activeSounds:
                uuid = random.random()
            if self.path.find(".mp3") != -1:
                duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
            else:
                duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
            obj.activeSounds[uuid] = [self.path.split("\\")[-1], "window", pytools.clock.getDateTime(), duration]
            soundReportObj = reportSound(uuid)
            threading.Thread(target=soundReportObj.run).start()
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
                    
                    if (hosts.listf == []) or (random.random() < 0.5):
                        return pytools.IO.getJson("..\\serverSettings.json")["ip"]
                    
                    randomInt = -1
                    while (randomInt == -1) or (os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl")) or (os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl")) or (hosts.soundsf[hosts.listf[randomInt]]["play"] == False):
                        randomInt = tools.getRandomInt(hosts.soundsf)
                        if hosts.listf[randomInt] in hosts.soundsf:
                            if (randomInt != -1) and (not os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl")) and (not os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl")) and (hosts.soundsf[hosts.listf[randomInt]]["play"] == True):
                                if tools.ping(hosts.listf[randomInt]):
                                    break
                        else:
                            randomInt = -1
                            grabHostData()
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
                        threading.Thread(target=runSound, args=(randomInt,)).start()
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
                        threading.Thread(target=runSound, args=(randomInt,)).start()
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

class playSoundAll:
    def __init__(self, path, volume, speed, balence, wait, remember=False, lowPass=False, highPass=False, sendFile=False):
        self.path = path
        self.volume = volume
        self.speed = speed
        self.balence = balence
        self.wait = wait
        self.remember = remember
        self.lowPass = lowPass
        self.highPass = highPass
        
        self.run(sendFile=sendFile)
    
    def run(self, sendFile=False):
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
        
        eventData = {
            "events": [
                {
                    "path": ".\\working\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "clock",
                    "effects": effects
                },
                {
                    "path": ".\\working\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "generic",
                    "effects": effects
                },
                {
                    "path": ".\\working\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "fireplace",
                    "effects": effects
                },
                {
                    "path": ".\\working\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "window",
                    "effects": effects
                },
                {
                    "path": ".\\working\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "outside",
                    "effects": effects
                },
                {
                    "path": ".\\working\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "porch",
                    "effects": effects
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
        obj.activeSounds[uuid] = [self.path.split("\\")[-1], "clock", pytools.clock.getDateTime(), duration]
        soundReportObj = reportSound(uuid)
        threading.Thread(target=soundReportObj.run).start()
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [self.path.split("\\")[-1], "generic", pytools.clock.getDateTime(), duration]
        soundReportObj = reportSound(uuid)
        threading.Thread(target=soundReportObj.run).start()
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [self.path.split("\\")[-1], "fireplace", pytools.clock.getDateTime(), duration]
        soundReportObj = reportSound(uuid)
        threading.Thread(target=soundReportObj.run).start()
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [self.path.split("\\")[-1], "windown", pytools.clock.getDateTime(), duration]
        soundReportObj = reportSound(uuid)
        threading.Thread(target=soundReportObj.run).start()
        
        
        startms = time.time()
        
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
                
                if (hosts.listf == []) or (random.random() < 0.5):
                    return pytools.IO.getJson("..\\serverSettings.json")["ip"]
                
                randomInt = -1
                while (randomInt == -1) or (os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl")) or (os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl")) or (hosts.soundsf[hosts.listf[randomInt]]["play"] == False):
                    randomInt = tools.getRandomInt(hosts.soundsf)
                    if hosts.listf[randomInt] in hosts.soundsf:
                        if (randomInt != -1) and (not os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl")) and (not os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl")) and (hosts.soundsf[hosts.listf[randomInt]]["play"] == True):
                            if tools.ping(hosts.listf[randomInt]):
                                break
                    else:
                        randomInt = -1
                        grabHostData()
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
                                        "data": pytools.cipher.base64_encode(json.dumps(eventData))
                                    })), timeout=10)
                                    hasFired = True
                                except:
                                    import traceback
                                    print(traceback.format_exc())
                                    errorCount = errorCount + 1
                                    if errorCount > 100:
                                        log.audio("Failed audio event.")
                                        log.audio(str(eventData))
                                        log.audio(traceback.format_exc())
                                        log.crash("Failed audio event.")
                                        log.crash(str(eventData))
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
                            log.audio(str(eventData))
                            log.audio(traceback.format_exc())
                            log.crash("Failed audio event.")
                            log.crash(str(eventData))
                            log.crash(traceback.format_exc())
                        try:
                            endms = time.time()
                            pytools.IO.appendFile("fire_times.cxl", "\n" + str(hosts.listf[randomInt]) + ", " + str(endms - startms) + ", " + str(self.eventData))
                        except:
                            print(traceback.format_exc())
                    threading.Thread(target=runSound, args=(randomInt,)).start()
                    played = True
                    for sound in eventData["events"]:
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
                            print(eventData["events"][0]["path"])
                            hasFired = False
                            errorCount = 0
                            while (not hasFired) and (errorCount < 100):
                                try:
                                    pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":" + str(getPort(hosts.listf[randomInt])) + "?json=" + urllib.parse.quote(json.dumps({
                                        "command": "fireEvent",
                                        "data": pytools.cipher.base64_encode(json.dumps(eventData)),
                                        "fileData": {
                                            "data" : pytools.cipher.base64_encode(pytools.IO.getBytes(eventData["events"][0]["path"].replace(".\\working\\", ".\\")), isBytes=True),
                                            "fileName": eventData["events"][0]["path"].split("\\")[-1]
                                        }
                                    })), timeout=10)
                                    hasFired = True
                                except:
                                    import traceback
                                    print(traceback.format_exc())
                                    errorCount = errorCount + 1
                                    if errorCount > 100:
                                        log.audio("Failed audio event.")
                                        log.audio(str(eventData))
                                        log.audio(traceback.format_exc())
                                        log.crash("Failed audio event.")
                                        log.crash(str(eventData))
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
                            log.audio(str(eventData))
                            log.audio(traceback.format_exc())
                            log.crash("Failed audio event.")
                            log.crash(str(eventData))
                            log.crash(traceback.format_exc())
                        try:
                            endms = time.time()
                            pytools.IO.appendFile("fire_times.cxl", "\n" + str(hosts.listf[randomInt]) + ", " + str(endms - startms) + ", " + str(self.eventData))
                        except:
                            print(traceback.format_exc())
                    threading.Thread(target=runSound, args=(randomInt,)).start()
                    played = True
                    for sound in eventData["events"]:
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
            log.audio(str(eventData))
            log.audio(traceback.format_exc())
            log.crash("Failed to send audio event. Trying again...")
            log.crash(str(eventData))
            log.crash(traceback.format_exc())
        time.sleep(1)
        if eventData["wait"]:
            time.sleep(duration)
        if played != True:
            log.audio("Failed audio event.")
            log.audio(str(eventData))
                
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
    
    def registerWindow(self, path, volume, speed, balence, wait, remember=False, lowPass=False, highPass=False):
        self.eventData["events"].extend(playSoundWindow(path, volume, speed, balence, wait, remember=remember, lowPass=lowPass, highPass=highPass, play=False).eventData["events"])
        if path.split(";")[0].find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + path.split(";")[0]).info.length) / speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + path.split(";")[0]).info.length) / speed
        uuid = random.random()
        obj.activeSounds[uuid] = [path.split("\\")[-1].split(";")[0], "window", pytools.clock.getDateTime(), duration]
        soundReportObj = reportSound(uuid)
        threading.Thread(target=soundReportObj.run).start()
        uuid = random.random()
        obj.activeSounds[uuid] = [path.split("\\")[-1].split(";")[0], "outside", pytools.clock.getDateTime(), duration]
        soundReportObj = reportSound(uuid)
        threading.Thread(target=soundReportObj.run).start()
        
        
    def register(self, path, speaker, volume, speed, balence, wait, clock=True, remember=False, lowPass=False, highPass=False, keepLoaded=False, muteFlag=False, defaultMuteState=False, muteFade=False):
        
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
        
        for channel in speakern:
            self.eventData["events"].append({
                "path": ".\\working\\sound\\assets\\" + path,
                "volume": volume,
                "speed": speed,
                "channel": channel,
                "balence": balence,
                "effects": effects
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
            try:
                if self.duration < duration:
                    self.duration = duration
            except:
                self.duration = duration
            obj.activeSounds[uuid] = [path.split("\\")[-1], channel, pytools.clock.getDateTime(), duration]
            soundReportObj = reportSound(uuid)
            threading.Thread(target=soundReportObj.run).start()
    
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
                
                if (hosts.listf == []) or (random.random() < 0.5):
                    return pytools.IO.getJson("..\\serverSettings.json")["ip"]
                
                randomInt = -1
                while (randomInt == -1) or (os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl")) or (os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl")) or (hosts.soundsf[hosts.listf[randomInt]]["play"] == False):
                    randomInt = tools.getRandomInt(hosts.soundsf)
                    if hosts.listf[randomInt] in hosts.soundsf:
                        if (randomInt != -1) and (not os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl")) and (not os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl")) and (hosts.soundsf[hosts.listf[randomInt]]["play"] == True):
                            if tools.ping(hosts.listf[randomInt]):
                                break
                    else:
                        randomInt = -1
                        grabHostData()
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
                    threading.Thread(target=runSound, args=(randomInt,)).start()
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
                    threading.Thread(target=runSound, args=(randomInt,)).start()
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
                
    def setFlag(flagName, boolf, target=False):
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
                            })))
                            if not target:
                                if boolf:
                                    pytools.IO.saveFile(".\\" + flagName + ".derp", boolf)
                                else:
                                    pytools.IO.saveFile("del \".\\" + flagName + ".derp\" /f /q")
                            print("Flag Set.")
                        except:
                            print("Error. Flag could not be set.")
                        try:
                            hostsDataFile.pop(host)
                        except:
                            pass
                if os.path.exists(".\\hostData.json"):
                    pytools.IO.saveJson(".\\hostData.json", hostsDataFile)
                else:
                    pytools.IO.saveJson(".\\working\\hostData.json", hostsDataFile)
            except:
                print(traceback.format_exc())

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
