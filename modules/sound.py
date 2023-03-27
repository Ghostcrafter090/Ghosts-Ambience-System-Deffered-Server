import sys
import math
import os
import sounddevice as sd
import json
import time
import threading

from pyaudio import PyAudio
from pydub.utils import make_chunks
from pydub import AudioSegment
from pydub.scipy_effects import low_pass_filter
from pydub.scipy_effects import high_pass_filter

from mutagen.mp3 import MP3
from mutagen.wave import WAVE

AudioSegment.ffmpeg = ".\\ffmpeg.exe"

class IO:
    def getJson(path, doPrint=True):
        error = 0
        try:
            file = open(path, "r")
            jsonData = json.loads(file.read())
            file.close()
        except:
            if doPrint:
                print("Unexpected error:", sys.exc_info())
            error = 1
        if error != 0:
            jsonData = error
        return jsonData

class globals:
    speakers = {}
    chunks = False

if os.path.exists(".\\soundOutputs.json"):
    globals.speakers = IO.getJson(".\\soundOutputs.json")
if os.path.exists("..\\soundOutputs.json"):
    globals.speakers = IO.getJson("..\\soundOutputs.json")

class sound:
    def __init__(self, seg, speed, index, soundIndex, lastPlayed, bufferSize):
        self.channels = seg.channels
        self.frame_rate = seg.frame_rate
        self.sample_width = seg.sample_width
        globals.chunks = make_chunks(seg, 500)
        self.chunks = False
        self.speed = speed
        self.index = index
        self.soundIndex = soundIndex
        self.lastPlayed = lastPlayed
        self.bufferSize = bufferSize
    
    def run(self):
        p = PyAudio()
        stream = p.open(
            format=p.get_format_from_width(self.sample_width),
            channels=self.channels,
            output_device_index=self.index,
            rate=int(self.frame_rate * self.speed),
            output=True
        )

        try:
            i = 0
            while i < 3000:
                print(i)
                if globals.chunks == True:
                    i = i + 1
                    time.sleep(0.05)
                else:
                    i = 0
                self.chunks = globals.chunks
                globals.chunks = True
                if (self.chunks != True) and (self.chunks != False):
                    for chunk in self.chunks:
                        stream.write(chunk._data)
            
        finally:
            stream.stop_stream()
            stream.close()

            p.terminate()

def get(path, index, bufferSize):
    return AudioSegment.from_file_using_temporary_files(file=path.replace("\t", "\\t"), format="mp3", start_second=index, duration=bufferSize)
            
    
def play(path, volume, speed, speaker, lowPass=False, highPass=False, startTime=0):
    
    bufferSize = 10.0
    
    if path.find(".mp3") != -1:
        wait = MP3(path).info.length * speed
    else:
        wait = WAVE(path).info.length * speed
    index = 0
    lastPlayed = 0
    while index < wait:
        wf = get(path, index, bufferSize)
        if index == 0:
            if startTime != 0:
                time.sleep((((math.floor(round(time.time() * 1000000) / 2000000) + 1) - round(time.time() * 1000000) / 2000000) * 2) + ((startTime)))
            startPlayed = round(time.time() * 1000000)
        playSound(wf, volume, speed, speaker, bufferSize, lowPass=lowPass, highPass=highPass, lastPlayed=lastPlayed, soundIndex=index)
        index = index + bufferSize
        lastPlayed = startPlayed + (index * 1000000)
    globals.chunks = False

def playSound(wf, volume, speed, speaker, bufferSize, lowPass=False, highPass=False, lastPlayed=0, soundIndex=0):
    if speed > 0.1:
        if speed < 15:
            speaker[0] = speaker[0].replace(".exe", "")
                
            if lowPass:
                wf = wf.low_pass_filter(lowPass, order=24)
                
            if highPass:
                wf = wf.high_pass_filter(highPass, order=24)
                
            wf = wf + (20 * math.log(volume / 100, 10))
    
            try:
                print(speaker)
                index = globals.speakers[speaker[0]][2]
            except:
                for n in sd.query_devices():
                    if globals.speakers[speaker[0]][0] == n["name"]:
                        if globals.speakers[speaker[0]][1] == "MME":
                            if n["hostapi"] == 0:
                                index = n["index"]
                        if globals.speakers[speaker[0]][1] == "WDM-KS":
                            if n["hostapi"] == 4:
                                index = n["index"]
                globals.speakers[speaker[0]].append(index)
            init = sound(wf, speed, index, soundIndex, lastPlayed, bufferSize)
            thread = threading.Thread(target=init.run)
            if soundIndex != 0:
                print("waiting...")
                time.sleep(((lastPlayed / 1000000) + bufferSize) - (lastPlayed / 1000000))
            else:
                thread.start()
                time.sleep(1)