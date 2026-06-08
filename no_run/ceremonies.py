import modules.audio as audio
import modules.pytools as pytools
import os
import time
import modules.audio as audio 
import modules.logManager as log

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

class handlers:
    def stopSound(permBool: bool):
        if permBool == 1:
            pytools.IO.saveFile('remember.derp', "derp")
            audio.command.setFlag("remember", True)
            audio.command.sendStop()
    
    def startSound():
        os.system('del remember.derp /f /q')
        audio.command.setFlag("remember", False)
        
class RDC:
    def run():
        handlers.stopSound(1)
        audio.playSoundAll('remember.mp3', 100, 1, 0, 1, remember=True)
        handlers.startSound()

def main():
    while not status.exit:
        dateArray = pytools.clock.getDateTime()
        if dateArray[1] == 11:
            if dateArray[2] == 11:
                if dateArray[3] == 10:
                    if dateArray[4] == 58:
                        if dateArray[5] > 30:
                            RDC.run()
                    elif dateArray[4] == 59:
                        RDC.run()
        else:
            time.sleep(193)
        time.sleep(1)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True
        
def run():
    status.hasExited = False
    main()
    status.hasExited = True
