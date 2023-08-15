import modules.audio as audio
import modules.pytools as pytools
import random
import time
import os
import modules.logManager as log

print = log.printLog

class status:
    apiKey = ""
    audioObj = False
    exit = False
    hasExited = False
    finishedLoop = False
    vars = {
        "lastLoop": [],
        "foolsType": False
    }
    
class globals:
    foolsType = False
    
def main():
    while not status.exit:
        status.vars["foolsType"] = globals.foolsType
        if globals.foolsType != 1:
            if os.path.exists(".\\randomSounds.derp"):
                os.system("del randomSounds.derp /f /s /q")
                audio.command.setFlag("randomSounds", False)
        if globals.foolsType != 5:
            if os.path.exists(".\\speakSounds.derp"):
                pass
                os.system("del speakSounds.derp /f /s /q")
                os.system("del .\\sound\\assets\\speak_troll-*.wav /f /q")
                audio.command.setFlag("speakSounds", False)
        dateArray = pytools.clock.getDateTime()
        if dateArray[1] == 4:
            if dateArray[2] == 1:
                if dateArray[3] < 12:
                    if globals.foolsType == False:
                        globals.foolsType = random.randint(0, 5)
                    if globals.foolsType == 0:
                        if dateArray[3] > 9:
                            if dateArray[3] < 12:
                                if dateArray[4] == 7:
                                    audio.playSoundAll("rickroll.mp3", 50, 1.0, 0.0, 1)
                                    globals.foolsType = False
                    if globals.foolsType == 1:
                        if dateArray[3] > 9:
                            if dateArray[3] < 12:
                                status.vars["foolsType"] = globals.foolsType
                                pytools.IO.saveFile("randomSounds.derp", "")
                                audio.command.setFlag("randomSounds", True)
                                time.sleep(30 * 60)
                                globals.foolsType = False
                    if globals.foolsType == 2:
                        if dateArray[3] > 8:
                            if dateArray[4] < 10:
                                audio.playSoundAll("jumanji.mp3", 100, 1.0, 0.0, 1)
                                globals.foolsType = False
                    if globals.foolsType == 3:
                        status.vars["foolsType"] = globals.foolsType
                        speakerg = 5
                        while (speakerg == 5) or (speakerg == 3) or (speakerg == 4):
                            speakerg = random.randint(0, 7)
                        # audioEvent = audio.event()
                        # audioEvent.register("porn_troll.mp3", speakerg, 100, 1.0, 0.0, 1)
                        # audioEvent.run()
                        globals.foolsType = False
                    if globals.foolsType == 4:
                        if dateArray[3] > 9:
                            if dateArray[3] < 12:
                                status.vars["foolsType"] = globals.foolsType
                                audio.playSoundAll("fbi_troll.mp3", 100, 1.0, 0.0, 1)
                                globals.foolsType = False
                    if globals.foolsType == 5:
                        if dateArray[3] > 9:
                            if dateArray[3] < 12:
                                status.vars["foolsType"] = globals.foolsType
                                pytools.IO.saveFile("speakSounds.derp", "")
                                audio.command.setFlag("speakSounds", False)
                                time.sleep(10 * 60)
                                globals.foolsType = False
                    time.sleep(1)
                else:
                    globals.foolsType = False
                    time.sleep(300) 
            else:
                globals.foolsType = False
                time.sleep(300)
        else:
            globals.foolsType = False
            time.sleep(300)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
            
def run():
    status.hasExited = False
    main()
    status.hasExited = True
