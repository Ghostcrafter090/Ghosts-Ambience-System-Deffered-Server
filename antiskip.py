# Read in a WAV and find the freq's
import pyaudio
import wave
from scipy.signal import lfilter
from scipy.signal import butter
from scipy.io import wavfile
import numpy as np
import sounddevice as sd
import modules.logManager as log
import io
import os
from scipy.io.wavfile import write
import traceback
import modules.audio as audio
import modules.pytools as pytools
import time
import threading
import sys

print = log.printLog

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": []
    }

class globals:
    theFreqFix = 0
    chunk = 2048
    speakerType = ""
    
def simple_record(deviceIndex):
    
    dtype = 'int16'
    
    sd.default.samplerate = 44100
    sd.default.channels = 1
    myrecording = sd.rec(int(1 * 44100), dtype=dtype, device=deviceIndex)
    sd.wait()
    bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    write(byte_io, 44100, myrecording)
    return byte_io

class bandpass_filter:
    def __init__(self, lowcut, highcut, frame_rate):
        self.FRAME_RATE = frame_rate
        self.lowcut = lowcut
        self.highcut = highcut
        
    def run(self, buffer):
        return self.butter_bandpass_filter(buffer, self.lowcut, self.highcut, self.FRAME_RATE, order=5)
    
    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

class speakerManager:
    
    def __init__(self, speakerType):
        self.speakerType = speakerType
        
    deviceIndex = False
        
    def run(self):
        
        checkCount = 6
        
        while not status.exit:
            try:
                if checkCount > 5:
                    try:
                        speakerName = pytools.IO.getJson(".\\serverOutputs.json")[self.speakerType]
                    
                        for device in sd.query_devices():
                            if device["name"] == "CABLE Output (" + speakerName.split("(")[1].split("-")[0] + "- VB-Audio Virtu":
                                self.deviceIndex = device["index"]
                                print("Found Speaker " + self.speakerType + " On Index: " + str(self.deviceIndex))
                    except:
                        if not self.deviceIndex:
                            print(traceback.format_exc())
                    
                    while (self.deviceIndex == False) and not status.exit:
                        try:
                            speakerName = pytools.IO.getJson(".\\serverOutputs.json")[self.speakerType]
                        
                            for device in sd.query_devices():
                                if device["name"] == "CABLE Output (" + speakerName.split("(")[1].split("-")[0] + "- VB-Audio Virtu":
                                    self.deviceIndex = device["index"]
                                    print("Found Speaker " + self.speakerType + " On Index: " + str(self.deviceIndex))
                        except:
                            if not self.deviceIndex:
                                print(traceback.format_exc())
                    
                    checkCount = 0
                
                recording = simple_record(self.deviceIndex)
                
                samplerate, data = wavfile.read(recording)
                        
                highpass = bandpass_filter(19900, 20100, samplerate)
                
                filteredData = np.apply_along_axis(highpass.run, 0, data).astype('int16')
                bytes_wav = bytes()
                byte_io = io.BytesIO(bytes_wav)
                wavfile.write(byte_io, 44100, filteredData)
                
                wf = wave.open(byte_io, 'rb')
                RATE = wf.getframerate()
                
                swidth = wf.getsampwidth()
                # use a Blackman window
                window = np.blackman(globals.chunk)

                # read some data
                data = wf.readframes(globals.chunk)
                
                # play stream and find the frequency of each chunk
                theFreqFixDo = False
                while len(data) == globals.chunk * swidth:
                    # write data out to the audio stream
                    # stream.write(data)
                    # unpack the data and times by the hamming window
                    indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), data)) * window
                    # Take the fft and square each value
                    fftData=abs(np.fft.rfft(indata))**2
                    # find the maximum
                    which = fftData[1:].argmax() + 1
                    # use quadratic interpolation around the max
                    if which != len(fftData)-1:
                        y0,y1,y2 = np.log(fftData[which-1:which+2:])
                        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                        # find the frequency and output it
                        thefreq = (which + x1) * RATE / globals.chunk
                        # print("The freq is %f Hz." % (thefreq))
                    else:
                        thefreq = which*RATE/globals.chunk
                        # print("The freq is %f Hz." % (thefreq))
                    if not (19950 < thefreq < 20050):
                        # print("error: Frequency Buffer Overload.")
                        theFreqFixDo = True
                    # read some more data
                    data = wf.readframes(globals.chunk)
                if theFreqFixDo:
                    globals.theFreqFix = globals.theFreqFix + 1
                    print("Buffer overload counter at " + str(globals.theFreqFix))
                else:
                    globals.theFreqFix = 0
                if globals.theFreqFix >= 15:
                    os.system('"C:\\Program Files (x86)\\VB\\Voicemeeter\\voicemeeter8.exe" -r')
                    print("Buffer Overload Detected. Refreshing Voicemeeter...")
                    globals.theFreqFix = 0
                    
                checkCount = checkCount + 1
            except:
                print(traceback.format_exc())
                time.sleep(1)

def main():
    
    speakerManagerInst = speakerManager(globals.speakerType)
    
    speakerThread = threading.Thread(target=speakerManagerInst.run)
    
    speakerThread.start()
    
    while not status.exit:
        time.sleep(7)
    
def run():
    status.hasExited = False
    main()
    status.hasExited = True
    
try:
    for n in sys.argv:
        if n.split("=")[0] == "--speaker":
            globals.speakerType = n.split("=")[1]
    if sys.argv[1] == "--run":
        run()
except:
    pass