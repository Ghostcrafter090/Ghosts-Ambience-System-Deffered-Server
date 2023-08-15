# Print out realtime audio volume as ascii bars

import sounddevice as sd
import numpy as np
import modules.pytools as pytools
import modules.logManager as log
import modules.audio as audio

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
    micSettings = {
        -1: -1
    }
    
class sounds:
    set = []
    max = {}
    events = {}

def print_sound(indata, outdata, frames, time, status):
    volume_norm = float(np.linalg.norm(indata)*10)
    sounds.set.append(volume_norm)
    if len(sounds.set) > 100:
        if len(sounds.set[100:]) < 100:
            sounds.set = sounds.set[len(sounds.set) - 100:100]
        else:
            sounds.set = []
    try:
        if sounds.max[sd.default.device[0]] < volume_norm:
            sounds.max[sd.default.device[0]] = volume_norm
    except:
        sounds.max[sd.default.device[0]] = volume_norm
    if (sounds.max[sd.default.device[0]] * 0.75) < volume_norm:
        if volume_norm > 1:
            sounds.events[sd.default.device[0]] = pytools.clock.getDateTime()
            print("Sound event on mic " + str(sd.default.device[0]) + " detected at volume " + str(volume_norm) + ".") 
            pytools.IO.saveJson("soundEvents.json", sounds.events)
    

def main():
    while not status.exit:
        dateArray = pytools.clock.getDateTime()
        for n in sd.query_devices():
            if n["max_input_channels"] > 0:
                try:
                    sd.default.device[0] = n["index"]
                    do = True
                    try:
                        if n["hostapi"] == 0:
                            if globals.micSettings[n["index"]]:
                                if globals.micSettings[n["index"]] != -1:
                                    sd.default.device[1] = globals.micSettings[n["index"]]
                                    try:
                                        with sd.Stream(callback=print_sound):
                                            sd.sleep(30)
                                        globals.micSettings[n["index"]] = [f["index"]]
                                        do = False
                                    except:
                                        pass
                                else:
                                    if (dateArray[5] % 30) != 0:
                                        do = False
                    except:
                        pass
                    if do:
                        notFound = True
                        for f in sd.query_devices():
                            if f["max_output_channels"] > 0:
                                if f["hostapi"] == 0:
                                    sd.default.device[1] = f["index"]
                                    try:
                                        with sd.Stream(callback=print_sound):
                                            sd.sleep(100)
                                        globals.micSettings[n["index"]] = [f["index"]]
                                        notFound = False
                                    except:
                                        pass
                        if notFound:
                            globals.micSettings[n["index"]] = -1
                except:
                    pass
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True
        
def run():
    status.hasExited = False
    main()
    status.hasExited = True

                        