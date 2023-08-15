import modules.pytools as pytools
import modules.logManager as log

import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import time
import threading
import traceback

# print = log.printLog
     
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
    transcript = []
    r = sr.Recognizer()
    
class tools:
    def record(device, duration): # device):
        # Sampling frequency
        freq = 48000
        
        # sd.default.device = device
        
        # Start recorder with the given values
        # of duration and sample frequency
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=1, device=device)
        
        # Record audio for the given number of seconds
        sd.wait()
        
        # This will convert the NumPy array to an audio
        # file with the given sampling frequency
        write(".\\stt\\speech_" + str(device) + ".wav", freq, recording)
        
        # Convert the NumPy array to audio file
        wv.write(".\\stt\\speech_" + str(device) + ".wav", recording, freq, sampwidth=2)
    
    def getTranscript(path):
        """
        Splitting the large audio file into chunks
        and apply speech recognition on each of these chunks
        """
        # open the audio file using pydub
        sound = AudioSegment.from_wav(path)  
        # split audio sound where silence is 700 miliseconds or more and get chunks
        chunks = split_on_silence(sound,
            # experiment with this value for your target audio file
            min_silence_len = 500,
            # adjust this per requirement
            silence_thresh = sound.dBFS-14,
            # keep the silence for 1 second, adjustable as well
            keep_silence=500,
        )
        folder_name = "audio-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        # process each chunk 
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            with sr.AudioFile(chunk_filename) as source:
                audio_listened = globals.r.record(source)
                # try converting it to text
                try:
                    text = globals.r.recognize_google(audio_listened)
                except sr.UnknownValueError as e:
                    print("Error:", str(e))
                    return False
                else:
                    text = f"{text.capitalize()}. "
                    print(chunk_filename, ":", text)
                    whole_text += text
        # return the text for all chunks detected
        return whole_text

class mic:
    def __init__(self, deviceIndex):
        self.index = deviceIndex
        
    def main(self):
        while not status.exit:
            try:
                tools.record(self.index, 5)
                # transcript = tools.getTranscript(".\\stt\\speech_" + str(self.index) + ".wav")
                transcript = False
                if transcript:
                    globals.transcript.append(transcript)
            except:
                print(traceback.format_exc())
                time.sleep(1)
    
def main():
    mics = []
    i = 0
    devices = sd.query_devices() 
    while i < len(devices):
        if devices[i]["hostapi"] == 0:
            if devices[i]["max_input_channels"] > 0:
                obj = mic(i)
                thread = threading.Thread(target=obj.main)
                mics.append([obj, thread])
        i = i + 1
    
    if not os.path.exists(".\\stt"):
        os.system("mkdir stt")
    
    for micf in mics:
        micf[1].start()
    
    transcriptString = ""
    
    while not status.exit:
        if not os.path.exists(".\\stt"):
            os.system("mkdir stt")
        do = False
        while globals.transcript != []:
            transcriptString = transcriptString + "\n" + globals.transcript[-1]
            globals.transcript.pop(-1)
            if len(transcriptString.split("\n")) > 20:
                transcriptStringf = transcriptString.split("\n")
                transcriptStringf.pop(-1)
                transcriptString = "\n".join(transcriptStringf)
            do = True
        if do:
            pytools.IO.saveFile("transcripts.cxl", transcriptString)
        time.sleep(1)
                
def run():
    status.hasExited = False
    main()
    status.hasExited = True