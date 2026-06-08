import psutil
import os
import random
import sys

p = psutil.Process(os.getpid())

oldAffinity = p.cpu_affinity()
oldPriority = p.nice()
p.cpu_affinity([random.randint(0, psutil.cpu_count() - 1)])
p.nice(psutil.IDLE_PRIORITY_CLASS)
import sounddevice as sd
import pickle
import shutil
import time
import math
import sys
import atexit
import signal
import base64
import json
import sys
import pydub
import zipfile
import xmltodict
import numpy
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import gtts
import threading
import pydub.utils

from datetime import datetime

from pydub.scipy_effects import high_pass_filter
from pydub.scipy_effects import low_pass_filter
p.cpu_affinity(oldAffinity)
p.nice(oldPriority)

if not os.path.exists(".\\logs"):
    os.system("mkdir \".\\logs\"")
    
if not os.path.exists(".\\logs\\errors"):
    os.system("mkdir \".\\logs\\errors\"")

class log:
    
    data = []
    hasLogged = False
    dateString = ""
    timeString = ""
    profile = True

    doPrint = False
    debug = True
    
    def crash(*strff):
        for strf in strff:
            if log.doPrint or log.debug:
                print(str(strf))
            if not log.hasLogged:
                log.data.append([pytools.clock.getDateTime(), str(strf), str(traceback.format_stack())])
                if ("Traceback" in str(strf)) or ("Error" in str(strf)) or ("error" in str(strf)) or ("Failed" in str(strf)) or ("failed" in str(strf)) or ("Unable" in str(strf)) or ("unable" in str(strf)) or ("WARNING" in str(strf)) or ("Warning" in str(strf)) or ("warning" in str(strf)):
                    dateArray = pytools.clock.getDateTime()
                    if log.dateString == "":
                        log.dateString = str(dateArray[0]) + "-" + str(dateArray[1]) + "-" + str(dateArray[2])
                        log.timeString =  str(dateArray[3]) + "."  + str(dateArray[4]) + "."  + str(dateArray[5]) + "_" + str(time.time() * 100000).split(".")[0]
                    if not os.path.exists(".\\logs\\errors\\" + log.dateString):
                        os.system("mkdir \".\\logs\\errors\\" + log.dateString + "\"")
                    for data in log.data:
                        dateArray = data[0]
                        message = str(data[1])
                        callStack = str(data[2])
                        pytools.IO.appendFile(".\\logs\\errors\\" + log.dateString + "\\event_" + log.timeString + ".log", "\n" + str(dateArray) + " :;: " + message + " :;: " + callStack.replace("\n", "    \\n\t"))
                    log.hasLogged = True
            else:
                dateArray = pytools.clock.getDateTime()
                pytools.IO.appendFile(".\\logs\\errors\\" + log.dateString + "\\event_" + log.timeString + ".log", "\n" + str(dateArray) + " :;: " + str(strf) + " :;: " + str(traceback.format_stack()).replace("\n", "    \\n\t"))

    def doEndDump():
        
        dateArray = pytools.clock.getDateTime()
        if log.dateString == "":
            log.dateString = str(dateArray[0]) + "-" + str(dateArray[1]) + "-" + str(dateArray[2])
            log.timeString =  str(dateArray[3]) + "."  + str(dateArray[4]) + "."  + str(dateArray[5]) + "_" + str(time.time() * 100000).split(".")[0]
        
        if not os.path.exists(".\\logs\\sounds"):
            os.system("mkdir \".\\logs\\sounds\"")
        if pytools.clock.getDateTime()[3] == 3:
            if not os.path.exists(".\\logs\\sounds\\" + log.dateString + ".log"):
                pytools.IO.saveFile(".\\logs\\sounds\\" + log.dateString + ".log", "no_data")
                soundData = ""
                for n in os.listdir(".\\logs\\today"):
                    logData = pytools.IO.getFile(".\\logs\\today\\" + n)
                    for data in logData.split("\n"):
                        if "Playing sound of path" in data:
                            soundData = soundData + data + " ;;; Sound exited at time " + str([eval(i) for i in logData.split("\n")[-1].split(" :;:")[0].strip('][').split(', ')]) + "\n"
                if pytools.IO.getFile(".\\logs\\sounds\\" + log.dateString + ".log") == "no_data":
                    pytools.IO.saveFile(".\\logs\\sounds\\" + log.dateString + ".log", soundData)
                    os.system("del \".\\logs\\today\\*\" /f /q")

        if not os.path.exists(".\\logs\\today"):
            os.system("mkdir \".\\logs\\today\"")
        for data in log.data:
            dateArray = data[0]
            message = str(data[1])
            callStack = str(data[2])
            
            
def printDebug(strf):
    log.crash(strf)
   
def exit_handler():
    log.crash("Audio Engine Instance Has Finished.")
    log.doEndDump()

def kill_handler(*args):
    sys.exit(0)

class traceback:
    def format_exc():
        return ""
    
    def format_stack():
        return ""

if log.debug:
    import traceback as f
    traceback = f
    
def exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    log.crash("Uncaught exception")
    log.crash('Type:', exc_type)
    log.crash('Value:', exc_value)
    log.crash('Traceback:', exc_traceback)

if __name__ == '__main__':
    sys.excepthook = exception_handler

def getFlag(flagName):
    if os.path.exists(".\\" + flagName + ".derp"):
        try:
            return float(pytools.IO.getFile(".\\" + flagName + ".derp"))
        except:
            return True
    
    return False

class pytools:
    class clock:
        def getDateTime(utc = False):
            if utc:
                daten = datetime.utcnow()
            else:
                daten = datetime.now()
            dateArray = [1970, 1, 1, 0, 0, 0]
            dateArray[0] = int(str(daten).split(" ")[0].split("-")[0])
            dateArray[1] = int(str(daten).split(" ")[0].split("-")[1])
            dateArray[2] = int(str(daten).split(" ")[0].split("-")[2])
            dateArray[3] = int(str(daten).split(" ")[1].split(":")[0])
            dateArray[4] = int(str(daten).split(" ")[1].split(":")[1])
            dateArray[5] = int(str(daten).split(" ")[1].split(":")[2].split(".")[0])
            return dateArray
    
    class cipher:  
        def base64_encode(s):
            encode = base64.standard_b64encode(bytes(s, encoding="utf-8")).decode("utf-8").replace("=", "?")
            return encode
            
        def base64_decode(s: str):
            decode = base64.standard_b64decode(s.replace("?", "=")).decode("utf-8")
            return decode
    
    class IO:
        def getJson(path, doPrint=True):
            error = 0
            try:
                file = open(path, "r")
                jsonData = json.loads(file.read())
                file.close()
            except:
                if doPrint:
                    log.crash("Unexpected error: " + traceback.format_exc())
                error = 1
            if error != 0:
                jsonData = error
            return jsonData
        
        def getXml(path, doPrint=True):
            return xmltodict.parse(pytools.IO.getFile(path, doPrint=doPrint))
        
        def saveXml(path, doPrint=True):
            pass

        def saveJson(path, jsonData):
            error = 0
            try:
                file = open(path, "w")
                file.write(json.dumps(jsonData))
                file.close()
            except:
                log.crash("Unexpected error: " + traceback.format_exc())
                error = 1
            return error

        def getFile(path, doPrint=True):
            error = 0
            try:
                file = open(path, "r")
                jsonData = file.read()
                file.close()
            except:
                if doPrint:
                    log.crash("Unexpected error: " + traceback.format_exc())
                error = 1
            if error != 0:
                jsonData = error
            return jsonData
        
        def getBytes(path, doPrint=True):
            error = 0
            try:
                file = open(path, "rb")
                jsonData = file.read()
                file.close()
            except:
                if doPrint:
                    log.crash("Unexpected error: " + traceback.format_exc())
                error = 1
            if error != 0:
                jsonData = error
            return jsonData

        def saveFile(path, jsonData):
            error = 0
            try:
                file = open(path, "w")
                file.write(jsonData)
                file.close()
            except:
                log.crash("Unexpected error: " + traceback.format_exc())
                error = 1
            return error
        
        def saveBytes(path, jsonData):
            error = 0
            try:
                file = open(path, "wb")
                file.write(jsonData)
                file.close()
            except:
                log.crash("Unexpected error: " + traceback.format_exc())
                error = 1
            return error

        def saveList(path, list):
            error = 0
            try:
                file = open(path, "wb")
                pickle.dump(list, file)
                file.close()
            except:
                log.crash("Unexpected error: " + traceback.format_exc())
                error = 1
            return error

        def getList(path, doPrint=True):
            list = []
            error = 0
            try:
                file = open(path, "rb")
                jsonData = pickle.load(file)
                file.close()
            except:
                if doPrint:
                    log.crash("Unexpected error: " + traceback.format_exc())
                error = 1
            if error != 0:
                jsonData = error
            return [list, jsonData]

        def appendFile(path, jsonData):
            error = 0
            try:
                file = open(path, "a")
                file.write(jsonData)
                file.close()
            except:
                log.crash("Unexpected error: " + traceback.format_exc())
                error = 1
            return error
        
        def unpack(path, outDir):
            try:
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    log.crash(zip_ref.printdir())
                    log.crash('Extracting zip resources...')
                    zip_ref.extractall(outDir)
                    log.crash("Done.")
            except Exception as erro:
                    log.crash("Could not unpack zip file.")
                    log.crash(erro)

        def pack(path, dir):
            shutil.make_archive(path, 'zip', dir)

if __name__ == '__main__':
    atexit.register(exit_handler)
    signal.signal(signal.SIGINT, kill_handler)
    signal.signal(signal.SIGTERM, kill_handler)

class info:
    def __init__(self):
        self.uuid = random.random()
    
    globalSoundStart = False
    loopSync = {}
    skipParodyCheck = False
    timeingInfo = 0
    
def intenseSleep(i):
    x = time.perf_counter() + i
    while time.perf_counter() < x:
        pass

class thread_handler:
    def __init__(self, obj):
        self.obj = obj
        
    def run(self):
        try:
            self.obj()
        except:
            log.crash(traceback.format_exc())
        log.crash("Thread " + str(self.obj) + " has exited.")

# Sound Events
# syncEvents = {
#     "events": [
#         {
#             "path": "",
#             "volume": 0,
#             "speed": 1.0,
#             "channel": "clock",
#             "effects": [
#                  {
#                      "type": "<type>", # lowpass, highpass, remeberbypass
#                      <highpass, lowpass> "freqency": <float>
#                      <highpass, lowpass> "db": <float>
#                 }
#             ]
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
    chunkSize = 2048
    speakers = {}
    maxCount = 100
    close = False
    maxStreamDelay = 0

if os.path.exists(".\\soundOutputs.json"):
    globals.speakers = pytools.IO.getJson(".\\soundOutputs.json")
if os.path.exists("..\\soundOutputs.json"):
    globals.speakers = pytools.IO.getJson("..\\soundOutputs.json")
    
class tools:
    def setOutputs():
        if os.path.exists(".\\soundOutputs.json"):
            globals.speakers = pytools.IO.getJson(".\\soundOutputs.json")
        if os.path.exists("..\\soundOutputs.json"):
            globals.speakers = pytools.IO.getJson("..\\soundOutputs.json")
        try:
            devices = sd.query_devices()
            for channel in globals.speakers:
                for n in devices:
                    time.sleep(0.1)
                    if globals.speakers[channel][0] == n["name"]:
                        if globals.speakers[channel][1] == "MME":
                            if n["hostapi"] == 0:
                                deviceIndex = n["index"]
                                break
                        if globals.speakers[channel][1] == "WDM-KS":
                            if n["hostapi"] == 4:
                                deviceIndex = n["index"]
                                break
                globals.speakers[channel].append(deviceIndex)
            pytools.IO.saveJson("speakerSets.json", {
                "speakers": globals.speakers
            })
        except:
            log.crash(traceback.format_exc())
    
class audioEffects:
    def lowPass(data, frequency, db=24):
        if (data != False) and (type(data) != float):
            return data.low_pass_filter(frequency, order=db)
        else:
            return False
    
    def highPass(data, frequency, db=24):
        if (data != False) and (type(data) != float):
            return data.high_pass_filter(frequency, order=db)
        else:
            return False
        
class stream:
    def __init__(self, seg, speed, device, duration, soundIndex, lastPlayed, startPlayed, bufferSize, balence, startDelay=0):
        self.channels = seg.channels
        self.frame_rate = seg.frame_rate
        self.sample_width = seg.sample_width
        self.chunksActive = pydub.utils.make_chunks(seg, globals.chunkSize)
        self.chunks = False
        self.speed = speed
        self.device = device
        self.startDelay = startDelay
        self.duration = duration
        self.soundIndex = soundIndex
        self.lastPlayed = lastPlayed
        self.isDone = False
        self.startPlayed = startPlayed
        self.bufferSize = bufferSize
        
    audioStream = False
    p = False
    _info = info()
    
    def run(self):
        
        try:
            self.audioStream.start()
            def audioSegmentNumPy(audio):
                return numpy.array(audio.get_array_of_samples(), dtype=numpy.float32).reshape((-1, audio.channels)) / (1 << (8 * audio.sample_width - 1))
            self.i = 0
            
            self.delayStart = time.perf_counter()
            self.startPlayed = time.time() * 1000000
            
            if (self.startDelay + self.duration) >= globals.maxStreamDelay:
                globals.maxStreamDelay = (self.startDelay + self.duration)
            
            while (((self.startPlayed + (self.duration * 1000000) + (5 * 1000000))) > round(time.time() * 1000000)) or (type(self.chunksActive) != bool):
                
                # if (self.delayStart + self.startDelay) <= time.perf_counter():
                self.chunks = self.chunksActive
                self.chunksActive = True
                
                
                if (self.chunks != True) and (self.chunks != False):
                    def forChunkMapFunction(chunk):
                        if chunk:
                            if self.i == 0:
                                if self._info.globalSoundStart != False:
                                    self._info.globalSoundStart = time.perf_counter()
                                
                                self.startPlayed = round(time.time() * 1000000)
                            timeingInfo = ((self._info.globalSoundStart + self.i) - time.perf_counter())
                            if timeingInfo > 0.01:
                                intenseSleep(timeingInfo)
                                self.audioStream.write(audioSegmentNumPy(chunk))
                            elif timeingInfo < -0.01:
                                if timeingInfo > -(globals.chunkSize / 1000):
                                    sampleDuration = chunk[0:100].duration_seconds / 100
                                    self.audioStream.write(audioSegmentNumPy(chunk[int(math.fabs(timeingInfo) / sampleDuration):]))
                            else:
                                self.audioStream.write(audioSegmentNumPy(chunk))
                        else:
                            if log.debug:
                                log.crash("Chunked Buffer Overflow!")
                        self.i = self.i + (chunk.duration_seconds / self.speed)
                    list(map(forChunkMapFunction, self.chunks))
                else:
                    # if ((self.delayStart + self.startDelay) <= time.perf_counter()):
                    if log.debug:
                        log.crash("Buffer Overflow!")
                    time.sleep(0.1)
                    # else:
                    #     print("Sleeping stream for " + str(((self.delayStart + self.startDelay) - time.perf_counter())) + " seconds.")
                    #     intenseSleep(((self.delayStart + self.startDelay) - time.perf_counter()))
            
            time.sleep(globals.bufferSize)
            self.audioStream.stop()
            self.audioStream.close()

            self.isDone = True
            
            if (self.startDelay + self.duration) >= globals.maxStreamDelay:
                globals.close = True
            
        except:
            printDebug(traceback.format_exc())
            time.sleep(globals.bufferSize)
            self.audioStream.stop()        
            self.audioStream.close()
            
            self.isDone = True

            if (self.startDelay + self.duration) >= globals.maxStreamDelay:
                globals.close = True

class speakers:
    def getOutputs():
        if os.path.exists(".\\soundInputs.json"):
            speakers = pytools.IO.getJson(".\\soundInputs.json")
        if os.path.exists("..\\soundInputs.json"):
            speakers = pytools.IO.getJson("..\\soundInputs.json")
        try:
            devices = sd.query_devices()
            for channel in speakers:
                for n in devices:
                    if speakers[channel][0].lower() == n["name"].lower():
                        if speakers[channel][1] == "MME":
                            if n["hostapi"] == 0:
                                deviceIndex = n["index"]
                                break
                        if speakers[channel][1] == "WDM-KS":
                            if n["hostapi"] == 4:
                                deviceIndex = n["index"]
                                break
                try:
                    speakers[channel].append(deviceIndex)
                except:
                    printDebug("Append error: " + str(channel))
            pytools.IO.saveJson("inputSets.json", {
                "speakers": speakers
            })
            return speakers
        except:
            printDebug(traceback.format_exc())

class soundEvent:
    def __init__(self, path, volume, speed, channel, effects, balence, muteOptions=False, startDelay=0):
        self.path = path
        self.uuid = random.random()
        while self.uuid in obj.activeSounds:
            self.uuid = random.random()
        self.volume = volume
        self.speed = speed
        self.balence = balence
        self.channel = channel
        self.effects = effects
        self.startDelay = startDelay
        if path.find(".mp3") != -1:
            self.duration = float(MP3(path).info.length) / speed
        else:
            self.duration = float(WAVE(path).info.length) / speed

        if muteOptions:
            self.muteFlag = muteOptions["flag_name"]
            self.booleanValueToMuteOn = muteOptions["do_mute"]
            self.doMuteFade = muteOptions["fade"]
            
            if getFlag(self.muteFlag) and self.booleanValueToMuteOn:
                self.muteState = (1 - getFlag(self.muteFlag)) * 99
            elif (not getFlag(self.muteFlag)) and (not self.booleanValueToMuteOn):
                self.muteState = 0
            else:
                if self.booleanValueToMuteOn:
                    self.muteState = (1 - getFlag(self.muteFlag)) * 99
                else:
                    self.muteState = getFlag(self.muteFlag) * 99
            
            self.previousMuteState = self.muteState
                
        else:
            self.muteFlag = "no_flag"
            self.booleanValueToMuteOn = True
            self.doMuteFade = False
            self.muteState = False
            
        self.previousMuteState = self.muteState
     
    doneLoading = False
    
    def initStream(self):
        try:
                    
            deviceIndex = speakers.getOutputs()[self.channel][2]

            self.itsStream = stream(self.data, self.speed, deviceIndex, self.duration, self.index, self.lastPlayed, round(time.time() * 1000000), globals.bufferSize, self.balence, startDelay=self.startDelay)
            time.sleep(1)
            self.itsStream.audioStream = sd.OutputStream(
                blocksize=2048,
                channels=self.itsStream.channels,
                device=self.itsStream.device,
                samplerate=int(self.itsStream.frame_rate * self.speed),
            )
        except:
            printDebug(traceback.format_exc())
            
        self.doneLoading = True
        
    data = False
    itsStream = False
    index = 0
    lastPlayed = 0
    
    def load(self, index):
        self.index = index
        if math.floor((self.duration / globals.bufferSize) + 1) >= index:
            lastModif = os.path.getmtime(self.path)
            if os.path.exists(".\\.audiocache\\" + self.path.split("\\")[-1] + "-cache." + str(index * globals.bufferSize) + ".pyl"):
                printDebug("".join(["loading cached index " + str(index), "..."]))
                cachedData = pytools.IO.getList(".\\.audiocache\\" + self.path.split("\\")[-1] + "-cache." + str(index * globals.bufferSize) + ".pyl")[1]
                self.data = cachedData[0]
                if cachedData[1] != lastModif:
                    printDebug("".join(["not cached! loading index " + str(index), "..."]))
                    self.data = pydub.AudioSegment.from_file(file=self.path.replace("\t", "\\t"), format="mp3", start_second=index * globals.bufferSize, duration=globals.bufferSize)
                    pytools.IO.saveList(".\\.audiocache\\" + self.path.split("\\")[-1] + "-cache." + str(index * globals.bufferSize) + ".pyl", [self.data, lastModif])
            else:
                printDebug("".join(["not cached! loading index " + str(index), "..."]))
                self.data = pydub.AudioSegment.from_file(file=self.path.replace("\t", "\\t"), format="mp3", start_second=index * globals.bufferSize, duration=globals.bufferSize)
                pytools.IO.saveList(".\\.audiocache\\" + self.path.split("\\")[-1] + "-cache." + str(index * globals.bufferSize) + ".pyl", [self.data, lastModif])
        else:
            self.data = False
            
        bal = False
        
        if self.muteFlag != "no_flag":
            if getFlag(self.muteFlag) and self.booleanValueToMuteOn:
                self.muteState = (1 - getFlag(self.muteFlag)) * 99
            elif (not getFlag(self.muteFlag)) and (not self.booleanValueToMuteOn):
                self.muteState = 0
            else:
                if self.booleanValueToMuteOn:
                    self.muteState = (1 - getFlag(self.muteFlag)) * 99
                else:
                    self.muteState = getFlag(self.muteFlag) * 99
                
            if self.muteState != self.previousMuteState:
                if self.doMuteFade:
                    if globals.chunkSize < 4096:
                        self.data = self.data.fade(from_gain=(20 * math.log((self.previousMuteState + 0.01) / 100, 10)), start=0, duration=globals.chunkSize)
                        self.data = self.data.fade(to_gain=(20 * math.log((self.muteState + 0.01) / 100, 10)), start=0, duration=globals.chunkSize)
                        self.previousMuteState = self.muteState
                    else:
                        self.data = self.data.fade(from_gain=(20 * math.log((self.previousMuteState + 0.01) / 100, 10)), start=0, duration=4096)
                        self.data = self.data.fade(to_gain=(20 * math.log((self.muteState + 0.01) / 100, 10)), start=0, duration=4096)
                        self.previousMuteState = self.muteState
                else:
                    self.data = self.data + (20 * math.log((self.muteState + 0.01) / 100, 10))
                    self.previousMuteState = self.muteState
            else:
                self.data = self.data + (20 * math.log((self.muteState + 0.01) / 100, 10))
            
        if self.balence != 0:
            monoSets = self.data.split_to_mono()
            if len(monoSets) == 1:
                monoSets = [monoSets[0], monoSets[0]]
                self.data = pydub.AudioSegment.from_mono_audiosegments(*monoSets)
            if self.balence < 0:
                monoSets[1] = monoSets[1] + (20 * math.log((0.01 + 100 - math.fabs(self.balence)) / 100, 10))
                bal = True
            elif self.balence > 0:
                monoSets[0] = monoSets[0] + (20 * math.log((0.01 + 100 - math.fabs(self.balence)) / 100, 10))
                bal = True
        
        if bal:
            self.data = pydub.AudioSegment.from_mono_audiosegments(*monoSets)

        
    def iter(self):
        self.load(self.index + 1)
        
    def handleEffects(self, effect):
        try:
            log.crash(str(self.data) + "\t" + str(effect["frequency"]) + "\t" + str(effect["db"]))
        except:
            pass
        try:
            if effect["type"] == "lowpass":
                try:
                    self.data = audioEffects.lowPass(self.data, effect["frequency"], effect["db"])
                except:
                    self.data = audioEffects.lowPass(self.data, effect["frequency"])
                    
            if effect["type"] == "highpass":
                try:
                    self.data = audioEffects.highPass(self.data, effect["frequency"], effect["db"])
                except:
                    self.data = audioEffects.highPass(self.data, effect["frequency"])
        except:
            log.crash("Could not add effects to sound.")
    
    def handleRun(self):
        try:
            startPlayed = round(time.time() * 1000000)
            obj.activeSounds[self.uuid] = self.path.split("\\")[-1]
            log.crash("".join(["Playing sound of path ", self.path, " on the ", self.channel, " channel at volume ", str((20 * math.log(self.volume / 100, 10))), " at ", str(self.speed), "x speed..."]))
            justStarted = True
            while ((self.data != False) or justStarted) and (not self.itsStream.isDone):
                time.sleep(0.05)
                if globals.close or self.itsStream.isDone:
                    print("exit detected.")
                    return
                
                # while (self.itsStream.chunksActive != True) and ((self.itsStream.delayStart + self.itsStream.startDelay) > time.perf_counter()):
                #     if globals.close:
                #         return
                #     intenseSleep(((self.itsStream.delayStart + self.itsStream.startDelay) - time.perf_counter()))
                
                self.iter()
                justStarted = False
                shift = (20 * math.log(self.volume / 100, 10))
                self.data = self.data + shift
                if (type(self.data) == float) or (self.data == False): # < possible problem (returning on datatype False)
                    return
                
                def handleEffectsMapFunction(effect):
                    if globals.close:
                        return
                    self.handleEffects(effect)
                list(map(handleEffectsMapFunction, self.effects))
                self.itsStream.chunksActive = pydub.utils.make_chunks(self.data, globals.chunkSize)
                self.lastPlayed = (startPlayed + (self.index * 1000000)) / 1000000
                self.itsStream.lastPlayed = self.lastPlayed
                
                def syncEventKey(idf):
                    return info.loopSync[idf]
                
                try:
                    if (max(info.loopSync, key=syncEventKey) - min(info.loopSync, key=syncEventKey)) < 0.01:
                        info.skipParodyCheck = True
                except:
                    pass
                
                while self.itsStream.chunksActive != True:
                    if globals.close or self.itsStream.isDone:
                        return
                    time.sleep(0.5)
            obj.activeSounds.pop(self.uuid)
        except:
            printDebug(traceback.format_exc())
        
class multiEvent:
    def __init__(self, eventData):
        log.crash("multiEvent_init_0")
        self.wait = eventData["wait"]
        self.eventData = eventData
        def loadEventsMapFunction(event):
            log.crash("multiEvent_init_1")
            time.sleep(0.1)
            if event["volume"] > 0.0:
                if os.path.exists(".\\randomSounds.derp"):
                    audioList = os.listdir(".\\sound\\assets")
                    event["path"] = "".join([".\\sound\\assets\\", audioList[random.randint(0, len(audioList))]]).replace("\\", "\\")
                    while (event["path"].find(".mp3") == -1) and (event["path"].find(".wav") == -1):
                        time.sleep(0.1)
                        event["path"] = "".join([".\\sound\\assets\\", audioList[random.randint(0, len(audioList))]]).replace("\\", "\\")
                if os.path.exists(".\\speakSounds.derp"):
                    if not os.path.exists("".join([".\\sound\\assets\\speak_troll-", event["path"].split("\\")[-1], ".wav"]).replace("\\", "\\")):
                        ln = 1
                        try:
                            if event["path"].find(".mp3") == -1:
                                audiowave = WAVE("".join([".\\sound\\assets\\", event["path"].split("\\")[-1]]).replace("\\", "\\"))
                                ln = int(audiowave.info.length) + 1
                            else:
                                audiomp3 = MP3("".join([".\\sound\\assets\\", event["path"].split("\\")[-1]]).replace("\\", "\\"))
                                ln = int(audiomp3.info.length) + 1
                        except:
                            pass
                        textf = "".join([event["path"].split("\\")[-1].replace("_", " ").replace(".mp3", "").replace(".wav", ""), " "]).replace("\\", "\\")
                        textf = textf * (int(ln / (len(textf.split(" ")))) + 1)
                        gtts.gTTS(text=textf, lang="en", slow=False).save("".join([".\\sound\\assets\\speak_troll-" + event["path"].split("\\")[-1], ".wav"]).replace("\\", "\\"))
                    event["path"] = "".join([".\\sound\\assets\\", "speak_troll-", event["path"].split("\\")[-1], ".wav"]).replace("\\", "\\")
                
                if "start_delay" not in event:
                    event["start_delay"] = 0
                
                print("start_delay: " + str(event["start_delay"]))
                
                if "mute_options" not in event:
                    self.syncEvents.append(soundEvent(event["path"].replace("\\working\\", "\\"), event["volume"], event["speed"], event["channel"], event["effects"], event["balence"], startDelay=event["start_delay"]))
                else:
                    self.syncEvents.append(soundEvent(event["path"].replace("\\working\\", "\\"), event["volume"], event["speed"], event["channel"], event["effects"], event["balence"], muteOptions=event["mute_options"], startDelay=event["start_delay"]))
        list(map(loadEventsMapFunction, eventData["events"]))
    
    def load(self):
        def loadSoundsMapFunction(sound):
            time.sleep(0.05)
            sound.load(0)
        list(map(loadSoundsMapFunction, self.syncEvents))
            
    def iter(self, event=False, index=False):
        if event:
            if index:
                self.syncEvents[event].load(index)
            else:
                self.syncEvents[event].iter()
        else:
            if index:
                def soundLoadMapFunction(sound):
                    time.sleep(0.05)
                    sound.load(index)
                list(map(soundLoadMapFunction, self.syncEvents))
            else:
                def soundIterMapFunction(sound):
                    time.sleep(0.05)
                    sound.iter()
                list(map(soundIterMapFunction, self.syncEvents))
                
    def process(self, event=False):
        if event:
            shift = (20 * math.log(self.syncEvents[event].volume / 100, 10))
            self.syncEvents[event].data = self.syncEvents[event].data + shift
            def processEffectMapFunction(effect):
                time.sleep(0.05)
                self.syncEvents[event].handleEffects(effect)
            list(map(processEffectMapFunction, self.syncEvents[event].effects))
        else:
            def processSoundMapFunction(sound):
                shift = (20 * math.log(sound.volume / 100, 10))
                sound.data = sound.data + shift
                time.sleep(0.05)
                list(map(sound.handleEffects, sound.effects))
            list(map(processSoundMapFunction, self.syncEvents))
                    
    def run(self):
        
        log.crash("running...")
        printDebug(0)
        self.load()
        printDebug(1)
        self.process()
        printDebug(2)
        
        def begin(currentSyncEvents):
            
            class _inside:
                streamThreads = []
                handlerThreads = []
            
            _info = info()
            
            _info.globalSoundStart = time.perf_counter() + 3
            
            printDebug(5)
            def streamThreadAppendMapFunction(sound):
                time.sleep(0.05)
                printDebug(sound)
                
                sound._info = _info
                sound.itsStream._info = _info
                
                _inside.streamThreads.append(threading.Thread(target=thread_handler(sound.itsStream.run).run))
                _inside.handlerThreads.append(threading.Thread(target=thread_handler(sound.handleRun).run))
            list(map(streamThreadAppendMapFunction, currentSyncEvents))
            
            printDebug(6)
            def threadStartMapFunction(thread):
                thread.start()
                
            list(map(threadStartMapFunction, _inside.streamThreads))
            
            time.sleep((globals.chunkSize / 2.5) / 1000)
            
            printDebug(7)
            def handlerThreadStartMapFunction(thread):
                thread.start()
            list(map(handlerThreadStartMapFunction, _inside.handlerThreads))
        
        printDebug(30)
        def initStreamMapFunction(sound):
            printDebug(sound)
            threading.Thread(target=sound.initStream).start()
        list(map(initStreamMapFunction, self.syncEvents))
        
        printDebug(4)
        def streamWaitMapFunction(sound):
            time.sleep(0.05)
            while sound.doneLoading == False:
                time.sleep(0.1)
                print("Waiting...")
        list(map(streamWaitMapFunction, self.syncEvents))
        
        startTime = time.perf_counter()
        
        self.hasRan = []
        
        def _sortedKey(x):
            return x.startDelay
        
        self.syncEvents = sorted(self.syncEvents, key=_sortedKey, reverse=True) 
        
        printDebug(31)
        self._isWaiting = True
        self.nextDelay = 0
        self.currentDelay = 0
        while self._isWaiting and (not globals.close):
            self._isWaiting = False
            self.currentSyncEvents = []
            self.streamThreads = []
            self.handlerThreads = []
            
            if (self.nextDelay - self.currentDelay) < 0.1:
                intenseSleep(self.nextDelay - self.currentDelay)
            else:
                st = time.perf_counter()
                time.sleep((self.nextDelay - self.currentDelay) - 0.1)
                intenseSleep(0.1 - (time.perf_counter() - (st + ((self.nextDelay - self.currentDelay) - 0.1))))
            
            def initStreamMapFunction(sound):
                # printDebug(sound)
                if (sound.startDelay + startTime) < time.perf_counter():
                    if sound.uuid not in self.hasRan:
                        # sound.initStream()
                        self.hasRan.append(sound.uuid)
                        self.currentSyncEvents.append(sound)
                        self.currentDelay = sound.startDelay
                else:
                    self.nextDelay = sound.startDelay
                    self._isWaiting = True
            list(map(initStreamMapFunction, self.syncEvents))
            
            currentSyncEvents = self.currentSyncEvents
            
            if len(currentSyncEvents):
                threading.Thread(target=begin, args=(currentSyncEvents,)).start()
            
    syncEvents = []
    
    streamThreads = []
    handlerThreads = []


for arg in sys.argv:
    log.crash(os.getpid())
    if arg.split("=")[0] == "--event":
        print(arg.split("=")[1])
        eventData = json.loads(pytools.cipher.base64_decode(arg.split("=")[1]))
        multiEvent(eventData).run()
        
