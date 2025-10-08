import time
import math
import os
import random
import sys
import atexit
import signal

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
            from datetime import datetime
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
            import base64
            encode = base64.standard_b64encode(bytes(s, encoding="utf-8")).decode("utf-8").replace("=", "?")
            return encode
            
        def base64_decode(s: str):
            import base64
            decode = base64.standard_b64decode(s.replace("?", "=")).decode("utf-8")
            return decode
    
    class IO:
        def getJson(path, doPrint=True):
            import json
            import sys
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
            import xmltodict
            return xmltodict.parse(pytools.IO.getFile(path, doPrint=doPrint))
        
        def saveXml(path, doPrint=True):
            pass

        def saveJson(path, jsonData):
            import json
            import sys
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
            import sys
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
            import sys
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
            import sys
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
            import sys
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
            import pickle
            import sys
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
            import pickle
            import sys
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
            import sys
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
            import zipfile
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
            import shutil
            shutil.make_archive(path, 'zip', dir)

if __name__ == '__main__':
    atexit.register(exit_handler)
    signal.signal(signal.SIGINT, kill_handler)
    signal.signal(signal.SIGTERM, kill_handler)

class info:
    globalSoundStart = False
    loopSync = {}
    skipParodyCheck = False
    
def intenseSleep(i):
    x = time.time() + i
    while time.time() < x:
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

import os
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
            import sounddevice as sd
            devices = sd.query_devices()
            for channel in globals.speakers:
                for n in devices:
                    import time
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
            import traceback
            log.crash(traceback.format_exc())
    
class audioEffects:
    def lowPass(data, frequency, db=24):
        from pydub.scipy_effects import low_pass_filter
        if (data != False) and (type(data) != float):
            return data.low_pass_filter(frequency, order=db)
        else:
            return False
    
    def highPass(data, frequency, db=24):
        from pydub.scipy_effects import high_pass_filter
        if (data != False) and (type(data) != float):
            return data.high_pass_filter(frequency, order=db)
        else:
            return False
        
class stream:
    def __init__(self, seg, speed, device, duration, soundIndex, lastPlayed, startPlayed, bufferSize, balence):
        import pydub.utils
        self.channels = seg.channels
        self.frame_rate = seg.frame_rate
        self.sample_width = seg.sample_width
        self.chunksActive = pydub.utils.make_chunks(seg, globals.chunkSize)
        self.chunks = False
        self.speed = speed
        self.device = device
        self.duration = duration
        self.soundIndex = soundIndex
        self.lastPlayed = lastPlayed
        self.startPlayed = startPlayed
        self.bufferSize = bufferSize
        
    audioStream = False
    p = False
    
    def run(self):
        
        import random
        idf = random.random()
        
        try:
            import math
            loopTic = 0
            import numpy
            import sounddevice as sd
            self.audioStream.start()
            def audioSegmentNumPy(audio):
                return numpy.array(audio.get_array_of_samples(), dtype=numpy.float32).reshape((-1, audio.channels)) / (1 << (8 * audio.sample_width - 1))
            self.i = 0
            
            while (self.startPlayed + (self.duration * 1000000) + (5 * 1000000)) > round(time.time() * 1000000):
                self.chunks = self.chunksActive
                self.chunksActive = True
                if (self.chunks != True) and (self.chunks != False):
                    def forChunkMapFunction(chunk):
                        if chunk:
                            if self.i == 0:
                                info.globalSoundStart = time.time()
                                self.startPlayed = round(time.time() * 1000000)
                            timeingInfo = ((info.globalSoundStart + self.i) - time.time())
                            if timeingInfo > 0.005:
                                intenseSleep(timeingInfo)
                                self.audioStream.write(audioSegmentNumPy(chunk))
                            elif timeingInfo < -0.005:
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
                    if log.debug:
                        log.crash("Buffer Overflow!")
                    time.sleep(0.1)
            
            self.audioStream.stop()
            self.audioStream.close()

            globals.close = True
            
        except:
            import traceback
            printDebug(traceback.format_exc())
            self.audioStream.stop()        
            self.audioStream.close()

            globals.close = True

class speakers:
    def getOutputs():
        if os.path.exists(".\\soundInputs.json"):
            speakers = pytools.IO.getJson(".\\soundInputs.json")
        if os.path.exists("..\\soundInputs.json"):
            speakers = pytools.IO.getJson("..\\soundInputs.json")
        try:
            import sounddevice as sd
            devices = sd.query_devices()
            for channel in speakers:
                for n in devices:
                    import time
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
            import traceback
            printDebug(traceback.format_exc())

class soundEvent:
    def __init__(self, path, volume, speed, channel, effects, balence, muteOptions=False):
        self.path = path
        import random
        self.uuid = random.random()
        while self.uuid in obj.activeSounds:
            self.uuid = random.random()
        self.volume = volume
        self.speed = speed
        self.balence = balence
        self.channel = channel
        self.effects = effects
        if path.find(".mp3") != -1:
            from mutagen.mp3 import MP3
            self.duration = float(MP3(path).info.length) / speed
        else:
            from mutagen.wave import WAVE
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
     
    def initStream(self):
        try:
                    
            deviceIndex = speakers.getOutputs()[self.channel][2]
                    
            from pyaudio import PyAudio
            import sounddevice as sd
            import time
            self.itsStream = stream(self.data, self.speed, deviceIndex, self.duration, self.index, self.lastPlayed, round(time.time() * 1000000), globals.bufferSize, self.balence)
            time.sleep(1)
            self.itsStream.audioStream = sd.OutputStream(
                channels=self.itsStream.channels,
                device=self.itsStream.device,
                samplerate=int(self.itsStream.frame_rate * self.speed),
            )
        except:
            import traceback
            printDebug(traceback.format_exc())
        
    data = False
    itsStream = False
    index = 0
    lastPlayed = 0
    
    def load(self, index):
        self.index = index
        import math
        if math.floor((self.duration / globals.bufferSize) + 1) >= index:
            import os
            lastModif = os.path.getmtime(self.path)
            if os.path.exists(".\\.audiocache\\" + self.path.split("\\")[-1] + "-cache." + str(index * globals.bufferSize) + ".pyl"):
                printDebug("".join(["loading cached index " + str(index), "..."]))
                cachedData = pytools.IO.getList(".\\.audiocache\\" + self.path.split("\\")[-1] + "-cache." + str(index * globals.bufferSize) + ".pyl")[1]
                self.data = cachedData[0]
                if cachedData[1] != lastModif:
                    printDebug("".join(["not cached! loading index " + str(index), "..."]))
                    import pydub
                    self.data = pydub.AudioSegment.from_file(file=self.path.replace("\t", "\\t"), format="mp3", start_second=index * globals.bufferSize, duration=globals.bufferSize)
                    pytools.IO.saveList(".\\.audiocache\\" + self.path.split("\\")[-1] + "-cache." + str(index * globals.bufferSize) + ".pyl", [self.data, lastModif])
            else:
                printDebug("".join(["not cached! loading index " + str(index), "..."]))
                import pydub
                self.data = pydub.AudioSegment.from_file(file=self.path.replace("\t", "\\t"), format="mp3", start_second=index * globals.bufferSize, duration=globals.bufferSize)
                pytools.IO.saveList(".\\.audiocache\\" + self.path.split("\\")[-1] + "-cache." + str(index * globals.bufferSize) + ".pyl", [self.data, lastModif])
        else:
            self.data = False
            
        bal = False
        
        import os
        
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
                import pydub
                monoSets = [monoSets[0], monoSets[0]]
                self.data = pydub.AudioSegment.from_mono_audiosegments(*monoSets)
            if self.balence < 0:
                monoSets[1] = monoSets[1] + (20 * math.log((0.01 + 100 - math.fabs(self.balence)) / 100, 10))
                bal = True
            elif self.balence > 0:
                monoSets[0] = monoSets[0] + (20 * math.log((0.01 + 100 - math.fabs(self.balence)) / 100, 10))
                bal = True
        
        if bal:
            import pydub
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
            import time
            import math
            startPlayed = round(time.time() * 1000000)
            obj.activeSounds[self.uuid] = self.path.split("\\")[-1]
            log.crash("".join(["Playing sound of path ", self.path, " on the ", self.channel, " channel at volume ", str((20 * math.log(self.volume / 100, 10))), " at ", str(self.speed), "x speed..."]))
            while self.data != False:
                time.sleep(0.05)
                if globals.close:
                    return
                self.iter()
                import math
                shift = (20 * math.log(self.volume / 100, 10))
                self.data = self.data + shift
                if (type(self.data) == float) or (self.data == False): # < possible problem (returning on datatype False)
                    return
                
                def handleEffectsMapFunction(effect):
                    if globals.close:
                        return
                    self.handleEffects(effect)
                list(map(handleEffectsMapFunction, self.effects))
                import pydub
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
                    if globals.close:
                        return
                    time.sleep(0.5)
            obj.activeSounds.pop(self.uuid)
        except:
            import traceback
            printDebug(traceback.format_exc())
        
class multiEvent:
    def __init__(self, eventData):
        log.crash("multiEvent_init_0")
        self.wait = eventData["wait"]
        self.eventData = eventData
        def loadEventsMapFunction(event):
            log.crash("multiEvent_init_1")
            import time
            time.sleep(0.1)
            if event["volume"] > 0.0:
                if os.path.exists(".\\randomSounds.derp"):
                    audioList = os.listdir(".\\sound\\assets")
                    import random
                    event["path"] = "".join([".\\sound\\assets\\", audioList[random.randint(0, len(audioList))]]).replace("\\", "\\")
                    while (event["path"].find(".mp3") == -1) and (event["path"].find(".wav") == -1):
                        time.sleep(0.1)
                        event["path"] = "".join([".\\sound\\assets\\", audioList[random.randint(0, len(audioList))]]).replace("\\", "\\")
                if os.path.exists(".\\speakSounds.derp"):
                    if not os.path.exists("".join([".\\sound\\assets\\speak_troll-", event["path"].split("\\")[-1], ".wav"]).replace("\\", "\\")):
                        ln = 1
                        try:
                            if event["path"].find(".mp3") == -1:
                                from mutagen.wave import WAVE
                                audiowave = WAVE("".join([".\\sound\\assets\\", event["path"].split("\\")[-1]]).replace("\\", "\\"))
                                ln = int(audiowave.info.length) + 1
                            else:
                                from mutagen.mp3 import MP3
                                audiomp3 = MP3("".join([".\\sound\\assets\\", event["path"].split("\\")[-1]]).replace("\\", "\\"))
                                ln = int(audiomp3.info.length) + 1
                        except:
                            pass
                        textf = "".join([event["path"].split("\\")[-1].replace("_", " ").replace(".mp3", "").replace(".wav", ""), " "]).replace("\\", "\\")
                        textf = textf * (int(ln / (len(textf.split(" ")))) + 1)
                        import gtts
                        gtts.gTTS(text=textf, lang="en", slow=False).save("".join([".\\sound\\assets\\speak_troll-" + event["path"].split("\\")[-1], ".wav"]).replace("\\", "\\"))
                    event["path"] = "".join([".\\sound\\assets\\", "speak_troll-", event["path"].split("\\")[-1], ".wav"]).replace("\\", "\\")
                if "mute_options" not in event:
                    self.syncEvents.append(soundEvent(event["path"].replace("\\working\\", "\\"), event["volume"], event["speed"], event["channel"], event["effects"], event["balence"]))
                else:
                    self.syncEvents.append(soundEvent(event["path"].replace("\\working\\", "\\"), event["volume"], event["speed"], event["channel"], event["effects"], event["balence"], muteOptions=event["mute_options"]))
        list(map(loadEventsMapFunction, eventData["events"]))
    
    def load(self):
        def loadSoundsMapFunction(sound):
            import time
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
                    import time
                    time.sleep(0.05)
                    sound.load(index)
                list(map(soundLoadMapFunction, self.syncEvents))
            else:
                def soundIterMapFunction(sound):
                    import time
                    time.sleep(0.05)
                    sound.iter()
                list(map(soundIterMapFunction, self.syncEvents))
                
    def process(self, event=False):
        if event:
            import math
            shift = (20 * math.log(self.syncEvents[event].volume / 100, 10))
            self.syncEvents[event].data = self.syncEvents[event].data + shift
            def processEffectMapFunction(effect):
                import time
                time.sleep(0.05)
                self.syncEvents[event].handleEffects(effect)
            list(map(processEffectMapFunction, self.syncEvents[event].effects))
        else:
            def processSoundMapFunction(sound):
                import math
                shift = (20 * math.log(sound.volume / 100, 10))
                sound.data = sound.data + shift
                import time
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
        
        printDebug(3)
        def initStreamMapFunction(sound):
            import time
            time.sleep(0.05)
            printDebug(sound)
            sound.initStream()
        list(map(initStreamMapFunction, self.syncEvents))
        
        printDebug(4)
        def streamWaitMapFunction(sound):
            import time
            time.sleep(0.05)
            xf = 0
            while (sound.itsStream == False) and (xf < 1200):
                time.sleep(0.1)
                xf = xf + 1
        list(map(streamWaitMapFunction, self.syncEvents))
            
        info.globalSoundStart = time.time() + 3
            
        printDebug(5)
        def streamThreadAppendMapFunction(sound):
            import time
            time.sleep(0.05)
            printDebug(sound)
            import threading
            self.streamThreads.append(threading.Thread(target=thread_handler(sound.itsStream.run).run))
            self.handlerThreads.append(threading.Thread(target=thread_handler(sound.handleRun).run))
        list(map(streamThreadAppendMapFunction, self.syncEvents))
        
        printDebug(6)
        def threadStartMapFunction(thread):
            thread.start()
        list(map(threadStartMapFunction, self.streamThreads))
        
        time.sleep((globals.chunkSize / 2.5) / 1000)
        
        printDebug(7)
        def handlerThreadStartMapFunction(thread):
            thread.start()
        list(map(handlerThreadStartMapFunction, self.handlerThreads))
            
    syncEvents = []
    
    streamThreads = []
    handlerThreads = []


import sys
for arg in sys.argv:
    import os
    log.crash(os.getpid())
    if arg.split("=")[0] == "--event":
        import json
        print(arg.split("=")[1])
        eventData = json.loads(pytools.cipher.base64_decode(arg.split("=")[1]))
        multiEvent(eventData).run()
        
