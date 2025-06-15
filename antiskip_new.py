import pyaudio
import numpy as np
from scipy.signal import butter, sosfilt
import traceback
import os
import sounddevice as sd
import time
import threading
from pydub import AudioSegment
from pydub import utils
import numpy

class filter:
    def butter_bandpass_worker(lowcut, highcut, fs, order=5):
            nyq = 0.5 * fs
            low = lowcut / nyq
            high = highcut / nyq
            sos = butter(order, [low, high], analog=False, btype='band', output='sos')
            return sos

    def butter_bandpass(data, lowcut, highcut, fs, order=5):
            sos = filter.butter_bandpass_worker(lowcut, highcut, fs, order=order)
            y = sosfilt(sos, data)
            return y
        
class globals:
    isNotDetectedCount = 0

CHUNK = 4096 * 2 # number of data points to read at a time
RATE = 48000 # time resolution of the recording device (Hz)
LISTEN_DEVICE = "Hi-Fi Cable Output (3- VB-Audio" # default
PLAY_DEVICE = "Speakers (2- VB-Audio Hi-Fi Cab"

p = pyaudio.PyAudio()

def fixVoiceMeeter():
    print("WARNING: Fixing Voicemeeter...")
    os.system('\"C:\\Program Files (x86)\\VB\\Voicemeeter\\voicemeeter8.exe\" -r')
    os.system('\"C:\\Program Files (x86)\\VB\\VBAudioMatrix\\VBAudioMatrixCoconut.exe\" -r')

def findDevice(name):
    for device in sd.query_devices():
        if device["name"] == name:
            return device
    
    return False

def audioSegmentNumPy(audio):
    return numpy.array(audio.get_array_of_samples(), dtype=numpy.float32).reshape((-1, audio.channels)) / (1 << (8 * audio.sample_width - 1))

def playSound():
    
    soundFile = AudioSegment.from_file(".\\working\\sound\\assets\\high_pitch.mp3", format="mp3")
    soundFile = utils.make_chunks(soundFile, 1024)
    
    device = findDevice(PLAY_DEVICE)
    audioStream = sd.OutputStream(
        channels=soundFile[0].channels,
        device=device["index"],
        samplerate=soundFile[0].frame_rate,
    )
    
    audioStream.start()
    
    while True:
        try:
            print(str(time.time()) + " ;;; Playing high_pitch effect...")
            for chunk in soundFile:
                audioStream.write(audioSegmentNumPy(chunk))
        except:
            print(traceback.format_exc())

def main():
    
    soundThread = threading.Thread(target=playSound)
    soundThread.start()
    
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True, input_device_index=findDevice(LISTEN_DEVICE)["index"],
                frames_per_buffer=CHUNK)

    try:
        while True:
            indata = np.fromstring(stream.read(CHUNK),dtype=np.int16)

            # Remove everything except 300Hz..500Hz
            # TODO: does not work
            indata = filter.butter_bandpass(indata, 16050, 17050, RATE, order=5)

            # Take the fft and square each value
            fftData=abs(np.fft.rfft(indata))**2

            # TODO: find out volume
            noiselevel = np.average(fftData)

            # JUST FOR TESTING: Find out frequency (to see if band pass works correctly)
            # find the maximum
            which = fftData[1:].argmax() + 1
            # use quadratic interpolation around the max
            if which != len(fftData)-1:
                y0,y1,y2 = np.log(fftData[which-1:which+2:])
                x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                # find the frequency and output it
                thefreq = (which+x1)*RATE/CHUNK
            else:
                thefreq = which*RATE/CHUNK
            # END <JUST FOR TESTING>
            
            if (noiselevel < 10000000000):
                globals.isNotDetectedCount = globals.isNotDetectedCount + 1
                if (globals.isNotDetectedCount % 5) == 0:
                    print("Voicemeeter detected as fapping. Count is currently at: " + str(globals.isNotDetectedCount))
            else:
                globals.isNotDetectedCount = globals.isNotDetectedCount - 1
                
                if globals.isNotDetectedCount < 0:
                    globals.isNotDetectedCount = 0
            
            if globals.isNotDetectedCount > 118:
                fixVoiceMeeter()
                globals.isNotDetectedCount = 0
                
    except:
        print(traceback.format_exc())       

    stream.close()
    p.terminate()
    
if __name__ == "__main__":
    main()