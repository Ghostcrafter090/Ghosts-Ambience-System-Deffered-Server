import modules.audio as audio
from tempfile import TemporaryFile
import speech_recognition as sr
import pyttsx3
import modules.pytools as pytools
import threading
import time
import importlib
import os

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": []
    }
 
# Initialize the recognizer
r = sr.Recognizer()
 
# Function to convert text to
# speech
def SpeakText(command):
     
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

mics = {}
     
# Loop infinitely for user to
# speak

class globals:
    speech = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    writing = False
    speeches = 0
 
class micInstance:
    def __init__(self, micf, namef):
        self.mic = micf
        self.name = namef
        
    mic = 0
    name = ""
    
    def getText(self, mic):
        while(1 and not status.exit):
        
            # Exception handling to handle
            # exceptions at the runtime
            try:
                
                # use the microphone as source for input.
                with sr.Microphone(device_index=mic) as source2:
                    
                    # wait for a second to let the recognizer
                    # adjust the energy threshold based on
                    # the surrounding noise level
                    r.adjust_for_ambient_noise(source2, duration=0.2)
                    
                    #listens for the user's input
                    try:
                        audio2 = r.listen(source2, timeout=1, phrase_time_limit=5)
                        
                        # Using google to recognize audio
                        MyText = r.recognize_google(audio2)
                        MyText = MyText.lower()
                    
                        return MyText
                    except:
                        return False
            
            except:
                pass

    def micRun(self):
        while not status.exit:
            text = micInstance.getText(self, self.mic)
            n = True
            if text != False:
                if os.path.exists("transcripts\\" + str(self.mic) + ".cxl") == False:
                    pytools.IO.saveFile("transcripts\\" + str(self.mic) + ".cxl", text + ";" + str(self.name) + "\n")
                else:
                    try:
                        file = pytools.IO.getFile("transcripts\\" + str(self.mic) + ".cxl").split("\n")
                        if len(file) > 10:
                            file = file[1:]
                            file.append(text + ";" + str(self.name))
                            n = False
                        filef = ""
                        for r in file:
                            filef = filef + r + "\n"
                        pytools.IO.saveFile("transcripts\\" + str(self.mic) + ".cxl", filef.replace("\n\n", "\n"))
                    except:
                        n = True
                    if n:
                        if text:
                            pytools.IO.appendFile("transcripts\\" + str(self.mic) + ".cxl", text + ";" + str(self.name) + "\n")

class handlers:    
    mics = []

def runMic(*args):
    string = ""
    for x in args:
        string += x
        # print(int(handlers.mics[int(x)][0][0]))
    n = micInstance(int(handlers.mics[int(x)][0][0]), handlers.mics[int(x)][0][1])
    print(int(handlers.mics[int(x)][0][0]))
    n.micRun()
        
def main():
    # while pytools.sound.audioObj == False:
#         pytools.sound.audioObj = status.audioObj
    pytools.IO.saveFile("transcript.cxl", "")
    mics = pytools.IO.getJson("mics.json")
    i = 0
    n = 0
    f = 0
    while n < sr.Microphone.get_pyaudio().PyAudio().get_device_count():
        # if key == sr.Microphone.get_pyaudio().PyAudio().get_device_info_by_index(n)["name"]:
        if sr.Microphone.get_pyaudio().PyAudio().get_device_info_by_index(n)["hostApi"] == 0:
            handlers.mics.append(["", ""])
            handlers.mics[f][0] = [n, sr.Microphone.get_pyaudio().PyAudio().get_device_info_by_index(n)["name"]]
            handlers.mics[f][1] = threading.Thread(target=runMic, args=str(f))
            f = f + 1
        n = n + 1
    print(handlers.mics)
    for n in handlers.mics:
        n[1].start()
    while not status.exit:
        pytools.IO.saveFile("speechPerMinute.cx", "0")
        dateArray = pytools.clock.getDateTime()
        if dateArray[4] % 5:
            globals.speech[i] = globals.speeches
            pytools.IO.saveFile("speechPerMinute.cx", str(globals.speeches))
            globals.speeches = 0
            i = i + 1
            if i > 9:
                i = 0
            status.vars['lastLoop'] = pytools.clock.getDateTime()
            status.finishedLoop = True
            
def run():
    status.hasExited = False
    main()
    status.hasExited = True

