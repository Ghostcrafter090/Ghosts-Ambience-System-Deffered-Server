import modules.audio as audio
from datetime import datetime
import os
import time
import modules.pytools as pytools
import threading
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

class globals:
    isChime = False
    isGong = False

def getDate():
    sequence = str(datetime.now()).replace(" ", "-").replace(":", "-").replace(".", "-")
    list = sequence.split("-")
    return list

class mech:
    def chimePR():
        print(str(datetime.now()) + " ;; Playing whirr prep sound...")
        # os.system('cmd.exe /c start /d ".\\sound\\clock" /b "" ..\..\clock.exe whirr_prep.vbs')
        event = audio.event()
        event.register("whirr_prep.mp3", 0, 20, 1.0, 0.0, 0, clock=False)
        event.run()
        time.sleep(60)

    def windCL():
        print(str(datetime.now()) + " ;; Winding the clock...")
        # os.system('cmd.exe /c start /wait /b /d ".\\sound\\clock" "" ..\..\clock.exe winding_clock.vbs')
        event = audio.event()
        event.register("winding_clock.mp3", 0, 100, 1.0, 0.0, 0, clock=False)
        event.run()
        time.sleep(60)
        
class whirr:
    def standard():
        globals.isChime = True
        while globals.isChime:
            event = audio.event()
            event.register("whirr_cont.mp3", 0, 50, 1.0, 0.0, 0, clock=False, keepLoaded=True)
            event.run()
            time.sleep(1)
        event = audio.event()
        event.register("whirr_ed.mp3", 0, 50, 1.0, 0.0, 0, clock=False)
        event.run()
            
    def gong():
        globals.isGong = True
        while globals.isGong:
            event = audio.event()
            event.register("gong_whirr_cont.mp3", 0, 50, 1.0, 0.0, 0, clock=False, keepLoaded=True)
            event.run()
            time.sleep(1)
        event = audio.event()
        event.register("gong_whirr_ed.mp3", 0, 50, 1.0, 0.0, 0, clock=False)
        event.run()
            
class chime:
    def chimeFH():
        print(str(datetime.now()) + " ;; Starting whirr effect...")
        # os.system('cmd.exe /c start /b /d ".\\sound\\clock" "" ..\..\clock.exe whirr_st.vbs')
        event = audio.event()
        event.register("whirr_st.mp3", 0, 50, 1.0, 0.0, 0, clock=False)
        event.run()
        time.sleep(3)
        gongWhirr = threading.Thread(target=whirr.standard)
        gongWhirr.start()
        print(str(datetime.now()) + " ;; Playing hour chime...")
        # os.system('cmd.exe /c start /b /d ".\\sound\\clock" "" ..\..\clock.exe hcs.vbs')
        event = audio.event()
        event.register("hcs.wav", 0, 20, 1.0, 0.0, 0, clock=False)
        event.run()
        file = open(".\\clocks\\default\\hcs_config.txt", "r")
        hcst = int(file.read()) - 2
        file.close()
        print(str(datetime.now()) + " ;; Waiting for " + str(hcst) + " seconds...")
        time.sleep(hcst)
        print(str(datetime.now()) + " ;; Chime sequence finished.")
        globals.isChime = False
        
    def chimeQH():
        print(str(datetime.now()) + " ;; Starting whirr effect...")
        # os.system('cmd.exe /c start /b /d ".\\sound\\clock" "" ..\..\clock.exe whirr_st.vbs')
        event = audio.event()
        event.register("whirr_st.mp3", 0, 50, 1.0, 0.0, 0, clock=False)
        event.run()
        time.sleep(3)
        gongWhirr = threading.Thread(target=whirr.standard)
        gongWhirr.start()
        print(str(datetime.now()) + " ;; Playing quarter hour chime...")
        # os.system('cmd.exe /c start /b /d ".\\sound\\clock" "" ..\..\clock.exe qhcs.vbs')
        event = audio.event()
        event.register("qhcs.wav", 0, 20, 1.0, 0.0, 0, clock=False)
        event.run()
        file = open(".\\clocks\\default\\qhcs_config.txt", "r")
        hcst = int(file.read()) - 2
        file.close()
        print(str(datetime.now()) + " ;; Waiting for " + str(hcst) + " seconds...")
        time.sleep(hcst)
        print(str(datetime.now()) + " ;; Chime sequence finished.")
        globals.isChime = False
        
    def chimeHH():
        print(str(datetime.now()) + " ;; Starting whirr effect...")
        # os.system('cmd.exe /c start /b /d ".\\sound\\clock" "" ..\..\clock.exe whirr_st.vbs')
        event = audio.event()
        event.register("whirr_st.mp3", 0, 50, 1.0, 0.0, 0, clock=False)
        event.run()
        time.sleep(3)
        gongWhirr = threading.Thread(target=whirr.standard)
        gongWhirr.start()
        print(str(datetime.now()) + " ;; Playing half hour chime...")
        # os.system('cmd.exe /c start /b /d ".\\sound\\clock" "" ..\..\clock.exe hhcs.vbs')
        event = audio.event()
        event.register("hhcs.wav", 0, 20, 1.0, 0.0, 0, clock=False)
        event.run()
        file = open(".\\clocks\\default\\hhcs_config.txt", "r")
        hcst = int(file.read()) - 2
        file.close()
        print(str(datetime.now()) + " ;; Waiting for " + str(hcst) + " seconds...")
        time.sleep(hcst)
        print(str(datetime.now()) + " ;; Chime sequence finished.")
        globals.isChime = False
        
    def chimeTH():
        print(str(datetime.now()) + " ;; Starting whirr effect...")
        # os.system('cmd.exe /c start /b /d ".\\sound\\clock" "" ..\..\clock.exe whirr_st.vbs')
        event = audio.event()
        event.register("whirr_st.mp3", 0, 50, 1.0, 0.0, 0, clock=False)
        event.run()
        time.sleep(3)
        gongWhirr = threading.Thread(target=whirr.standard)
        gongWhirr.start()
        print(str(datetime.now()) + " ;; Playing third quarter hour chime...")
        # os.system('cmd.exe /c start /b /d ".\\sound\\clock" "" ..\..\clock.exe tqhcs.vbs')
        event = audio.event()
        event.register("tqhcs.wav", 0, 20, 1.0, 0.0, 0, clock=False)
        event.run()
        file = open(".\\clocks\\default\\tqhcs_config.txt", "r")
        hcst = int(file.read()) - 2
        file.close()
        print(str(datetime.now()) + " ;; Waiting for " + str(hcst) + " seconds...")
        time.sleep(hcst)
        print(str(datetime.now()) + " ;; Chime sequence finished.")
        globals.isChime = False
        
    def chimeHN():
        print(str(datetime.now()) + " ;; Starting gong penis whirr effect...")
        # os.system('cmd.exe /c start /b /d ".\\sound\\clock" "" ..\..\clock.exe gong_whirr_st.vbs')
        event = audio.event()
        event.register("gong_whirr_st.mp3", 0, 50, 1.0, 0.0, 0, clock=False)
        event.run()
        time.sleep(3)
        gongWhirr = threading.Thread(target=whirr.gong)
        gongWhirr.start()
        hour = int(getDate()[3])
        if hour > 12:
            hour = hour - 12
        if hour < 1:
            hour = 12
        hourn = hour
        file = open(".\\clocks\\default\\gong_config.txt", "r")
        hcst = int(file.read())
        file.close()
        while hour > 0:
            print(str(datetime.now()) + " ;; Playing gong number " + str(hourn - hour) + "...")
            # os.system('cmd.exe /c start /b /d ".\\sound\\clock" "" ..\..\clock.exe gong.vbs')
            event = audio.event()
            event.register("gong.wav", 0, 20, 1.0, 0.0, 0, clock=False)
            event.run()
            print(str(datetime.now()) + " ;; Waiting for " + str(hcst) + " seconds...")
            time.sleep(hcst)
            hour = hour - 1
        print(str(datetime.now()) + " ;; Chime sequence finished.")
        globals.isGong = False
        
    def chimeCH():
        print(str(datetime.now()) + " ;; Playing christmas chime...")
        event = audio.event()
        event.register("cotb.mp3", 0, 10, 1.0, 0.0, 1, clock=False)
        event.run()

def main():
    chime.chimeFH()
    chime.chimeHN()
    time.sleep(60)
    while not status.exit:
        if os.path.exists(".\\remember.derp") == False:
            if int(getDate()[3]) == 19:
                if int(getDate()[4]) == 8:
                    mech.windCL()
            if int((getDate()[4])) == 58:
                mech.chimePR()
            if int((getDate()[4])) == 13:
                mech.chimePR()
            if int((getDate()[4])) == 28:
                mech.chimePR()
            if int((getDate()[4])) == 43:
                mech.chimePR()
            if int((getDate()[4])) == 0:
                chime.chimeFH()
                print(getDate())
                if int(getDate()[1]) == 12:
                    if int(getDate()[3]) == 12:
                        chime.chimeCH()
                chime.chimeHN()
                time.sleep(60)
            if int((getDate()[4])) == 15:
                chime.chimeQH()
                time.sleep(60)
            if int((getDate()[4])) == 30:
                chime.chimeHH()
                time.sleep(60)
            if int((getDate()[4])) == 45:
                chime.chimeTH()
                time.sleep(60)
        time.sleep(10)
        status.vars['lastLoop'] = pytools.clock.getDateTime()
        status.finishedLoop = True

def run():
    status.hasExited = False
    main()
    status.hasExited = True
