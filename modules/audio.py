from traceback import format_exc as traceback_format_exc, format_stack as traceback_format_stack
class traceback:
    format_exc = traceback_format_exc
    format_stack = traceback_format_stack

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

# print = log.printLog

def _mk_butter_filter(freq, type, order):
    """
    Args:
        freq: The cutoff frequency for highpass and lowpass filters. For
            band filters, a list of [low_cutoff, high_cutoff]
        type: "lowpass", "highpass", or "band"
        order: nth order butterworth filter (default: 5th order). The
            attenuation is -6dB/octave beyond the cutoff frequency (for 1st
            order). A Higher order filter will have more attenuation, each level
            adding an additional -6dB (so a 3rd order butterworth filter would
            be -18dB/octave).

    Returns:
        function which can filter a mono audio segment

    """
    def filter_fn(seg):
        assert seg.channels == 1

        nyq = 0.5 * seg.frame_rate
        try:
            freqs = [f / nyq for f in freq]
        except TypeError:
            freqs = freq / nyq

        sos = butter(order, freqs, btype=type, output='sos')
        y = sosfilt(sos, seg.get_array_of_samples())

        return seg._spawn(y.astype(seg.array_type))

    return filter_fn

def high_pass_filter(seg, cutoff_freq, order=5):
    filter_fn = _mk_butter_filter(cutoff_freq, 'highpass', order=order)
    return seg.apply_mono_filter_to_each_channel(filter_fn)

def low_pass_filter(seg, cutoff_freq, order=5):
    filter_fn = _mk_butter_filter(cutoff_freq, 'lowpass', order=order)
    return seg.apply_mono_filter_to_each_channel(filter_fn)

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
    
if os.path.exists(".\\soundOutputs.json"):
    globals.speakers = pytools.IO.getJson(".\\soundOutputs.json")
if os.path.exists("..\\soundOutputs.json"):
    globals.speakers = pytools.IO.getJson("..\\soundOutputs.json")
    
class audioEffects:
    def lowPass(data, frequency, db=24):
        return data.low_pass_filter(frequency, order=db)
    
    def highPass(data, frequency, db=24):
            return data.high_pass_filter(frequency, order=db)
        
class stream:
    def __init__(self, seg, speed, device, duration, soundIndex, lastPlayed, startPlayed, bufferSize, balence):
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
        printDebug(self.channels)
        
        printDebug(self.chunksActive)

        try:
            print((self.startPlayed + (self.duration * 1000000) + (5 * 1000000)))
            print(round(time.time() * 1000000))
            loopTic = 0
            while (self.startPlayed + (self.duration * 1000000) + (5 * 1000000)) > round(time.time() * 1000000):
                self.chunks = self.chunksActive
                self.chunksActive = True
                if (self.chunks != True) and (self.chunks != False):
                    def forChunkMapFunction(chunk):
                        self.audioStream.write(chunk._data)
                    list(map(forChunkMapFunction, self.chunks))
                else:
                    time.sleep(0.1)
                        
            self.audioStream.stop_stream()
            self.audioStream.close()

            self.p.terminate()
            globals.close = True
            exit()
            
        except:
            printDebug(traceback.format_exc())
            self.audioStream.stop_stream()
            self.audioStream.close()

            self.p.terminate()
            globals.close = True
            exit()

class soundEvent:
    def __init__(self, path, volume, speed, channel, effects, balence):
        self.path = path
        self.uuid = random.random()
        while self.uuid in obj.activeSounds:
            self.uuid = random.random()
        self.volume = volume
        self.speed = speed
        self.balence = balence
        self.channel = channel
        self.effects = effects
        if path.find(".mp3") != -1:
            self.duration = float(MP3(path).info.length) / speed
        else:
            self.duration = float(WAVE(path).info.length) / speed
            
    def initStream(self):
        try:
            try:
                try:
                    globals.speakers = pytools.IO.getJson("speakerSets.json")["speakers"]
                except:
                    pass
                printDebug(self.channel)
                deviceIndex = globals.speakers[self.channel][2]
            except:
                devices = sd.query_devices()
                for n in devices:
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
                pytools.IO.saveJson("speakerSets.json", {
                    "speakers": globals.speakers
                })
            self.itsStream = stream(self.data, self.speed, deviceIndex, self.duration, self.index, self.lastPlayed, round(time.time() * 1000000), globals.bufferSize, self.balence)
            self.itsStream.p = PyAudio()
            self.itsStream.audioStream = self.itsStream.p.open(
                format=self.itsStream.p.get_format_from_width(self.itsStream.sample_width),
                channels=self.itsStream.channels,
                output_device_index=self.itsStream.device,
                rate=int(self.itsStream.frame_rate * self.speed),
                output=True
            )
        except:
            printDebug(traceback.format_exc())
        
    data = False
    itsStream = False
    index = 0
    lastPlayed = 0
    
    def load(self, index):
        self.index = index
        printDebug("".join(["loading index " + str(index), "..."]))
        if math.floor((self.duration / globals.bufferSize) + 1) >= index:
            self.data = pydub.AudioSegment.from_file(file=self.path.replace("\t", "\\t"), format="mp3", start_second=index * globals.bufferSize, duration=globals.bufferSize)
        else:
            self.data = False
        if self.balence != 0:
            monoSets = self.data.split_to_mono()
            bal = False
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
    
    def handleRun(self):
        try:
            startPlayed = round(time.time() * 1000000)
            obj.activeSounds[self.uuid] = self.path.split("\\")[-1]
            print("".join(["Playing sound of path ", self.path, " on the ", self.channel, " channel at volume ", str((20 * math.log(self.volume / 100, 10))), " at ", str(self.speed), "x speed..."]))
            while self.data != False:
                time.sleep(0.05)
                if globals.close:
                    exit()
                self.iter()
                shift = (20 * math.log(self.volume / 100, 10))
                self.data = self.data + shift
                # for effect in self.effects:
                def handleEffectsMapFunction(effect):
                    if globals.close:
                        exit()
                    self.handleEffects(effect)
                list(map(handleEffectsMapFunction, self.effects))
                self.itsStream.chunksActive = pydub.utils.make_chunks(self.data, globals.chunkSize)
                self.lastPlayed = (startPlayed + (self.index * 1000000)) / 1000000
                self.itsStream.lastPlayed = self.lastPlayed
                while self.itsStream.chunksActive != True:
                    if globals.close:
                        exit()
                    time.sleep(0.5)
            obj.activeSounds.pop(self.uuid)
        except:
            printDebug(traceback.format_exc())
        exit()
        
class multiEvent:
    def __init__(self, eventData):
        self.wait = eventData["wait"]
        self.eventData = eventData
        def loadEventsMapFunction(event):
            time.sleep(0.1)
            if event["volume"] > 0.0:
                if os.path.exists(".\\working\\randomSounds.derp"):
                    audioList = os.listdir(".\\working\\sound\\assets")
                    event["path"] = "".join([".\\working\\sound\\assets\\", audioList[random.randint(0, len(audioList))]])
                    while (event["path"].find(".mp3") == -1) and (event["path"].find(".wav") == -1):
                        time.sleep(0.1)
                        event["path"] = "".join([".\\working\\sound\\assets\\", audioList[random.randint(0, len(audioList))]])
                if os.path.exists(".\\working\\speakSounds.derp"):
                    if not os.path.exists("".join([".\\working\\sound\\assets\\speak_troll-", event["path"].split("\\")[-1], ".wav"])):
                        ln = 1
                        try:
                            if event["path"].find(".mp3") == -1:
                                audiowave = WAVE("".join([".\\working\\sound\\assets\\", event["path"].split("\\")[-1]]))
                                ln = int(audiowave.info.length) + 1
                            else:
                                audiomp3 = MP3("".join([".\\working\\sound\\assets\\", event["path"].split("\\")[-1]]))
                                ln = int(audiomp3.info.length) + 1
                        except:
                            pass
                        textf = "".join([event["path"].split("\\")[-1].replace("_", " ").replace(".mp3", "").replace(".wav", ""), " "])
                        textf = textf * (int(ln / (len(textf.split(" ")))) + 1)
                        gtts.gTTS(text=textf, lang="en", slow=False).save("".join([".\\working\\sound\\assets\\speak_troll-" + event["path"].split("\\")[-1], ".wav"]))
                    event["path"] = "".join([".\\working\\sound\\assets\\", "speak_troll-", event["path"].split("\\")[-1], ".wav"])
                self.syncEvents.append(soundEvent(event["path"], event["volume"], event["speed"], event["channel"], event["effects"], event["balence"]))
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
                # for sound in self.syncEvents:
                def soundLoadMapFunction(sound):
                    time.sleep(0.05)
                    sound.load(index)
                list(map(soundLoadMapFunction, self.syncEvents))
            else:
                # for sound in self.syncEvents:
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
        printDebug(0)
        self.load()
        printDebug(1)
        self.process()
        printDebug(2)
        
        printDebug(3)
        # for sound in self.syncEvents:
        def initStreamMapFunction(sound):
            time.sleep(0.05)
            printDebug(sound)
            sound.initStream()
        list(map(initStreamMapFunction, self.syncEvents))
        
        printDebug(4)
        # for sound in self.syncEvents:
        def streamWaitMapFunction(sound):
            time.sleep(0.05)
            # printDebug("waiting on: " + str(i))
            while sound.itsStream == False:
                time.sleep(0.1)
        list(map(streamWaitMapFunction, self.syncEvents))
            
        printDebug(5)
        # for sound in self.syncEvents:
        def streamThreadAppendMapFunction(sound):
            time.sleep(0.05)
            printDebug(sound)
            self.streamThreads.append(threading.Thread(target=sound.itsStream.run))
            self.handlerThreads.append(threading.Thread(target=sound.handleRun))
        list(map(streamThreadAppendMapFunction, self.syncEvents))
            
        printDebug(6)
        # for thread in self.streamThreads:
        def threadStartMapFunction(thread):
            time.sleep(0.05)
            printDebug(thread)
            thread.start()
        list(map(threadStartMapFunction, self.streamThreads))
        
        printDebug(7)
        # for thread in self.handlerThreads:
        def handlerThreadStartMapFunction(thread):
            time.sleep(0.05)
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
                    if not os.path.exists(".\\host-" + hosts.listf[hostWeights[i][1]] + ".bl"):
                        if hostWeights[i][1] != "0.0.0.0":
                            return hostWeights[i][1]
                        else:
                            return -1
                    else:
                        return -1
                i = i + 1
        except:
            print(traceback.format_exc())
            return -1
        
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
            if False:
                if self.wait:
                    os.system("start /low /d \"" + os.getcwd().replace("\\working", "") + "\" /b /wait "" .\\ambience.exe .\\modules\\audio.py --event=\"" + pytools.cipher.base64_encode(json.dumps(eventData)) + "\"")
                else:
                    os.system("start /low /d \"" + os.getcwd().replace("\\working", "") + "\" /b "" .\\ambience.exe .\\modules\\audio.py --event=\"" + pytools.cipher.base64_encode(json.dumps(eventData)) + "\"")
            else:
                played = False
                while not played:
                    try:
                        noHosts = True
                        while noHosts:
                            try:
                                hostsf = pytools.IO.getJson(".\\hosts.json")["hosts"]
                                if hostsf != []:
                                    noHosts = False
                                    break
                                else:
                                    print("No hosts connected. Waiting for connection...")
                            except:
                                print("Hosts file not found or corrupted. Stack Trace: \n" + traceback.format_exc())
                            time.sleep(1)
                        soundsf = pytools.IO.getJson(".\\hostData.json")
                        if str(soundsf)[0] != "{":
                            if str(hosts.soundsf)[0] != "{":
                                hosts.soundsf = {}
                        else:
                            hosts.soundsf = soundsf
                        for puppet in hosts.listf:
                            try:
                                puppetMax = hosts.soundsf[puppet]["max"]
                            except:
                                try:
                                    puppetMax = pytools.net.getJsonAPI("http://" + puppet + ":4507?json=" + urllib.parse.quote(json.dumps({
                                        "command": "getMaxSoundCount"
                                    })))["maxSoundCount"],
                                except:
                                    puppetMax = 0
                            try:
                                puppetCurrent = hosts.soundsf[puppet]["current"]
                            except:
                                try:
                                    puppetCurrent = pytools.net.getJsonAPI("http://" + puppet + ":4507?json=" + urllib.parse.quote(json.dumps({
                                        "command": "getSoundCount"
                                    })))["soundCount"]
                                except:
                                    puppetCurrent = 1
                            print(puppetMax)
                            hosts.soundsf[puppet] = {
                                "max": puppetMax,
                                "current": puppetCurrent,
                                "play": False
                            }
                            if str(hosts.soundsf[puppet]["max"])[0] == "(":
                                hosts.soundsf[puppet]["max"] = hosts.soundsf[puppet]["max"][0]
                            if hosts.soundsf[puppet]["max"] >= hosts.soundsf[puppet]["current"]:
                                hosts.soundsf[puppet]["play"] = True
                        error = True
                        while error:
                            try:
                                if hosts.soundsf.keys() != pytools.IO.getJson(".\\hostData.json").keys():
                                    pytools.IO.saveJson(".\\hostData.json", hosts.soundsf)
                                error = False
                            except:
                                time.sleep(1)
                        randomInt = -1
                        while randomInt == -1:
                            randomInt = tools.getRandomInt(hosts.soundsf)
                            if randomInt != -1:
                                break
                            print("No hosts connected. Waiting for connection...")
                            time.sleep(3)
                        if not os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl"):
                            if not os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl"):
                                try:
                                    if hosts.soundsf[hosts.listf[randomInt]]["play"] == True:
                                        try:
                                            if not sendFile:
                                                def runSound():
                                                    try:
                                                        hasFired = False
                                                        errorCount = 0
                                                        while (not hasFired) and (errorCount < 100):
                                                            try:
                                                                pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":4507?json=" + urllib.parse.quote(json.dumps({
                                                                    "command": "fireEvent",
                                                                    "data": pytools.cipher.base64_encode(json.dumps(eventData))
                                                                })))
                                                                hasFired = True
                                                            except:
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
                                                            time.sleep(1)
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
                                                threading.Thread(target=runSound).start()
                                                played = True
                                                for sound in self.eventData["events"]:
                                                    logError = True
                                                    while logError:
                                                        try:
                                                            log.audio("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                                                            logError = False
                                                        except:
                                                            pass
                                                    # print("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                                            else:
                                                def runSound():
                                                    try:
                                                        hasFired = False
                                                        errorCount = 0
                                                        while (not hasFired) and (errorCount < 100):
                                                            try:
                                                                pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":4507?json=" + urllib.parse.quote(json.dumps({
                                                                    "command": "fireEvent",
                                                                    "data": pytools.cipher.base64_encode(json.dumps(self.eventData)),
                                                                    "fileData": {
                                                                        "data" : pytools.cipher.base64_encode(pytools.IO.getBytes(".\\sound\\assets\\" + self.path.split(";")[0]), isBytes=True),
                                                                        "fileName": self.path.split("\\")[-1]
                                                                    }
                                                                })))
                                                                hasFired = True
                                                            except:
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
                                                            time.sleep(1)
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
                                                threading.Thread(target=runSound).start()
                                                played = True
                                                for sound in self.eventData["events"]:
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
                                    print(traceback.format_exc())
                    except:
                        log.audio("Failed to send audio event. Trying again...")
                        log.audio(str(self.eventData))
                        log.audio(traceback.format_exc())
                        log.crash("Failed to send audio event. Trying again...")
                        log.crash(str(self.eventData))
                        log.crash(traceback.format_exc())
                    time.sleep(0.3)
            if eventData["wait"]:
                time.sleep(duration)
            if played != True:
                log.audio("Failed audio event.")
                log.audio(str(self.eventData))
                log.audio(traceback.format_exc())

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
        if False:
            if self.wait:
                os.system("start /low /d \"" + os.getcwd().replace("\\working", "") + "\" /b /wait "" .\\ambience.exe .\\modules\\audio.py --event=\"" + pytools.cipher.base64_encode(json.dumps(eventData)) + "\"")
            else:
                os.system("start /low /d \"" + os.getcwd().replace("\\working", "") + "\" /b "" .\\ambience.exe .\\modules\\audio.py --event=\"" + pytools.cipher.base64_encode(json.dumps(eventData)) + "\"")
        else:
            played = False
            while not played:
                try:
                    noHosts = True
                    while noHosts:
                        try:
                            hostsf = pytools.IO.getJson(".\\hosts.json")["hosts"]
                            if hostsf != []:
                                noHosts = False
                                break
                            else:
                                print("No hosts connected. Waiting for connection...")
                        except:
                            print("Hosts file not found or corrupted. Stack Trace: \n" + traceback.format_exc())
                        time.sleep(1)
                    soundsf = pytools.IO.getJson(".\\hostData.json")
                    if str(soundsf)[0] != "{":
                        if str(hosts.soundsf)[0] != "{":
                            hosts.soundsf = {}
                    else:
                        hosts.soundsf = soundsf
                    for puppet in hosts.listf:
                        try:
                            puppetMax = hosts.soundsf[puppet]["max"]
                        except:
                            try:
                                puppetMax = pytools.net.getJsonAPI("http://" + puppet + ":4507?json=" + urllib.parse.quote(json.dumps({
                                    "command": "getMaxSoundCount"
                                })))["maxSoundCount"],
                            except:
                                puppetMax = 0
                        try:
                            puppetCurrent = hosts.soundsf[puppet]["current"]
                        except:
                            try:
                                puppetCurrent = pytools.net.getJsonAPI("http://" + puppet + ":4507?json=" + urllib.parse.quote(json.dumps({
                                    "command": "getSoundCount"
                                })))["soundCount"]
                            except:
                                puppetCurrent = 1
                        print(puppetMax)
                        hosts.soundsf[puppet] = {
                            "max": puppetMax,
                            "current": puppetCurrent,
                            "play": False
                        }
                        if str(hosts.soundsf[puppet]["max"])[0] == "(":
                            hosts.soundsf[puppet]["max"] = hosts.soundsf[puppet]["max"][0]
                        if hosts.soundsf[puppet]["max"] >= hosts.soundsf[puppet]["current"]:
                            hosts.soundsf[puppet]["play"] = True
                    if hosts.soundsf.keys() != pytools.IO.getJson(".\\hostData.json").keys():
                        pytools.IO.saveJson(".\\hostData.json", hosts.soundsf)
                    
                    randomInt = -1
                    while randomInt == -1:
                        randomInt = tools.getRandomInt(hosts.soundsf)
                        if randomInt != -1:
                            break
                        print("No hosts connected. Waiting for connection...")
                        time.sleep(3)
                    if not os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl"):
                        if not os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl"):
                            try:
                                if hosts.soundsf[hosts.listf[randomInt]]["play"] == True:
                                    try:
                                        if not sendFile:
                                            def runSound():
                                                try:
                                                    hasFired = False
                                                    errorCount = 0
                                                    while (not hasFired) and (errorCount < 100):
                                                        try:
                                                            pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":4507?json=" + urllib.parse.quote(json.dumps({
                                                                "command": "fireEvent",
                                                                "data": pytools.cipher.base64_encode(json.dumps(eventData))
                                                            })))
                                                            hasFired = True
                                                        except:
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
                                                        time.sleep(1)
                                                except:
                                                    log.audio("Failed audio event.")
                                                    log.audio(str(eventData))
                                                    log.audio(traceback.format_exc())
                                                    log.crash("Failed audio event.")
                                                    log.crash(str(eventData))
                                                    log.crash(traceback.format_exc())
                                                try:
                                                    endms = time.time()
                                                    pytools.IO.appendFile("fire_times.cxl", "\n" + str(hosts.listf[randomInt]) + ", " + str(endms - startms) + ", " + str(eventData))
                                                except:
                                                    print(traceback.format_exc())
                                            threading.Thread(target=runSound).start()
                                            played = True
                                            for sound in eventData["events"]:
                                                logError = True
                                                while logError:
                                                    try:
                                                        log.audio("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                                                        logError = False
                                                    except:
                                                        pass
                                                # print("Playing sound " + str(sound["path"]) + " on speaker " + str(sound["channel"]) + " with volume " + str(sound["volume"]) + " at speed " + str(sound["speed"]) + " using client " + hosts.listf[randomInt] + "...")
                                        else:
                                            def runSound():
                                                try:
                                                    hasFired = False
                                                    errorCount = 0
                                                    while (not hasFired) and (errorCount < 100):
                                                        try:
                                                            pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":4507?json=" + urllib.parse.quote(json.dumps({
                                                                "command": "fireEvent",
                                                                "data": pytools.cipher.base64_encode(json.dumps(eventData)),
                                                                "fileData": {
                                                                    "data" : pytools.cipher.base64_encode(pytools.IO.getBytes(self.path.replace(".\\working\\", ".\\")), isBytes=True),
                                                                    "fileName": self.path.split("\\")[-1]
                                                                }
                                                            })))
                                                            hasFired = True
                                                        except:
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
                                                        time.sleep(1)
                                                except:
                                                    log.audio("Failed audio event.")
                                                    log.audio(str(eventData))
                                                    log.audio(traceback.format_exc())
                                                    log.crash("Failed audio event.")
                                                    log.crash(str(eventData))
                                                    log.crash(traceback.format_exc())
                                                try:
                                                    endms = time.time()
                                                    pytools.IO.appendFile("fire_times.cxl", "\n" + str(hosts.listf[randomInt]) + ", " + str(endms - startms) + ", " + str(eventData))
                                                except:
                                                    print(traceback.format_exc())
                                            threading.Thread(target=runSound).start()
                                            played = True
                                            for sound in eventData["events"]:
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
                                print(traceback.format_exc())
                except:
                    log.audio("Failed to send audio event. Trying again...")
                    log.audio(str(self.eventData))
                    log.audio(traceback.format_exc())
                    log.crash("Failed to send audio event. Trying again...")
                    log.crash(str(self.eventData))
                    log.crash(traceback.format_exc())
            time.sleep(1)
        if eventData["wait"]:
            time.sleep(duration)
        if played != True:
            log.audio("Failed audio event.")
            log.audio(str(eventData))
            log.audio(traceback.format_exc())
                
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
    
    def run(self, spawnChild=True, sendFile=False):
        startms = time.time()
        if False:
            if spawnChild:
                if self.eventData["wait"]:
                    os.system("start /low /d \"" + os.getcwd().replace("\\working", "") + "\" /b /wait "" .\\ambience.exe .\\modules\\audio.py --event=\"" + pytools.cipher.base64_encode(json.dumps(self.eventData)) + "\"")
                else:
                    os.system("start /low /d \"" + os.getcwd().replace("\\working", "") + "\" /b "" .\\ambience.exe .\\modules\\audio.py --event=\"" + pytools.cipher.base64_encode(json.dumps(self.eventData)) + "\"")
            else:
                multiEvent(self.eventData).run()
        else:
            played = False
            while not played:
                try:
                    noHosts = True
                    while noHosts:
                        try:
                            hostsf = pytools.IO.getJson(".\\hosts.json")["hosts"]
                            if hostsf != []:
                                noHosts = False
                                break
                            else:
                                print("No hosts connected. Waiting for connection...")
                        except:
                            print("Hosts file not found or corrupted. Stack Trace: \n" + traceback.format_exc())
                        time.sleep(1)
                    soundsf = pytools.IO.getJson(".\\hostData.json")
                    while True:
                        try:
                            hosts.listf = pytools.IO.getJson(".\\hosts.json")["hosts"]
                            break
                        except:
                            pass
                        time.sleep(1)
                    if str(soundsf)[0] != "{":
                        if str(hosts.soundsf)[0] != "{":
                            hosts.soundsf = {}
                    else:
                        hosts.soundsf = soundsf
                    for puppet in hosts.listf:
                        try:
                            puppetMax = hosts.soundsf[puppet]["max"]
                        except:
                            try:
                                puppetMax = pytools.net.getJsonAPI("http://" + puppet + ":4507?json=" + urllib.parse.quote(json.dumps({
                                    "command": "getMaxSoundCount"
                                })))["maxSoundCount"],
                            except:
                                puppetMax = 0
                        try:
                            puppetCurrent = hosts.soundsf[puppet]["current"]
                        except:
                            try:
                                puppetCurrent = pytools.net.getJsonAPI("http://" + puppet + ":4507?json=" + urllib.parse.quote(json.dumps({
                                    "command": "getSoundCount"
                                })))["soundCount"]
                            except:
                                puppetCurrent = 1
                        print(puppetMax)
                        hosts.soundsf[puppet] = {
                            "max": puppetMax,
                            "current": puppetCurrent,
                            "play": False
                        }
                        if str(hosts.soundsf[puppet]["max"])[0] == "(":
                            hosts.soundsf[puppet]["max"] = hosts.soundsf[puppet]["max"][0]
                        if hosts.soundsf[puppet]["max"] >= hosts.soundsf[puppet]["current"]:
                            hosts.soundsf[puppet]["play"] = True
                    try:
                        if hosts.soundsf.keys() != pytools.IO.getJson(".\\hostData.json").keys():
                            pytools.IO.saveJson(".\\hostData.json", hosts.soundsf)
                    except:
                        pytools.IO.saveJson(".\\hostData.json", hosts.soundsf)
                    randomInt = -1
                    while randomInt == -1:
                        randomInt = tools.getRandomInt(hosts.soundsf)
                        if randomInt != -1:
                            break
                        print("No hosts connected. Waiting for connection...")
                        time.sleep(3)
                    if not os.path.exists(".\\host-" + hosts.listf[randomInt] + ".bl"):
                        if not os.path.exists(".\\working\\host-" + hosts.listf[randomInt] + ".bl"):
                            try:
                                if hosts.soundsf[hosts.listf[randomInt]]["play"] == True:
                                    try:
                                        if not sendFile:
                                            def runSound():
                                                try:
                                                    hasFired = False
                                                    errorCount = 0
                                                    while (not hasFired) and (errorCount < 100):
                                                        try:
                                                            pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":4507?json=" + urllib.parse.quote(json.dumps({
                                                                "command": "fireEvent",
                                                                "data": pytools.cipher.base64_encode(json.dumps(self.eventData))
                                                            })))
                                                            hasFired = True
                                                        except:
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
                                                        time.sleep(1)
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
                                            threading.Thread(target=runSound).start()
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
                                            def runSound():
                                                try:
                                                    print(self.eventData["events"][0]["path"])
                                                    hasFired = False
                                                    errorCount = 0
                                                    while (not hasFired) and (errorCount < 100):
                                                        try:
                                                            pytools.net.getJsonAPI("http://" + hosts.listf[randomInt] + ":4507?json=" + urllib.parse.quote(json.dumps({
                                                                "command": "fireEvent",
                                                                "data": pytools.cipher.base64_encode(json.dumps(self.eventData)),
                                                                "fileData": {
                                                                    "data" : pytools.cipher.base64_encode(pytools.IO.getBytes(self.eventData["events"][0]["path"].replace(".\\working\\", ".\\")), isBytes=True),
                                                                    "fileName": self.eventData["events"][0]["path"].split("\\")[-1]
                                                                }
                                                            })))
                                                            hasFired = True
                                                        except:
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
                                                        time.sleep(1)
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
                                            threading.Thread(target=runSound).start()
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
                                print("Host not found. Relooping...")
                except:
                    log.audio("Failed to send audio event. Trying again...")
                    log.audio(str(self.eventData))
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
                        print("Setting flag " + flagName + " on host " + host + " to " + str(boolf) + '...')
                        try:
                            pytools.net.getJsonAPI("http://" + host + ":4507?json=" + urllib.parse.quote(json.dumps({
                                "command": "setFlag",
                                "data": {
                                    "flagName": flagName,
                                    "bool": boolf
                                }
                            })))
                            print("Flag Set.")
                        except:
                            print("Error. Flag could not be set.")
                        try:
                            hostsDataFile.pop(host)
                        except:
                            pass
                if loc:
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

for arg in sys.argv:
    if arg.split("=")[0] == "--event":
        eventData = json.loads(pytools.cipher.base64_decode(arg.split("=")[1]))
        multiEvent(eventData).run()
