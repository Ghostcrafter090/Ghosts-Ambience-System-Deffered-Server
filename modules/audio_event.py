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
            # pytools.IO.appendFile(".\\logs\\today\\event_" + log.timeString + ".log", "\n" + str(dateArray) + " :;: " + message + " :;: " + callStack.replace("\n", "    \\n\t"))

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
                            timeingInfo = ((info.globalSoundStart + self.i) - time.time())
                            if timeingInfo > 0.005:
                                intenseSleep(timeingInfo)
                            elif timeingInfo < -0.005:
                                info.globalSoundStart = info.globalSoundStart + math.fabs(timeingInfo)
                            self.audioStream.write(audioSegmentNumPy(chunk))
                        else:
                            if log.debug:
                                log.crash("Chunked Buffer Overflow!")
                        self.i = self.i + (chunk.duration_seconds / self.speed)
                    list(map(forChunkMapFunction, self.chunks))
                else:
                    if log.debug:
                        log.crash("Buffer Overflow! No more input.")
                    time.sleep(0.1)
            
            self.audioStream.stop()
            self.audioStream.close()

            # self.p.terminate()
            globals.close = True
            
        except:
            import traceback
            printDebug(traceback.format_exc())
            self.audioStream.stop()        
            self.audioStream.close()

            # self.p.terminate()
            globals.close = True
            
        # pytools.IO.appendFile("test_loop_syncs.cxl", "\n" + str(info.loopSync))

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
                    if speakers[channel][0] == n["name"]:
                        if speakers[channel][1] == "MME":
                            if n["hostapi"] == 0:
                                deviceIndex = n["index"]
                                break
                        if speakers[channel][1] == "WDM-KS":
                            if n["hostapi"] == 4:
                                deviceIndex = n["index"]
                                break
                speakers[channel].append(deviceIndex)
            pytools.IO.saveJson("inputSets.json", {
                "speakers": speakers
            })
            return speakers
        except:
            import traceback
            print(traceback.format_exc())

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
            self.muteBoolModifier = muteOptions["do_mute"]
            self.doMuteFade = muteOptions["fade"]
            if not os.path.exists(".\\" + self.muteFlag + ".derp") and not self.muteBoolModifier:
                self.isMuted = False
                self.muteState = True
            elif os.path.exists(".\\" + self.muteFlag + ".derp") and self.muteBoolModifier:
                self.isMuted = False
                self.muteState = True
            else:
                self.isMuted = True
                self.muteState = False
        else:
            self.isMuted = True
            self.muteFlag = "no_flag"
            self.muteBoolModifier = True
            self.doMuteFade = False
            self.muteState = False
            
    def initStream(self):
        try:
            if False:
                try:
                    try:
                        globals.speakers = pytools.IO.getJson("speakerSets.json", doPrint=False)["speakers"]
                    except:
                        log.crash("Unnable to load speakerSets file. Reloading...")
                        error = True
                        errorTic = 0
                        while error and (errorTic < 10):
                            try:
                                globals.speakers = pytools.IO.getJson("speakerSets.json", doPrint=False)["speakers"]
                            except:
                                log.crash("Unnable to load speakerSets file. Reloading...")
                            time.sleep(1)
                            errorTic = errorTic + 1
                    printDebug(self.channel)
                    deviceIndex = globals.speakers[self.channel][2]
                    import sounddevice as sd
                    if globals.speakers[self.channel][0] != sd.query_devices()[deviceIndex]["name"]:
                        import sounddevice as sd
                        devices = sd.query_devices()
                        for n in devices:
                            import time
                            time.sleep(0.1)
                            if globals.speakers[self.channel][0] == n["name"]:
                                if globals.speakers[self.channel][1] == "MME":
                                    if n["hostapi"] == 0:
                                        deviceIndex = n["index"]
                                        break
                                if globals.speakers[self.channel][1] == "WDM-KS":
                                    if n["hostapi"] == 4:
                                        deviceIndex = n["index"]
                                        break
                        globals.speakers[self.channel].append(deviceIndex)
                        # pytools.IO.saveJson("speakerSets.json", {
                        #     "speakers": globals.speakers
                        # })
                except:
                    import sounddevice as sd
                    devices = sd.query_devices()
                    for n in devices:
                        import time
                        time.sleep(0.1)
                        if globals.speakers[self.channel][0] == n["name"]:
                            if globals.speakers[self.channel][1] == "MME":
                                if n["hostapi"] == 0:
                                    deviceIndex = n["index"]
                                    break
                            if globals.speakers[self.channel][1] == "WDM-KS":
                                if n["hostapi"] == 4:
                                    deviceIndex = n["index"]
                                    break
                    globals.speakers[self.channel].append(deviceIndex)
                    # pytools.IO.saveJson("speakerSets.json", {
                    #     "speakers": globals.speakers
                    # })
                    
            deviceIndex = speakers.getOutputs()[self.channel][2]
                    
            from pyaudio import PyAudio
            import sounddevice as sd
            import time
            self.itsStream = stream(self.data, self.speed, deviceIndex, self.duration, self.index, self.lastPlayed, round(time.time() * 1000000), globals.bufferSize, self.balence)
            # self.itsStream.p = PyAudio()
            time.sleep(1)
            self.itsStream.audioStream = sd.OutputStream(
                # format=self.itsStream.p.get_format_from_width(self.itsStream.sample_width),
                channels=self.itsStream.channels,
                device=self.itsStream.device,
                samplerate=int(self.itsStream.frame_rate * self.speed),
            )
            # self.itsStream.audioStream.write
        except:
            import traceback
            printDebug(traceback.format_exc())
        
    data = False
    itsStream = False
    index = 0
    lastPlayed = 0
    muteState = False
    
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
            if not os.path.exists(".\\" + self.muteFlag + ".derp") and not self.muteBoolModifier:
                self.muteState = True
            elif os.path.exists(".\\" + self.muteFlag + ".derp") and self.muteBoolModifier:
                self.muteState = True
            else:
                self.muteState = False
                
            if not self.muteState:
                if not self.isMuted:
                    if self.doMuteFade:
                        if globals.chunkSize < 4096:
                            self.data = self.data.fade_in(globals.chunkSize * 1000)
                        else:
                            self.data = self.data.fade_in(4096)
                    self.isMuted = True
            else:
                if self.isMuted:
                    if self.doMuteFade:
                        if globals.chunkSize < 4096:
                            self.data = self.data.fade_out(globals.chunkSize * 1000)
                        else:
                            self.data = self.data.fade_out(4096)
                    else:
                        self.data = self.data - 100
                    self.isMuted = False
                else:
                    self.data = self.data - 100
            
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
                
                # for effect in self.effects:
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
                # for sound in self.syncEvents:
                def soundLoadMapFunction(sound):
                    import time
                    time.sleep(0.05)
                    sound.load(index)
                list(map(soundLoadMapFunction, self.syncEvents))
            else:
                # for sound in self.syncEvents:
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
        # for sound in self.syncEvents:
        def initStreamMapFunction(sound):
            import time
            time.sleep(0.05)
            printDebug(sound)
            sound.initStream()
        list(map(initStreamMapFunction, self.syncEvents))
        
        printDebug(4)
        # for sound in self.syncEvents:
        def streamWaitMapFunction(sound):
            import time
            time.sleep(0.05)
            # printDebug("waiting on: " + str(i))
            while sound.itsStream == False:
                time.sleep(0.1)
        list(map(streamWaitMapFunction, self.syncEvents))
            
        info.globalSoundStart = time.time() + 3
            
        printDebug(5)
        # for sound in self.syncEvents:
        def streamThreadAppendMapFunction(sound):
            import time
            time.sleep(0.05)
            printDebug(sound)
            import threading
            self.streamThreads.append(threading.Thread(target=thread_handler(sound.itsStream.run).run))
            self.handlerThreads.append(threading.Thread(target=thread_handler(sound.handleRun).run))
        list(map(streamThreadAppendMapFunction, self.syncEvents))
        
        printDebug(6)
        # for thread in self.streamThreads:
        def threadStartMapFunction(thread):
            thread.start()
        list(map(threadStartMapFunction, self.streamThreads))
        
        time.sleep((globals.chunkSize / 2.5) / 1000)
        
        printDebug(7)
        # for thread in self.handlerThreads:
        def handlerThreadStartMapFunction(thread):
            # printDebug("launching: " + str(i))
            thread.start()
        list(map(handlerThreadStartMapFunction, self.handlerThreads))
        
        # if self.wait == 1:
        #     # for thread in self.handlerThreads:
        #     def handlerThreadJoinMapFunction(thread):
        #         time.sleep(0.1)
        #         thread.join()
        #     list(map(handlerThreadJoinMapFunction, self.handlerThreads))
            
    syncEvents = []
    
    streamThreads = []
    handlerThreads = []
    
class playSoundWindow:
    def __init__(self, path, volume, speed, balence, wait, remember=False, lowPass=False, highPass=False, play=True):
        self.path = path
        self.volume = volume
        self.speed = speed
        self.balence = balence
        self.wait = wait
        self.remember = remember
        self.lowPass = lowPass
        self.highPass = highPass
        self.run(play=play)
        
    eventData = {}
    
    def getVolume(self, intf):
        if str(self.volume)[0] == "[":
            return self.volume[intf]
        else:
            return self.volume
    
    def run(self, play=True):
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
            if os.path.exists(".\\nomufflewn.derp"):
                eventData = {
                    "events": [
                        {
                            "path": ".\\sound\\assets\\" + self.path.split(";")[1],
                            "volume": self.getVolume(1),
                            "speed": self.speed,
                            "balence": self.balence,
                            "channel": "windown",
                            "effects": effects
                        },
                    ],
                    "wait": self.wait
                }
                import random
                uuid = random.random()
                while uuid in obj.activeSounds:
                    uuid = random.random()
                if self.path.split(";")[1].find(".mp3") != -1:
                    from mutagen.mp3 import MP3
                    duration = float(MP3(".\\sound\\assets\\" + self.path.split(";")[1]).info.length) / self.speed
                else:
                    from mutagen.wave import WAVE
                    duration = float(WAVE(".\\sound\\assets\\" + self.path.split(";")[1]).info.length) / self.speed
                obj.activeSounds[uuid] = [self.path.split(";")[1].split("\\")[-1], "windown", pytools.clock.getDateTime(), duration]
            else:
                eventData = {
                    "events": [
                        {
                            "path": ".\\sound\\assets\\" + self.path.split(";")[0],
                            "volume": self.getVolume(0),
                            "speed": self.speed,
                            "balence": self.balence,
                            "channel": "window",
                            "effects": effects
                        },
                        {
                            "path": ".\\sound\\assets\\" + self.path.split(";")[1],
                            "volume": self.getVolume(1),
                            "speed": self.speed,
                            "balence": self.balence,
                            "channel": "outside",
                            "effects": effects
                        }
                    ],
                    "wait": self.wait
                }
                import random
                uuid = random.random()
                while uuid in obj.activeSounds:
                    uuid = random.random()
                if self.path.split(";")[1].find(".mp3") != -1:
                    duration = float(MP3(".\\sound\\assets\\" + self.path.split(";")[1]).info.length) / self.speed
                else:
                    duration = float(WAVE(".\\sound\\assets\\" + self.path.split(";")[1]).info.length) / self.speed
                obj.activeSounds[uuid] = [self.path.split(";")[1].split("\\")[-1], "outside", pytools.clock.getDateTime(), duration]
                uuid = random.random()
                while uuid in obj.activeSounds:
                    uuid = random.random()
                if self.path.split(";")[0].find(".mp3") != -1:
                    duration = float(MP3(".\\sound\\assets\\" + self.path.split(";")[0]).info.length) / self.speed
                else:
                    duration = float(WAVE(".\\sound\\assets\\" + self.path.split(";")[0]).info.length) / self.speed
                obj.activeSounds[uuid] = [self.path.split(";")[0].split("\\")[-1], "window", pytools.clock.getDateTime(), duration]
        else:
            if os.path.exists(".\\nomufflewn.derp"):
                eventData = {
                    "events": [
                        {
                            "path": ".\\sound\\assets\\" + self.path,
                            "volume": self.getVolume(1),
                            "speed": self.speed,
                            "balence": self.balence,
                            "channel": "windown",
                            "effects": effects
                        },
                    ],
                    "wait": self.wait
                }
                uuid = random.random()
                while uuid in obj.activeSounds:
                    uuid = random.random()
                if self.path.find(".mp3") != -1:
                    duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
                else:
                    duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
                obj.activeSounds[uuid] = [self.path.split("\\")[-1], "windown", pytools.clock.getDateTime(), duration]
            else:
                eventData = {
                    "events": [
                        {
                            "path": ".\\sound\\assets\\" + self.path,
                            "volume": self.getVolume(0),
                            "speed": self.speed,
                            "balence": self.balence,
                            "channel": "window",
                            "effects": effects
                        },
                        {
                            "path": ".\\sound\\assets\\" + self.path,
                            "volume": self.getVolume(1),
                            "speed": self.speed,
                            "balence": self.balence,
                            "channel": "outside",
                            "effects": effects
                        }
                    ],
                    "wait": self.wait
                }
                uuid = random.random()
                while uuid in obj.activeSounds:
                    uuid = random.random()
                if self.path.find(".mp3") != -1:
                    duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
                else:
                    duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
                obj.activeSounds[uuid] = [self.path.split("\\")[-1], "outside", pytools.clock.getDateTime(), duration]
                uuid = random.random()
                while uuid in obj.activeSounds:
                    uuid = random.random()
                if self.path.find(".mp3") != -1:
                    duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
                else:
                    duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
                obj.activeSounds[uuid] = [self.path.split("\\")[-1], "window", pytools.clock.getDateTime(), duration]
        self.eventData = eventData
        if play:
            if duration < 30:
                try:
                    try:
                        test = int(pytools.IO.getFile("soundCount.cx"))
                    except:
                        test = globals.maxCount + 1
                    if test > globals.maxCount:
                        while test > globals.maxCount:
                            try:
                                test = int(pytools.IO.getFile("soundCount.cx"))
                            except:
                                test = globals.maxCount + 1
                            import time
                            time.sleep(1)
                except:
                    pass
            import json
            if self.wait:
                os.system("start /realtime /d \"" + os.getcwd().replace("\\working", "") + "\" /b /wait "" .\\ambience.exe .\\modules\\audio.py --event=\"" + pytools.cipher.base64_encode(json.dumps(eventData)) + "\"")
            else:
                os.system("start /realtime /d \"" + os.getcwd().replace("\\working", "") + "\" /b "" .\\ambience.exe .\\modules\\audio.py --event=\"" + pytools.cipher.base64_encode(json.dumps(eventData)) + "\"")
            
    
class playSoundAll:
    def __init__(self, path, volume, speed, balence, wait, remember=False, lowPass=False, highPass=False):
        self.path = path
        self.volume = volume
        self.speed = speed
        self.balence = balence
        self.wait = wait
        self.remember = remember
        self.lowPass = lowPass
        self.highPass = highPass
        self.run()
    
    def run(self):
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
                    "path": ".\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "clock",
                    "effects": effects
                },
                {
                    "path": ".\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "generic",
                    "effects": effects
                },
                {
                    "path": ".\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "fireplace",
                    "effects": effects
                },
                {
                    "path": ".\\sound\\assets\\" + self.path,
                    "volume": self.volume,
                    "speed": self.speed,
                    "balence": self.balence,
                    "channel": "windown",
                    "effects": effects
                },
            ],
            "wait": self.wait
        }
        import random
        from mutagen.mp3 import MP3
        from mutagen.wave import WAVE
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [self.path.split("\\")[-1], "clock", pytools.clock.getDateTime(), duration]
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [self.path.split("\\")[-1], "generic", pytools.clock.getDateTime(), duration]
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [self.path.split("\\")[-1], "fireplace", pytools.clock.getDateTime(), duration]
        uuid = random.random()
        while uuid in obj.activeSounds:
            uuid = random.random()
        if self.path.find(".mp3") != -1:
            duration = float(MP3(".\\sound\\assets\\" + self.path).info.length) / self.speed
        else:
            duration = float(WAVE(".\\sound\\assets\\" + self.path).info.length) / self.speed
        obj.activeSounds[uuid] = [self.path.split("\\")[-1], "windown", pytools.clock.getDateTime(), duration]
        if duration < 30:
            try:
                try:
                    test = int(pytools.IO.getFile("soundCount.cx"))
                except:
                    test = globals.maxCount + 1
                if test > globals.maxCount:
                    while test > globals.maxCount:
                        try:
                            test = int(pytools.IO.getFile("soundCount.cx"))
                        except:
                            test = globals.maxCount + 1
                        import time
                        time.sleep(1)
            except:
                pass
        import json
        if self.wait:
            os.system("start /realtime /d \"" + os.getcwd().replace("\\working", "") + "\" /b /wait "" .\\ambience.exe .\\modules\\audio.py --event=\"" + pytools.cipher.base64_encode(json.dumps(eventData)) + "\"")
        else:
            os.system("start /realtime /d \"" + os.getcwd().replace("\\working", "") + "\" /b "" .\\ambience.exe .\\modules\\audio.py --event=\"" + pytools.cipher.base64_encode(json.dumps(eventData)) + "\"")
            
class event:
    def __init__(self):
        self.eventData = {
            "events": [],
            "wait": False
        }
    
    eventData = {
        "events": [],
        "wait": False
    }
    
    duration = 0
    
    def registerWindow(self, path, volume, speed, balence, wait, remember=False, lowPass=False, highPass=False):
        self.eventData["events"].extend(playSoundWindow(path, volume, speed, balence, wait, remember=remember, lowPass=lowPass, highPass=highPass, play=False).eventData["events"])
    
    def register(self, path, speaker, volume, speed, balence, wait, clock=True, remember=False, lowPass=False, highPass=False, keepLoaded=False):
        
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
        if remember:
            effects.append({
                "type": "rememberbypass",
            })
        
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
        else:
            speakern = ["windown"]
        
        for channel in speakern:
            self.eventData["events"].append({
                "path": ".\\sound\\assets\\" + path,
                "volume": volume,
                "speed": speed,
                "channel": channel,
                "balence": balence,
                "effects": effects
            })
            import random
            from mutagen.mp3 import MP3
            from mutagen.wave import WAVE
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
    
    def run(self, spawnChild=True):
        if self.duration < 30:
            try:
                try:
                    test = int(pytools.IO.getFile("soundCount.cx"))
                except:
                    test = globals.maxCount + 1
                if test > globals.maxCount:
                    while test > globals.maxCount:
                        try:
                            test = int(pytools.IO.getFile("soundCount.cx"))
                        except:
                            test = globals.maxCount + 1
                        import time
                        time.sleep(1)
            except:
                pass
        if spawnChild:
            import json
            if self.eventData["wait"]:
                os.system("start /realtime /d \"" + os.getcwd().replace("\\working", "") + "\" /b /wait "" .\\ambience.exe .\\modules\\audio.py --event=\"" + pytools.cipher.base64_encode(json.dumps(self.eventData)) + "\"")
            else:
                os.system("start /realtime /d \"" + os.getcwd().replace("\\working", "") + "\" /b "" .\\ambience.exe .\\modules\\audio.py --event=\"" + pytools.cipher.base64_encode(json.dumps(self.eventData)) + "\"")
        else:
            multiEvent(self.eventData).run()

import sys
for arg in sys.argv:
    import os
    log.crash(os.getpid())
    if arg.split("=")[0] == "--event":
        import json
        print(arg.split("=")[1])
        eventData = json.loads(pytools.cipher.base64_decode(arg.split("=")[1]))
        multiEvent(eventData).run()
        
